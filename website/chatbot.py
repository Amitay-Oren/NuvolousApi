import openai
from flask import Blueprint

class Chatbot:
    #A class for generating responses to user input based on the extracted text.
    def __init__(self, context: str):
        #Initializes the class with the extracted text as context.
        #use the openai envornment variable to set the API key
        openai.api_key = "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"  # Replace with your OpenAI API key
        self.completion = openai.ChatCompletion()

        self.context = context
        last_messages = []
        self.chat_history = []

    def get_response(self, input_text: str) -> str:
        #Generates a response to the user input based on the context.
        prompt = f"{self.context}\nUser: {input_text}\nAI:"
        messages = [
            {"role": "system", "content": "You are a chatbot employee for the company whose website content I will now send you. Answer user inquiries based on that content."},
            {"role": "system", "content": self.context},
            {"role": "user", "content": input_text},
            {"role": "assistant", "content": ""}
        ]
        response = self.completion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            temperature=0.5,
            max_tokens=150,
            top_p=1.0,
            n=1,
            stop=None
        )
        message = response.choices[0].message.content
        self.chat_history.append(f"User: {input_text}\nAI: {message}")
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)
        return message
