import google.generativeai as genai

from .base_llm import BaseLlm


class GeminiLlm(BaseLlm):
    """
    Gemini is an implementation of the LLM interface that uses the Gemini API.
    """

    def __init__(self, api_key, system_instruction=None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "models/gemini-1.5-pro",
            system_instruction=system_instruction,
            generation_config=genai.GenerationConfig(
                max_output_tokens=100,
            ),
        )
        self.chat = self.model.start_chat(history=[])

    def prompt(self, prompts, clean_message=False):
        response = self.chat.send_message(prompts)
        answer = response.text

        if clean_message:
            self.chat.history.pop()  # Remove the answer from the history
            self.chat.history.pop()  # Remove the given prompt from the history
        return answer
