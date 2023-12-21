import os
import openai
from .openai_funcs import get_response

def generate_notes_system_message(obj_language, answer_language):
    message = f'''You are helping an individual learn {obj_language} by generate notes based on conversation history about language learning.
      Your notes should be in {answer_language}. Please only generate notes (not other contents). For example, do not say you are an AI.'''
    return message

def get_notes(obj_language, answer_language, conv_hist, temperature, model):
    system_message = generate_notes_system_message(obj_language, answer_language)
    message = [{"role": "system", "content": system_message}]
    user_messages = f"The conversation history is: {conv_hist}"
    message.append({"role": "user", "content": user_messages})
    
    answer = get_response(message, temperature, model)

    return answer