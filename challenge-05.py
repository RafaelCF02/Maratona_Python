import requests
from bs4 import BeautifulSoup

url = "https://www.iban.com/currency-codes"

#Função que faz o scraping da tabela de países e moedas e retorna uma lista de dicionários.
def obter_dados():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tabela = soup.find("table")
    #Para ignorar o cabeçalho, o código irá pegar a partir do item 1
    linhas = tabela.find_all("tr")[1:]

    lista_paises = []

    for linha in linhas:
        colunas = linha.find_all("td")
        nome_pais = colunas[0].text.strip()
        nome_moeda = colunas[1].text.strip()
        codigo_moeda = colunas[2].text.strip()

        if nome_moeda != "No universal currency":
            lista_paises.append({"nome": nome_pais, "codigo": codigo_moeda})

    return lista_paises

#Função para exibir o menu de países

def exibir_menu(lista_paises):
    print("\nLista de Países Disponíveis:")
    for i, pais in enumerate(lista_paises):
        print(f"[{i + 1}] {pais['nome']}")

#Função para consultar o código de moeda do país escolhido

def consultar_codigo(lista_paises):
    while True:
        try:
            escolha = int(input("\nDigite o número do país para consultar o código da moeda: "))
            if 1 <= escolha <= len(lista_paises):
                pais_selecionado = lista_paises[escolha - 1]
                print(f"\nO código da moeda de {pais_selecionado['nome']} é {pais_selecionado['codigo']}.\n")
                break
            else:
                print(f"Por favor, digite um número entre 1 e {len(lista_paises)}.")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar um número.")

#Função principal do programa, para mostrar o painel

def inicio_programa():
    print("Bem-vindo ao Negociador de Moedas!")
    print("Carregando a lista de países...")
    lista_paises = obter_dados()
    exibir_menu(lista_paises)
    consultar_codigo(lista_paises)

    while True:
        escolha = input("Deseja realizar uma nova consulta? [s/n]: ").lower()
        if escolha == "s":
            inicio_programa()
        elif escolha == "n":
            print("Obrigado por usar o Negociador de Moedas! Até a próxima.")
            break  
        else:
            print("Valor inválido. Por favor, escolha [s/n].")


if __name__ == "__main__":
    inicio_programa()
    