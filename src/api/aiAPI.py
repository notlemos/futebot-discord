import os 
from groq import Groq 
import google.genai as genai
client = Groq(
        api_key=(os.getenv("apiGroqKey"))
)
client_gemini = genai.Client(api_key=os.getenv("apiGemini"))
async def geminiResume(msg):
        prompt = (
                "Aja como um assistente especialista em análise cinematográfica. "
                "Abaixo, fornecerei um trecho da transcrição de um filme (extraído de legendas). "
                "Sua tarefa é: 1. Criar um resumo conciso (em português) do que aconteceu nesse período; "
                "2. Identificar personagens interagindo; 3. Destacar o tom da cena. "
                "Importante: Ignore erros de transcrição e FOQUE NA NARRATIVA. "
                "RESPONDA TUDO EM UM ÚNICO PARÁGRAFO CURTO, SEM QUEBRAS DE LINHA. "
                f"Trecho: {msg}"
        )
        
        response = await client_gemini.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
        )
        return response.text
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
def groqMovie(msg):
    if not msg:
        return "Não há texto suficiente para resumir."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Sua tarefa é  resumir o filme com base no trecho da legenda. Apenas os acontecimentos RELEVANTES. "
                    "Colocando os acontecimentos em varios tópicos começando com ""-"" "
                    "o trecho da legenda fornecido com o MÁXIMO de detalhes possível.\n\n"
                    "OBJETIVO: Escrever um texto rico e extenso que se aproxime dos 500 caracteres.\n"
                    "CONTEÚDO: Descreva as ações, os diálogos cruciais\n"
                    "TRAVA: NUNCA NUNCA MAS NUNCA ultrapasse 500 caracteres sob nenhuma circunstância."
                    "ESTILO: TUDO EM TÓPICOS COMEÇANDO COM ""-"""
                )
            },
            {
                "role": "user",
                "content": f"Faça um resume deste trecho: {msg}"
            }, 
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.6,
        
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
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
                                "content": "você será encarregado de ler as ultimas mensagens e começar a frase com ""O VAR FOI CHAMADO E O CORRETO FOI **NOME DA PESSOA CERTA.**"" (pule linha)  e depois obrigado a dissertar o porque da escolha de quem esta correto na discussão que esta ocorrendo. em 1 linha"
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
