from datetime import datetime
from typing import List, Dict, Any
from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.db_utils import db

class OpportunityAnalysisService:
    def __init__(self, nlp_model, qualification_model, matching_model):
        self.nlp_model = nlp_model
        self.qualification_model = qualification_model
        self.matching_model = matching_model
    
    def analyze_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Full analysis of an opportunity"""
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            raise ValueError(f"Opportunity with ID {opportunity_id} not found")
        
        # Extract key information from description
        tech_skills = self.extract_technology_requirements(opportunity.tech_stack)
        
        # Score opportunity qualification
        qualification_score = self.score_qualification(opportunity)
        
        # Find matching candidates
        candidate_matches = self.find_matching_candidates(opportunity, tech_skills)
        
        # Generate pricing recommendation
        pricing_recommendation = self.recommend_pricing(opportunity, candidate_matches)
        
        return {
            'opportunity': opportunity.to_dict(),
            'qualification_score': qualification_score,
            'extracted_skills': tech_skills,
            'candidate_matches': [match.to_dict() for match in candidate_matches],
            'pricing_recommendation': pricing_recommendation
        }
        
    def extract_technology_requirements(self, tech_stack: str) -> List[str]:
        """Use NLP to extract technology requirements from description"""
        if not tech_stack:
            return []
            
        # Use NLP model to extract and normalize technology requirements
        extracted_skills = self.nlp_model.extract_skills(tech_stack)
        return extracted_skills
        
    def score_qualification(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Calculate opportunity qualification score"""
        # Prepare features for qualification model
        features = {
            'project_duration': opportunity.project_duration,
            'budget_average': (opportunity.budget_min + opportunity.budget_max) / 2 if opportunity.budget_min and opportunity.budget_max else None,
            'resources_count': opportunity.resources_count,
            'client_history_months': self._get_client_history_months(opportunity.client_company),
            'competition_count': self._parse_competition_count(opportunity.competition_status),
            'requirements_clarity': self._calculate_requirements_clarity(opportunity)
        }
        
        # Get qualification score and risk factors
        qualification_result = self.qualification_model.predict_qualification(features)
        
        return {
            'score': qualification_result['qualification_score'],
            'confidence': qualification_result['confidence'],
            'risk_factors': qualification_result['risk_factors'],
            'recommendations': qualification_result['recommendations']
        }
        
    def find_matching_candidates(self, opportunity: Opportunity, tech_skills: List[str]) -> List[CandidateMatch]:
        """Find candidates matching the opportunity requirements"""
        # Get all available candidates
        candidates = Candidate.query.filter(
            Candidate.availability_date <= opportunity.start_date
        ).all()
        
        matches = []
        for candidate in candidates:
            # Calculate match score using matching model
            match_score = self.matching_model.calculate_match_score(
                candidate=candidate,
                opportunity=opportunity,
                required_skills=tech_skills
            )
            
            if match_score['overall_score'] > 50:  # Only include matches above 50%
                match = CandidateMatch(
                    opportunity_id=opportunity.id,
                    candidate_id=candidate.id,
                    match_score=match_score['overall_score'],
                    skill_match_pct=match_score['skill_match'],
                    rate_match_pct=match_score['rate_match'],
                    availability_match=match_score['availability_match'],
                    notes=match_score['notes']
                )
                matches.append(match)
        
        # Sort matches by score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches
        
    def recommend_pricing(self, opportunity: Opportunity, candidate_matches: List[CandidateMatch]) -> Dict[str, Any]:
        """Generate pricing recommendations based on opportunity and available candidates"""
        if not candidate_matches:
            return {
                'recommended_rate': None,
                'confidence': 0,
                'factors': ['No matching candidates found']
            }
            
        # Calculate average rate from matching candidates
        rates = [match.candidate.hourly_rate_min for match in candidate_matches if match.candidate.hourly_rate_min]
        if not rates:
            return {
                'recommended_rate': None,
                'confidence': 0,
                'factors': ['No rate information available from matching candidates']
            }
            
        avg_rate = sum(rates) / len(rates)
        
        # Adjust rate based on opportunity factors
        adjustments = []
        if opportunity.project_duration and opportunity.project_duration > 6:
            avg_rate *= 0.9  # 10% discount for long-term engagements
            adjustments.append('Long-term engagement discount')
            
        if opportunity.resources_count and opportunity.resources_count > 3:
            avg_rate *= 0.95  # 5% discount for bulk resources
            adjustments.append('Bulk resource discount')
            
        return {
            'recommended_rate': round(avg_rate, 2),
            'confidence': 0.8 if len(rates) > 2 else 0.6,
            'factors': adjustments
        }
        
    def _get_client_history_months(self, client_name: str) -> int:
        """Get months of history with this client"""
        # Implementation would query historical opportunities
        return 0
        
    def _parse_competition_count(self, competition_status: str) -> int:
        """Parse number of competitors from status string"""
        if not competition_status:
            return 0
        # Simple implementation - could be enhanced with NLP
        return len(competition_status.split(','))
        
    def _calculate_requirements_clarity(self, opportunity: Opportunity) -> float:
        """Calculate a score for how clear the requirements are"""
        score = 0.0
        factors = 0
        
        if opportunity.tech_stack:
            score += 1.0
            factors += 1
            
        if opportunity.project_duration:
            score += 1.0
            factors += 1
            
        if opportunity.budget_min and opportunity.budget_max:
            score += 1.0
            factors += 1
            
        if opportunity.resources_count:
            score += 1.0
            factors += 1
            
        if opportunity.seniority_levels:
            score += 1.0
            factors += 1
            
        return score / factors if factors > 0 else 0.0 