import requests
import os

API_TOKEN = "nfp_EXkJbseAYhj4fMLCnbh15rkCzx1PCSzVfb0c"
SITE_ID = "67335cc6-8410-4a0d-8412-1d47f55817cd"

def subir_a_netlify():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }

    # Creamos un nuevo deploy con el archivo resultados.html
    files = {
        "files[resultados.html]": ("resultados.html", open("resultados.html", "rb"), "text/html")
    }

    data = {
        "title": "Actualización automática desde Python",
    }

    response = requests.post(
        f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
        headers=headers,
        files=files,
        data=data
    )

    if response.status_code == 200:
        url = response.json().get("deploy_ssl_url") or response.json().get("deploy_url")
        print("✅ Subido a Netlify (live deploy):", url)
    else:
        print("❌ Error al subir:", response.status_code, response.text)

if __name__ == "__main__":
    subir_a_netlify()
