import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, HTTPError
from decouple import config
import logging


def modif_url(url):
    """Función que modifica los url de manera de poder bajar el archivo en formato csv"""
    url = '/'.join(url.split('/')[:-1] + ['export?format=csv'])

    return url


def generate_files(c, fecha_carga):

    if c == 'bibliotecas':
        url = config('URL_BIBLIOTECAS')
    elif c == 'cines':
        url = config('URL_CINES')
    else:
        url = config('URL_MUSEOS')

    url = modif_url(url)

    try:
        r = requests.get(url)
        r.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, TooManyRedirects) as e:
        logging.error(e)

    with open(f'{c}/{fecha_carga.year}-{fecha_carga.month}/{c}-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}.csv', 'wb') as f:
        f.write(r.content)
    
    logging.info(
        f'Se creo el archivo: "{c}-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}"')
