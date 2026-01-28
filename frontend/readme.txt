TrueTrip Colombia — Plataforma de Recomendación Turística

Este proyecto corresponde a un prototipo funcional de una plataforma de recomendación turística para Colombia, desarrollada como parte de un trabajo de grado. El sistema integra análisis de reseñas turísticas, generación automática de itinerarios mediante inteligencia artificial y visualización interactiva de resultados.

El sistema está compuesto por un backend basado en API REST, una interfaz web interactiva y una base de datos relacional que almacena información turística estructurada.

Componentes principales del sistema:

Backend desarrollado en FastAPI.

Frontend desarrollado en Streamlit.

Base de datos PostgreSQL.

Módulo de envío de itinerarios por correo electrónico.

Modelos de lenguaje para resumen de reseñas.

Requisitos previos

Antes de ejecutar el proyecto es necesario contar con los siguientes elementos:

Python versión 3.9 o superior.

PostgreSQL en ejecución.

Gestor de paquetes pip.

Conexión a internet para descarga de dependencias.

Creación del entorno virtual (recomendado)

Desde la carpeta raíz del proyecto se recomienda crear un entorno virtual para aislar las dependencias:

python -m venv venv

Activación del entorno virtual:

En Windows:
venv\Scripts\activate

En Linux o macOS:
source venv/bin/activate

Instalación de dependencias

Todas las librerías necesarias para ejecutar el proyecto se encuentran listadas en el archivo requirements.txt.
Para instalarlas, ejecutar el siguiente comando desde la raíz del proyecto:

pip install -r requirements.txt

Este comando instalará automáticamente las dependencias necesarias para el backend, el frontend y los módulos de inteligencia artificial.

Configuración de la base de datos

El sistema utiliza una base de datos PostgreSQL que contiene información sobre ciudades, atracciones, hoteles, reseñas y estadísticas turísticas.

La cadena de conexión a la base de datos se define en los archivos db_utils_1.py y db_query.py.
Debe ajustarse según las credenciales locales, incluyendo usuario, contraseña, puerto y nombre de la base de datos.

Ejemplo de estructura de conexión:
postgresql+pg8000://usuario:password@localhost:5432/nombre_base_datos

Configuración del envío de correos electrónicos

Para habilitar el envío de itinerarios por correo electrónico, es necesario crear un archivo llamado correo.env en la raíz del proyecto.

Este archivo debe contener las variables de entorno necesarias para el servidor SMTP:

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=correo_emisor@gmail.com

SMTP_PASS=contraseña_o_contraseña_de_aplicación

Se recomienda el uso de contraseñas de aplicación en caso de utilizar servicios como Gmail.

Ejecución del backend (API REST)

Una vez instaladas las dependencias y configurada la base de datos, el backend puede ejecutarse con el siguiente comando:

uvicorn api:app --reload

La API quedará disponible en la siguiente dirección:
http://127.0.0.1:8000

La documentación automática de la API puede consultarse en:
http://127.0.0.1:8000/docs

Ejecución del frontend (interfaz Streamlit)

En una nueva terminal, con el entorno virtual activo, ejecutar el siguiente comando:

streamlit run app.py

La interfaz web se abrirá automáticamente en el navegador, normalmente en la dirección:
http://localhost:8501

Flujo de uso del sistema

El usuario puede interactuar con el sistema siguiendo estos pasos:

Seleccionar región, ciudad, tipo de turismo y duración del viaje.

Generar el itinerario turístico personalizado.

Visualizar reseñas resumidas, itinerarios por día, mapas y estadísticas territoriales.

Enviar el itinerario generado al correo electrónico, si así lo desea.

Manejo de errores del sistema

El backend utiliza los mecanismos estándar de manejo de errores de una API REST.
Esto permite:

Retornar códigos de estado HTTP (400, 404, 500).

Identificar errores de conexión a la base de datos.

Detectar fallos durante la generación de texto o el envío de correos.

Registrar mensajes de error directamente en la consola del servidor.

Este enfoque elimina la necesidad de definir manualmente listas cerradas de errores y facilita la trazabilidad de fallos durante la ejecución del sistema.

Reproducibilidad del proyecto

Para ejecutar el proyecto en otro equipo se deben seguir los mismos pasos:

Clonar el repositorio.

Crear y activar un entorno virtual.

Ejecutar pip install -r requirements.txt.

Configurar base de datos y archivo correo.env.

Ejecutar backend y frontend.

Notas finales

El prototipo fue validado en un entorno controlado de laboratorio.
La arquitectura modular permite reemplazar o ampliar componentes sin modificar el flujo general del sistema.
El diseño está orientado a facilitar futuras integraciones con datos reales y entornos productivos.