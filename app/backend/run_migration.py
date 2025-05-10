"""Script to run database migrations"""

import os
from dotenv import load_dotenv
from migrations.01_create_initial_schema import run_migration

def main():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Run the migration
    run_migration(database_url)

if __name__ == "__main__":
    main() 