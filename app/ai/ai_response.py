from openai import OpenAI
from dotenv import load_dotenv
from app.config import settings

load_dotenv()
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = settings.OPENAI_API_KEY
)

def get_response(q: str):
    text = []

    completion = client.chat.completions.create(
      model="meta/llama3-70b-instruct",
      messages=[
         {"role": "system", "content": "Always answer in Russian"},
         {"role":"user","content": q}
      ],
      temperature=0.5,
      top_p=1,
      max_tokens=1024,
      stream=True
    )

    for chunk in completion:
      if chunk.choices[0].delta.content is not None:
        text.append(chunk.choices[0].delta.content)
    return {"response": "".join(text)}