# API Backend Python – Gestión de Usuarios y Productos

## Descripción General

Este proyecto implementa una **API RESTful en Python (Django REST Framework)** para la administración de **usuarios y productos**, con **autenticación JWT**, persistencia en base de datos y despliegue mediante **Docker Compose**.  

---

## Arquitectura del Proyecto

```
api-python-omar-cetzal/
├── backend/                # Código fuente del API
│   ├── api/                # Vistas, serializadores, modelos
│   ├── core/               # Configuración general y rutas
│   ├── requirements.txt    # Dependencias del proyecto
│   ├── Dockerfile          # Imagen del backend
│   ├── entrypoint.sh       # Script de arranque
│   └── .env                # Variables de entorno
├── frontend/               # Carpeta reservada (demo opcional)
│   └── README.md
├── docker-compose.yml      # Orquestación de servicios
├── .env.example            # Plantilla de entorno
└── README.md               # Este archivo
```

---

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.11+
- **Framework:** Django + Django REST Framework  
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Base de datos:** PostgreSQL (via Docker)
- **Contenedores:** Docker & Docker Compose
- **Documentación API:** drf-spectacular (Swagger / OpenAPI)

---

## Instalación y Ejecución

### 1 Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/api-python-omar-cetzal.git
cd api-python-omar-cetzal
```

### 2 Configurar variables de entorno
Crear un archivo `.env` en la carpeta `backend/` usando `.env.example` como referencia.

Ejemplo:
```
DEBUG=True
SECRET_KEY=tu_clave_secreta
DB_NAME=backend_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### 3 Construir y levantar los contenedores
```bash
docker-compose up --build
```

---

## Comandos Útiles

| Acción | Comando |
|--------|----------|
| Aplicar migraciones | `docker-compose exec backend python manage.py migrate` |
| Crear superusuario | `docker-compose exec backend python manage.py createsuperuser` |
| Acceder al contenedor | `docker-compose exec backend bash` |
| Revisar logs | `docker-compose logs -f backend` |

---


## Autor

**Omar Cetzal**  
Desarrollador Fullstack

