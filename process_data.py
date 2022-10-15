from crypt import methods
import pandas as pd
import numpy as np
import logging


dict_columns = {'cod_loc': 'cod_localidad',
                'idprovincia': 'id_provincia',
                'iddepartamento': 'id_departamento',
                'direccion': 'domicilio',
                'cp': 'codigo_postal'}


def normalize_l(s):
    """Quita las tildes de las palabras"""
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


def normalize(df):
    """Normaliza los nombres de las columnas,para ello se le sacan las tildes a las palabras, 
    se convierten en  minuscula y algunas se reescriben segun un diccionario
    """

    # normalize column names
    df.columns = [normalize_l(c).lower() for c in df.columns]
    df = df.rename(columns=dict_columns)

    return df


def create_helper(df1, df2, df3, dt):
    """Genera un df concatenando los 3 archivos originales que luego se usara en todas las funciones que generan las tablas"""

    df = pd.concat([df1, df2, df3], axis=0, join='outer', ignore_index=True)

    # seteo tipo de datos de las columnas
    df = df.astype({'cod_localidad': int, 'id_provincia': int, 'id_departamento': int, 'categoria': str, 'provincia': str,
                    'localidad': str, 'nombre': str, 'domicilio': str, 'codigo_postal': str, 'telefono': str, 'mail': str, 'web': str, "fuente": str})

    # se normalizan los nombres de las provincias
    df['provincia'] = df['provincia'].apply(lambda x: normalize_l(x.strip()))
    df['provincia'].replace(
        {'Tierra del Fuego, Antartida e Islas del Atlantico Sur': 'Tierra del Fuego'}, inplace=True)

    # se reemplaza 's/d', 'nan'  por valores nulos
    df['telefono'].replace({'s/d': None, 'nan': None}, inplace=True)
    df['mail'].replace({'s/d': None, 'nan': None}, inplace=True)
    df['web'].replace({'s/d': None, 'nan': None}, inplace=True)
    df['codigo_postal'].replace({'s/d': None, 'nan': None}, inplace=True)

    # se agrega la columna con fecha de carga
    df['fecha_carga'] = dt

    return df


def create_espacios(df):

    df = df[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
             'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fecha_carga']]

    logging.info('Tabla "ESPACIOS" creada')
    return df


def create_rxcategoria(df):

    df = df.groupby('categoria').agg(
        registros_totales=('nombre', 'count'), fecha_carga=('fecha_carga', 'first')).reset_index()
    df = df.astype({"registros_totales": int})

    logging.info('Tabla "RXCATEGORIA" creada')
    return df


def create_rxfuente(df):

    df = df.groupby('fuente').agg(
        registros_totales=('nombre', 'count'), fecha_carga=('fecha_carga', 'first')).reset_index()
    df = df.astype({"registros_totales": int})

    logging.info('Tabla "RXFUENTE" creada')
    return df


def create_rxprovincia(df):

    df = df.groupby(['provincia', 'categoria']).agg(
        registros_totales=('nombre', 'count'), fecha_carga=('fecha_carga', 'first')).reset_index()
    df = df.astype({"registros_totales": int})

    logging.info('Tabla "RXPROVINCIA" creada')
    return df


def create_cine(df):

    df = df.loc[df['categoria'] == 'Salas de cine', [
        'provincia', 'pantallas', 'butacas', 'espacio_incaa', 'fecha_carga']]

    df['espacio_incaa'].replace({'SI': 'si'}, inplace=True)
    df['espacio_incaa'] = np.where((df['espacio_incaa'].values == 'si'), 1, 0)
    df['espacio_incaa'] = df['espacio_incaa'].astype('bool')

    df = df.astype({"pantallas": int})
    df = df.astype({"butacas": int})

    logging.info('Tabla "CINES" creada')
    return df
