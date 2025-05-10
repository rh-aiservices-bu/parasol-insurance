"""Initial database schema migration for IT Staffing Sales Opportunity Assessment App"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.models.sales_representative import SalesRepresentative
from app.backend.db_utils import Base

def run_migration(database_url: str):
    """Run the initial database migration"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        
        # Add any initial data if needed
        # For example, create a default admin sales representative
        admin_rep = SalesRepresentative(
            name="Admin User",
            email="admin@example.com",
            territory="Global",
            tech_domain="All",
            quota=1000000.0,
            ytd_sales=0.0,
            win_rate=0.0
        )
        session.add(admin_rep)
        
        # Commit the changes
        session.commit()
        
        print("Migration completed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
        
    # Run the migration
    run_migration(database_url) 