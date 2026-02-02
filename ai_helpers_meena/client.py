import google.generativeai as genai

class AIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)

            # WORKING MODEL FOR v1beta KEYS
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def format_response(self, text: str) -> str:
        return " ".join(text.split())

    def get_response(self, prompt: str) -> str:
        if not prompt.strip():
            return "Please provide a prompt."

        if not self.api_key:
            return self._get_mock_response(prompt)

        if not self.model:
            return "Error: Google Generative AI library not initialized."

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error from AI Provider: {str(e)}"

    def _get_mock_response(self, prompt: str):
        return "Mock response: " + prompt
