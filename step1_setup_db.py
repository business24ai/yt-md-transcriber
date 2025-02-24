"""Database models for YouTube data."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import text


# Create SQLAlchemy Base
class Base(DeclarativeBase):
    pass


# Simplified Channel Model
class YTChannel(Base):
    __tablename__ = "yt_channel"

    id = Column(String, primary_key=True)  # Channel ID
    title = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    videos = relationship("YTVideo", back_populates="channel")
    notes = relationship("Note", back_populates="channel")


# Video Model
class YTVideo(Base):
    __tablename__ = "yt_video"

    id = Column(String, primary_key=True)  # Video ID
    channel_id = Column(String, ForeignKey("yt_channel.id"))
    title = Column(String)
    video_url = Column(String)  # Full YouTube video URL
    published_at = Column(DateTime)  # Added published date
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    channel = relationship("YTChannel", back_populates="videos")


# Define the VideoTranscription model for complete output
class VideoTranscription(Base):
    __tablename__ = "video_transcriptions"

    id = Column(Integer, primary_key=True)
    video_id = Column(String(50), unique=True)
    text = Column(Text)  # Complete transcription text
    language = Column(String(10))  # Detected language
    duration = Column(Float)  # Duration in seconds
    language_probability = Column(Float)  # Language detection probability
    task = Column(String(20))  # Task type (e.g., "transcribe")
    created_at = Column(String(50))  # Timestamp when transcription was created
    note = relationship("Note", back_populates="video_transcription", uselist=False)


# Update the Transcription model to include all segment information
class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True)
    video_id = Column(String(50))
    segment_id = Column(Integer)
    start = Column(Float)
    end = Column(Float)  # Added end timestamp
    text = Column(Text)
    avg_logprob = Column(Float)  # Confidence score
    compression_ratio = Column(Float)
    no_speech_prob = Column(Float)
    temperature = Column(Float)
    seek = Column(Integer)
    tokens = Column(Text)  # Will store tokens as JSON string


# Define the NewVideos model for tracking new videos to process
class NewVideos(Base):
    __tablename__ = "new_videos"

    video_url = Column(String, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# Define the Notes model for tracking Obsidian markdown notes
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    video_id = Column(String(50), ForeignKey("video_transcriptions.video_id"), unique=True)
    channel_id = Column(String, ForeignKey("yt_channel.id"))
    channel_name = Column(String)
    file_name = Column(String)
    relative_path = Column(String)  # Path relative to vault root
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    video_transcription = relationship("VideoTranscription", back_populates="note")
    channel = relationship("YTChannel", back_populates="notes")


# Create view for videos not yet transcribed
def create_not_yet_transcribed_view(engine):
    """Create a view showing videos that haven't been transcribed yet."""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE VIEW IF NOT EXISTS not_yet_transcribed AS 
            SELECT v.id as video_id, v.published_at, v.video_url 
            FROM yt_video v 
            LEFT JOIN video_transcriptions t ON v.id = t.video_id 
            WHERE t.video_id IS NULL 
            ORDER BY v.published_at DESC;
        """))
        conn.commit()

# Create view for transcribed videos not yet stored as markdown
def create_not_yet_stored_as_md_view(engine):
    """Create a view showing transcribed videos that don't have markdown notes yet."""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE VIEW IF NOT EXISTS not_yet_stored_as_md AS 
            SELECT t.video_id, v.published_at, v.video_url
            FROM video_transcriptions t
            JOIN yt_video v ON t.video_id = v.id
            LEFT JOIN notes n ON t.video_id = n.video_id
            WHERE n.video_id IS NULL
            ORDER BY v.published_at DESC;
        """))
        conn.commit()

# The database connection and table creation is now handled in db_config.py
if __name__ == "__main__":
    from db_config import engine, SessionLocal
    print("Database and tables created successfully")
