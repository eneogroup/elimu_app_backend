import requests

# URL de base de votre API (modifiez selon vos besoins)
BASE_URL = "http://localhost:8000/api/"

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


token = get_auth_token()
HEADERS = get_headers(token)

def create_tag(name):
    url = f"{BASE_URL}tags/"
    data = {
        "name": name,
        'slug':''
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Créer un Tag: {response.status_code}, {response.json()}")
    return response.json()

def get_tags():
    url = f"{BASE_URL}tags/"
    response = requests.get(url, headers=HEADERS)
    print(f"Liste des Tags: {response.status_code}, {response.json()}")
    return response.json()

def update_tag(tag_id, new_name):
    url = f"{BASE_URL}tags/{tag_id}/"
    data = {
        "name": new_name
    }
    response = requests.put(url, json=data, headers=HEADERS)
    print(f"Mise à jour du Tag {tag_id}: {response.status_code}, {response.json()}")

def delete_tag(tag_id):
    url = f"{BASE_URL}tags/{tag_id}/"
    response = requests.delete(url, headers=HEADERS)
    print(f"Suppression du Tag {tag_id}: {response.status_code}")

def create_information(name, content,):
    url = f"{BASE_URL}informations/"
    data = {
        "name": name,
        "content": content,
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Créer une Information: {response.status_code}, {response.json()}")
    return response.json()

def get_informations():
    url = f"{BASE_URL}informations/"
    response = requests.get(url, headers=HEADERS)
    print(f"Liste des Informations: {response.status_code}, {response.json()}")
    return response.json()

def create_event(name, description):
    url = f"{BASE_URL}evenements/"
    data = {
        "name": name,
        "description": description,
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Créer un Événement: {response.status_code}, {response.json()}")
    return response.json()

def create_announcement(title, content):
    url = f"{BASE_URL}announcements/"
    data = {
        "title": title,
        "content": content,
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Créer une Annonce: {response.status_code}, {response.json()}")
    return response.json()

def send_message(content, recipient_id):
    url = f"{BASE_URL}messages/"
    data = {
        "content": content,
        "recipient": recipient_id
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Envoyer un message: {response.status_code}, {response.json()}")
    return response.json()

def mark_message_as_read(message_id):
    url = f"{BASE_URL}messages/{message_id}/mark_as_read/"
    response = requests.post(url, headers=HEADERS)
    print(f"Marquer le message {message_id} comme lu: {response.status_code}, {response.json()}")

def mark_message_as_unread(message_id):
    url = f"{BASE_URL}messages/{message_id}/mark_as_unread/"
    response = requests.post(url, headers=HEADERS)
    print(f"Marquer le message {message_id} comme non lu: {response.status_code}, {response.json()}")


# EXEMPLES D'UTILISATION

# Créer des Tags
# tag1 = create_tag("Python")
# tag2 = create_tag("Django")
# tag3 = create_tag("Flutter")
# tag4 = create_tag("REST API")

# Obtenir la liste des Tags
tags = get_tags()

# # Mettre à jour un Tag
# update_tag(tags[0]['id'], "Advanced Python")

# # Supprimer un Tag
# delete_tag(tags[1]['id'])

# Créer une Information
information = create_information("Nouvelle Information", "Ceci est le contenu")

# Créer un Événement
event = create_event("Événement Annuel", "Description de l'événement")

# Créer une Annonce
announcement = create_announcement("Annonce Importante", "Détails de l'annonce",)

# Envoyer un Message
message = send_message("Bonjour, ceci est un test de message", 2)  # Remplacez '2' par l'ID du destinataire

# Marquer un message comme lu
mark_message_as_read(message['id'])

# Marquer un message comme non lu
mark_message_as_unread(message['id'])