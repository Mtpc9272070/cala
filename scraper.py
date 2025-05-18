import requests
from bs4 import BeautifulSoup
import base64
import json

url = 'https://television.libre.futbol/tv3/agenda.html'
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

partidos = []

for li in soup.find_all('li'):
    a_tag = li.find('a')
    hora_tag = li.find('span', class_='t')
    enlaces_embed = li.select('ul a[href*="/embed/eventos/?r="]')  # Busca enlaces internos dentro del <ul>

    if a_tag and hora_tag and enlaces_embed:
        titulo = a_tag.get_text(strip=True).replace(hora_tag.get_text(strip=True), '').strip()
        hora = hora_tag.get_text(strip=True)

        for enlace in enlaces_embed:
            try:
                codificado = enlace['href'].split('r=')[1]
                decodificado = base64.b64decode(codificado).decode('utf-8')
                partidos.append({
                    "titulo": titulo,
                    "hora": hora,
                    "enlace": decodificado
                })
            except Exception as e:
                partidos.append({
                    "titulo": titulo,
                    "hora": hora,
                    "enlace": f"Error decoding: {e}"
                })
from datetime import datetime

# Guardar archivo JSON con marca de tiempo incluida
with open('partidos_completos.json', 'w', encoding='utf-8') as f:
    json.dump({
        "actualizado": datetime.now().isoformat(),  # <-- Esta línea asegura que siempre haya un cambio
        "partidos": partidos
    }, f, ensure_ascii=False, indent=2)
