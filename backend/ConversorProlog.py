import json
import re
import unicodedata

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = re.sub(r'[^a-z0-9 ]', '', texto)  # remove caracteres especiais
    texto = texto.replace(" ", "_")
    return texto

def limpar_ano(ano):
    return int(re.sub(r'\D', '', ano))

def limpar_nota(nota):
    return int(nota)

def converter_duracao(duracao):
    horas = re.search(r'(\d+)h', duracao)
    minutos = re.search(r'(\d+)m', duracao)

    h = int(horas.group(1)) if horas else 0
    m = int(minutos.group(1)) if minutos else 0

    return h * 60 + m

# Carrega o JSON
with open('filmes.json', encoding='utf-8') as f:
    dados = json.load(f)

# Cria o arquivo Prolog
with open('filmes.pl', 'w', encoding='utf-8') as f:
    for filme in dados:
        nome = normalizar_texto(filme['titulo'])

        ano = limpar_ano(filme['ano']) if filme['ano'] else 0
        duracao = converter_duracao(filme['duracao']) if filme['duracao'] else 0
        nota = limpar_nota(filme['nota']) if filme['nota'] else 0

        # ignora filmes sem nota válida
        if nota == 0:
            continue

        f.write(f"filme({nome}).\n")

        # gêneros
        for g in filme.get('generos', []):
            genero = normalizar_texto(g)
            f.write(f"genero({nome}, {genero}).\n")

        f.write(f"nota({nome}, {nota}).\n")
        f.write(f"duracao({nome}, {duracao}).\n")
        f.write(f"ano({nome}, {ano}).\n\n")

print("✅ Arquivo filmes.pl gerado com sucesso!")