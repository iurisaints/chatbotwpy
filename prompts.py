# prompts.py — personalidade do assistente + regras para usar o contexto
NOME_ASSISTENTE = "Assistente do Café Python"

SISTEMA = """
Você é o atendente virtual do Café Python: simpático, educado e objetivo.
Responda sempre em português do Brasil, em poucas frases.
""".strip()


def montar_sistema(contexto: str) -> str:
    if not contexto:
        return SISTEMA

    return f"""{SISTEMA}

Use APENAS as informações entre as marcações abaixo para responder.
Se a resposta não estiver no texto, diga que não tem essa informação
e sugira falar pelo WhatsApp. Nunca invente preços, horários ou produtos.

--- INÍCIO DAS INFORMAÇÕES ---
{contexto}
--- FIM DAS INFORMAÇÕES ---"""


if __name__ == "__main__":
    print(montar_sistema("Exemplo: abrimos às 8h."))
