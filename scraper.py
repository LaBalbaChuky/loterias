
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

def obtener_resultados():
    url = "https://loteriasdominicanas.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    loterias = []

    for item in soup.find_all('div', class_='game-block'):
        loteria = {}
        nombre_tag = item.find('a', class_='game-title')
        loteria['nombre'] = nombre_tag.text.strip() if nombre_tag else "Nombre no disponible"
        fecha_tag = item.find('div', class_='session-date')
        loteria['fecha'] = fecha_tag.text.strip() if fecha_tag else "Fecha no disponible"
        numeros_tag = item.find_all('span', class_='score')
        loteria['numeros'] = [n.text.strip() for n in numeros_tag]
        img_tag = item.find('img', class_='lazy')
        src = img_tag.get('data-src') if img_tag else None
        loteria['imagen'] = f"https://loteriasdominicanas.com{src}" if src and src.startswith('/') else (src or "https://via.placeholder.com/100")
        loterias.append(loteria)

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return loterias, timestamp

def agrupar_loterias(loterias):
    grupos = {
        "Nacional": [], "Leidsa": [], "Loteka": [], "Lotería Real": [],
        "La Primera": [], "New York": [], "Otras": []
    }
    for l in loterias:
        nombre = l['nombre'].lower()
        if "nacional" in nombre:
            grupos["Nacional"].append(l)
        elif "leidsa" in nombre:
            grupos["Leidsa"].append(l)
        elif "loteka" in nombre:
            grupos["Loteka"].append(l)
        elif "real" in nombre:
            grupos["Lotería Real"].append(l)
        elif "primera" in nombre:
            grupos["La Primera"].append(l)
        elif "new york" in nombre or "florida" in nombre:
            grupos["New York"].append(l)
        else:
            grupos["Otras"].append(l)
    return grupos

def crear_html(grupos, actualizacion):
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultados de Hoy RD</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f4f6f8; margin: 0; padding: 0; }}
        header {{ background: #004aad; padding: 20px; text-align: center; }}
        header img {{ max-width: 260px; height: auto; }}
        .grupo-loteria {{ margin: 30px auto; max-width: 1100px; padding: 20px; background: white; border-radius: 12px; }}
        .company-title {{ font-size: 22px; font-weight: bold; color: #004aad; margin-bottom: 10px; border-left: 4px solid #0077ff; padding-left: 10px; }}
        .contenedor-loterias {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
        .tarjeta {{ background: #f9fbfe; border-radius: 12px; width: 250px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 16px; text-align: center; }}
        .tarjeta img {{ height: 50px; object-fit: contain; margin-bottom: 10px; }}
        .tarjeta h3 {{ font-size: 18px; color: #007bff; margin: 0; }}
        .tarjeta .fecha {{ font-size: 14px; color: #555; margin-bottom: 10px; }}
        .numeros {{ display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }}
        .bola {{ background: #fbc02d; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
        footer {{ text-align: center; padding: 20px; font-size: 13px; color: #555; }}
    </style>
</head>
<body>
<header>
    <a href="/"><img src="https://cdn-lottery.kiskoo.com/63e850adcd8910c986e861e8fbab7d34.png" alt="Logo"></a>
</header>
<p style="text-align:center;color:#666;">Última actualización: {actualizacion}</p>
"""
    for grupo, lotes in grupos.items():
        if not lotes:
            continue
        html += f'<div class="grupo-loteria"><div class="company-title">{grupo}</div><div class="contenedor-loterias">'
        for l in lotes:
            html += f"""
            <div class="tarjeta">
                <img src="{l['imagen']}" alt="{l['nombre']}">
                <h3>{l['nombre']}</h3>
                <p class="fecha">{l['fecha']}</p>
                <div class="numeros">
                    {''.join(f'<div class="bola">{n}</div>' for n in l['numeros'])}
                </div>
            </div>
            """
        html += '</div></div>'
    html += '<footer>© Resultados de Hoy RD</footer></body></html>'
    return html

def guardar_html(html):
    with open("resultados.html", "w", encoding="utf-8") as f:
        f.write(html)
