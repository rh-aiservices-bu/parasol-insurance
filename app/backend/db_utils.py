from datetime import datetime
import logging
import os
from typing import List, Optional, Dict, Any

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import text

from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.models.sales_representative import SalesRepresentative

Base = declarative_base()

class Database:
    def __init__(self, config: Dict[str, str], logger: logging.Logger):
        self.logger = logger
        self.engine = create_engine(config["DATABASE_URL"])
        self.Session = sessionmaker(bind=self.engine)
        
    def init_db(self):
        """Initialize the database with all tables"""
        Base.metadata.create_all(self.engine)
        
    def list_tables(self) -> List[str]:
        """List all tables in the database"""
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            return [row[0] for row in result]
            
    # Opportunity methods
    def create_opportunity(self, opportunity_data: Dict[str, Any]) -> int:
        """Create a new opportunity"""
        session = self.Session()
        try:
            opportunity = Opportunity(**opportunity_data)
            session.add(opportunity)
            session.commit()
            return opportunity.id
        finally:
            session.close()
            
    def get_opportunity(self, opportunity_id: int) -> Optional[Opportunity]:
        """Get an opportunity by ID"""
        session = self.Session()
        try:
            return session.query(Opportunity).get(opportunity_id)
        finally:
            session.close()
            
    def list_opportunities(self, filters: Dict[str, Any] = None) -> List[Opportunity]:
        """List opportunities with optional filtering"""
        session = self.Session()
        try:
            query = session.query(Opportunity)
            if filters:
                for key, value in filters.items():
                    if hasattr(Opportunity, key):
                        query = query.filter(getattr(Opportunity, key) == value)
            return query.all()
        finally:
            session.close()
            
    def update_opportunity(self, opportunity_id: int, opportunity_data: Dict[str, Any]) -> bool:
        """Update an opportunity"""
        session = self.Session()
        try:
            opportunity = session.query(Opportunity).get(opportunity_id)
            if opportunity:
                for key, value in opportunity_data.items():
                    if hasattr(opportunity, key):
                        setattr(opportunity, key, value)
                session.commit()
                return True
            return False
        finally:
            session.close()
            
    # Candidate methods
    def create_candidate(self, candidate_data: Dict[str, Any]) -> int:
        """Create a new candidate"""
        session = self.Session()
        try:
            candidate = Candidate(**candidate_data)
            session.add(candidate)
            session.commit()
            return candidate.id
        finally:
            session.close()
            
    def get_candidate(self, candidate_id: int) -> Optional[Candidate]:
        """Get a candidate by ID"""
        session = self.Session()
        try:
            return session.query(Candidate).get(candidate_id)
        finally:
            session.close()
            
    def list_candidates(self, filters: Dict[str, Any] = None) -> List[Candidate]:
        """List candidates with optional filtering"""
        session = self.Session()
        try:
            query = session.query(Candidate)
            if filters:
                for key, value in filters.items():
                    if hasattr(Candidate, key):
                        query = query.filter(getattr(Candidate, key) == value)
            return query.all()
        finally:
            session.close()
            
    def update_candidate(self, candidate_id: int, candidate_data: Dict[str, Any]) -> bool:
        """Update a candidate"""
        session = self.Session()
        try:
            candidate = session.query(Candidate).get(candidate_id)
            if candidate:
                for key, value in candidate_data.items():
                    if hasattr(candidate, key):
                        setattr(candidate, key, value)
                session.commit()
                return True
            return False
        finally:
            session.close()
            
    # Sales Representative methods
    def create_sales_rep(self, sales_rep_data: Dict[str, Any]) -> int:
        """Create a new sales representative"""
        session = self.Session()
        try:
            sales_rep = SalesRepresentative(**sales_rep_data)
            session.add(sales_rep)
            session.commit()
            return sales_rep.id
        finally:
            session.close()
            
    def get_sales_rep(self, sales_rep_id: int) -> Optional[SalesRepresentative]:
        """Get a sales representative by ID"""
        session = self.Session()
        try:
            return session.query(SalesRepresentative).get(sales_rep_id)
        finally:
            session.close()
            
    def list_sales_reps(self, filters: Dict[str, Any] = None) -> List[SalesRepresentative]:
        """List sales representatives with optional filtering"""
        session = self.Session()
        try:
            query = session.query(SalesRepresentative)
            if filters:
                for key, value in filters.items():
                    if hasattr(SalesRepresentative, key):
                        query = query.filter(getattr(SalesRepresentative, key) == value)
            return query.all()
        finally:
            session.close()
            
    def update_sales_rep(self, sales_rep_id: int, sales_rep_data: Dict[str, Any]) -> bool:
        """Update a sales representative"""
        session = self.Session()
        try:
            sales_rep = session.query(SalesRepresentative).get(sales_rep_id)
            if sales_rep:
                for key, value in sales_rep_data.items():
                    if hasattr(sales_rep, key):
                        setattr(sales_rep, key, value)
                session.commit()
                return True
            return False
        finally:
            session.close()
            
    # Candidate Match methods
    def create_candidate_match(self, match_data: Dict[str, Any]) -> int:
        """Create a new candidate match"""
        session = self.Session()
        try:
            match = CandidateMatch(**match_data)
            session.add(match)
            session.commit()
            return match.id
        finally:
            session.close()
            
    def get_candidate_match(self, match_id: int) -> Optional[CandidateMatch]:
        """Get a candidate match by ID"""
        session = self.Session()
        try:
            return session.query(CandidateMatch).get(match_id)
        finally:
            session.close()
            
    def list_candidate_matches(self, filters: Dict[str, Any] = None) -> List[CandidateMatch]:
        """List candidate matches with optional filtering"""
        session = self.Session()
        try:
            query = session.query(CandidateMatch)
            if filters:
                for key, value in filters.items():
                    if hasattr(CandidateMatch, key):
                        query = query.filter(getattr(CandidateMatch, key) == value)
            return query.all()
        finally:
            session.close()
            
    def update_candidate_match(self, match_id: int, match_data: Dict[str, Any]) -> bool:
        """Update a candidate match"""
        session = self.Session()
        try:
            match = session.query(CandidateMatch).get(match_id)
            if match:
                for key, value in match_data.items():
                    if hasattr(match, key):
                        setattr(match, key, value)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
