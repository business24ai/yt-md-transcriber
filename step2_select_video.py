from db_config import SessionLocal, YTChannel, YTVideo, NewVideos
import yt_dlp
from urllib.parse import parse_qs, urlparse
from datetime import datetime

def get_video_id(youtube_url):
    """Extract video ID from YouTube URL"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            video_id = info['id']
            return video_id
        except Exception as e:
            print(f"Error extracting video info: {str(e)}")
            return None


def get_video_info(video_id):
    """Get video information using yt-dlp"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return {
                'title': info.get('title'),
                'channel': info.get('uploader'),
                'channel_id': info.get('uploader_id'),
                'upload_date': info.get('upload_date'),
                'duration': info.get('duration', 0),
                'video_url': video_url,
                'id': video_id
            }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None


def upsert_channel(session, video_info):
    """Upsert channel information to database"""
    channel_id = video_info.get("channel_id")
    
    # Try to get existing channel
    channel = session.query(YTChannel).filter(YTChannel.id == channel_id).first()
    
    if channel:
        # Update existing channel
        channel.title = video_info.get("channel", "")
        channel.updated_at = datetime.now()
    else:
        # Create new channel
        channel = YTChannel(
            id=channel_id,
            title=video_info.get("channel", ""),
            updated_at=datetime.now()
        )
        session.add(channel)
    
    session.commit()


def upsert_video(session, video_info):
    """Upsert video information to database"""
    video_id = video_info["id"]
    
    # Convert upload_date from YYYYMMDD format to datetime
    upload_date_str = video_info.get("upload_date", "")
    published_at = None
    if upload_date_str:
        try:
            published_at = datetime.strptime(upload_date_str, "%Y%m%d")
        except ValueError:
            print(f"Warning: Could not parse upload date: {upload_date_str}")
    
    # Try to get existing video
    video = session.query(YTVideo).filter(YTVideo.id == video_id).first()
    
    if video:
        # Update existing video
        video.channel_id = video_info["channel_id"]
        video.title = video_info["title"]
        video.video_url = video_info["video_url"]
        video.published_at = published_at
        video.updated_at = datetime.now()
    else:
        # Create new video
        video = YTVideo(
            id=video_id,
            channel_id=video_info["channel_id"],
            title=video_info["title"],
            video_url=video_info["video_url"],
            published_at=published_at,
            updated_at=datetime.now()
        )
        session.add(video)
    
    session.commit()
    return video


def process_video(session, video_id):
    """Process a video by getting its info and updating the database"""
    # Get video info
    video_info = get_video_info(video_id)
    if not video_info:
        raise ValueError(f"Could not get info for video {video_id}")

    # Update database
    upsert_channel(session, video_info)
    video = upsert_video(session, video_info)
    return video


def process_youtube_url(youtube_url, session):
    """Process YouTube URL and store information in database"""
    # Get video ID
    video_id = get_video_id(youtube_url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL")

    # Process video
    video = process_video(session, video_id)
    return video


def main():
    """Main function to process YouTube videos from new_videos table"""
    # Create session
    session = SessionLocal()

    try:
        # Query new videos ordered by created_at desc
        new_videos = session.query(NewVideos).order_by(NewVideos.created_at.desc()).all()

        if not new_videos:
            print("No new videos found in the database to process.")
            process_manual = input("Would you like to process a video manually? (y/n): ")
            
            if process_manual.lower() == 'y':
                youtube_url = input("Please enter the YouTube URL to process: ")
                try:
                    video = process_youtube_url(youtube_url, session)
                    print(f"Successfully processed video: {video.title}")
                except Exception as e:
                    print(f"Error processing video: {str(e)}")
            return

        # Convert to pandas DataFrame for easier processing
        import pandas as pd
        videos_df = pd.DataFrame([
            {
                'video_url': video.video_url,
                'created_at': video.created_at
            } for video in new_videos
        ])

        print(f"Found {len(videos_df)} new videos to process:")
        for _, video in videos_df.iterrows():
            print(f"\n\n=== Processing video: {video['video_url']}")
            try:
                processed_video = process_youtube_url(video['video_url'], session)
                print(f"Successfully processed video: {processed_video.title}")
                # Remove the video from new_videos table after processing
                session.query(NewVideos).filter(NewVideos.video_url == video['video_url']).delete()
                session.commit()
            except Exception as e:
                print(f"Error processing video {video['video_url']}: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
