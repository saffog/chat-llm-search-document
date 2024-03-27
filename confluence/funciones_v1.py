import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup

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

def extraer_informacion(contenido, tipo_pagina):

    info = []
    paginas = {
        'Divisiones' : []
    }

    if tipo_pagina == '?expand=body.view':
        contenido_general = contenido['body']['view']['value']
        soup = BeautifulSoup(contenido_general, 'html.parser')
        texto = soup.get_text().replace('\n', ' ')
        info.extend([{'contenido': texto}])
        return info
    
    elif tipo_pagina == '/child/page':
        for contenido_general in contenido['results']:
            id = contenido_general['id']
            titulo = contenido_general['title']
            link = contenido_general['_links']['self']
            pagina = {
                'id' : id,
                'División' : titulo,
                'URL' : link
            }
            paginas['Divisiones'].append(pagina)
        info.extend([paginas])
        return info
    
    else:
        autor = contenido['version']['by']['displayName']
        titulo = contenido['title']
        info.extend([{
                'autor': autor,
                'titulo': titulo
            }])
        return info
    
def verificar_nivel(profundidad):
    if profundidad == 1:
        nivel = 'Clientes'
    elif profundidad >= 2:
        nivel = 'Proyectos'
    else:
        nivel = 'Industrias'
    return nivel

def verificar_nivel_anterior(profundidad):
    if profundidad == 0:
        nivel = 'Cliente'
    elif profundidad >= 1:
        nivel = 'Proyecto'
    else:
        nivel = 'Industria'
    return nivel

def guardar_archivo(contenido, nombre_archivo, indice):

    confluence = json.dumps(contenido, ensure_ascii=False, indent=4)
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(confluence)
    print(f"Todo el contenido se ha guardado en '{nombre_archivo}'")
    
    if indice == 'Industrias' or indice == 'Clientes' or indice == 'Proyectos':

        if "contenido" in contenido and contenido["contenido"]:
            if 'Proyecto' in contenido and contenido['Proyecto']: 
                proyecto = contenido['Proyecto']
                parte_contenido = contenido['contenido']
                texto_final = f'Las características del proyecto: {proyecto}, son: {parte_contenido}'
                archivo_modificado = nombre_archivo.replace("archivos/", "textos/")
            else: 
                texto_final = str(contenido)

        else:
            subindice = indice[:-1]
            indices = ', '.join([d[subindice] for d in contenido[0][indice]])
            
            if indice == 'Industrias':
                indice_principal = contenido[0]['División']
                texto_final = f'Comercial cuenta en su cartera con la division {indice_principal} y dicha division cuenta con los siguientes industrias: {indices}'
            elif indice == 'Clientes':
                indice_principal = contenido[0]['Industria']
                texto_final = f'Comercial cuenta en su cartera con la industria {indice_principal} y dicha industria cuenta con los siguientes clientes: {indices}'
            else:
                if 'Proyecto' in contenido[0]: 
                    indice_principal = contenido[0]['Proyecto']
                    texto_final = f'Comercial cuenta en su cartera con el proyecto {indice_principal} y para ese proyecto se cuenta con los siguientes subproyectos: {indices}'
                else:
                    indice_principal = contenido[0]['Cliente']
                    texto_final = f'Comercial cuenta en su cartera con el cliente {indice_principal} y para ese cliente se cuenta con los siguientes proyectos: {indices}'

        archivo_modificado = nombre_archivo.replace("archivos/", "textos/")

    else:
        parte_contenido = contenido[1]['contenido']
        divisiones = ', '.join([d['División'] for d in contenido[2]['Divisiones']])
        texto_final = f'contenido: {parte_contenido}\n Comercial cuenta en su cartera con las siguientes divisiones: {divisiones}'
        archivo_modificado = f'textos/{nombre_archivo}'

    with open(archivo_modificado, 'w', encoding='utf-8') as archivo:
            archivo.write(texto_final)
    print(f"Todo el contenido se ha guardado en '{archivo_modificado}'")

def extraer_informacion_hijos(contenido, titulo, secundario, nivel, nivel_anterior):

    info = []

    paginas = {
        secundario : titulo,
        nivel : []
    }
    
    for contenido_general in contenido['results']:
        id = contenido_general['id']
        titulo = contenido_general['title']
        link = contenido_general['_links']['self']
        pagina = {
            'id' : id,
            nivel_anterior : titulo,
            'URL' : link
        }
        paginas[nivel].append(pagina)
    info.extend([paginas])
    return info

def extraer_contenido(contenido, objeto, nivel):

    contenido_general = contenido['body']['view']['value']
    soup = BeautifulSoup(contenido_general, 'html.parser')
    texto = soup.get_text()
    
    objeto.pop(nivel)
    objeto["contenido"] = texto
    
    return objeto