import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

while True:
    user_input = input("You: ")  # Demande une question à l'utilisateur
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye! 👋")
        break
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )

    print("GPT-4o:", response.choices[0].message.content)

