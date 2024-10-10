import requests

# URL de base de votre API (modifiez selon vos besoins)
BASE_URL = "http://127.0.0.1:8000/api/"

# Identifiants de connexion
username = "directeur_petit_prince"
password = "qwerty123"
school_code = "d8b5b69d0df1f6d"

def get_auth_token():
    """Obtenir un jeton d'authentification JWT"""
    login_url = f"{BASE_URL}auth/login/"
    data = {
        "username": username,
        "password": password,
        "school_code": school_code
    }
    response = requests.post(login_url, data=data)
    if response.status_code == 200:
        print(response.json()["access"])
        return response.json()["access"]
    else:
        print("Erreur lors de la connexion :", response.json())
        return None

def get_headers(token):
    """Retourne les en-têtes avec le token JWT"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_get_request(view_url, token):
    """Tester une requête GET"""
    response = requests.get(view_url, headers=get_headers(token))
    print(f"GET {view_url} -> {response.status_code}")
    if response.status_code == 200:
        print("Data:", response.json())
    else:
        print("Erreur :", response.json())

if __name__ == "__main__":
    token = get_auth_token()
    if token:
        # Test des différentes vues
        print("\n--- SchoolYear ---")
        school_cycle_url = f"{BASE_URL}school-years/"
        test_get_request(school_cycle_url, token)
        
        print("\n--- SchoolSeries ---")
        school_series_url = f"{BASE_URL}school-series/"
        test_get_request(school_series_url, token)
        
        print("\n--- SchoolLevel ---")
        school_level_url = f"{BASE_URL}school-levels/"
        test_get_request(school_level_url, token)

