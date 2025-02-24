"""Transcribe YouTube videos and store transcriptions in the database."""
import os
import warnings
import pandas as pd
import yt_dlp
from datetime import datetime
from db_config import SessionLocal, VideoTranscription, Transcription, YTChannel, YTVideo
from step2_select_video import get_video_id, get_video_info
import whisper


# Suppress the warning using warnings filter
warnings.filterwarnings("ignore", category=FutureWarning)

def ensure_directories():
    """Ensure required directories exist"""
    for dir_name in ['csv_segments', 'csv_timestamps']:
        os.makedirs(dir_name, exist_ok=True)

def download_youtube_audio(youtube_url):
    """Download audio from YouTube video"""
    video_id = get_video_id(youtube_url)  
    if not video_id:
        raise ValueError("Could not extract video ID from URL")

    watch_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Download audio only
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{video_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([watch_url])
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            return None, None
    
    return video_id, watch_url

def transcribe_audio(video_id):
    """Transcribe audio using Whisper"""
    ensure_directories()
    
    model = whisper.load_model("base")
    output = model.transcribe(f"./downloads/{video_id}.wav", fp16=False)
    segments = output["segments"]

    # Get database session
    session = SessionLocal()
    try:
        # Store complete transcription output
        video_transcription = VideoTranscription(
            video_id=video_id,
            text=output["text"],
            language=output["language"],
            duration=output.get("duration", 0.0),
            language_probability=output.get("language_probability", 0.0),
            task=output.get("task", "transcribe"),
            created_at=datetime.now().isoformat()
        )
        session.add(video_transcription)

        # Store detailed segment information
        for segment in segments:
            transcription = Transcription(
                video_id=video_id,
                segment_id=segment["id"],
                start=segment["start"],
                end=segment["end"],
                text=segment["text"],
                avg_logprob=segment.get("avg_logprob", 0.0),
                compression_ratio=segment.get("compression_ratio", 0.0),
                no_speech_prob=segment.get("no_speech_prob", 0.0),
                temperature=segment.get("temperature", 0.0),
                seek=segment.get("seek", 0),
                tokens=str(segment.get("tokens", []))
            )
            session.add(transcription)

        session.commit()

        # Cache the transcription to CSV
        df = pd.DataFrame(segments)
        df.to_csv(f"./csv_segments/{video_id}.csv", index=False)
        
        return df
    
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def process_transcription(video_id, watch_url):
    """Process transcription and add video metadata"""
    ensure_directories()
    
    df_backup = pd.read_csv(f"./csv_segments/{video_id}.csv")
    # Create an explicit copy to avoid the SettingWithCopyWarning
    df_export = df_backup[["id", "start", "text"]].copy()

    # Add video metadata
    df_export.insert(0, "video_id", video_id)
    df_export.insert(0, "watch_url", watch_url)

    # Add timestamps to URLs
    df_export["watch_url"] = df_export.apply(
        lambda row: f"{row['watch_url']}&t={int(row['start'])}", 
        axis=1
    )

    # Save processed data
    df_export.to_csv(f"./csv_timestamps/{video_id}_timestamps.csv", index=False)
    return df_export

def check_transcription_exists(video_id):
    """Check if video has already been transcribed"""
    session = SessionLocal()
    try:
        exists_in_db = session.query(VideoTranscription).filter_by(video_id=video_id).first() is not None
        exists_in_csv = os.path.exists(f"./csv_segments/{video_id}.csv")
        return exists_in_db or exists_in_csv
    finally:
        session.close()

def transcribe_video(youtube_url):
    """Main process to transcribe a single video"""
    try:
        # Download audio and get video info
        video_id, watch_url = download_youtube_audio(youtube_url)
        
        # Get video information
        video_info = get_video_info(video_id)
        if not video_info:
            raise ValueError(f"Could not get video info for {video_id}")
        
        # Store video info in database
        db = SessionLocal()
        try:
            # Create or update channel
            channel = db.query(YTChannel).filter_by(id=video_info['channel_id']).first()
            if not channel:
                channel = YTChannel(
                    id=video_info['channel_id'],
                    title=video_info['channel'],
                    name=video_info['channel']
                )
                db.add(channel)
            
            # Create or update video
            video = db.query(YTVideo).filter_by(id=video_id).first()
            if not video:
                video = YTVideo(
                    id=video_id,
                    channel_id=video_info['channel_id'],
                    title=video_info['title'],
                    published_at=datetime.strptime(video_info['upload_date'], "%Y%m%d") if video_info.get('upload_date') else None
                )
                db.add(video)
            else:
                video.title = video_info['title']
                if video_info.get('upload_date'):
                    video.published_at = datetime.strptime(video_info['upload_date'], "%Y%m%d")
            
            db.commit()
        finally:
            db.close()

        # Transcribe audio
        transcription = transcribe_audio(video_id)
        
        # Process and store transcription
        process_transcription(video_id, watch_url)
        
        print(f"Successfully transcribed video: {video_id}")
        return True
        
    except Exception as e:
        print(f"Error transcribing video: {str(e)}")
        return False

def main():
    """Main function to transcribe the 3 newest untranscribed videos"""
    ensure_directories()
    
    # Get database session
    session = SessionLocal()
    try:
        # Query for videos that haven't been transcribed yet, ordered by publish date descending
        untranscribed_videos = session.query(YTVideo)\
            .outerjoin(VideoTranscription, YTVideo.id == VideoTranscription.video_id)\
            .filter(VideoTranscription.video_id == None)\
            .order_by(YTVideo.published_at.desc())\
            .limit(3)\
            .all()
        
        if not untranscribed_videos:
            print("No untranscribed videos found in the database.")
            return
        
        # Process each video
        for video in untranscribed_videos:
            youtube_url = f"https://www.youtube.com/watch?v={video.id}"
            print(f"\n\n===Processing video: {video.title} ({youtube_url})")
            
            if check_transcription_exists(video.id):
                print(f"Video {video.id} has already been transcribed. Skipping...")
                continue
                
            success = transcribe_video(youtube_url)
            if success:
                print(f"Successfully transcribed video: {video.title}")
            else:
                print(f"Failed to transcribe video: {video.title}")
                
    finally:
        session.close()

if __name__ == "__main__":
    main()
