import requests
from flask import Flask, render_template, request, abort

app = Flask('maratona_news')

@app.route('/')
def home():
    order_by = request.args.get("order_by", "popular")  
    if order_by == 'news':
        url = 'https://hn.algolia.com/api/v1/search_by_date?tags=story'
    else:
        url = 'https://hn.algolia.com/api/v1/search?tags=story'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta erro em caso de status HTTP >= 400
        resultados = response.json().get("hits", [])
    except requests.exceptions.RequestException as e:
        resultados = []
        print(f"Erro ao buscar dados: {e}")

    return render_template('index.html', resultados=resultados, order_by=order_by)

@app.route('/<id>')
def by_id(id):
    url = f"http://hn.algolia.com/api/v1/items/{id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        resultados = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        abort(404, description="Matéria não encontrada")

    return render_template('id.html', resultados=resultados)

app.run(host='0.0.0.0')