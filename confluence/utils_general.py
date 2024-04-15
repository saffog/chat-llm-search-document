import requests
from requests.auth import HTTPBasicAuth

def solicitud_get(url, usuario, token):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(usuario, token))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f'Error HTTP: {err} en {url}')
    except requests.exceptions.RequestException as e:
        print(f'Error de red: {e} en {url}')
    return None