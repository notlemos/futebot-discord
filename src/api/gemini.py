import google.generativeai as genai
import os 

API_KEY = os.getenv('GEMINIKEY')

model = genai.GenerativeModel('gemini-1.5-flash')


def geminiVar(msg):
    full_prompt = (
        "você será encarregado de ler as ultimas mensagens e começar a frase com "
        "\"O VAR FOI CHAMADO E O CORRETO FOI **NOME DA PESSOA CERTA.**\" "
        "(pule linha) e depois obrigado a dissertar o porque da escolha de quem esta correto na discussão que esta ocorrendo. em 1 paragrafo apenas."
        f"\n\nÚltimas mensagens da discussão:\n{'\n'.join(msg)}"
    )
        
    try: 
        response = model.generate_content(full_prompt)
        return response.text
    except genai.types.BlockedPromptException as e:
        print(f"O prompt foi bloqueado por motivos de segurança: {e.safety_ratings}")
        return "Desculpe, não consigo processar essa solicitação devido a problemas de segurança."


        