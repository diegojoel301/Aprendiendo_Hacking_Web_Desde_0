#!/bin/bash

admin_password=$(openssl rand -base64 35)

echo """
-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS user (
	id INTEGER NOT NULL, 
	username VARCHAR(150) NOT NULL, 
	password VARCHAR(150) NOT NULL, 
    is_admin BOOLEAN DEFAULT FALSE,
	PRIMARY KEY (id), 
	UNIQUE (username)
);

-- Crear tabla de posts del blog
CREATE TABLE IF NOT EXISTS blog_post (
	id INTEGER NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	content TEXT NOT NULL, 
	image VARCHAR(150), 
	summary VARCHAR(300), 
	author_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES user (id)
);

-- Crear tabla de comentarios
CREATE TABLE IF NOT EXISTS comment (
	id INTEGER NOT NULL, 
	content TEXT NOT NULL, 
	user_id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(post_id) REFERENCES blog_post (id)
);

-- Insertar datos de ejemplo en la tabla de usuarios
INSERT INTO user (username, password, is_admin) VALUES ('admin', '$admin_password', 1);

-- Insertar datos de ejemplo en la tabla de posts del blog
INSERT INTO blog_post (title, content, image, summary, author_id) VALUES
    ('Hacking Firewall', 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quam magni tempore ipsam mollitia inventore ducimus quas aspernatur perspiciatis nulla, iusto, hic illum nobis fugiat laudantium velit libero aliquam quidem aut.', 'image1.png', 'Phasellus orci sem, fringilla sit amet consequat a, scelerisque id tellus. Nunc et scelerisque enim. Nulla faucibus risus metus, at varius leo accumsan semper. In at lectus ut mauris mollis pulvinar iaculis sodales sapien. Maecenas elementum tempus tellus vitae vestibulum. Aliquam velit enim, congue nec condimentum mattis, porttitor vitae lectus. Vestibulum in felis ex. ', 1),
    ('Uso de la IA para Pentesting', 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quam magni tempore ipsam mollitia inventore ducimus quas aspernatur perspiciatis nulla, iusto, hic illum nobis fugiat laudantium velit libero aliquam quidem aut.', 'image2.png', 'Phasellus orci sem, fringilla sit amet consequat a, scelerisque id tellus. Nunc et scelerisque enim. Nulla faucibus risus metus, at varius leo accumsan semper. In at lectus ut mauris mollis pulvinar iaculis sodales sapien. Maecenas elementum tempus tellus vitae vestibulum. Aliquam velit enim, congue nec condimentum mattis, porttitor vitae lectus. Vestibulum in felis ex.', 1),
    ('Pentesting Web Automatizado', 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quam magni tempore ipsam mollitia inventore ducimus quas aspernatur perspiciatis nulla, iusto, hic illum nobis fugiat laudantium velit libero aliquam quidem aut..', 'image3.png', 'Phasellus orci sem, fringilla sit amet consequat a, scelerisque id tellus. Nunc et scelerisque enim. Nulla faucibus risus metus, at varius leo accumsan semper. In at lectus ut mauris mollis pulvinar iaculis sodales sapien. Maecenas elementum tempus tellus vitae vestibulum. Aliquam velit enim, congue nec condimentum mattis, porttitor vitae lectus. Vestibulum in felis ex.', 1),
    ('Mentiras de la Deep Web', 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quam magni tempore ipsam mollitia inventore ducimus quas aspernatur perspiciatis nulla, iusto, hic illum nobis fugiat laudantium velit libero aliquam quidem aut..', 'image4.png', 'Phasellus orci sem, fringilla sit amet consequat a, scelerisque id tellus. Nunc et scelerisque enim. Nulla faucibus risus metus, at varius leo accumsan semper. In at lectus ut mauris mollis pulvinar iaculis sodales sapien. Maecenas elementum tempus tellus vitae vestibulum. Aliquam velit enim, congue nec condimentum mattis, porttitor vitae lectus. Vestibulum in felis ex.', 1);

-- Insertar datos de ejemplo en la tabla de comentarios
INSERT INTO comment (content, user_id, post_id) VALUES
    ('Mauris viverra libero bibendum dui aliquet, in facilisis ligula convallis. Nunc sit amet rutrum quam. Nam eget gravida neque. Vestibulum fringilla arcu at mauris ullamcorper volutpat. Nam volutpat, metus vel tempus aliquet, dui nisl pulvinar ante, nec ornare enim sem a lectus. Phasellus in leo rutrum, imperdiet nisl a, imperdiet mi. Curabitur eget lacus lectus. Nulla quis odio eu lacus tempus placerat.', 1, 1),
    ('Mauris viverra libero bibendum dui aliquet, in facilisis ligula convallis. Nunc sit amet rutrum quam. Nam eget gravida neque. Vestibulum fringilla arcu at mauris ullamcorper volutpat. Nam volutpat, metus vel tempus aliquet, dui nisl pulvinar ante, nec ornare enim sem a lectus. Phasellus in leo rutrum, imperdiet nisl a, imperdiet mi. Curabitur eget lacus lectus. Nulla quis odio eu lacus tempus placerat.', 1, 2),
    ('Mauris viverra libero bibendum dui aliquet, in facilisis ligula convallis. Nunc sit amet rutrum quam. Nam eget gravida neque. Vestibulum fringilla arcu at mauris ullamcorper volutpat. Nam volutpat, metus vel tempus aliquet, dui nisl pulvinar ante, nec ornare enim sem a lectus. Phasellus in leo rutrum, imperdiet nisl a, imperdiet mi. Curabitur eget lacus lectus. Nulla quis odio eu lacus tempus placerat.', 1, 3),
    ('Mauris viverra libero bibendum dui aliquet, in facilisis ligula convallis. Nunc sit amet rutrum quam. Nam eget gravida neque. Vestibulum fringilla arcu at mauris ullamcorper volutpat. Nam volutpat, metus vel tempus aliquet, dui nisl pulvinar ante, nec ornare enim sem a lectus. Phasellus in leo rutrum, imperdiet nisl a, imperdiet mi. Curabitur eget lacus lectus. Nulla quis odio eu lacus tempus placerat.', 1, 4);
""" > /app/deepsec_blog/code.sql

cd /app/deepsec_blog/

rm db.sqlite 2>/dev/null

sqlite3 db.sqlite < code.sql

Xvfb :99 -ac &
export DISPLAY=:99

chmod 777 /app/bot -R
chmod +t /app/bot
chown -R seluser:seluser /app/bot

# Iniciar el servidor Flask del blog en segundo plano
cd /app/deepsec_blog
#export FLASK_APP=app.py
#flask run --host=0.0.0.0 --port=5000 &
python2.7 app.py &

# Iniciar el servidor Flask del bot en segundo plano
#export FLASK_APP=app.py
#flask run --host=0.0.0.0 --port=7000 &
sudo -u seluser ADMIN_PASSWORD=$admin_password python2.7 /app/bot/app.py &

# Mantener el contenedor en ejecución
wait -n

# Salir cuando uno de los servidores se detenga
exit $?
