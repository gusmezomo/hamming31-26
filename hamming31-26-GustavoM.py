def validar_entrada(bits):
    bits = bits.strip()

    # verifica o tamanho e por cada caracter
    
    if len(bits) != 26:
        return False, "a entrada deve ter 26 bits"

    for c in bits:
        if c != "0" and c != "1":
            return False, "a entrada deve conter apenas 0 e 1"

    return True, "entrada valida"


def paridade(pos):
    posicoes_paridade = [1, 2, 4, 8, 16]
    if pos in posicoes_paridade:
        return True
    else:
        return False


def montar_palavra(dados):
    # lista com 32 espaços, o 0 não é usado,
    # assim o índice da lista é igual à posição (1 a 31)
    palavra = [0] * 32

    indice_dado = 0  # qual bit de dado estamos colocando

    for pos in range(1, 32):
        if paridade(pos):
            palavra[pos] = 0  # paridade, será calculada depois
        else:
            palavra[pos] = int(dados[indice_dado])
            indice_dado = indice_dado + 1

    return palavra


def posicoes_verificadas(p):
    # retorna a lista de posições que a paridade p verifica
    posicoes = []
    for pos in range(1, 32):
        if (pos // p) % 2 == 1:
            posicoes.append(pos)
    return posicoes


def calcular_paridades(palavra):
    for p in [1, 2, 4, 8, 16]:
        contador_uns = 0

        for pos in posicoes_verificadas(p):
            if pos != p:  # não conta a própria paridade
                if palavra[pos] == 1:
                    contador_uns = contador_uns + 1

        # paridade par: se a quantidade de 1s for ímpar, a paridade vale 1
        if contador_uns % 2 == 1:
            palavra[p] = 1
        else:
            palavra[p] = 0

    return palavra


def codificar(dados):
    palavra = montar_palavra(dados)
    palavra = calcular_paridades(palavra)
    return palavra


def palavra_para_texto(palavra):
    # junta as posições 1 a 31 em uma string (ignora o 0)
    texto = ""
    for pos in range(1, 32):
        texto = texto + str(palavra[pos])
    return texto


def exibir_resultado(dados, palavra):
    print("entrada (26 bits):   ", dados)
    print("hamming (31 bits):   ", palavra_para_texto(palavra))

    # linha marcando onde estão os bits de paridade
    marcador = ""
    for pos in range(1, 32):
        if paridade(pos):
            marcador = marcador + "P"
        else:
            marcador = marcador + " "
    print("paridades:           ", marcador)


def calcular_sindrome(palavra):
    sindrome = 0

    for p in [1, 2, 4, 8, 16]:
        contador_uns = 0

        for pos in posicoes_verificadas(p):
            if palavra[pos] == 1:  # agora conta a própria paridade também
                contador_uns = contador_uns + 1

        # se a quantidade de 1s for ímpar, essa paridade falhou
        if contador_uns % 2 == 1:
            sindrome = sindrome + p

    return sindrome


def corrigir(palavra):
    corrigida = palavra.copy()
    sindrome = calcular_sindrome(corrigida)

    if sindrome != 0:
        if corrigida[sindrome] == 1:
            corrigida[sindrome] = 0
        else:
            corrigida[sindrome] = 1

    return corrigida, sindrome


# converte a síndrome para binário de 5 bits (ex: 13 -> 01101)
def para_binario_5bits(numero):
    texto = ""
    for p in [16, 8, 4, 2, 1]:
        if numero >= p:
            texto = texto + "1"
            numero = numero - p
        else:
            texto = texto + "0"
    return texto


# mostra como cada bit de paridade foi calculado
def detalhar_paridades(palavra):
    print("\ndetalhe das paridades:")
    for p in [1, 2, 4, 8, 16]:
        posicoes = posicoes_verificadas(p)

        bits = ""
        contador_uns = 0
        for pos in posicoes:
            if pos != p:
                bits = bits + str(palavra[pos])
                if palavra[pos] == 1:
                    contador_uns = contador_uns + 1

        print(f"P{p}: verifica as posições {posicoes}")
        print(f"     bits de dados: {bits} -> {contador_uns} uns -> P{p} = {palavra[p]}")


def validar_palavra_recebida(bits):
    # mesma ideia de validar_entrada, mas com 31 bits
    if len(bits) != 31:
        return False, "a palavra recebida deve ter 31 bits"

    for c in bits:
        if c != "0" and c != "1":
            return False, "a palavra deve conter apenas 0 e 1"

    return True, "palavra valida"


def texto_para_palavra(bits):
    # transforma a string em lista, com o índice 0 sobrando
    palavra = [0]
    for c in bits:
        palavra.append(int(c))
    return palavra


def main():
    while True:
        print("\nHamming (31, 26)")
        print("1 - codificar (26 bits)")
        print("2 - verificar e corrigir palavra recebida (31 bits)")
        opcao = input("escolha: ").strip()

        if opcao == "1":
            dados = input("digite os 26 bits: ").strip()
            valido, mensagem = validar_entrada(dados)

            if not valido:
                print("erro:", mensagem)
            else:
                palavra = codificar(dados)
                exibir_resultado(dados, palavra)
                detalhar_paridades(palavra)

        elif opcao == "2":
            recebida = input("digite a palavra recebida (31 bits): ").strip()
            valido, mensagem = validar_palavra_recebida(recebida)

            if not valido:
                print("erro:", mensagem)
            else:
                palavra = texto_para_palavra(recebida)
                corrigida, sindrome = corrigir(palavra)

                print("palavra recebida:  ", recebida)
                print("sindrome:          ", sindrome, "=", para_binario_5bits(sindrome))

                if sindrome == 0:
                    print("nenhum erro detectado.")
                else:
                    print("erro na posição:   ", sindrome)
                    print("palavra corrigida: ", palavra_para_texto(corrigida))

        else:
            print("opção invalida.")


main()