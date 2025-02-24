"""Database configuration and connection management."""

# Database configuration
SQLITE_DB = "youtube.db"
SQLITE_URL = f"sqlite:///{SQLITE_DB}"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine(SQLITE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models after engine creation to avoid circular imports
from step1_setup_db import (
    Base, YTChannel, YTVideo, VideoTranscription, Transcription, Note, NewVideos,
    create_not_yet_transcribed_view, create_not_yet_stored_as_md_view
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create views
create_not_yet_transcribed_view(engine)
create_not_yet_stored_as_md_view(engine)
