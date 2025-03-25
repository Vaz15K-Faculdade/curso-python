from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Você é responsável por ajudar na criação de códigos em Python. Seja criativa, clara e concisa. Se o usuário enviar um código para ser melhorado, mantenha o código original e forneça sugestões de melhoria, a menos que ele solicite explicitamente que você o substitua."
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

print(completion.choices[0].message)
