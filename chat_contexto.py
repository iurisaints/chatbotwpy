# chat_contexto.py — chat no terminal que responde com base no contexto.txt
from contexto import carregar_contexto
from llm_memoria import perguntar
from prompts import NOME_ASSISTENTE, montar_sistema

MAX_MENSAGENS = 20
COMANDOS = "Comandos: ajuda | limpar | recarregar | sair"


def historico_para_envio(historico: list) -> list:
    if not historico:
        return historico

    if historico[0].get("role") == "system":
        system = historico[0]
        resto = historico[1:]
        return [system] + resto[-MAX_MENSAGENS:]

    return historico[-MAX_MENSAGENS:]


def novo_historico() -> list:
    sistema = montar_sistema(carregar_contexto())
    return [{"role": "system", "content": sistema}]


def main() -> None:
    print(f"{NOME_ASSISTENTE} — digite 'ajuda' para ver os comandos\n")

    historico = novo_historico()
    total_perguntas = 0

    while True:
        pergunta = input("você> ").strip()
        comando = pergunta.lower()

        if comando == "sair":
            print(f"Até logo! Você fez {total_perguntas} pergunta(s).")
            break

        if comando == "ajuda":
            print(COMANDOS)
            continue

        if comando == "limpar":
            historico = novo_historico()
            print("(memória da conversa limpa)")
            continue

        if comando == "recarregar":
            historico = novo_historico()
            print("(contexto.txt lido de novo — conversa reiniciada)")
            continue

        if not pergunta:
            continue

        historico.append({"role": "user", "content": pergunta})
        resposta = perguntar(historico_para_envio(historico))
        total_perguntas += 1
        print("ia>", resposta)
        print()
        historico.append({"role": "assistant", "content": resposta})


if __name__ == "__main__":
    main()
