# API Backend Python – Gestión de Usuarios y Productos

## Descripción General

Este proyecto implementa una **API RESTful en Python (Django REST Framework)** para la administración de **usuarios y productos**, con **autenticación JWT**, persistencia en base de datos y despliegue mediante **Docker Compose**.  


# Elección del Framework: Django + Django REST Framework (DRF)

Se eligió **Django** junto con **DRF** por:

- **Productividad y ecosistema maduro:** DRF facilita la creación de APIs CRUD con ViewSets y Serializers; Django aporta un ORM robusto y sistema de migraciones.
- **Seguridad integrada:** Protecciones nativas contra XSS, CSRF y SQL Injection; autenticación mediante JWT para proteger endpoints.
- **POO y separación de responsabilidades:** Django y DRF permiten una arquitectura orientada a objetos con clases y capas bien definidas.

---

# Arquitectura del Proyecto

Se adoptó una **arquitectura por capas** dentro de un **monorepo**, gestionado con **Docker**, garantizando mantenibilidad, escalabilidad y legibilidad.

## Principios clave

- **Modularidad:** La lógica de negocio se divide en aplicaciones independientes, cada una con alta cohesión y bajo acoplamiento. Esto facilita el mantenimiento y la expansión del proyecto.
- **Escalabilidad:** Añadir nuevas funcionalidades no afecta el código existente; se integran como nuevos módulos independientes.
- **Arquitectura por capas dentro de cada módulo:** Se separan responsabilidades en capas, repositorio, servicios, serialización y presentación.
  - **Repositorio:** Abstrae el acceso a la base de datos.
  - **Servicios:** Contienen la lógica de negocio principal.
  - **Serializadores:** Definen el formato de entrada/salida de la API(DTO).
  - **Presentación (views):** Manejan las peticiones HTTP.
- **Legibilidad y mantenibilidad:** La estructura clara facilita depuración, modificaciones y optimización de consultas.

---

# Contenerización con Docker

- Docker y Docker Compose garantizan un **entorno consistente y reproducible**, alineado con buenas prácticas de DevOps.
- Facilita el despliegue y desarrollo local sin conflictos, asegurando que migraciones, usuarios demo y servicios se ejecuten de forma automatizada al iniciar el contenedor.

---

# Resumen

La arquitectura implementada combina **modularidad, capas desacopladas, seguridad y contenerización**, resultando en un proyecto **robusto, escalable, legible y fácil de mantener**.

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

## 2 Configuración del entorno

Antes de levantar los contenedores con Docker Compose, debes crear y configurar el archivo `.env` que contiene las variables de entorno necesarias para el docker-compose.

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Ejemplo:
```
DJANGO_DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=api_db
POSTGRES_USER=user_root
POSTGRES_PASSWORD=12345
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

### 2 Configurar variables de entorno (opcional antes de ejecutar los contenedores)
Crear un archivo `.env` en la carpeta `backend/` usando `.env.example` como referencia. en caso de no realizarlo el contenedor usara en env.example

Ejemplo:
```
DJANGO_DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=api_db
POSTGRES_USER=user_root
POSTGRES_PASSWORD=12345
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

### 3 Construir y levantar los contenedores
Al crear los contenedor en automatico ejecutara los migretes nesario y creara el primer usario
```bash
docker-compose up --build
```

## URL swager
Usar swagger para pruenas listados
http://127.0.0.1:8000/swagger/

---

## TEST

email:demo@demo.com
pass:12345

---

## Comandos Útiles

| Acción | Comando |
|--------|----------|
| Aplicar migraciones | `docker-compose exec backend python manage.py migrate` |
| Crear superusuario | `docker-compose exec backend python manage.py createsuperuser` |
| Acceder al contenedor | `docker-compose exec backend bash` |
| Revisar logs | `docker-compose logs -f backend` |


--


## Autor

**Omar Cetzal**  
Desarrollador Fullstack

