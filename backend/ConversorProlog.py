import json
import re
import unicodedata

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = texto.replace(" ", "_")
    texto = texto.replace("'", "")
    return texto

def limpar_ano(ano):
    return int(re.sub(r'\D', '', ano))

def limpar_nota(nota):
    return int(nota)

with open('filmes.json', encoding='utf-8') as f:
    dados = json.load(f)

with open('filmes.pl', 'w', encoding='utf-8') as f:
    for filme in dados:
        nome = normalizar_texto(filme['titulo'])
        ano = limpar_ano(filme['ano'])
        nota = limpar_nota(filme['nota'])
        if nota == 0:
            continue

        f.write(f"filme({nome}).\n")

        for g in filme['generos']:
            genero = normalizar_texto(g)
            f.write(f"genero({nome}, {genero}).\n")

        f.write(f"nota({nome}, {nota}).\n")
        f.write(f"ano({nome}, {ano}).\n\n")