from .web_scraper import WebScraper
from .chatbot import Chatbot
from .preprocessor import Preprocessor
from typing import List
from flask import request, render_template, jsonify, Blueprint


class WebApp:
    def __init__(self):
        self.chatbot = None
        self.last_messages = []

    def get_website_text(self, url: str) -> str:
        scraper = WebScraper(url)
        self.chatbot = Chatbot(scraper.get_text())
        return self.chatbot.context

    def preprocess_text(self, text: str) -> str:
        preprocessor = Preprocessor()
        return preprocessor.remove_blank_lines(text)

    def generate_chatbot(self, text: str) -> None:
        preprocessed_text = self.preprocess_text(text)
        self.chatbot = Chatbot(preprocessed_text)

    def save_message(self, message: str) -> None:
        self.last_messages.append(message)
        if len(self.last_messages) > 10:
            self.last_messages.pop(0)

    def get_last_messages(self) -> List[str]:
        return self.last_messages

    def get_chat_response(self, input_text: str) -> str:
        message = f"User: {input_text}"
        self.save_message(message)

        if self.chatbot is None:
            website_text = ""  # Replace with the appropriate website text
            self.generate_chatbot(website_text)

        response = self.chatbot.get_response(input_text)
        message = f"AI: {response}"
        self.save_message(message)
        return response
    
    def clear_last_messages(self):
        """
        Clears the last_messages list, removing all chat history.
        """
        self.last_messages = self.last_messages[:0]


web_app = WebApp()
