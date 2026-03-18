from requests import get
from bs4 import BeautifulSoup
import json
import time
filmes = []
titulos = []
notas = []
classificacao = []
duracao = []
ano = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
for start in range(1, 1000, 25):
    response = get(f'https://www.imdb.com/pt/search/title/?groups=top_1000&start={start}', headers=headers)
    site = BeautifulSoup(response.content, 'html.parser')
    itens = site.select('li.ipc-metadata-list-summary-item')
    for i in itens:
        titulo = i.select_one('h3').text
        titulo = titulo.split('.', 1)[-1].strip()
        titulos.append(titulo)
        nota = i.find('span', attrs={'class': 'ipc-rating-star--rating'})
        nota = nota.text if nota else None
        notas.append(nota)
        itens2 = i.select('span.dli-title-metadata-item')
        idade = None
        tempo = None
        a = None
        for m in itens2:
            texto = m.text.strip()
            if texto.lower() in ['livre', '10', '12', '14', '16', '18']:
                idade = texto
            elif 'h' in texto or 'min' in texto:
                tempo = texto
            elif texto.isdigit() and len(texto) == 4:
                a = texto
        classificacao.append(idade)
        duracao.append(tempo)
        ano.append(a)
        filmes.append({
            "titulo": titulo,
            "nota": nota,
            "classificacao": idade,
            "duracao": tempo,
            "ano": a
        })
    time.sleep(0.5)
print(len(titulos))
print(len(notas))
print(len(classificacao))
print(len(duracao))
print(len(ano))
print(f'{titulos[0]}')
print(f'{notas[0]}')
print(f'{classificacao[0]}')
print(f'{duracao[0]}')
print(f'{ano[0]}')
with open('filmes.json', 'w', encoding='utf-8') as f:
    json.dump(filmes, f, ensure_ascii=False, indent=4)