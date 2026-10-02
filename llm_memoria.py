# llm_memoria.py — perguntar() recebe a LISTA de mensagens (histórico)
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.groq.com/openai/v1/chat/completions"
MODELO = "openai/gpt-oss-20b"


def perguntar(mensagens: list) -> str:
    """Envia a lista completa de mensagens (histórico) para a Groq."""
    api_key = os.getenv("GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODELO,
        "messages": mensagens,
    }

    try:
        resposta = requests.post(URL, headers=headers, json=body, timeout=30)
    except requests.exceptions.RequestException:
        return "Erro de conexão. Verifique sua internet e tente novamente."

    if resposta.status_code == 401:
        return "Erro: API key inválida ou ausente. Verifique GROQ_API_KEY no .env."

    if resposta.status_code == 429:
        return "Erro: limite do free tier da Groq. Aguarde um pouco e tente de novo."

    if resposta.status_code != 200:
        detalhe = ""
        try:
            detalhe = resposta.json().get("error", {}).get("message", "")
        except Exception:
            pass
        return f"Erro inesperado (status {resposta.status_code}). {detalhe}".strip()

    dados = resposta.json()
    return dados["choices"][0]["message"]["content"]


if __name__ == "__main__":
    teste = [{"role": "user", "content": "Diga oi em uma frase curta."}]
    print(perguntar(teste))
