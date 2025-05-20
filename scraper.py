import requests
from bs4 import BeautifulSoup
import base64
import json
from datetime import datetime

# URL a scrapear
url = 'https://television.libre.futbol/tv3/agenda.html'
headers = {'User-Agent': 'Mozilla/5.0'}

# Solicitud y análisis del HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

partidos = []

# Buscar todos los <li> con partidos
for li in soup.find_all('li'):
    a_tag = li.find('a')
    hora_tag = li.find('span', class_='t')

    if not a_tag or not hora_tag:
        continue

    titulo = a_tag.get_text(strip=True).replace(hora_tag.get_text(strip=True), '').strip()
    hora = hora_tag.get_text(strip=True)

    # Buscar todos los enlaces dentro del <li> que sean del tipo embed
    enlaces_embed = li.select('a[href*="/embed/eventos/?r="]')
    enlaces_decodificados = []

    for enlace in enlaces_embed:
        try:
            codificado = enlace['href'].split('r=')[1]
            decodificado = base64.b64decode(codificado).decode('utf-8')
            enlaces_decodificados.append(decodificado)
        except Exception as e:
            enlaces_decodificados.append(f"Error decoding: {e}")

    if enlaces_decodificados:
        partidos.append({
            "titulo": titulo,
            "hora": hora,
            "enlace": enlaces_decodificados
        })

# Guardar resultados en JSON
with open('partidos_completos.json', 'w', encoding='utf-8') as f:
    json.dump({
        "actualizado": datetime.now().isoformat(),
        "partidos": partidos
    }, f, ensure_ascii=False, indent=2)

print(f"Scraper finalizado. Se encontraron {len(partidos)} partidos.")
