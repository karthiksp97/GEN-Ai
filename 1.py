from dotenv import load_dotenv
load_dotenv(override=True)
import os 
from openai import OpenAI
from pypdf import PdfReader  
import gradio as gr
api_key = os.getenv('APIKEY')

if api_key:
    print(api_key)
else:
    raise KeyError("couldn't Load the api key make sure api is there in the.env file ")



reader = PdfReader("Profile.pdf")
linked_in = ""
for pages in reader.pages:
    text = pages.extract_text()
    if text:
        linked_in+=text



summary = ""
with open("summary.txt", "r") as f:
    summary =f.read()



name = "karthikeyan S.p"




system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."




system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linked_in}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."




def chat(message,history):
    chatollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
    messages = [{'role':'system','content':system_prompt}]+history+[{'role':'user','content':message}]
    response = chatollama.chat.completions.create(
    model="mistral:latest",
    messages=messages,
    max_tokens=1000)
    return response.choices[0].message.content
   


gr.ChatInterface(chat, type="messages").launch()