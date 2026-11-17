import requests
import requests.exceptions

BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
TIMEOUT = 3

# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
    server."""
    response = requests.get(BASE + "/get", params=params, timeout=TIMEOUT)
    return response.json()["args"]
    pass
def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu
    parametri."""
    response = requests.get(BASE + "/get", params=params, timeout=TIMEOUT)
    return response.url
    pass
# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
    server."""
    response = requests.get(BASE + agent, timeout=TIMEOUT)
    return response.headers["User-Agent"]
    pass
def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    return requests.utils.default_headers()["User-Agent"]
    pass
# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
    server."""
    response = requests.post(BASE + "/post", json=data, timeout=TIMEOUT)
    return response.json()
    pass
def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de
    server."""
    response = requests.post(BASE + "/post", json=data, timeout=TIMEOUT)
    return response.json()
    pass
# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau
    'eroare server'."""
    response = requests.get(BASE + "/status/" + code, timeout=TIMEOUT)
    if 400 <= response.status_code < 500:
        return "eroare client"
    elif response.status_code >= 500:
        return "eroare server"
    else:
        return "succes"
    pass
def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
    False."""
    response = requests.get(BASE + "/status/" + code, timeout=TIMEOUT)
    if response:
        return True
    else:
        return False
    pass
# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost
    urmate."""
    response = requests.get(BASE + "/redirect/" + str(n), timeout=TIMEOUT)
    return len(response.history)
    pass
def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    response = requests.get(BASE + "/redirect/" + str(n), timeout=TIMEOUT)
    return response.url
    pass
def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
    Location."""
    response = requests.get(BASE + "/redirect/" + str(n), timeout=TIMEOUT)
    return response.json("Location")
    pass
# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ
    sesiune."""
    response = requests.Session()
    response.get(f"https://httpbin.org/cookies/{name}/{value}")
    response.get(f"https://httpbin.org/cookies")
    return response.json()
    pass
def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie-
    urile văzute de server."""
    requests.get(f"https://httpbin.org/cookies/{name}/{value}")
    r = requests.get(f"https://httpbin.org/cookies")
    return r.json()["cookies"]
    pass
# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    url = BASE + path
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return {
            "status": response.status_code,
            "final_url": response.url,
            "redirects": len(response.history),
            "seconds": round(response.elapsed.total_seconds(), 2),
            "content_type": response.headers.get("Content-Type"),
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
def main():
    for path in PATHS:
        print(path, report(path))
# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel
    False."""
    response = requests.get(BASE + "/login", timeout=TIMEOUT)
    if response.status_code == 200:
        return True
    else:
        return False
if __name__ == "__main__":
    main()