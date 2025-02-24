"""Transcribe YouTube videos and store transcriptions in the database."""
import os
import re
import pandas as pd
import yt_dlp
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv
from db_config import SessionLocal, VideoTranscription, Transcription, Note
from step2_select_video import get_video_id, get_video_info
from sqlalchemy import text
import sys


def ensure_directories():
    """Ensure required directories exist"""
    for dir_name in ['markdown']:
        os.makedirs(dir_name, exist_ok=True)



def sanitize_name(title):
    """Convert special characters in title to dashes"""
    # Replace special characters with dash
    # Added quotes and other problematic characters to the pattern
    sanitized = re.sub(r'[:/\\;,!?|"\'<>*]', "-", title)
    # Remove any double dashes that might have been created
    sanitized = re.sub(r"-+", "-", sanitized)
    # Remove leading/trailing dashes and spaces
    sanitized = sanitized.strip("- ")
    return sanitized



def get_video_title(youtube_url):
    """Get the title of the YouTube video using yt-dlp"""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }

    # Extract video ID from URL for fallback
    query = urlparse(youtube_url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get("title", "Untitled Video")
        except Exception as e:
            print(f"Error getting video title: {e}")
            return f"Video_{video_id}"


def format_timestamp(seconds, total_duration):
    """Convert seconds to appropriate time format
    Uses HH:MM:SS if total_duration >= 1 hour, otherwise MM:SS
    """
    if total_duration >= 3600:  # 1 hour = 3600 seconds
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        remaining_seconds = int(seconds) % 60
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    else:
        minutes = int(seconds) // 60
        remaining_seconds = int(seconds) % 60
        return f"{minutes:02d}:{remaining_seconds:02d}"


def create_obsidian_note(video_id, youtube_url, df, channel_name, video_date, video_title, duration, channel_id):
    """Create markdown file for Obsidian with video transcription"""
    # Load environment variables
    load_dotenv()
    obsidian_path = os.getenv("B24_OBSIDIAN_VAULT_PATH")

    if not obsidian_path:
        raise ValueError("B24_OBSIDIAN_VAULT_PATH not set in .env file")

    # Format the date and sanitize the title for the filename
    date_str = video_date.strftime("%Y-%m-%d")
    date_prefix = video_date.strftime("%Y%m%d")
    filename = sanitize_name(video_title)
    full_filename = f"{date_prefix} {filename}.md"

    # Get transcription text from database
    db = SessionLocal()
    try:
        transcription = db.query(VideoTranscription).filter_by(video_id=video_id).first()
        transcription_text = transcription.text if transcription else "No transcription available"
    finally:
        db.close()

    # Create markdown content
    content = [
        f"\n![]({youtube_url})\n\n"
        f"### Video\n",
        "| Field | Value |",
        "|-------|-------|",
        f"| Channel | {channel_name} |",
        f"| Title | {video_title} |",
        f"| Published | {date_str} |",
        f"| URL | {youtube_url} |\n\n",
        f"### Transcription\n",
        f"{transcription_text}\n\n",
        "### Segments\n",
    ]

    # Create markdown table
    content.append("| Timestamp | Text |")
    content.append("|-----------|------|")

    for _, row in df.iterrows():
        timestamp = format_timestamp(row['start'], duration)
        content.append(
            f"| [{timestamp}]({row['watch_url']}) | {row['text']} |"
        )

    # First write to markdown folder
    markdown_path = os.path.join('markdown', channel_name)
    os.makedirs(markdown_path, exist_ok=True)
    markdown_file_path = os.path.join(markdown_path, full_filename)
    with open(markdown_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    # Then copy to Obsidian vault
    channel_dir = os.path.join(obsidian_path, "YouTube", "Videos", channel_name)
    os.makedirs(channel_dir, exist_ok=True)
    obsidian_file_path = os.path.join(channel_dir, full_filename)
    
    # Copy the file from markdown folder to Obsidian vault
    import shutil
    shutil.copy2(markdown_file_path, obsidian_file_path)

    # Calculate relative path from vault root
    relative_path = os.path.relpath(obsidian_file_path, obsidian_path)

    # Record note in database
    db = SessionLocal()
    try:
        # Check if note already exists
        existing_note = db.query(Note).filter_by(video_id=video_id).first()
        if existing_note:
            # Update existing note
            existing_note.channel_name = channel_name
            existing_note.file_name = full_filename
            existing_note.relative_path = relative_path
            existing_note.updated_at = datetime.now()
        else:
            # Create new note
            note = Note(
                video_id=video_id,
                channel_id=channel_id,
                channel_name=channel_name,
                file_name=full_filename,
                relative_path=relative_path
            )
            db.add(note)
        db.commit()
    finally:
        db.close()

    return obsidian_file_path


def transcription_exists(video_id):
    """Check if video has already been transcribed by checking DB.
    Returns:
        bool: True if transcription exists, False if not found
    """
    try:
        db = SessionLocal()
        exists_in_db = (
            db.query(VideoTranscription.id).filter_by(video_id=video_id).first()
            is not None
        )
        db.close()
    except Exception as e:
        print(f"Database error: {e}")
        exists_in_db = False

    return exists_in_db


def main():
    """Process all transcribed videos that haven't been stored as markdown yet"""
    ensure_directories()
    
    # Get database session
    db = SessionLocal()
    try:
        # Query for videos that have been transcribed but not stored as markdown
        # Using the not_yet_stored_as_md view and joining with necessary tables
        query = text("""
            SELECT 
                v.video_id,
                yv.title,
                yv.published_at,
                yv.channel_id,
                c.title as channel_name
            FROM not_yet_stored_as_md v
            JOIN yt_video yv ON v.video_id = yv.id
            JOIN yt_channel c ON yv.channel_id = c.id
            ORDER BY yv.published_at DESC
        """)
        videos = db.execute(query).fetchall()
        
        if not videos:
            print("No transcribed videos pending markdown creation found.")
            return
            
        for video in videos:
            try:
                video_id = video.video_id
                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                
                print(f"Processing video: {video.title} ({youtube_url})")
                
                # Convert published_at string to datetime, handling full timestamp format
                try:
                    # Try parsing the full timestamp format first
                    video_date = datetime.strptime(video.published_at, "%Y-%m-%d %H:%M:%S.%f")
                except (ValueError, TypeError):
                    try:
                        # Try just the date part if full timestamp fails
                        video_date = datetime.strptime(video.published_at.split()[0], "%Y-%m-%d")
                    except (ValueError, TypeError, AttributeError):
                        print(f"Warning: Could not parse date {video.published_at}, using current date")
                        video_date = datetime.now()
                
                # Load transcription segments
                df = pd.read_csv(f"./csv_segments/{video_id}.csv")
                df_export = df[["id", "start", "text"]].copy()
                df_export.insert(0, "video_id", video_id)
                df_export.insert(0, "watch_url", youtube_url)
                df_export["watch_url"] = df_export.apply(
                    lambda row: f"{youtube_url}&t={int(row['start'])}", 
                    axis=1
                )
                
                # Create Obsidian note
                file_path = create_obsidian_note(
                    video_id=video_id,
                    youtube_url=youtube_url,
                    df=df_export,
                    channel_name=video.channel_name,
                    video_date=video_date,
                    video_title=video.title,
                    duration=0,  # Default to 0 since we don't have duration
                    channel_id=video.channel_id
                )
                
                print(f"Created markdown file: {file_path}")
                
            except Exception as e:
                print(f"Error processing video {video_id}: {str(e)}")
                continue
                
    finally:
        db.close()

if __name__ == "__main__":
    main()
