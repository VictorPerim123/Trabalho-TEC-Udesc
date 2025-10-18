import sys
import os

# =============================================================
# Tradutor de Máquinas de Turing entre os modelos de Sipser e
# Fita Duplamente Infinita.
# -------------------------------------------------------------
# Autor: <Seu Nome>
# Disciplina: Teoria da Computação
# Descrição: Este programa traduz autômatos entre os dois
# modelos de Máquina de Turing utilizados no simulador online:
#   http://morphett.info/turing/turing.html
# =============================================================


def ler_linha(linha):
    """Lê uma linha da MT e separa os elementos da transição."""
    partes = linha.strip().split()
    if not partes or partes[0].startswith(';'):
        return None
    return partes[0], partes[1], partes[2], partes[3], partes[4]


def traduzir_sipser_para_dupla_infinita(linhas):
    """Traduz uma MT do modelo de Sipser (fita com início) para o modelo de fita duplamente infinita."""

    saida = [";I ; Traduzido do modelo de Sipser para fita duplamente infinita"]

    # --- Fase 1: preparação da fita (Esta parte estava correta) ---
    saida.extend([
        "; Fase 1: Preparar a fita marcando o início com '#' e deslocando a entrada para a direita",
        "0 0 # R desloca_0",
        "0 1 # R desloca_1",
        "0 * # R desloca_outro", # Adicionando caso genérico para '*'
        "0 _ # R volta_inicio ; Entrada vazia",
        "",
        "desloca_0 0 0 R desloca_0",
        "desloca_0 1 0 R desloca_1",
        "desloca_0 * 0 R desloca_outro",
        "desloca_0 _ 0 L volta_inicio",
        "",
        "desloca_1 0 1 R desloca_0",
        "desloca_1 1 1 R desloca_1",
        "desloca_1 * 1 R desloca_outro",
        "desloca_1 _ 1 L volta_inicio",
        "",
        # Estado para 'outro' (caso a fita tenha símbolos além de 0 e 1)
        "desloca_outro 0 * R desloca_0",
        "desloca_outro 1 * R desloca_1",
        "desloca_outro * * R desloca_outro",
        "desloca_outro _ * L volta_inicio",
        "",
        "volta_inicio * * L volta_inicio",
        "volta_inicio # # R sim_0 ; Pronto para iniciar simulação no estado 0",
        ""
    ])

    # --- Fase 2: adiciona as regras originais ---
    saida.append("; Fase 2: Regras originais traduzidas")
    
    estados_originais = set()
    # Guarda estados que já têm uma regra para 'blank' (_)
    estados_com_regra_blank = set()

    for linha in linhas:
        regra = ler_linha(linha)
        if not regra:
            continue

        q_atual, s_atual, s_novo, direcao, q_novo = regra
        
        # Adiciona estados (não-halt) ao conjunto
        estados_originais.add(q_atual)
        if not q_novo.startswith("halt"):
            estados_originais.add(q_novo)

        q_atual_sim = f"sim_{q_atual}"
        q_novo_sim = f"sim_{q_novo}" if not q_novo.startswith("halt") else q_novo

        if s_atual == '_':
            # Esta é uma regra de 'blank' no Sipser.
            estados_com_regra_blank.add(q_atual_sim)
            
            # 1. Adiciona a regra para o 'blank' da direita
            saida.append(f"{q_atual_sim} _ {s_novo} {direcao} {q_novo_sim} ; Regra original de blank (lado direito)")
            
            # 2. Adiciona a regra para a 'parede' da esquerda
            # (A parede '#' deve ser preservada, então s_novo é '#')
            saida.append(f"{q_atual_sim} # # {direcao} {q_novo_sim} ; Tradução da regra de blank (parede esquerda)")
        else:
            # Regra normal
            saida.append(f"{q_atual_sim} {s_atual} {s_novo} {direcao} {q_novo_sim}")

    # --- Fase 3: simulação da parede (para estados SEM regra de blank) ---
    saida.append("\n; Fase 3: Simulação da parede esquerda (símbolo '#') para estados sem regra de blank")
    
    for estado in sorted(list(estados_originais)):
        sim_estado = f"sim_{estado}"
        if sim_estado not in estados_com_regra_blank:
            # Este estado não esperava bater na parede, então adiciona "bounce"
            saida.append(f"{sim_estado} # # R {sim_estado} ; Cabeçote encontrou o limite esquerdo (bounce)")

    return saida


