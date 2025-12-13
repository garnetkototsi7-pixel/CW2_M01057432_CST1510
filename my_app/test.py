from google.genai import Client

import streamlit as st

api_key="AIzaSyAImZJ_CAIWVWOaOXtwKQpT_ljcOPgb08g"
client =Client(api_key=api_key)
print("Gemini with Memory. Type 'quit' to exit.\n")
messages = [
{
"role": "user",
"parts": [
{
"text": "Your name is now Tom"
}]
},]
while True:
  user_input = input("You: ")
  if user_input.lower() == "quit":
   break # Add user message to history
  
  messages.append({"role": "user", "parts": [{"text": user_input}]})
  response = client.models.generate_content_stream(
  model="gemini-flash-lite-latest",
  contents=messages,
  )

full_reply = ""
for chunk in response:
  full_reply += chunk.text
  print(full_reply, end="")
  messages.append({"role": "model", "parts": [{"text": full_reply}]})
