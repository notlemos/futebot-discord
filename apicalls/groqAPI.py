import os 
from groq import Groq 


client = Groq(
        api_key=(os.getenv("apiGroqKey"))
)
def groqFut(msg):
        chat_completation = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "você é um assistente brasileiro que vai receber apenas perguntas para explicar algum acontecimento em termos futebolisticos FUTEBOL NORMAL, NÃO FUTEBOL AMERICANO, em 1 parágrafo, com linguagem informal, levando em conta e procurando cada referência da mensagem enviada pelo usuário, seja artista, ou qualquer coisa." 
                        },
                        {
                                "role": "user",
                                "content": f"{msg}"
                        }, 
                ],
                
                model="llama-3.3-70b-versatile",  
        )
        return chat_completation.choices[0].message.content
def groqPop(msg):
        chat_completation = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "você é um assistente brasileiro que vai receber apenas perguntas para explicar algum acontecimento em termos do mundo da musica POP, em 1 parágrafo, com linguagem informal, levando em conta e procurando cada referência da mensagem do usuário"
                        },
                        {
                                "role": "user",
                                "content": f"{msg}"
                        }
                ],
                model="llama-3.3-70b-versatile",
        )
        return chat_completation.choices[0].message.content


