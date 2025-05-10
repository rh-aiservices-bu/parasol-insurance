from datetime import datetime
from typing import List, Dict, Any, Optional
from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.db_utils import db

class OpportunityAnalysisService:
    def __init__(self, nlp_model, qualification_model, matching_model):
        self.nlp_model = nlp_model
        self.qualification_model = qualification_model
        self.matching_model = matching_model
        
        # TGS service areas
        self.tgs_services = {
            'cloud': {
                'name': 'Cloud & Infrastructure Modernization',
                'technologies': ['AWS', 'Azure', 'OpenShift', 'Hybrid Cloud'],
                'keywords': ['cloud migration', 'infrastructure', 'modernization']
            },
            'virtualization': {
                'name': 'Virtualization Strategy',
                'technologies': ['VMware', 'OpenShift Virtualization'],
                'keywords': ['virtualization', 'VMware', 'consolidation']
            },
            'mlops': {
                'name': 'AI/ML Foundations',
                'technologies': ['OpenShift AI', 'Kubeflow', 'MLOps'],
                'keywords': ['mlops', 'model deployment', 'pipeline']
            },
            'rag': {
                'name': 'RAG & Document Assistants',
                'technologies': ['InstructLab', 'RAG', 'LLM'],
                'keywords': ['rag', 'chatbot', 'document assistant']
            },
            'data': {
                'name': 'Data Engineering & Governance',
                'technologies': ['Data Pipeline', 'Lineage', 'RBAC'],
                'keywords': ['data pipeline', 'governance', 'compliance']
            },
            'devsecops': {
                'name': 'DevSecOps & Secure AI',
                'technologies': ['Security', 'Compliance', 'AI Operations'],
                'keywords': ['security', 'compliance', 'devsecops']
            },
            'incubator': {
                'name': 'AI Incubator',
                'technologies': ['PoC', 'Quick Start'],
                'keywords': ['poc', 'quick start', 'incubator']
            }
        }
    
    def analyze_opportunity(self, opportunity_id: int) -> Dict[str, Any]:
        """Full analysis of an opportunity"""
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            raise ValueError(f"Opportunity with ID {opportunity_id} not found")
        
        # Extract key information from description
        tech_skills = self.extract_technology_requirements(opportunity.tech_stack)
        
        # Analyze IT landscape and maturity
        landscape_analysis = self.analyze_it_landscape(opportunity)
        
        # Identify TGS service opportunities
        service_opportunities = self.identify_tgs_opportunities(opportunity, landscape_analysis)
        
        # Score opportunity qualification
        qualification_score = self.score_qualification(opportunity, landscape_analysis)
        
        # Find matching candidates
        candidate_matches = self.find_matching_candidates(opportunity, tech_skills)
        
        # Generate pricing recommendation
        pricing_recommendation = self.recommend_pricing(opportunity, candidate_matches)
        
        return {
            'opportunity': opportunity.to_dict(),
            'landscape_analysis': landscape_analysis,
            'service_opportunities': service_opportunities,
            'qualification_score': qualification_score,
            'extracted_skills': tech_skills,
            'candidate_matches': [match.to_dict() for match in candidate_matches],
            'pricing_recommendation': pricing_recommendation
        }
        
    def analyze_it_landscape(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Analyze customer's IT landscape and maturity"""
        # Extract information from opportunity description and tech stack
        description = f"{opportunity.tech_stack} {opportunity.required_certs}"
        
        # Analyze business transformation goals
        transformation_goals = self._analyze_transformation_goals(description)
        
        # Analyze AI/ML maturity
        ai_maturity = self._analyze_ai_maturity(description)
        
        # Analyze infrastructure setup
        infrastructure = self._analyze_infrastructure(description)
        
        # Analyze security and compliance
        security_compliance = self._analyze_security_compliance(description)
        
        return {
            'transformation_goals': transformation_goals,
            'ai_maturity': ai_maturity,
            'infrastructure': infrastructure,
            'security_compliance': security_compliance
        }
        
    def identify_tgs_opportunities(self, opportunity: Opportunity, 
                                 landscape_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify TGS service opportunities based on analysis"""
        opportunities = []
        
        # Analyze description and tech stack for service matches
        description = f"{opportunity.tech_stack} {opportunity.required_certs}"
        
        for service_key, service_info in self.tgs_services.items():
            # Check for technology matches
            tech_matches = any(tech.lower() in description.lower() 
                             for tech in service_info['technologies'])
            
            # Check for keyword matches
            keyword_matches = any(keyword.lower() in description.lower() 
                                for keyword in service_info['keywords'])
            
            if tech_matches or keyword_matches:
                opportunities.append({
                    'service': service_info['name'],
                    'confidence': self._calculate_service_confidence(
                        description, service_info['technologies'], service_info['keywords']
                    ),
                    'recommendations': self._generate_service_recommendations(
                        service_key, landscape_analysis
                    )
                })
        
        return sorted(opportunities, key=lambda x: x['confidence'], reverse=True)
        
    def score_qualification(self, opportunity: Opportunity, 
                          landscape_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate opportunity qualification score"""
        # Prepare features for qualification model
        features = {
            'project_duration': opportunity.project_duration,
            'budget_average': (opportunity.budget_min + opportunity.budget_max) / 2 
                            if opportunity.budget_min and opportunity.budget_max else None,
            'resources_count': opportunity.resources_count,
            'client_history_months': self._get_client_history_months(opportunity.client_company),
            'competition_status': self._parse_competition_count(opportunity.competition_status),
            'requirements_clarity': self._calculate_requirements_clarity(opportunity),
            'service_opportunities': len(self.identify_tgs_opportunities(opportunity, landscape_analysis))
        }
        
        # Get qualification score and risk factors
        qualification_result = self.qualification_model.predict_qualification(features)
        
        # Map score to TGS opportunity rating
        opportunity_rating = self._map_to_tgs_rating(qualification_result['qualification_score'])
        
        return {
            'score': qualification_result['qualification_score'],
            'rating': opportunity_rating,
            'confidence': qualification_result['confidence'],
            'risk_factors': qualification_result['risk_factors'],
            'recommendations': qualification_result['recommendations']
        }
        
    def _analyze_transformation_goals(self, description: str) -> Dict[str, Any]:
        """Analyze business transformation goals"""
        goals = {
            'cloud_migration': False,
            'ai_adoption': False,
            'security_enhancement': False,
            'details': []
        }
        
        # Use NLP model to extract goals
        extracted_goals = self.nlp_model.extract_goals(description)
        
        for goal in extracted_goals:
            if 'cloud' in goal.lower():
                goals['cloud_migration'] = True
            if 'ai' in goal.lower() or 'ml' in goal.lower():
                goals['ai_adoption'] = True
            if 'security' in goal.lower() or 'compliance' in goal.lower():
                goals['security_enhancement'] = True
            goals['details'].append(goal)
            
        return goals
        
    def _analyze_ai_maturity(self, description: str) -> Dict[str, Any]:
        """Analyze AI/ML maturity"""
        maturity = {
            'stage': 'none',  # none, r&d, poc, production
            'mlops_ready': False,
            'data_engineering': False,
            'devsecops': False,
            'toolchain': []
        }
        
        # Use NLP model to analyze AI maturity
        analysis = self.nlp_model.analyze_ai_maturity(description)
        
        maturity.update(analysis)
        return maturity
        
    def _analyze_infrastructure(self, description: str) -> Dict[str, Any]:
        """Analyze infrastructure setup"""
        infrastructure = {
            'cloud_provider': None,
            'container_platform': None,
            'virtualization': None,
            'gpu_available': False,
            'hybrid_setup': False
        }
        
        # Use NLP model to analyze infrastructure
        analysis = self.nlp_model.analyze_infrastructure(description)
        
        infrastructure.update(analysis)
        return infrastructure
        
    def _analyze_security_compliance(self, description: str) -> Dict[str, Any]:
        """Analyze security and compliance"""
        security = {
            'compliance_framework': None,
            'security_gaps': [],
            'governance_issues': [],
            'risk_level': 'low'  # low, medium, high
        }
        
        # Use NLP model to analyze security
        analysis = self.nlp_model.analyze_security(description)
        
        security.update(analysis)
        return security
        
    def _calculate_service_confidence(self, description: str, 
                                    technologies: List[str], 
                                    keywords: List[str]) -> float:
        """Calculate confidence score for service match"""
        tech_matches = sum(1 for tech in technologies 
                          if tech.lower() in description.lower())
        keyword_matches = sum(1 for keyword in keywords 
                             if keyword.lower() in description.lower())
        
        total_matches = tech_matches + keyword_matches
        total_possible = len(technologies) + len(keywords)
        
        return total_matches / total_possible if total_possible > 0 else 0.0
        
    def _generate_service_recommendations(self, service_key: str, 
                                        landscape_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for a service"""
        recommendations = []
        
        if service_key == 'cloud':
            if landscape_analysis['infrastructure']['cloud_provider']:
                recommendations.append(
                    f"Migrate to {landscape_analysis['infrastructure']['cloud_provider']}"
                )
            if landscape_analysis['infrastructure']['hybrid_setup']:
                recommendations.append("Implement hybrid cloud strategy")
                
        elif service_key == 'mlops':
            if not landscape_analysis['ai_maturity']['mlops_ready']:
                recommendations.append("Implement MLOps pipeline")
            if landscape_analysis['ai_maturity']['stage'] == 'poc':
                recommendations.append("Scale PoC to production")
                
        # Add more service-specific recommendations
        
        return recommendations
        
    def _map_to_tgs_rating(self, score: float) -> str:
        """Map qualification score to TGS opportunity rating"""
        if score >= 0.8:
            return "🔥 Hot"
        elif score >= 0.5:
            return "🟠 Lukewarm"
        else:
            return "❄️ Cold"
            
    def _get_client_history_months(self, client_name: str) -> int:
        """Get months of history with this client"""
        # Implementation would query historical opportunities
        return 0
        
    def _parse_competition_count(self, competition_status: str) -> int:
        """Parse number of competitors from status string"""
        if not competition_status:
            return 0
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
        
    def extract_technology_requirements(self, tech_stack: str) -> List[str]:
        """Use NLP to extract technology requirements from description"""
        if not tech_stack:
            return []
            
        # Use NLP model to extract and normalize technology requirements
        extracted_skills = self.nlp_model.extract_skills(tech_stack)
        return extracted_skills
        
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