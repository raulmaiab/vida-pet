import os
from datetime import datetime

# Arquivos de dados (cada linha: campos separados por '|')
ARQUIVO_PETS    = "pets.txt"
ARQUIVO_EVENTOS = "eventos.txt"
ARQUIVO_METAS   = "metas.txt"
ARQUIVO_TINDER  = "tinder.txt"

def inicializar_arquivos():
    # Garante que todos os arquivos existam, criando-os vazios se necessário
    for caminho in (ARQUIVO_PETS, ARQUIVO_EVENTOS, ARQUIVO_METAS, ARQUIVO_TINDER):
        if not os.path.exists(caminho):
            open(caminho, "a", encoding="utf-8").close()

def ler_registros(caminho, campos_esperados):
#Lê um arquivo de texto e retorna uma lista de listas, cada sublista tem 'campos_esperados' itens
    registros = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split("|")
                if len(partes) != campos_esperados:
                    continue
                registros.append(partes)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna lista vazia
        pass
    return registros

def salvar_registros(caminho, lista_de_listas):
#Regrava todo o arquivo com as linhas em 'lista_de_listas'
    with open(caminho, "w", encoding="utf-8") as f:
        for campos in lista_de_listas:
            f.write("|".join(campos) + "\n")



cadastros_tinder = {}

