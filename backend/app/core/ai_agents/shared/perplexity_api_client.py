import httpx
from typing import List, Dict, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class PerplexityAPIClient:
    def __init__(self):
        # Determine which AI provider to use
        self.provider = getattr(settings, 'AI_PROVIDER', 'perplexity').lower()
        
        if self.provider == 'grok':
            self.api_key = settings.GROK_API_KEY
            self.api_url = settings.GROK_API_URL
            self.default_model = "grok-4-latest"  # Grok 4 latest model
            if not self.api_key:
                logger.error("GROK_API_KEY is not set in environment")
                raise ValueError("GROK_API_KEY is required when AI_PROVIDER is set to 'grok'")
            logger.info("Using Grok (xAI) as AI provider")
        else:
            self.api_key = settings.PERPLEXITY_API_KEY
            self.api_url = settings.PERPLEXITY_API_URL
            self.default_model = "sonar-pro"
            if not self.api_key:
                logger.error("PERPLEXITY_API_KEY is not set in environment")
                raise ValueError("PERPLEXITY_API_KEY is required when AI_PROVIDER is set to 'perplexity'")
            logger.info("Using Perplexity as AI provider")
        
        self.base_url = f"{self.api_url}/chat/completions"
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.3,
        s: int = 2000
    ) -> Dict:
        """
        Send chat completion request to AI provider (Perplexity or Grok)
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (if None, uses default for provider)
            temperature: Sampling temperature
            s: Maximum tokens to generate
        
        Returns:
            API response dict
        """
        # Use default model if none specified
        if model is None:
            model = self.default_model
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"Making {self.provider} API call with key: {self.api_key[:10]}...{self.api_key[-5:]}")
        logger.info(f"API URL: {self.base_url}")
        logger.info(f"Model: {model}")
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "s": s
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.text
                logger.error(f"{self.provider.upper()} API Error ({response.status_code}): {error_detail}")
                logger.error(f"Request payload: {payload}")
                response.raise_for_status()
                
            return response.json()
            
    
    def extract_response_text(self, response: Dict) -> str:
        """Extract text from API response"""
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return ""


# Global instance
perplexity_client = PerplexityAPIClient()