from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODELS = {
    "bdd": "llama-3.3-70b-versatile",
    "code": "llama-3.3-70b-versatile"
}

def generate(prompt: str, task_type="bdd"):

    response = client.chat.completions.create(
        model=MODELS[task_type],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content