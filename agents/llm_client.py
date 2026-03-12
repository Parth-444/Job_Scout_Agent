from langchain_google_genai import ChatGoogleGenerativeAI
import os

key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", api_key=key)

