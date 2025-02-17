class BaseLlm:
    def prompt(self, prompts):
        pass


def _user_message(message):
    return {"role": "user", "content": message}


def _system_message(message):
    return {"role": "system", "content": message}


class LlmSession:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def prompt(self, prompt, llm_clean_message=False):
        # self.history.append(_user_message(prompt))
        answer = self.llm.prompt(prompt, llm_clean_message)
        # self.history.append(_system_message(answer))
        return answer

    def get_history(self):
        return self.history
