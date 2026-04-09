# FujiMovie

Aplicación Spring Boot para consultar información de películas desde la API de OMDB.

## Descripción

Esta aplicación permite buscar películas por título utilizando la API gratuita de OMDB (Open Movie Database). Devuelve información detallada como título, año, género, director, duración, sinopsis y póster.

## Requisitos Previos

- **Java 17** o superior
- **Maven 3.6+**
- **Clave API de OMDB** (gratuita)

## Instalación

### 1. Instalar Java 17

Descarga e instala Java 17 desde [Adoptium](https://adoptium.net/):

1. Ve a https://adoptium.net/
2. Descarga la versión 17 para Windows
3. Instala y verifica con:
   ```bash
   java -version
   ```

### 2. Instalar Maven

1. Descarga Maven desde [Apache Maven](https://maven.apache.org/download.cgi)
2. Descomprime el archivo ZIP
3. Agrega la carpeta `bin` al PATH del sistema
4. Verifica con:
   ```bash
   mvn -version
   ```

### 3. Obtener Clave API de OMDB

1. Ve a http://www.omdbapi.com/apikey.aspx
2. Regístrate gratis
3. Obtén tu clave API
4. Edita el archivo `src/main/resources/application.properties`
5. Reemplaza `YOUR_API_KEY_HERE` con tu clave real:
   ```
   omdb.api.key=tu_clave_aqui
   ```

## Ejecución

1. Abre una terminal en la raíz del proyecto
2. Ejecuta:
   ```bash
   mvn spring-boot:run
   ```
3. El servidor se iniciará en http://localhost:8080

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

- **Spring Boot 3.2.4**
- **Java 17**
- **WebClient** para llamadas HTTP
- **OMDB API** para datos de películas

## Estructura del Proyecto

```
src/
├── main/
│   ├── java/com/fujimovie/catalog/
│   │   ├── FujiMovieApplication.java    # Clase principal
│   │   ├── controller/
│   │   │   └── MovieController.java     # Endpoints REST
│   │   ├── model/
│   │   │   └── Movie.java               # Modelo de datos
│   │   └── service/
│   │       └── MovieService.java        # Lógica de negocio
│   └── resources/
│       └── application.properties       # Configuración
```

## Notas

- La API de OMDB tiene límites de uso gratuitos
- Asegúrate de tener conexión a internet para las consultas
- Los títulos deben estar en inglés para mejores resultados

---

*Proyecto para Fujitsu Talent Academy*
