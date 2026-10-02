# contexto.py — lê o arquivo de texto que o assistente vai usar como "conhecimento"

# O free tier da Groq limita tokens por minuto; um arquivo enorme estoura o limite.
LIMITE_CARACTERES = 6000


def carregar_contexto(caminho: str = "contexto.txt") -> str:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            texto = arquivo.read().strip()
    except FileNotFoundError:
        print(f"Aviso: arquivo '{caminho}' não encontrado. Seguindo sem contexto.")
        return ""

    if len(texto) > LIMITE_CARACTERES:
        print(f"Aviso: o arquivo tem {len(texto)} caracteres. Usando só os primeiros {LIMITE_CARACTERES}.")
        texto = texto[:LIMITE_CARACTERES]

    return texto


if __name__ == "__main__":
    conteudo = carregar_contexto()
    print(conteudo)
    print("\nTotal de caracteres:", len(conteudo))
