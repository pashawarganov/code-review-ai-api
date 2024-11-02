from groq import Groq

from settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)

if __name__ == "__main__":  # Test script
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "What is python dzen?",
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)
