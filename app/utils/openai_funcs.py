import os
import openai

try:
    from dotenv import load_dotenv,find_dotenv
    load_dotenv(find_dotenv())
    openai.api_key = os.environ["OPENAI_API_KEY"]
    print("Using OpenAI API key from environment variable.")
except:     
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key
    

temperature = 0.7
model = "gpt-3.5-turbo-1106"
client = openai.OpenAI()
example_prompt = 'show me some examples of how to use the words, or phrases, or grammar discussed above'
related_prompt = 'show me some related words, or phrases, or grammar that I may not know and can help me understand the the questions better'

def get_response(messages, temperature, model):
    #print(messages)
    try:
        #response = openai.ChatCompletion.create(
        response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        #stream=True
    )
    except Exception as e:
        print(e)
    #print(response)
    #return response['choices'][0]['message']['content']
    return response.choices[0].message.content

def generate_system_message(obj_language, answer_language):
    message = f'''You are helping an individual learn {obj_language}. Please answer in {answer_language}.'''
    return message



