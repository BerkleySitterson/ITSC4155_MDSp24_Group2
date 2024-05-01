OPENAI_API_KEY = # Security Issues in putting key

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system", "content": "You are a music assistant, extremely knowledgeable in songs, artists, and albums."},
        {"role":"user", "content": "Show me a list of pop songs."}
    ]
)

print(completion.choices[0].message)
