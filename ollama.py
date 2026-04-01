import json

import requests

class BaseLLM:
    def generate(self, prompt):
        raise NotImplementedError

class OllamaLLM(BaseLLM):

    def __init__(self, model: str = "llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        return response.json()["response"]

    def _clean_output(self, text: str) -> str:
        # remove unwanted formatting
        return text.strip().replace("\n", " ")

    def _enforce_word_limit(self, text: str, max_words: int) -> str:
        words = text.split()

        if len(words) <= max_words:
            return text

        return " ".join(words[:max_words])

class LLMService:

    def __init__(self, llm):
        self.llm = llm

    def suggest_resume_improvements(self, resume_text: str, job_description):
        prompt = PromptManager().load(
            "resume_json_generator_prompt",
            {"resume_text": resume_text, "job_description":job_description}
        )

        raw = self.llm.generate(prompt)

        return raw

class PromptManager:

    def __init__(self, base_path="prompts"):
        self.base_path = base_path

    def load(self, prompt_file_name: str, variables: dict) -> str:
        with open(f"{self.base_path}/{prompt_file_name}.txt") as f:
            template = f.read()

        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", value)

        return template