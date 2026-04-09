# FujiMovie

Aplicación Flask para consultar información de películas desde la API de OMDB.

## Descripción

Esta aplicación permite buscar películas por título utilizando la API gratuita de OMDB (Open Movie Database). Devuelve información detallada como título, año, género, director, duración, sinopsis y póster.

## Requisitos Previos

- **Python 3.8+**
- **Clave API de OMDB** (gratuita)

## Instalación

### 1. Instalar Python

Asegúrate de tener Python 3.8 o superior instalado. Descárgalo desde [python.org](https://www.python.org/downloads/).

Verifica la instalación:
```bash
python --version
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Obtener Clave API de OMDB

1. Ve a http://www.omdbapi.com/apikey.aspx
2. Regístrate gratis
3. Obtén tu clave API
4. Edita el archivo `.env`
5. Reemplaza `YOUR_API_KEY_HERE` con tu clave real:
   ```
   OMDB_API_KEY=tu_clave_aqui
   ```

## Ejecución

Ejecuta la aplicación:

```bash
python app.py
```

El servidor se iniciará en http://localhost:8080

## Uso

### Buscar una película

Haz una petición GET al endpoint:

```
GET http://localhost:8080/api/movies/search?title={titulo}
```

**Ejemplo con curl:**
```bash
curl "http://localhost:8080/api/movies/search?title=Inception"
```

**Ejemplo con Postman/Browser:**
```
http://localhost:8080/api/movies/search?title=Inception
```

### Respuesta de ejemplo

```json
{
  "title": "Inception",
  "year": "2010",
  "genre": "Action, Sci-Fi, Thriller",
  "director": "Christopher Nolan",
  "runtime": "148 min",
  "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
  "poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg"
}
```

## Tecnologías Utilizadas

- **Flask 3.0.0**
- **Python 3.8+**
- **Requests** para llamadas HTTP
- **OMDB API** para datos de películas

## Estructura del Proyecto

```
├── app.py                          # Aplicación principal Flask
├── requirements.txt                # Dependencias Python
├── .env                           # Variables de entorno
└── src/
    ├── controller/
    │   └── movie_controller.py    # Endpoints REST
    ├── model/
    │   └── movie.py               # Modelo de datos
    └── service/
        └── movie_service.py        # Lógica de negocio
```

## Notas

- La API de OMDB tiene límites de uso gratuitos
- Asegúrate de tener conexión a internet para las consultas
- Los títulos deben estar en inglés para mejores resultados

---

*Proyecto para Fujitsu Talent Academy*
