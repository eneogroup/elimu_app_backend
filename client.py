import requests

BASE_URL = 'http://localhost:8000/api'  # Changez l'URL en fonction de votre configuration

# Fonction pour se connecter et obtenir un token d'accès
def login(school_code, username, password):
    url = f'{BASE_URL}/login/'
    payload = {
        'school_code': school_code,
        'username': username,
        'password': password,
    }
    response = requests.post(url, json=payload)
    return response.json()

# Fonction pour obtenir une liste des années scolaires
def get_school_years(access_token):
    url = f'{BASE_URL}/school-years/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Fonction pour créer une nouvelle année scolaire
def create_school_year(access_token, school_id, year, start_date, end_date):
    url = f'{BASE_URL}/school-years/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        'school': school_id,
        'year': year,
        'start_date': start_date,
        'end_date': end_date,
        'is_current_year': True,  # Exemple pour indiquer que c'est l'année en cours
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Fonction pour obtenir une salle de classe
def get_classrooms(access_token):
    url = f'{BASE_URL}/classrooms/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Fonction pour créer une nouvelle salle de classe
def create_classroom(access_token, school_id, name, school_level_id):
    url = f'{BASE_URL}/classrooms/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    payload = {
        'school': school_id,
        'name': name,
        'school_level': school_level_id,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    # Remplacez par vos informations de connexion
    school_code = '46aad1ff19564a0'
    username = 'directeur_alcare'
    password = 'test'

    # Connexion
    print("Tentative de connexion...")
    login_response = login(school_code, username, password)
    print("Réponse de la connexion:", login_response)

    if 'access' in login_response:
        access_token = login_response['access']
        print("\n\nToken d'accès:", access_token)

        # Obtenir les années scolaires
        print("\n\nRécupération des années scolaires...")
        school_years = get_school_years(access_token)
        print("Années scolaires:", school_years)

        # Créer une nouvelle année scolaire
        print("\nCréation d'une nouvelle année scolaire...")
        new_school_year = create_school_year(access_token, school_id=2, year='2024-2025', start_date='2024-09-01', end_date='2025-06-30')
        print("Nouvelle année scolaire créée:", new_school_year)

        # Obtenir les salles de classe
        print("\n\nRécupération des salles de classe...")
        classrooms = get_classrooms(access_token)
        print("Salles de classe:", classrooms)

        #Créer une nouvelle salle de classe
        # print("Création d'une nouvelle salle de classe...")
        # new_classroom = create_classroom(access_token, school_id=2, name='CP1 A', school_level_id=1)
        # print("Nouvelle salle de classe créée:", new_classroom)
    else:
        print("Échec de la connexion:", login_response)