def carregar_tinder():
#Lê cadastros do Tinder de 'tinder.txt' para o dicionário em memória
    cadastros_tinder.clear()
    try:
        with open(ARQUIVO_TINDER, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split("|")
                if len(partes) != 4:
                    continue
                nome, especie, sexo, descricao = partes
                cadastros_tinder[nome] = [especie, sexo, descricao]
    except FileNotFoundError:
#Garante que o arquivo exista para gravações futuras
        open(ARQUIVO_TINDER, "a", encoding="utf-8").close()

def salvar_tinder():
#Salva o dicionário 'cadastros_tinder' em 'tinder.txt'
    with open(ARQUIVO_TINDER, "w", encoding="utf-8") as f:
        for nome, info in cadastros_tinder.items():
            especie, sexo, descricao = info
            f.write(f"{nome}|{especie}|{sexo}|{descricao}\n")



def tinder_pets():
#Simula um "Tinder" para pets da mesma espécie, com persistência em arquivo
    print("\n--- Tinder de Pets ---")
    nome_login = input("Digite o nome do seu pet: ").strip()

#Verifica existência do pet em pets.txt
    registros = ler_registros(ARQUIVO_PETS, 5)
    encontrado = False
    for campos in registros:
        if campos[0].lower() == nome_login.lower():
            nome_pet = campos[0]
            especie_pet = campos[1]
            encontrado = True
            break
    if not encontrado:
        print("Pet não registrado. Cadastre antes.")
        return

#Coleta descrição e valida sexo
    descricao_pet = input("Breve descrição do seu pet: ").strip()
    sexo_pet = input("Sexo (Masculino/Feminino): ").strip().lower().capitalize()
    if sexo_pet not in ("Masculino", "Feminino"):
        print("Sexo inválido.")
        return

#Atualiza e persiste dicionário de Tinder
    cadastros_tinder[nome_pet] = [especie_pet, sexo_pet, descricao_pet]
    salvar_tinder()

#Menu de ações
    print("\n1 - Procurar match")
    print("2 - Ver meus pedidos")
    escolha = input("Opção: ").strip()

    if escolha == "1":
#Monta lista de possíveis matches
        candidatos = []
        for outro, info in cadastros_tinder.items():
            especie_outro, sexo_outro, _ = info
            if outro == nome_pet:
                continue
            if especie_outro == especie_pet and sexo_outro != sexo_pet:
                candidatos.append(outro)
        if not candidatos:
            print("Nenhum pet disponível para match.")
            return

#Exibe candidatos
        print("Pets disponíveis:")
        for i, cand in enumerate(candidatos, start=1):
            print(f"{i}. {cand}")
        try:
            sel = int(input("Número do pet para convidar: ").strip())
        except ValueError:
            print("Entrada inválida.")
            return
        if sel < 1 or sel > len(candidatos):
            print("Número fora do intervalo.")
            return

#Envia pedido
        destino = candidatos[sel - 1]
        with open(f"caixapostal_{destino}.txt", "a", encoding="utf-8") as f:
            f.write(f"{nome_pet} quer te encontrar\n")
        print("Pedido enviado!")

    elif escolha == "2":
#Lê e exibe pedidos recebidos
        arquivo_caixa = f"caixapostal_{nome_pet}.txt"
        try:
            with open(arquivo_caixa, "r", encoding="utf-8") as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print("Nenhum pedido recebido.")
            return
        if not linhas:
            print("Nenhum pedido recebido.")
            return

        print("Pedidos recebidos:")
        for i, linha in enumerate(linhas, start=1):
            print(f"{i}. {linha.strip()}")
        try:
            sel = int(input("Número do pedido para aceitar (0 para ignorar): ").strip())
        except ValueError:
            print("Entrada inválida.")
            return
        if sel == 0:
            print("Nenhum encontro marcado.")
            return
        if sel < 1 or sel > len(linhas):
            print("Número fora do intervalo.")
            return

        remetente = linhas[sel - 1].split()[0]
        print(f"Encontro marcado com {remetente}!")
    else:
        print("Opção inválida.")

#CRUD de Pets

def adicionar_pet():
#Solicita dados do pet e anexa a pets.txt
    nome = input("Nome do pet: ").strip()
    especie = input("Espécie: ").strip()
    raca = input("Raça: ").strip()
    nasc = input("Nascimento (DD/MM/AAAA): ").strip()
    try:
        datetime.strptime(nasc, "%d/%m/%Y")
    except ValueError:
        print("Data inválida.")
        return
    peso = input("Peso (kg): ").strip()
    try:
        float(peso)
    except ValueError:
        print("Peso inválido.")
        return
    with open(ARQUIVO_PETS, "a", encoding="utf-8") as f:
        f.write(f"{nome}|{especie}|{raca}|{nasc}|{peso}\n")
    print("Pet cadastrado!")

def listar_pets():
#Exibe todos os pets cadastrados
    registros = ler_registros(ARQUIVO_PETS, 5)
    if not registros:
        print("Nenhum pet cadastrado.")
    else:
        for i, campos in enumerate(registros, start=1):
            nome, esp, rac, nasc, pes = campos
            print(f"{i}. {nome} — {esp}, {rac} | Nasc.: {nasc} | Peso: {pes}kg")
    return registros

def editar_pet():
#Permite editar um campo de um pet existente
    registros = ler_registros(ARQUIVO_PETS, 5)
    if not registros:
        print("Nenhum pet para editar.")
        return
    listar_pets()
    try:
        sel = int(input("Número do pet: ").strip())
    except ValueError:
        print("Número inválido.")
        return
    if sel < 1 or sel > len(registros):
        print("Fora do intervalo.")
        return
    campos = registros[sel - 1]
    campo = input("Campo (nome, especie, raca, nascimento, peso): ").strip().lower()
    if campo == "nome":
        campos[0] = input("Novo nome: ").strip()
    elif campo == "especie":
        campos[1] = input("Nova espécie: ").strip()
    elif campo == "raca":
        campos[2] = input("Nova raça: ").strip()
    elif campo == "nascimento":
        novo = input("Nova data (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(novo, "%d/%m/%Y")
            campos[3] = novo
        except ValueError:
            print("Data inválida.")
            return
    elif campo == "peso":
        novo = input("Novo peso: ").strip()
        try:
            float(novo)
            campos[4] = novo
        except ValueError:
            print("Peso inválido.")
            return
    else:
        print("Campo inválido.")
        return
    salvar_registros(ARQUIVO_PETS, registros)
    print("Dados atualizados!")

def excluir_pet():
#Exclui um pet selecionado
    registros = ler_registros(ARQUIVO_PETS, 5)
    if not registros:
        print("Nenhum pet para excluir.")
        return
    listar_pets()
    try:
        sel = int(input("Número do pet: ").strip())
    except ValueError:
        print("Número inválido.")
        return
    if sel < 1 or sel > len(registros):
        print("Fora do intervalo.")
        return
    registros.pop(sel - 1)
    salvar_registros(ARQUIVO_PETS, registros)
    print("Pet excluído!")

def menu_pets():
#Exibe menu de CRUD de pets
    while True:
        print("\n--- Pets ---")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            adicionar_pet()
        elif opc == "2":
            listar_pets()
        elif opc == "3":
            editar_pet()
        elif opc == "4":
            excluir_pet()
        elif opc == "0":
            return
        else:
            print("Opção inválida.")

#CRUD de Eventos

def adicionar_evento():
#Cadastra um evento para um pet já existente
    pets = ler_registros(ARQUIVO_PETS, 5)
    nome_pet = input("Nome do pet: ").strip().lower()
    existe = False
    for registro in pets:
        if registro[0].lower() == nome_pet:
            existe = True
            break
    if not existe:
        print("Pet não cadastrado.")
        return
    tipo = input("Tipo (vacinação, consulta, remédio): ").strip()
    data = input("Data (DD/MM/AAAA): ").strip()
    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        print("Data inválida.")
        return
    observacoes = input("Observações: ").strip()
    with open(ARQUIVO_EVENTOS, "a", encoding="utf-8") as f:
        f.write(f"{nome_pet}|{tipo}|{data}|{observacoes}\n")
    print("Evento cadastrado!")

def listar_eventos():
#Exibe eventos de um pet específico
    registros = ler_registros(ARQUIVO_EVENTOS, 4)
    if not registros:
        print("Nenhum evento cadastrado.")
        return
    nome_pet = input("Nome do pet: ").strip().lower()
    filtros = []
    for registro in registros:
        if registro[0].lower() == nome_pet:
            filtros.append(registro)
    if not filtros:
        print("Nenhum evento para este pet.")
    else:
        contador = 1
        for evento in filtros:
            tipo, data, obs = evento[1], evento[2], evento[3]
            print(f"{contador}. {tipo.capitalize()} em {data}: {obs}")
            contador += 1

def menu_eventos():
#Exibe menu de CRUD de eventos
    while True:
        print("\n--- Eventos ---")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            adicionar_evento()
        elif opc == "2":
            listar_eventos()
        elif opc == "0":
            return
        else:
            print("Opção inválida.")

def sugestoes():
    # Gera sugestões com base em espécie e idade
    pets = ler_registros(ARQUIVO_PETS, 5)
    nome_pet = input("Nome do pet: ").strip().lower()
    dados_pet = None
    for registro in pets:
        if registro[0].lower() == nome_pet:
            dados_pet = registro
            break
    if not dados_pet:
        print("Pet não encontrado.")
        return
    nome, especie, _, nasc, _ = dados_pet
    data_nasc = datetime.strptime(nasc, "%d/%m/%Y")
    idade = (datetime.today() - data_nasc).days // 365
    print(f"\nSugestões para {nome} — {especie.capitalize()}, {idade} anos:")
    
    if especie.lower() == "cachorro":
        print("- Brinquedos: bola, corda, ossinho")
        print("- " + ("Brincadeiras leves" if idade < 1 else "Caminhada diária"))
    elif especie.lower() == "gato":
        print("- Brinquedos: bolinha, arranhador")
        print("- " + ("Brincadeiras curtas" if idade < 1 else "Brinquedos interativos"))
    elif especie.lower() == "hamster":
        print("- Brinquedos: roda de exercícios, tubos e esconderijos")
        print("- " + ("Manuseio delicado e supervisão constante" if idade < 1 else "Ambiente enriquecido com novos objetos semanalmente"))
    else:
        print("Sem sugestões para esta espécie.")

def adicionar_meta():
#Adiciona meta de saúde para um pet já cadastrado
    pets = ler_registros(ARQUIVO_PETS, 5)
    nome_pet = input("Nome do pet: ").strip().lower()
    existe = False
    for registro in pets:
        if registro[0].lower() == nome_pet:
            existe = True
            break
    if not existe:
        print("Pet não cadastrado.")
        return
    descricao_meta = input("Descrição da meta: ").strip()
    tipo_meta = input("Tipo (1-Única, 2-Recorrente): ").strip()
    if tipo_meta not in ("1", "2"):
        print("Tipo inválido.")
        return
    frequencia = input("Frequência: ").strip()
    with open(ARQUIVO_METAS, "a", encoding="utf-8") as f:
        f.write(f"{nome_pet}|{descricao_meta}|{tipo_meta}|{frequencia}|0\n")
    print("Meta adicionada!")

def listar_metas():
#Lista metas cadastradas para um pet específico
    registros = ler_registros(ARQUIVO_METAS, 5)
    if not registros:
        print("Nenhuma meta cadastrada.")
        return []
    nome_pet = input("Nome do pet: ").strip().lower()
    filtros = []
    for registro in registros:
        if registro[0].lower() == nome_pet:
            filtros.append(registro)
    if not filtros:
        print("Nenhuma meta para este pet.")
    else:
        contador = 1
        for registro in filtros:
            descricao_meta = registro[1]
            tipo_meta = registro[2]
            if tipo_meta == "1":
                tipo_texto = "Única"
            else:
                tipo_texto = "Recorrente"
            frequencia = registro[3]
            vezes = registro[4]
            print(f"{contador}. {descricao_meta} — {tipo_texto}, {frequencia} | Cumprida {vezes} vezes")
            contador += 1
    return registros

def marcar_meta():
#Marca uma meta como cumprida incrementando o contador
    registros = ler_registros(ARQUIVO_METAS, 5)
    if not registros:
        print("Nenhuma meta cadastrada.")
        return
    nome_pet = input("Nome do pet: ").strip().lower()
    indices = []
    posicao = 0
    for registro in registros:
        if registro[0].lower() == nome_pet:
            indices.append(posicao)
        posicao += 1
    if not indices:
        print("Nenhuma meta para este pet.")
        return
    contador = 1
    for pos in indices:
        descricao_meta = registros[pos][1]
        vezes = registros[pos][4]
        print(f"{contador}. {descricao_meta} — já cumprida {vezes} vezes")
        contador += 1
    try:
        escolha = int(input("Número da meta para marcar: ").strip())
    except ValueError:
        print("Digite um número válido.")
        return
    if escolha < 1 or escolha > len(indices):
        print("Número fora do intervalo.")
        return
    posicao_selecionada = indices[escolha - 1]
    registros[posicao_selecionada][4] = str(int(registros[posicao_selecionada][4]) + 1)
    salvar_registros(ARQUIVO_METAS, registros)
    print("Meta marcada!")

def menu_metas():
    # Exibe menu de CRUD de metas
    while True:
        print("\n--- Metas ---")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Marcar")
        print("0 - Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            adicionar_meta()
        elif opc == "2":
            listar_metas()
        elif opc == "3":
            marcar_meta()
        elif opc == "0":
            return
        else:
            print("Opção inválida.")

#Menu Principal

def main():
#Ponto de entrada: inicializa arquivos
    inicializar_arquivos()
    carregar_tinder()
    while True:
        print("=== Vida Pet ===")
        print("1 - Pets")
        print("2 - Eventos")
        print("3 - Sugestões")
        print("4 - Metas")
        print("5 - Tinder de Pets")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            menu_pets()
        elif escolha == "2":
            menu_eventos()
        elif escolha == "3":
            sugestoes()
        elif escolha == "4":
            menu_metas()
        elif escolha == "5":
            tinder_pets()
        elif escolha == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")
        input("\n[Enter para continuar]")

if __name__ == "__main__":
    main()
