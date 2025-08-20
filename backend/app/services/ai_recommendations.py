"""
AI-powered recommendations service
"""

import logging
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIRecommendationService:
    """Service for generating AI-powered code recommendations"""
    
    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_recommendations(
        self,
        code_content: str,
        language: str,
        analysis_type: str = "refactoring"
    ) -> List[Dict[str, Any]]:
        """Generate AI-powered recommendations for code"""
        if not self.openai_client:
            logger.warning("OpenAI API key not configured, returning mock recommendations")
            return self._get_mock_recommendations(code_content, language, analysis_type)
        
        try:
            # Prepare prompt for OpenAI
            prompt = self._build_prompt(code_content, language, analysis_type)
            
            # Call OpenAI API
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer and code reviewer. Analyze the provided code and provide specific, actionable recommendations for improvement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response and extract recommendations
            recommendations = self._parse_openai_response(response.choices[0].message.content)
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate AI recommendations: {e}")
            return self._get_mock_recommendations(code_content, language, analysis_type)
    
    def _build_prompt(self, code_content: str, language: str, analysis_type: str) -> str:
        """Build prompt for OpenAI API"""
        prompt = f"""
        Analyze the following {language} code and provide {analysis_type} recommendations.
        
        Code:
        ```{language}
        {code_content}
        ```
        
        Please provide recommendations in the following JSON format:
        {{
            "recommendations": [
                {{
                    "type": "refactoring|security|performance|maintainability",
                    "title": "Brief title",
                    "description": "Detailed description",
                    "severity": "low|medium|high|critical",
                    "confidence": 0.85,
                    "code_snippet": "Relevant code snippet",
                    "suggested_changes": {{
                        "action": "specific action",
                        "target": "what to change",
                        "replacement": "suggested replacement"
                    }},
                    "impact_score": 0.7,
                    "effort_estimate": "low|medium|high"
                }}
            ]
        }}
        
        Focus on practical, actionable improvements that will have the most impact.
        """
        return prompt
    
    def _parse_openai_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse OpenAI API response and extract recommendations"""
        try:
            # This is a simplified parser - in production you'd want more robust JSON parsing
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("recommendations", [])
            
            # Fallback: return empty list
            return []
            
        except Exception as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            return []
    
    def _get_mock_recommendations(
        self,
        code_content: str,
        language: str,
        analysis_type: str
    ) -> List[Dict[str, Any]]:
        """Get mock recommendations when AI service is not available"""
        return [
            {
                "type": "refactoring",
                "title": "Extract Complex Method",
                "description": "The method appears to be doing too many things and could benefit from being broken down into smaller, more focused methods.",
                "severity": "medium",
                "confidence": 0.8,
                "code_snippet": code_content[:100] + "..." if len(code_content) > 100 else code_content,
                "suggested_changes": {
                    "action": "extract_method",
                    "target": "complex_method",
                    "replacement": "Break down into smaller methods"
                },
                "impact_score": 0.7,
                "effort_estimate": "medium"
            },
            {
                "type": "maintainability",
                "title": "Add Documentation",
                "description": "Consider adding docstrings and comments to improve code readability and maintainability.",
                "severity": "low",
                "confidence": 0.9,
                "code_snippet": code_content[:100] + "..." if len(code_content) > 100 else code_content,
                "suggested_changes": {
                    "action": "add_documentation",
                    "target": "functions_and_classes",
                    "replacement": "Add docstrings and inline comments"
                },
                "impact_score": 0.5,
                "effort_estimate": "low"
            }
        ]
    
    async def analyze_code_complexity(self, code_content: str, language: str) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        # This would implement actual complexity analysis
        # For now, return mock data
        
        return {
            "cyclomatic_complexity": 5,
            "lines_of_code": len(code_content.split('\n')),
            "cognitive_complexity": 8,
            "maintainability_index": 75,
            "technical_debt": "medium"
        }
    
    async def generate_security_recommendations(self, code_content: str, language: str) -> List[Dict[str, Any]]:
        """Generate security-focused recommendations"""
        # This would implement security analysis
        # For now, return mock data
        
        return [
            {
                "type": "security",
                "title": "Input Validation",
                "description": "Ensure all user inputs are properly validated and sanitized.",
                "severity": "high",
                "confidence": 0.9,
                "code_snippet": code_content[:100] + "..." if len(code_content) > 100 else code_content,
                "suggested_changes": {
                    "action": "add_validation",
                    "target": "user_inputs",
                    "replacement": "Implement input validation"
                },
                "impact_score": 0.8,
                "effort_estimate": "medium"
            }
        ]
