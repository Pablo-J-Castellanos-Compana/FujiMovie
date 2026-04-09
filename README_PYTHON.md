# 🎬 FujiMovie - Aplicación Python Flask

Aplicación web para consumir la API de películas de Devs API Hub.

## 🚀 Instalación Rápida

### 1. Instala dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecuta la app
```bash
python app_new.py
```

### 3. Abre en tu navegador
```
http://localhost:5000
```

---

## 📁 Estructura

```
FujiMovie/
├── app_new.py              ← Aplicación Flask
├── requirements.txt        ← Dependencias
├── src/
│   ├── model/
│   │   └── movie.py        ← Modelo Movie
│   ├── service/
│   │   └── movie_service.py ← Servicio API
│   ├── controller/
│   │   └── movie_controller.py ← Controlador
│   └── templates/
│       ├── base.html
│       ├── error.html
│       └── movies/
│           ├── list.html
│           └── details.html
```

---

## 🌐 URLs

- `http://localhost:5000/movies` - Listar películas
- `http://localhost:5000/movies/1` - Detalles película
- `http://localhost:5000/movies?search=Shawshank` - Buscar
- `http://localhost:5000/movies?genre=Drama` - Por género
- `http://localhost:5000/movies?year=1994` - Por año
- `http://localhost:5000/movies?stars=5` - Por calificación

---

## 🎯 API
- `GET /api/movies` - Todas las películas
- `GET /api/movies/<id>` - Película por ID
- `GET /api/movies/search?q=query` - Buscar

---

¡Disfruta! 🍿
