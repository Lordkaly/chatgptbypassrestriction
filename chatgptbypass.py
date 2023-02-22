import os
import json
import requests
from termcolor import colored

# Lista de bibliotecas necessárias
required_libraries = ['requests', 'termcolor']

# Verifica se cada biblioteca está instalada e a instala se estiver faltando
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(colored(f"The '{library}' library is not installed. Installing it now...", "yellow"))
        os.system(f"pip install {library}")

# Restante do código...

API_KEY_FILE = 'api_key.txt'
API_URL = 'https://api.openai.com/v1/completions'

# Verifica se o arquivo de chave de API existe e lê a chave
try:
    with open(API_KEY_FILE) as f:
        api_key = f.read().strip()
except FileNotFoundError:
    api_key = input(colored("Please enter your OpenAI API key: ", "green"))
    with open(API_KEY_FILE, 'w') as f:
        f.write(api_key)

# Configuração padrão para solicitações à API
model = 'text-davinci-003'
max_tokens = 4000
temperature = 1.0

# Loop principal para permitir várias consultas
while True:
    # Solicita entrada do usuário
    write = input(colored("Ask me anything: ", "green"))
    
    # Verifica se a entrada não está vazia
    if not write:
        print(colored('Please enter a prompt', "red"))
        continue
    
    # Monta a solicitação à API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'prompt': write,
        'max_tokens': max_tokens,
        'temperature': temperature
    }

    # Envia a solicitação à API e verifica a resposta
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        text = response_data['choices'][0]['text']
        print("\n" + colored(text, "yellow"))

        # Pergunta se o usuário deseja salvar a resposta em um arquivo
        choice = input(colored("\nDo you want to save the response to a file? [y/n]: ", "green"))
        if choice.lower() == 'y':
            # Solicita ao usuário um nome para o arquivo de saída
            filename = input(colored("Please enter a name for the output file (without extension): ", "green"))
            filename += '.txt'

            try:
                # Grava a resposta no arquivo de saída
                with open(filename, 'w') as f:
                    f.write(text)
                    print(colored(f"\nResponse saved to {filename}", "blue"))
            except Exception as e:
                print(colored(f"An error occurred while writing the file: {e}", "red"))

    else:
        print(colored('API error: ' + response.text, "red"))
    
    # Pergunta se o usuário deseja fazer outra consulta
    choice = input(colored("\nDo you want to ask something else? [y/n]: ", "green"))
    if choice.lower() != 'y':
        break
