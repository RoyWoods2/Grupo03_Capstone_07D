# FighterChile


FighterChile es una plataforma web diseñada para la comunidad de jugadores de juegos de lucha. Permite gestionar eventos, noticias, rankings y la interacción entre los jugadores. El proyecto tiene como objetivo ofrecer una experiencia completa para los entusiastas de los juegos de pelea, especialmente para juegos como Dragon Ball FighterZ, Street Fighter, Tekken y otros.

# Funcionalidades
Gestión de Eventos: Crear y gestionar eventos para torneos de juegos de lucha, incluyendo información sobre fecha, lugar, participantes, y resultados.
Noticias: Publicar noticias relacionadas con la escena de juegos de pelea y torneos.
Ranking de Jugadores: Un sistema de ranking que clasifica a los jugadores según su rendimiento en eventos.
Perfil de Usuario: Los jugadores pueden tener un perfil personalizado con su avatar, puntuación y los juegos en los que compiten.
Glosario: Un glosario de términos utilizados en los juegos de lucha, ideal para los jugadores nuevos.
Integración con Frame Data: Acceso a datos técnicos de los movimientos de los personajes de juegos de lucha para mejorar las habilidades de los jugadores.

# Tecnologías Utilizadas
Django: Framework de desarrollo web en Python.
Bootstrap: Framework CSS para crear una interfaz de usuario atractiva y responsiva.
Chart.js: Biblioteca de JavaScript para mostrar gráficos dinámicos, utilizada para visualizar el ranking de personajes y otros datos.
PostgreSQL: Base de datos para almacenar la información del sistema.

# Requisitos
Python 3.8+
Django 3.2+
PostgreSQL o SQLite
Node.js y npm (para la generación de gráficos)

# Instalacion
Pasos para la Instalación
Clona el repositorio:

bash
Copiar código
git clone https://github.com/RoyWoods2/FighterChile.git
cd FighterChile
Crea un entorno virtual:
Copiar código
python -m venv env
source env/bin/activate  # En sistemas Unix
env\Scripts\activate     # En sistemas Windows

Instala las dependencias:
pip install -r requirements.txt


Configura la base de datos:
Asegúrate de tener PostgreSQL o SQLite configurado.
Si usas PostgreSQL, crea una base de datos y configura los detalles de conexión en settings.py.

Realiza las migraciones:
python manage.py migrate

Crea un superusuario para el panel de administración de Django:
python manage.py createsuperuser

Ejecuta el servidor de desarrollo:
python manage.py runserver

# Contribuir
Si deseas contribuir a este proyecto, por favor sigue estos pasos:

Haz un fork del repositorio.
Crea una rama nueva (git checkout -b feature/nueva-caracteristica).
Haz tus cambios y realiza un commit (git commit -am 'Añadir nueva característica').
Haz push a la rama (git push origin feature/nueva-caracteristica).
Abre un pull request.

# Contacto
Desarrollador: Hans Arancibia/ Joaquin Gallegos
Email: [hans.arancibia@live.com]
GitHub: https://github.com/RoyWoods2