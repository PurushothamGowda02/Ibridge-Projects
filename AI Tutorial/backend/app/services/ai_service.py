import json
import re
from typing import Any

import httpx

from app.core.config import settings


class AIService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def _chat_json(self, system_prompt: str, user_prompt: str) -> Any:
        if not self.api_key:
            raise Exception("AI Service not configured. Missing GROQ_API_KEY.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            raw = response.json()

        text = raw["choices"][0]["message"]["content"]
        return self._extract_json(text)

    @staticmethod
    def _extract_json(text: str) -> Any:
        clean = (text or "").strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", clean, flags=re.DOTALL)
        if fenced:
            clean = fenced.group(1).strip()
        try:
            return json.loads(clean)
        except Exception:
            match = re.search(r"\{.*\}", clean, flags=re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise

    async def generate_syllabus(self, topic: str, difficulty: str = "Beginner"):
        system_prompt = (
            "You are an expert curriculum architect. Return ONLY valid JSON."
        )
        user_prompt = f"""
Create a structured course syllabus for topic "{topic}" at "{difficulty}" level.
Return JSON:
{{
  "title": "Course title",
  "description": "2-sentence summary",
  "modules": [
    {{
      "title": "Module title",
      "description": "Short description",
      "search_term": "YouTube search phrase"
    }}
  ]
}}
Create 3 to 5 modules.
"""
        return await self._chat_json(system_prompt, user_prompt)

    async def generate_test(self, topic: str, difficulty: str = "Intermediate", test_type: str = "mixed"):
        system_prompt = "You are an expert examiner. Return ONLY valid JSON."
        user_prompt = f"""
Create a {difficulty} {test_type} test for topic "{topic}".
Return JSON in this exact shape:
{{
  "title": "Topic Test",
  "questions": [
    {{"id": 1, "type": "mcq", "question": "...", "options": ["A","B","C","D"], "correct_answer": "..."}},
    {{"id": 2, "type": "mcq", "question": "...", "options": ["A","B","C","D"], "correct_answer": "..."}},
    {{"id": 3, "type": "coding", "task": "..."}}
  ]
}}
Generate 5-7 total questions with at least one coding question.
"""
        return await self._chat_json(system_prompt, user_prompt)

    async def generate_coding_practice(self, subject: str, topic: str, difficulty: str = "Intermediate"):
        system_prompt = "You are a competitive programming mentor. Return ONLY valid JSON."
        user_prompt = f"""
Create coding-only practice for subject "{subject}", topic "{topic}", difficulty "{difficulty}".
Return JSON in this exact shape:
{{
  "problems": [
    {{
      "id": "p1",
      "title": "Problem title",
      "description": "Clear coding problem statement",
      "input_format": "Input format",
      "output_format": "Output format",
      "constraints": "Constraints",
      "sample_input": "Sample input",
      "sample_output": "Sample output",
      "hints": ["Hint 1", "Hint 2"]
    }}
  ]
}}
Generate exactly 3 coding problems.
"""
        return await self._chat_json(system_prompt, user_prompt)


ai_service = AIService()
