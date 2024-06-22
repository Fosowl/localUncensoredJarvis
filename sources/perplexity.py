import os
from openai import OpenAI

class Perplexity:
    def __init__(self, api_key=""):
        self.api_key = api_key if api_key == "" else os.getenv("PERPLEXITY_API_KEY")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.perplexity.ai")
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you need to "
                    "engage in a helpful, detailed, polite conversation with a user."
                ),
            }
        ]
    
    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
    
    def perplexity_search(self, message, streaming=False):
        if message is None or message == "":
            return "Please provide a message to search for."
        self.add_user_message(message)
        model = "llama-3-sonar-large-32k-online"
        response = None
        response = self.client.chat.completions.create(
            model=model,
            messages=self.messages,
        )
        ans = response.choices[0].message.content
        print("Perplexity search results:", ans)
        return ans

if __name__ == "__main__":
    search = Perplexity()
    res = search.perplexity_search("what are the most recent news")
    print(res)