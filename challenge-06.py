import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

url_ibans = "https://www.iban.com/currency-codes"

# Função que faz o scraping da tabela de países e moedas e retorna uma lista de dicionários
def obter_dados():
    response = requests.get(url_ibans)
    soup = BeautifulSoup(response.content, "html.parser")

    tabela = soup.find("table")
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

# Função para exibir o menu de países
def exibir_menu(lista_paises):
    print("\nLista de Países Disponíveis:")
    for i, pais in enumerate(lista_paises):
        print(f"[{i + 1}] {pais['nome']} ({pais['codigo']})")

# Função para realizar a conversão de moedas
def converter_moeda(codigo_origem, codigo_destino, quantia):
    url_wise = f"https://wise.com/gb/currency-converter/{codigo_origem.lower()}-to-{codigo_destino.lower()}-rate?amount={quantia}"
    response = requests.get(url_wise)
    soup = BeautifulSoup(response.content, "html.parser")

    # Localiza o valor da taxa de câmbio
    taxa_element = soup.find("span", class_="text-success")
    if not taxa_element:
        print("Não foi possível encontrar a taxa de câmbio no site.")
        return None

    taxa_cambio = float(taxa_element.text.strip().replace(",", ""))
    valor_convertido = quantia * taxa_cambio
    return valor_convertido

# Função para consultar e realizar a conversão
def consultar_codigo(lista_paises):
    while True:
        try:
            escolha_origem = int(input("\nDigite o número do país de origem: "))
            if 1 <= escolha_origem <= len(lista_paises):
                pais_origem = lista_paises[escolha_origem - 1]
                break
            else:
                print(f"Por favor, digite um número entre 1 e {len(lista_paises)}.")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar um número.")

    while True:
        try:
            escolha_destino = int(input("\nDigite o número do país de destino: "))
            if 1 <= escolha_destino <= len(lista_paises):
                pais_destino = lista_paises[escolha_destino - 1]
                break
            else:
                print(f"Por favor, digite um número entre 1 e {len(lista_paises)}.")
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar um número.")

    while True:
        try:
            quantia = float(input("\nDigite o valor que deseja converter: "))
            break
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar um valor numérico.")

    print(f"\nConvertendo {quantia} de {pais_origem['nome']} ({pais_origem['codigo']}) para {pais_destino['nome']} ({pais_destino['codigo']})...")

    valor_convertido = converter_moeda(pais_origem['codigo'], pais_destino['codigo'], quantia)
    if valor_convertido:
        # Formatar valor com código da moeda após o número
        valor_formatado = format_currency(
            valor_convertido, "", locale="pt_BR"
        ).strip()  # Sem o código da moeda
        valor_formatado = f"{valor_formatado} {pais_destino['codigo']}"  # Adiciona o código após o número

        print(f"\nO valor convertido é {valor_formatado}.\n")


# Função principal do programa, para mostrar o painel
def inicio_programa():
    print("Bem-vindo ao Negociador de Moedas!")
    print("Carregando a lista de países...")
    lista_paises = obter_dados()
    exibir_menu(lista_paises)

    while True:
        consultar_codigo(lista_paises)
        escolha = input("\nDeseja realizar uma nova conversão? [s/n]: ").lower()
        if escolha == "s":
            continue
        elif escolha == "n":
            print("Obrigado por usar o Negociador de Moedas! Até a próxima.")
            break
        else:
            print("Valor inválido. Por favor, escolha [s/n].")

if __name__ == "__main__":
    inicio_programa() 