#!/bin/sh

# Iniciar el backend Flask en el puerto 80
FLASK_APP=/app/backend/app.py flask run --host=127.0.0.1 --port=80 &

# Iniciar el panel de administración Flask en el puerto 7462
FLASK_APP=/app/admin/app.py flask run --host=127.0.0.1 --port=7462 &

# Iniciar el servidor Node.js
node server.js

