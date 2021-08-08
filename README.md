# web_school
Proyecto Open Source que consisten en un sistema de control de matricula y registro de notas.

# Config of enviroments
````
DATABASE_URL="db_engine//user:password@network/db_name"
SECRET_KEY="random strin"
CACHE_URL="memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213"
DEBUG=True
````

# to run the service with gunicorn
````
gunicorn --bind 0.0.0.0:8000 web_school.wsgi 
````

# For docker

# Build the python image with npm (command)
````
docker build -t tag-name .
````

