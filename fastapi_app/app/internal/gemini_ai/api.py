import google.generativeai as genai
from bs4 import BeautifulSoup
import json
from app.core.config import settings

class GeminiAI:
    """Gemini AI integration for intelligent site analysis"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def _get_clean_html(self, html_content: str) -> str:
        """Clean HTML using BeautifulSoup to improve AI analysis."""
        soup = BeautifulSoup(html_content, 'lxml')
        # Remove script and style tags
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        return soup.get_text(separator='\n', strip=True)

    async def analyze_signup_page(self, html_content: str) -> dict:
        """Analyze the signup page to find form elements."""
        clean_html = await self._get_clean_html(html_content)
        prompt = f"""
        Analyze the following HTML of an Amazon registration page and identify the CSS selectors for the form fields.
        I need to fill out the following fields: 'customer_name', 'email', 'password', and 'password_check'.
        Return a JSON object with the selectors.

        HTML:
        {clean_html[:4000]}

        JSON Response format:
        {{
            "customer_name_selector": "...",
            "email_selector": "...",
            "password_selector": "...",
            "password_check_selector": "...",
            "submit_button_selector": "..."
        }}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            response_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(response_text)
        except Exception as e:
            print(f"Error analyzing signup page with Gemini: {e}")
            return {}

    async def find_navigation_element(self, html_content: str, text_to_find: str) -> dict:
        """Find a navigation element (like 'Sign In' or 'Create Account') on the page."""
        clean_html = await self._get_clean_html(html_content)
        prompt = f"""
        Analyze the following HTML and find the CSS selector for the element that contains the text "{text_to_find}".
        This is likely a link (<a>) or a button (<button>).

        HTML:
        {clean_html[:4000]}

        JSON Response format:
        {{
            "selector": "..."
        }}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            response_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(response_text)
        except Exception as e:
            print(f"Error finding navigation element with Gemini: {e}")
            return {}