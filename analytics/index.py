import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ['OPENAI_SECRET']

print(os.environ['OPENAI_SECRET'])

response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)

print(response)