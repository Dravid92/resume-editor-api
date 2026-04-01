import json
import re

import requests


class LMStudioService:

    def __init__(self):
        self.url = "http://localhost:1234/v1/chat/completions"
        self.model = "local-model"  # LM Studio ignores exact name sometimes

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens":5000
            }
        )

        result = response.json()
        print(result["choices"][0]["message"]["content"])
        return self.parse(result["choices"][0]["message"]["content"])


    def parse(self, text: str) -> dict:
        output = re.sub(r"```json", "", text)
        output = re.sub(r"```", "", output)
        print(output)
        return json.loads(output)

