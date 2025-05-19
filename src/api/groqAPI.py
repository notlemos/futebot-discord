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
                                "content": "você é um assistente brasileiro que vai receber apenas perguntas para explicar algum acontecimento em termos futebolisticos FUTEBOL NORMAL, NÃO FUTEBOL AMERICANO, SEJA LA QUAL FOR A MENSAGEM VOCE VAI EXPLICAR EM TERMOS DOS FUTEBOL. em 3/4 linhas, com linguagem informal, levando em conta e procurando cada referência da mensagem enviada pelo usuário, seja artista, ou qualquer coisa." 
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
def groqVar(msg):
        content = "\n".join(msg)
        chat_completation = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "você será encarregado de ler as ultimas mensagens e começar a frase com ""O VAR FOI CHAMADO E O CORRETO FOI **NOME DA PESSOA CERTA.**"" (pule linha)  e depois obrigado a dissertar o porque da escolha de quem esta correto na discussão que esta ocorrendo. em 1 paragrafo apenas."
                        },
                        {
                                "role": "user",
                                "content": f"{content}"
                        }
                ],
                model="llama-3.3-70b-versatile"
        )
        return chat_completation.choices[0].message.content
def groqResenhemetro(msg):
        content = "\n".join(msg)
        chat_completation = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "Você sera encarregado de ser as ultimas mensagens, e retornar a porcentagem de 0 a 100, do quao resenha está a conversa, levando piadas e tudo mais em consideração, na primeira linha voce falará 'O RESENHOMETRO DO PAPO ESTÁ EM ...%, DEPOIS PULE LINHA E ESCREVA EM UMA OU DUAS LINHAS O MOTIVO"
                        },
                        {
                                "role": "user",
                                "content": f"{content}"
                        }
                ],
                model="llama-3.3-70b-versatile"
        )
        return chat_completation.choices[0].message.content 