def traduzir_dupla_infinita_para_sipser(linhas):
    """
    Traduz uma MT de fita duplamente infinita para o modelo de Sipser.
    Versão corrigida v3: Corrige a Fase 1 para deslocar a fita
    para a direita, preservando o primeiro caractere.
    """

    saida = [";S ; Traduzido do modelo de fita duplamente infinita para o modelo de Sipser"]

    # --- Fase 1: Deslocar a fita para a direita para criar espaço para o '#' ---
    saida.extend([
        "; Fase 1: Adicionar '#' e deslocar a entrada para a direita",
        "; Esta fase lê o primeiro símbolo, escreve '#', e então 'empurra' a fita",
        
        # Regras do estado inicial '0'
        "0 0 # R desloca_0",     # Leu 0, escreve #, lembra 0
        "0 1 # R desloca_1",     # Leu 1, escreve #, lembra 1
        "0 * # R desloca_outro", # Leu outro, escreve #, lembra 'outro' (*)
        "0 _ # * sim_0",         # Entrada vazia: escreve # e vai para sim_0
        "",
        
        # Estado 'desloca_0': lembra que leu '0'
        "desloca_0 0 0 R desloca_0",     # Leu 0, escreve 0 (lembrado), lembra 0
        "desloca_0 1 0 R desloca_1",     # Leu 1, escreve 0 (lembrado), lembra 1
        "desloca_0 * 0 R desloca_outro", # Leu outro, escreve 0 (lembrado), lembra 'outro'
        "desloca_0 _ 0 L volta_inicio",  # Fim da fita, escreve 0 (lembrado) e volta
        "",
        
        # Estado 'desloca_1': lembra que leu '1'
        "desloca_1 0 1 R desloca_0",     # Leu 0, escreve 1 (lembrado), lembra 0
        "desloca_1 1 1 R desloca_1",     # Leu 1, escreve 1 (lembrado), lembra 1
        "desloca_1 * 1 R desloca_outro", # Leu outro, escreve 1 (lembrado), lembra 'outro'
        "desloca_1 _ 1 L volta_inicio",  # Fim da fita, escreve 1 (lembrado) e volta
        "",

        # Estado 'desloca_outro': lembra que leu '*' (ou outro)
        "desloca_outro 0 * R desloca_0",     # Leu 0, escreve * (lembrado), lembra 0
        "desloca_outro 1 * R desloca_1",     # Leu 1, escreve * (lembrado), lembra 1
        "desloca_outro * * R desloca_outro", # Leu outro, escreve * (lembrado), lembra 'outro'
        "desloca_outro _ * L volta_inicio",  # Fim da fita, escreve * (lembrado) e volta
        "",

        "; Retorna o cabeçote para o início da fita (primeiro símbolo real)",
        "volta_inicio * * L volta_inicio",
        "volta_inicio # # R sim_0 ; Pronto para iniciar simulação no estado 0",
        ""
    ])

    # --- Fase 2: tradução das regras originais ---
    saida.append("; Fase 2: Regras originais traduzidas")
    saida.append("; Regras para símbolos não-brancos (0, 1, *) e brancos à direita (_)")
    
    estados_simulacao = set()
    estados_simulacao.add("sim_0") 
    regras_de_blank = [] 

    for linha in linhas:
        regra = ler_linha(linha)
        if not regra:
            continue

        q_atual, s_atual, s_novo, direcao, q_novo = regra
        q_atual_sim = f"sim_{q_atual}"
        
        if q_novo.startswith("halt"):
            q_novo_sim = q_novo
        else:
            q_novo_sim = f"sim_{q_novo}"
            estados_simulacao.add(q_novo_sim) 

        estados_simulacao.add(q_atual_sim) 

        if s_atual == '_':
            regras_de_blank.append((q_atual_sim, s_novo, direcao, q_novo_sim))
            saida.append(f"{q_atual_sim} _ {s_novo} {direcao} {q_novo_sim} ; Regra de blank (lado direito)")
        else:
            saida.append(f"{q_atual_sim} {s_atual} {s_novo} {direcao} {q_novo_sim}")

    # --- Fase 3: Adicionar regras da parede esquerda (tradução das regras de 'blank') ---
    saida.append("\n; Fase 3: Regras para simular a parede esquerda ('#')")
    saida.append("; (Tradução das regras que leem '_' no modelo original)")

    estados_com_regra_hash = set()

    for (q_atual_sim, s_novo_original, direcao, q_novo_sim) in regras_de_blank:
        # A parede '#' deve ser sempre preservada, então s_novo é '#'
        saida.append(f"{q_atual_sim} # # {direcao} {q_novo_sim} ; Tradução de ({q_atual}, _, {s_novo_original}, ...)")
        estados_com_regra_hash.add(q_atual_sim)

    # --- Fase 4: Adicionar "bounce" para estados que NÃO têm regra de blank ---
    saida.append("\n; Fase 4: Regras de 'bounce' para estados sem transição explícita para '_'")
    
    for estado in sorted(list(estados_simulacao)):
        if estado not in estados_com_regra_hash:
            saida.append(f"{estado} # # R {estado} ; Parede esquerda, 'bounce'")

    saida.append("\n; Fase 5: Fim da tradução")

    return saida

def main():
    if len(sys.argv) != 2:
        print("Uso: python tradutor_mt.py <arquivo_entrada.in>")
        sys.exit(1)

    caminho_entrada = sys.argv[1]
    if not os.path.exists(caminho_entrada):
        print(f"Erro: o arquivo '{caminho_entrada}' não foi encontrado.")
        sys.exit(1)

    base = os.path.splitext(caminho_entrada)[0]
    caminho_saida = f"{base}.out"

    with open(caminho_entrada, 'r') as arq_in:
        linhas = arq_in.readlines()

    if not linhas:
        print("Erro: o arquivo de entrada está vazio.")
        sys.exit(1)

    primeira = linhas[0].strip()
    programa = linhas[1:]

    if ';S' in primeira:
        print("Traduzindo do modelo de Sipser para o modelo de fita duplamente infinita...")
        conteudo_saida = traduzir_sipser_para_dupla_infinita(programa)
    elif ';I' in primeira:
        print("Traduzindo do modelo de fita duplamente infinita para o modelo de Sipser...")
        conteudo_saida = traduzir_dupla_infinita_para_sipser(programa)
    else:
        print("Erro: a primeira linha deve conter ';S' ou ';I' para indicar o modelo da máquina.")
        sys.exit(1)

    with open(caminho_saida, 'w') as arq_out:
        arq_out.write('\n'.join(conteudo_saida))

    print(f"Tradução concluída com sucesso! O resultado foi salvo em '{caminho_saida}'.")


if __name__ == "__main__":
    main()
