from crypt import methods
import pandas as pd
import numpy as np
import logging


dict_columns = {'cod_loc': 'cod_localidad',
                'idprovincia': 'id_provincia',
                'iddepartamento': 'id_departamento',
                'direccion': 'domicilio',
                'cp': 'codigo_postal'}


def normalize_t(s):
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


def normalize_column_n(df):
    """Normaliza los nombres de las columnas,para ello se le sacan las tildes a las palabras, 
    se convierten en  minuscula y algunas se reescriben segun un diccionario
    """

    # normalize column names
    df.columns = [normalize_t(c).lower() for c in df.columns]
    df = df.rename(columns=dict_columns)

    return df


def create_helper(df1, df2, df3, dt):
    """Normaliza el nombre de las columnas, selecciona columnas de interes,
    concatenana las tablas en una sola, setea tipos de datos de las columnas, normaliza la columna provincias,
    pone como nulos valores faltantes"""

    # bibliotecas
    df1 = normalize_column_n(df1)
    df1 = df1[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
               'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fuente']]

    # cines
    df2 = normalize_column_n(df2)
    df2 = df2[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
               'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fuente', 'pantallas', 'butacas', 'espacio_incaa']]

    # museos
    df3 = normalize_column_n(df3)
    df3 = df3[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
               'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fuente']]

    df = pd.concat([df1, df2, df3], axis=0, join='outer', ignore_index=True)

    # se setea tipo de datos de las columnas
    df = df.astype({'cod_localidad': int, 'id_provincia': int, 'id_departamento': int, 'categoria': str, 'provincia': str,
                    'localidad': str, 'nombre': str, 'domicilio': str, 'codigo_postal': str, 'telefono': str, 'mail': str, 'web': str, "fuente": str})

    # se normaliza los nombres de las provincias
    df['provincia'] = df['provincia'].apply(lambda x: normalize_t(x.strip()))
    df['provincia'].replace(
        {'Tierra del Fuego, Antartida e Islas del Atlantico Sur': 'Tierra del Fuego'}, inplace=True)

    # se reemplaza valores sin datos por nulos en las columnas tipo string
    cols_str = df.select_dtypes(include='object').columns.to_list()
    df.loc[:, cols_str] = df.loc[:, cols_str].replace(
        {'s/d': None, 'nan': None})

    # se agrega la columna con fecha de carga
    df['fecha_carga'] = dt

    return df


def create_informacion(df):

    df = df[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
             'localidad', 'nombre', 'domicilio', 'codigo_postal', 'telefono', 'mail', 'web', 'fecha_carga']]

    logging.info('Tabla "INFORMACION" creada')
    return df


def create_registros(df):

    df1 = df.groupby(['provincia', 'categoria']).agg(
        total=('nombre', 'count'), fuente=('fuente', 'first')).reset_index()
    df1 = df1.astype({"total": int})

    df1 = df1[['provincia', 'categoria', 'fuente', 'total']]

    df2 = df.groupby('categoria').agg(
        categoria_total=('nombre', 'count')).reset_index()
    df2 = df2.astype({"categoria_total": int})

    df3 = df1.merge(df2, how='left', on='categoria')

    df4 = df.groupby('fuente').agg(
        fuente_total=('nombre', 'count'), fecha_carga=('fecha_carga', 'first')).reset_index()
    df4 = df4.astype({"fuente_total": int})

    df5 = df3.merge(df4, how='left', on='fuente')

    logging.info('Tabla "REGISTROS" creada')
    return df5


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
