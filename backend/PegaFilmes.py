from requests import get
from bs4 import BeautifulSoup
import json
import time
filmes = []
titulos_vistos = set()
headers = {
    "User-Agent": "Mozilla/5.0"
}
for page in range(1, 30): 
    response = get(f'https://www.themoviedb.org/movie?page={page}', headers=headers)
    site = BeautifulSoup(response.content, 'html.parser')
    itens = site.select('div.card')
    for i in itens:
        titulo_tag = i.select_one('h2 a')
        if not titulo_tag:
            continue
        titulo = titulo_tag.text.strip()
        if titulo in titulos_vistos:
            continue
        titulos_vistos.add(titulo)
        link = titulo_tag['href']
        url_filme = 'https://www.themoviedb.org' + link
        response_filme = get(url_filme, headers=headers)
        site_filme = BeautifulSoup(response_filme.content, 'html.parser')
        nota_tag = site_filme.select_one('div.user_score_chart')
        nota = nota_tag['data-percent'] if nota_tag and nota_tag.has_attr('data-percent') else None
        duracao_tag = site_filme.select_one('span.runtime')
        duracao = duracao_tag.text.strip() if duracao_tag else None
        generos_tag = site_filme.select('span.genres a')
        generos = [g.text.strip() for g in generos_tag] if generos_tag else []
        ano_tag = site_filme.select_one('span.release_date')
        ano = ano_tag.text.strip() if ano_tag else None
        filmes.append({
            "titulo": titulo,
            "nota": nota,
            "duracao": duracao,
            "ano": ano,
            "generos": generos,
        })

        #print(f'✔ {titulo}')#

        time.sleep(0.3)  

print(f'Total de filmes: {len(filmes)}')

with open('filmes.json', 'w', encoding='utf-8') as f:
    json.dump(filmes, f, ensure_ascii=False, indent=4)