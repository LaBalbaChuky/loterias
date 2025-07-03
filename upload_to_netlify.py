
import requests

API_TOKEN = "nfp_EXkJbseAYhj4fMLCnbh15rkCzx1PCSzVfb0c"
SITE_ID = "67335cc6-8410-4a0d-8412-1d47f55817cd"

def subir_a_netlify():
    with open("resultados.html", "rb") as f:
        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys",
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            files={"file": ("resultados.html", f, "text/html")}
        )
    print("✅ Subido a Netlify:", response.status_code, response.json().get("deploy_ssl_url"))

if __name__ == "__main__":
    subir_a_netlify()
