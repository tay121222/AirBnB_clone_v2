#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
echo "<!DOCTYPE html>
<html>
<head></head>
<body>Holberton School</body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
nginx_config="server {
    listen 80;
    server_name xtechitsupport.tech;

    location /hbnb_static/ {
        alias /data/web_static/current/;
	index index.nginx-debian.html;
    }

    location / {
        add_header X-Served-By \$hostname;
    }
}"

echo "$nginx_config" | sudo tee /etc/nginx/sites-available/web_static > /dev/null
sudo ln -sf /etc/nginx/sites-available/web_static /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo service nginx restart
