import requests

urls = str(input("Insira os sites a serem verificados separados por vírgula: ")).lower().split(",")

for url in urls:
    url = url.strip()
    if "." not in url:
        print(f"{url} Site inválido")

    else:
        if "http://" not in url:
            url = f"http://{url}"

        try:

            status = requests.get(url, timeout=5).status_code
            if status == 200:
                print(f"{url} Site Ativo!")
            else:
                print(f"{url} Site Offline!")

        except:
        
            print(f"Erro ao acessar {url}")
       