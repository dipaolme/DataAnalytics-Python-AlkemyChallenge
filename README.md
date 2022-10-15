# DataAnalytics-Python-AlkemyChallenge
Alkemy challenge - Aceleracion octubre 2022

## Objetivo

Crear un proyecto que consuma datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural
sobre bibliotecas, museos y salas de cines argentinos.

### Deploy

1) Una vez descargado o clonado el ropositorio localmente, crear un ambiente virtual con venv (puede ser dentro o fuera, se recomienda adentro por una cuestion de orden)

    `python3 -m venv <myenv>`
  
   Luego activarlo
  
    `source <myenv>/bin/activate`
    
  
 2) Instalar todos los modulos necesario, para ello se utilizar la herramienta pip
  
    `pip3 install <modulo>`
  
    Se proporciona el archivo *requirements.txt* donde se listan todos los modulos utilizados, se pueden instalar todos de una vez 
  
    `pip3 install -r requirements.txt`
    
  
 3) Se necesita crear una base de datos PostgreSQL, una vez hecho recordar y tener a mano los siguientes parametros para completar el archivo de configuracion *.env*
  
      `host, user, password, name, port`
      
  
 4) Completar el archivo de configuracion *.env* con los parametros de la base de datos del punto 3 y las **URL** de descarga de los datos. Se dejan los valores utilizados por default, excepto el nombre de la base de datos que se deberara proporcionar. **IMPORTANTE: chequear que las URL funcionen**
  
  
 5) Crear las tablas de la base de datos
  
    `python3 create_tables.py`
  
  
### Ejecucion
  
   `python3 main.py`
   
   En el archivo *file.log* podran encontrar los diferentes pasos de ejecucucion.
  
