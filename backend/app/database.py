from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timezone
import json

# Create SQLite database engine
engine = create_engine('sqlite:///./listings.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(String, index=True, unique=True)  # e.g., "VA"
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    zip_codes = relationship("ZipCode", back_populates="state", cascade="all, delete-orphan")

class ZipCode(Base):
    __tablename__ = "zip_codes"

    id = Column(Integer, primary_key=True, index=True)
    zip_code = Column(String, index=True)
    state_id = Column(Integer, ForeignKey("states.id"))
    listings = Column(JSON)  # Store all listings for this zip code
    state = relationship("State", back_populates="zip_codes")

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_database():
    """Clear all data from the database."""
    db = SessionLocal()
    try:
        # Delete all records from both tables
        db.query(ZipCode).delete()
        db.query(State).delete()
        db.commit()
        print("Database cleared successfully")
    except Exception as e:
        db.rollback()
        print(f"Error clearing database: {str(e)}")
        raise
    finally:
        db.close()

def view_cached_states():
    """View all cached states and their zip codes in the database."""
    db = SessionLocal()
    try:
        states = db.query(State).all()
        for state in states:
            print(f"\nState: {state.state_code}")
            print(f"Last Updated: {state.last_updated}")
            print(f"Number of Zip Codes: {len(state.zip_codes)}")
            
            # Show sample data for first zip code
            if state.zip_codes:
                first_zip = state.zip_codes[0]
                listings = first_zip.listings
                print(f"\nSample Zip Code: {first_zip.zip_code}")
                print(f"Number of Listings: {len(listings)}")
                if listings:
                    sample = listings[0]
                    print(f"  Address: {sample.get('formattedAddress')}")
                    print(f"  City: {sample.get('city')}")
                    print(f"  Price: ${sample.get('price'):,.2f}")
            print("-" * 50)
    finally:
        db.close() 