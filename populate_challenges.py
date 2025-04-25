from datetime import datetime, timedelta
import requests
import json
import os
from time import sleep

# Configurações da API
BASE_URL = "http://localhost:8000/api/"
AUTH_URL = f"{BASE_URL}auth/admin/login/"

# Credenciais - substitua com variáveis de ambiente ou um usuário válido
CREDENTIALS = {
    "email": os.getenv("ADMIN_EMAIL", "wilck.oliveira16@gmail.com"),
    "password": os.getenv("ADMIN_PASSWORD", "Gomes#1234")
}

# Função para formatar datas no padrão ISO 8601
def get_formatted_date(days=0):
    date_obj = datetime.now() + timedelta(days=days)
    return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")

# 1. Obter token de autenticação
def get_auth_token():
    try:
        print("Obtendo token de autenticação...")
        response = requests.post(AUTH_URL, json=CREDENTIALS)
        response.raise_for_status()
        token = response.json()['access']
        print("Token obtido com sucesso!")
        return token
    except Exception as e:
        print(f"Erro ao obter token: {e}")
        if hasattr(e, 'response'):
            print(f"Resposta do servidor: {e.response.text}")
        raise

# 2. Funções para criar recursos com tratamento de erros aprimorado
def create_resource(url, data, headers):
    try:
        print(f"\nCriando recurso em {url}...")
        print(f"Dados enviados: {json.dumps(data, indent=2)}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        print("Recurso criado com sucesso!")
        print(f"Resposta: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao criar recurso: {e}")
        if hasattr(e, 'response'):
            print(f"Resposta do servidor ({e.response.status_code}): {e.response.text}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao criar recurso: {e}")
        raise

def create_track(data, headers):
    return create_resource(f"{BASE_URL}challenges/tracks/", data, headers)

def create_challenge(track_id, data, headers):
    """Cria um desafio associado a uma trilha"""
    payload = {
        "track": track_id,
        "start_date": get_formatted_date(),
        "end_date": get_formatted_date(365),
        **data
    }
    return create_resource(f"{BASE_URL}challenges/challenges/", payload, headers)

def create_question(challenge_id, data, headers):
    """Cria uma questão associada a um desafio"""
    payload = {
        "challenge": challenge_id,
        **data
    }
    return create_resource(f"{BASE_URL}challenges/questions/", payload, headers)

def create_option(question_id, data, headers):
    """Cria uma opção associada a uma questão"""
    payload = {
        "question": question_id,
        **data
    }
    return create_resource(f"{BASE_URL}challenges/options/", payload, headers)

# 3. Funções para tipos específicos de desafios
def create_descriptive_challenge(track_id, title, description, points, order, headers):
    return create_challenge(track_id, {
        "title": title,
        "description": description,
        "points": points,
        "difficulty": "EASY",
        "challenge_type": "DESCRIPTION",
        "order": order,
        "is_active": True
    }, headers)

def create_code_challenge(track_id, title, description, points, order, language, 
                         starter_code, solution_code, expected_output, headers):
    return create_challenge(track_id, {
        "title": title,
        "description": description,
        "points": points,
        "difficulty": "EASY",
        "challenge_type": "CODE",
        "language": language,
        "starter_code": starter_code,
        "solution_code": solution_code,
        "expected_output": expected_output,
        "order": order,
        "is_active": True
    }, headers)

def create_choice_challenge(track_id, title, description, points, order, 
                           question_text, options, is_multiple, headers):
    challenge_type = "MULTIPLE_CHOICE" if is_multiple else "SINGLE_CHOICE"
    
    # Criar desafio
    challenge = create_challenge(track_id, {
        "title": title,
        "description": description,
        "points": points,
        "difficulty": "EASY",
        "challenge_type": challenge_type,
        "order": order,
        "is_active": True
    }, headers)
    
    # Criar questão
    question = create_question(challenge['id'], {
        "text": question_text,
        "order": 1
    }, headers)
    
    # Criar opções
    for opt in options:
        create_option(question['id'], {
            "text": opt['text'],
            "is_correct": opt['is_correct'],
            "order": opt['order']
        }, headers)
    
    return challenge

# 4. População completa dos dados
def populate_challenges():
    print("\nIniciando população de dados...")
    
    try:
        # Obter token
        token = get_auth_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        # Pequena pausa para garantir que o token está pronto
        sleep(1)
        
        # ==============================================
        # TRILHA 1: Fundamentos de Python
        # ==============================================
        print("\nCriando Trilha 1: Fundamentos de Python...")
        track1 = create_track({
            "title": "Fundamentos de Python",
            "description": "Aprenda os conceitos básicos da linguagem Python",
            "is_active": True,
            "order": 1,
            "icon": "python"
        }, headers)
        
        print(f"\nTrilha criada com ID: {track1['id']}")
        
        # Desafios da Trilha 1
        print("\nCriando desafios para Trilha 1...")
        
        # Desafio 1 - Descritivo
        print("\n1. Criando desafio descritivo...")
        create_descriptive_challenge(
            track1['id'],
            "O que é Python?",
            "Explique com suas palavras o que é Python e para que é usado.",
            10, 1, headers
        )
        sleep(0.5)
        
        # Desafio 2 - Múltipla Escolha
        print("\n2. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track1['id'],
            "Tipos de dados básicos",
            "Quais dos seguintes são tipos de dados básicos em Python?",
            15, 2,
            "Selecione os tipos de dados básicos em Python:",
            [
                {"text": "int", "is_correct": True, "order": 1},
                {"text": "float", "is_correct": True, "order": 2},
                {"text": "str", "is_correct": True, "order": 3},
                {"text": "list", "is_correct": True, "order": 4},
                {"text": "double", "is_correct": False, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 3 - Única Escolha
        print("\n3. Criando desafio de única escolha...")
        create_choice_challenge(
            track1['id'],
            "Comando de saída",
            "Qual comando usado para imprimir na tela em Python?",
            10, 3,
            "Selecione a opção correta:",
            [
                {"text": "print()", "is_correct": True, "order": 1},
                {"text": "echo()", "is_correct": False, "order": 2},
                {"text": "console.log()", "is_correct": False, "order": 3},
                {"text": "System.out.println()", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        # Desafio 4 - Código
        print("\n4. Criando desafio de código...")
        create_code_challenge(
            track1['id'],
            "Hello World",
            "Complete o código para imprimir 'Hello World'",
            20, 4,
            "python",
            "# Complete o código abaixo\n\ndef hello_world():\n    # Seu código aqui",
            "def hello_world():\n    print('Hello World')",
            "Hello World",
            headers
        )
        sleep(0.5)
        
        # Desafio 5 - Múltipla Escolha
        print("\n5. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track1['id'],
            "Operadores matemáticos",
            "Quais são operadores matemáticos válidos em Python?",
            15, 5,
            "Selecione os operadores válidos:",
            [
                {"text": "+", "is_correct": True, "order": 1},
                {"text": "++", "is_correct": False, "order": 2},
                {"text": "**", "is_correct": True, "order": 3},
                {"text": "//", "is_correct": True, "order": 4},
                {"text": "%%", "is_correct": False, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 6 - Descritivo
        print("\n6. Criando desafio descritivo...")
        create_descriptive_challenge(
            track1['id'],
            "Variáveis em Python",
            "Explique como declarar variáveis em Python e dê exemplos.",
            10, 6, headers
        )
        sleep(0.5)
        
        # Desafio 7 - Única Escolha
        print("\n7. Criando desafio de única escolha...")
        create_choice_challenge(
            track1['id'],
            "Tipo de dado None",
            "O que representa o tipo None em Python?",
            10, 7,
            "Selecione a opção correta:",
            [
                {"text": "Representa um valor nulo ou vazio", "is_correct": True, "order": 1},
                {"text": "É equivalente a zero", "is_correct": False, "order": 2},
                {"text": "É um tipo de erro", "is_correct": False, "order": 3},
                {"text": "Representa um valor indefinido", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        # Desafio 8 - Código
        print("\n8. Criando desafio de código...")
        create_code_challenge(
            track1['id'],
            "Calculadora simples",
            "Complete a função para somar dois números",
            20, 8,
            "python",
            "def soma(a, b):\n    # Complete a função\n    return",
            "def soma(a, b):\n    return a + b",
            "5",
            headers
        )
        sleep(0.5)
        
        # Desafio 9 - Múltipla Escolha
        print("\n9. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track1['id'],
            "Estruturas de controle",
            "Quais são estruturas de controle de fluxo em Python?",
            15, 9,
            "Selecione as estruturas válidas:",
            [
                {"text": "if-elif-else", "is_correct": True, "order": 1},
                {"text": "switch-case", "is_correct": False, "order": 2},
                {"text": "for", "is_correct": True, "order": 3},
                {"text": "while", "is_correct": True, "order": 4},
                {"text": "do-while", "is_correct": False, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 10 - Única Escolha
        print("\n10. Criando desafio de única escolha...")
        create_choice_challenge(
            track1['id'],
            "Indentação em Python",
            "Qual a importância da indentação em Python?",
            10, 10,
            "Selecione a opção correta:",
            [
                {"text": "Define blocos de código", "is_correct": True, "order": 1},
                {"text": "Melhora a legibilidade apenas", "is_correct": False, "order": 2},
                {"text": "É opcional", "is_correct": False, "order": 3},
                {"text": "Define variáveis locais", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        # ==============================================
        # TRILHA 2: Estruturas de Dados em Python
        # ==============================================
        print("\nCriando Trilha 2: Estruturas de Dados em Python...")
        track2 = create_track({
            "title": "Estruturas de Dados em Python",
            "description": "Aprenda sobre listas, tuplas, dicionários e conjuntos",
            "is_active": True,
            "order": 2,
            "icon": "data-array"
        }, headers)
        
        print(f"\nTrilha criada com ID: {track2['id']}")
        
        # Desafios da Trilha 2
        print("\nCriando desafios para Trilha 2...")
        
        # Desafio 1 - Descritivo
        print("\n1. Criando desafio descritivo...")
        create_descriptive_challenge(
            track2['id'],
            "Listas em Python",
            "Explique o que são listas em Python e como são usadas.",
            10, 1, headers
        )
        sleep(0.5)
        
        # Desafio 2 - Múltipla Escolha
        print("\n2. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track2['id'],
            "Métodos de listas",
            "Quais são métodos válidos para listas em Python?",
            15, 2,
            "Selecione os métodos válidos:",
            [
                {"text": "append()", "is_correct": True, "order": 1},
                {"text": "add()", "is_correct": False, "order": 2},
                {"text": "remove()", "is_correct": True, "order": 3},
                {"text": "delete()", "is_correct": False, "order": 4},
                {"text": "pop()", "is_correct": True, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 3 - Única Escolha
        print("\n3. Criando desafio de única escolha...")
        create_choice_challenge(
            track2['id'],
            "Tuplas vs Listas",
            "Qual a principal diferença entre tuplas e listas?",
            10, 3,
            "Selecione a opção correta:",
            [
                {"text": "Tuplas são imutáveis", "is_correct": True, "order": 1},
                {"text": "Listas são mais rápidas", "is_correct": False, "order": 2},
                {"text": "Tuplas usam colchetes", "is_correct": False, "order": 3},
                {"text": "Não há diferença", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        # Desafio 4 - Código
        print("\n4. Criando desafio de código...")
        create_code_challenge(
            track2['id'],
            "Manipulação de listas",
            "Complete o código para adicionar um elemento a uma lista",
            20, 4,
            "python",
            "lista = [1, 2, 3]\n# Adicione o número 4 à lista",
            "lista = [1, 2, 3]\nlista.append(4)",
            "[1, 2, 3, 4]",
            headers
        )
        sleep(0.5)
        
        # Desafio 5 - Múltipla Escolha
        print("\n5. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track2['id'],
            "Operações com dicionários",
            "Quais operações são válidas para dicionários?",
            15, 5,
            "Selecione as operações válidas:",
            [
                {"text": "dicionario['chave']", "is_correct": True, "order": 1},
                {"text": "dicionario.keys()", "is_correct": True, "order": 2},
                {"text": "dicionario.sort()", "is_correct": False, "order": 3},
                {"text": "dicionario.items()", "is_correct": True, "order": 4},
                {"text": "dicionario.append()", "is_correct": False, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 6 - Descritivo
        print("\n6. Criando desafio descritivo...")
        create_descriptive_challenge(
            track2['id'],
            "Conjuntos em Python",
            "Explique o que são conjuntos (sets) em Python e suas características principais.",
            10, 6, headers
        )
        sleep(0.5)
        
        # Desafio 7 - Única Escolha
        print("\n7. Criando desafio de única escolha...")
        create_choice_challenge(
            track2['id'],
            "Fatiamento de listas",
            "Qual o resultado de lista[1:3] se lista = [10, 20, 30, 40]?",
            10, 7,
            "Selecione a opção correta:",
            [
                {"text": "[20, 30]", "is_correct": True, "order": 1},
                {"text": "[10, 20]", "is_correct": False, "order": 2},
                {"text": "[20, 30, 40]", "is_correct": False, "order": 3},
                {"text": "[10, 20, 30]", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        # Desafio 8 - Código
        print("\n8. Criando desafio de código...")
        create_code_challenge(
            track2['id'],
            "Dicionário de contatos",
            "Complete o código para adicionar um contato ao dicionário",
            20, 8,
            "python",
            "contatos = {'João': '1234-5678'}\n# Adicione Maria com telefone '9876-5432'",
            "contatos = {'João': '1234-5678'}\ncontatos['Maria'] = '9876-5432'",
            "{'João': '1234-5678', 'Maria': '9876-5432'}",
            headers
        )
        sleep(0.5)
        
        # Desafio 9 - Múltipla Escolha
        print("\n9. Criando desafio de múltipla escolha...")
        create_choice_challenge(
            track2['id'],
            "Características de conjuntos",
            "Quais são características dos conjuntos (sets) em Python?",
            15, 9,
            "Selecione as características corretas:",
            [
                {"text": "Não permitem elementos duplicados", "is_correct": True, "order": 1},
                {"text": "São ordenados", "is_correct": False, "order": 2},
                {"text": "Podem ser modificados", "is_correct": True, "order": 3},
                {"text": "Usam chaves {}", "is_correct": True, "order": 4},
                {"text": "São mais rápidos que listas para buscas", "is_correct": True, "order": 5}
            ],
            True, headers
        )
        sleep(0.5)
        
        # Desafio 10 - Única Escolha
        print("\n10. Criando desafio de única escolha...")
        create_choice_challenge(
            track2['id'],
            "Compreensão de listas",
            "Para que serve a compreensão de listas em Python?",
            10, 10,
            "Selecione a opção correta:",
            [
                {"text": "Para criar listas de forma concisa", "is_correct": True, "order": 1},
                {"text": "Para entender melhor as listas", "is_correct": False, "order": 2},
                {"text": "Para documentar listas", "is_correct": False, "order": 3},
                {"text": "Para converter strings em listas", "is_correct": False, "order": 4}
            ],
            False, headers
        )
        sleep(0.5)
        
        print("\nPopulação concluída com sucesso!")
        return True
    
    except Exception as e:
        print(f"\nErro durante a população: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando script de população de desafios...")
    try:
        if populate_challenges():
            print("\nTodos os dados foram criados com sucesso!")
        else:
            print("\nOcorreram erros durante a criação dos dados.")
    except Exception as e:
        print(f"\nFalha crítica durante a execução do script: {str(e)}")