# Dados iniciais

print("Bem-vindo ao NutriKids!")

login = {
    "status": "",
    "email": "user@nutrikids.com.br",
    "senha": "1234",
}

permissions = {
    "funcionario": ["criar", "editar", "visualizar"],
    "responsavel": ["visualizar"]
}

dados_modificados = {
    "nome_da_crianca": "",
    "recomendacao": "",
    "volume_prescrito": "",
    "observacoes": ""
}

quiz_lac = [
    ['Nome', ''],
    ['Idade', 0],
    ['Peso', 0.0],
    ['Sexo', ''],
    ['Tipo de Alimentação', ''],
    ['Fórmula ( se aplicável )', ''],
    ['Frequência de mamadas ( por dia )', 0],
    ['observações Clínicas', '']
]

# Função para forçar o usuário a escolher uma opção
def forca_opcao(msg, lista_opcoes, msg_erro='Opção inválida'):
    opcoes = '\n'.join(lista_opcoes)
    opcao = input(f"{msg}\n{opcoes}\n-> ")
    while opcao not in lista_opcoes:
        print(msg_erro)
        opcao = input(f"{msg}\n{opcoes}\n-> ")
    return opcao

#Função para checar se o número é inteiro
def checa_numero(msg):
    try:
        num = int(input(msg))
        return num
    except ValueError:
        print("Deve ser um número inteiro válido!")
        return checa_numero(msg)

# Funções para área de login*(status, verifica email e senha, fazer logout e login)
def emprega_usuario():
    status = forca_opcao("Você é:", ['funcionario', 'responsavel'])
    login['status'] = status
    print(f"\nSeja bem-vindo(a), {status}!\n")

def autentica_email():
    while True:
        email = input("Digite o seu email:\n-> ")
        if email == login["email"]:
            print("Email validado!\n")
            break
        print("Email incorreto. Tente novamente.")

def autentica_senha():
    while True:
        senha = input("Digite sua senha:\n-> ")
        if senha == login["senha"]:
            print("Senha correta! Acesso concedido.\n")
            break
        print("Senha incorreta. Tente novamente.")

def log_in():
    emprega_usuario()
    autentica_email()
    autentica_senha()
    return permissions.get(login["status"], [])

def logout():
    print(f"{login['status']} desconectado com sucesso.")
    login['status'] = ""

# Funções na area do funcionario

# Essa função serve para saber a idade em meses ou anos, se a criança for maior que 18 anos, não é permitida
# Em meses, deve ser até 12 meses, caso contrário, use a opção de anos
def obter_idade():
    while True:
        formato = forca_opcao("Deseja inserir a idade em:", ['meses', 'anos'], "Escolha 'meses' ou 'anos'")
        idade = input(f"Informe a idade em {formato}: ")
        if not idade.isdigit():
            print("A idade deve ser um número inteiro.")
            continue
        idade = int(idade)
        if formato == 'meses':
            if idade > 12:
                print("Idade em meses deve ser até 12. Se for maior, use anos.")
                continue
            return idade
        else:
            if idade > 18:
                print("A idade máxima permitida é 18 anos.")
                continue
            return idade * 12  # converte para meses


#Função para preencher o questionário com algumas excessões para validar
#Idade chama a função obter_idade()
#Sexo é um forca_opcao para saber se é feminino ou masculino
#Peso tem q ser em número decimal
def preencher_questionario():
    for i in range(len(quiz_lac)):
        campo = quiz_lac[i][0]
        while True:
            if campo == 'Idade':
                quiz_lac[i][1] = obter_idade()
                break
            elif campo == 'Sexo':
                quiz_lac[i][1] = forca_opcao("Informe o sexo da criança:", ['feminino', 'masculino'])
                break
            resposta = input(f"{campo}: ")
            if resposta:
                if campo == 'Frequência de mamadas ( por dia )':
                    if resposta.isdigit():
                        quiz_lac[i][1] = int(resposta)
                        break
                    else:
                        print("A frequência deve ser um número inteiro.")
                        continue
                elif campo == 'Peso':
                    try:
                        quiz_lac[i][1] = float(resposta)
                        break
                    except ValueError:
                        print("O peso deve ser um número decimal.")
                        continue
                else:
                    quiz_lac[i][1] = resposta
                    break
            else:
                print("Campo obrigatório. Tente novamente.")

def escolha_unidade():
    return forca_opcao("Escolha a unidade para visualização do volume: escolha 1 (ml) ou 2 (L)", ["1", "2"])

def calcular_volume():
    idade = quiz_lac[1][1]  # idade em meses
    peso = quiz_lac[2][1]
    mamadas = quiz_lac[6][1]
    fator = 130 if idade <= 12 else 150  # usa fator diferente para recém-nascidos
    volume_dia = peso * fator
    volume_mamada = volume_dia / mamadas

    unidade = "ml"
    if escolha_unidade() == "2":
        volume_dia /= 1000
        volume_mamada /= 1000
        unidade = "L"

    print("\n--- Resultado do Cálculo ---")
    idade_str = f"{idade} meses" if idade <= 12 else f"{idade // 12} anos"
    print(f"Idade: {idade_str}")
    print(f"Peso: {peso:.2f} kg")
    print(f"Volume por dia: {volume_dia:.2f} {unidade}")
    print(f"Volume por mamada: {volume_mamada:.2f} {unidade}")
    if quiz_lac[7][1]:
        print(f"Observações: {quiz_lac[7][1]}")
    else:
        print("Sem observações clínicas.")

    dados_modificados["nome_da_crianca"] = quiz_lac[0][1]
    dados_modificados["recomendacao"] = f"{quiz_lac[4][1]} / Fórmula: {quiz_lac[5][1]}"
    dados_modificados["volume_prescrito"] = f"{volume_mamada:.2f} {unidade} por mamada / {volume_dia:.2f} {unidade} por dia"
    dados_modificados["observacoes"] = quiz_lac[7][1]

def calcular_recomendacao():
    preencher_questionario()
    calcular_volume()

#Função na área do responsável
#O responsável poderá somente visualizar

def visualizar_recomendacao():
    print("\n--- Recomendações do Profissional ---")
    if not dados_modificados["nome_da_crianca"]:
        print("Nenhum dado disponível no momento.")
        return
    print(f"Criança: {dados_modificados['nome_da_crianca']}")
    print(f"Recomendação: {dados_modificados['recomendacao']}")
    print(f"Volume prescrito: {dados_modificados['volume_prescrito']}")
    print(f"Observações: {dados_modificados['observacoes'] or 'Sem observações.'}")

# Ações que para a área do funcionário
# Ações para o responsável

acoes_funcionario = {
    'preencher': calcular_recomendacao,
    'visualizar': visualizar_recomendacao
}

acoes_responsavel = {
    'visualizar': visualizar_recomendacao
}

# Função principal

def sistema_nutrikids():
    permissoes = log_in()
    if login['status'] == 'funcionario':
        while True:
            acao = forca_opcao("Escolha uma ação:", list(acoes_funcionario.keys()) + ['sair'])
            if acao == 'sair':
                logout()
                break
            acoes_funcionario[acao]()
    else:
        while True:
            acao = forca_opcao("Escolha uma ação:", list(acoes_responsavel.keys()) + ['sair'])
            if acao == 'sair':
                logout()
                break
            acoes_responsavel[acao]()

# Função para saber se quer continuar navegando no sistema ou não
while True:
    sistema_nutrikids()
    continuar = forca_opcao("Deseja continuar no sistema?", ['sim', 'não'])
    if continuar == 'não':
        print("Sistema finalizado. Até logo!")
        break
