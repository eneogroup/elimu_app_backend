import requests

BASE_URL = 'http://localhost:8000/api'  # Changez l'URL en fonction de votre configuration

def login(school_code, username, password):
    url = f'{BASE_URL}/login/'
    payload = {
        'school_code': school_code,
        'username': username,
        'password': password,
    }
    response = requests.post(url, json=payload)
    return response.json()

def logout(access_token):
    url = f'{BASE_URL}/logout/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        'token': access_token,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    # Remplacez par vos informations
    school_code = '46aad1ff19564a0'
    username = 'directeur_alcare'
    password = 'test'

    # Connexion
    print("Tentative de connexion...")
    login_response = login(school_code, username, password)
    print("Réponse de la connexion:", login_response)

    if 'access' in login_response:
        access_token = login_response['access']
        print("Token d'accès:", access_token)

        # Déconnexion
        print("Tentative de déconnexion...")
        logout_response = logout(access_token)
        print("Réponse de la déconnexion:", logout_response)
