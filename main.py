
import pandas as pd
import os
from datetime import date
from process_data import *
from generate_files import generate_files
from db_connection import *
import logging


def main():

    logging.basicConfig(filename='file.log', filemode='w', level=logging.INFO)


    fecha_carga = date.today()
    logging.info(f'"{fecha_carga}"')

    
    logging.info("VALIDANDO CONEXION A BASE DE DATOS...")
    check_connection()


    ######## GET FILES ########
    logging.info("OBTENIENDO ARCHIVOS...")

    categorias = [
            'bibliotecas',
            'cines',
            'museos'
          ]

    for c in categorias:

        dirName = c
        subdirName = f'{fecha_carga.year}-{fecha_carga.month}'

        if not os.path.exists(dirName):
            os.mkdir(dirName)

        if not os.path.exists(f'{dirName}/{subdirName}/{dirName}-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}.csv'):
            if not os.path.exists(dirName + '/' + subdirName):
                os.mkdir(dirName + '/' + subdirName)
            generate_files(c, fecha_carga)
        else:
            logging.info(
                f'Se encontro el archivo: "{c}-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}"')
            continue

    ######## DATA PROCESSING ########
    logging.info("PROCESANDO LOS DATOS...")

    # load df
    bibliotecas_df = pd.read_csv(
        f'bibliotecas/{fecha_carga.year}-{fecha_carga.month}/bibliotecas-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}.csv')
    cines_df = pd.read_csv(
        f'cines/{fecha_carga.year}-{fecha_carga.month}/cines-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}.csv')
    museos_df = pd.read_csv(
        f'museos/{fecha_carga.year}-{fecha_carga.month}/museos-{fecha_carga.day}-{fecha_carga.month}-{fecha_carga.year}.csv')

    # normalize df columns names
    bibliotecas_df_n = normalize(bibliotecas_df)
    cines_df_n = normalize(cines_df)
    museos_df_n = normalize(museos_df)

    # process df
    helper_df = create_helper(bibliotecas_df_n, cines_df_n,
                            museos_df_n, fecha_carga)

    espacios_df = create_espacios(helper_df)
    rxcategoria_df = create_rxcategoria(helper_df)
    rxfuente_df = create_rxfuente(helper_df)
    rxprovincia_df = create_rxprovincia(helper_df)
    cines_df = create_cine(helper_df)

    ######## DB UPDATE ########
    logging.info("ACTUALIZANDO LOS DATOS...")

    con = connect_2db()

    espacios_df.to_sql('espacios', con, if_exists='replace', index=False)
    logging.info('Tabla "ESPACIOS" actualizada')

    rxcategoria_df.to_sql('rxcategoria', con, if_exists='replace', index=False)
    logging.info('Tabla "RXCATEGORIA" actualizada')

    rxfuente_df.to_sql('rxfuente', con, if_exists='replace', index=False)
    logging.info('Tabla "RXFUENTE" actualizada')

    rxprovincia_df.to_sql('rxprovincia', con, if_exists='replace', index=False)
    logging.info('Tabla "RXPROVINCIA" actualizada')

    cines_df.to_sql('cines', con, if_exists='replace', index=False)
    logging.info('Tabla "CINES" actualizada')

    con.close()

if __name__ == '__main__':
    main()
