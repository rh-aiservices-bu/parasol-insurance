"""Tests for database models"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.models.sales_representative import SalesRepresentative
from app.backend.db_utils import Base

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)

def test_create_sales_representative(db_session):
    """Test creating a sales representative"""
    rep = SalesRepresentative(
        name="Test Rep",
        email="test@example.com",
        territory="Test Territory",
        tech_domain="Test Domain",
        quota=100000.0,
        ytd_sales=50000.0,
        win_rate=0.5
    )
    db_session.add(rep)
    db_session.commit()
    
    assert rep.id is not None
    assert rep.name == "Test Rep"
    assert rep.email == "test@example.com"

def test_create_opportunity(db_session):
    """Test creating an opportunity"""
    # First create a sales rep
    rep = SalesRepresentative(
        name="Test Rep",
        email="test@example.com",
        territory="Test Territory",
        tech_domain="Test Domain"
    )
    db_session.add(rep)
    db_session.commit()
    
    # Create opportunity
    opp = Opportunity(
        client_company="Test Company",
        opportunity_type="Contract",
        tech_stack=["Python", "Django"],
        project_duration=6,
        budget_min=50000.0,
        budget_max=100000.0,
        sales_rep_id=rep.id
    )
    db_session.add(opp)
    db_session.commit()
    
    assert opp.id is not None
    assert opp.client_company == "Test Company"
    assert opp.sales_rep_id == rep.id

def test_create_candidate(db_session):
    """Test creating a candidate"""
    candidate = Candidate(
        name="Test Candidate",
        email="candidate@example.com",
        phone="1234567890",
        primary_skills=["Python", "Django"],
        tech_stack=["Python", "Django", "React"],
        experience_years=5,
        hourly_rate_min=50.0,
        hourly_rate_max=75.0
    )
    db_session.add(candidate)
    db_session.commit()
    
    assert candidate.id is not None
    assert candidate.name == "Test Candidate"
    assert "Python" in candidate.primary_skills

def test_create_candidate_match(db_session):
    """Test creating a candidate match"""
    # Create sales rep
    rep = SalesRepresentative(
        name="Test Rep",
        email="test@example.com",
        territory="Test Territory",
        tech_domain="Test Domain"
    )
    db_session.add(rep)
    db_session.commit()
    
    # Create opportunity
    opp = Opportunity(
        client_company="Test Company",
        opportunity_type="Contract",
        tech_stack=["Python", "Django"],
        project_duration=6,
        budget_min=50000.0,
        budget_max=100000.0,
        sales_rep_id=rep.id
    )
    db_session.add(opp)
    db_session.commit()
    
    # Create candidate
    candidate = Candidate(
        name="Test Candidate",
        email="candidate@example.com",
        phone="1234567890",
        primary_skills=["Python", "Django"],
        tech_stack=["Python", "Django", "React"],
        experience_years=5,
        hourly_rate_min=50.0,
        hourly_rate_max=75.0
    )
    db_session.add(candidate)
    db_session.commit()
    
    # Create match
    match = CandidateMatch(
        opportunity_id=opp.id,
        candidate_id=candidate.id,
        match_score=0.85,
        match_reason="Strong technical match"
    )
    db_session.add(match)
    db_session.commit()
    
    assert match.id is not None
    assert match.opportunity_id == opp.id
    assert match.candidate_id == candidate.id
    assert match.match_score == 0.85 