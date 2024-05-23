# Sistema para gestión guardería de kayaks

Sistema de gestión para guardería de kayaks con estructura MVC.
Además comenzó como proyecto para la materia Programación II del 3er año del terciario Instituto Zona Oeste.

## Requisitos

- Python 3.12
- Poetry 1.8.3

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/JulianDeco/GuarderiaKayaks.git
    ```

2. Accede al directorio del proyecto:

    ```bash
    cd GuarderiaKayaks
    ```
    
3. Accede al directorio del proyecto:

    ```bash
    python -m venv venv
    ```
    
4. Accede al directorio del proyecto:

    ```bash
    .venv\Scripts\activate
    ```

5. Instala las dependencias utilizando Poetry:

    ```bash
    pip install setuptools poetry
    poetry install
    ```

6. Crear archivo .env y definir la siguientes variables de entorno:
    ```bash
    DB_HOST
    DB_USER
    DB_PASS
    DB_PORT
    DB_NAME
    ```

5. Inicia el servidor uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
