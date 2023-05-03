#!/usr/bin/env bash
# Prepares a server for deployment

sudo apt update -y
sudo apt install nginx -y
sudo [ -d /data/web_static/shared/ ] || sudo mkdir /data/web_static/shared/ -p
sudo [ -d /data/web_static/releases/test/ ] || sudo mkdir /data/web_static/releases/test/ -p
sudo touch /data/web_static/releases/test/index.html
echo "Hello Mike Rock, I'm Obidient and working" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
replacement="server_name _;\n\n\tlocation \/hbnb_static\/ {\n\t\t alias \/data\/web_static\/current\/;\n\t\tautoindex on;\n\t\tadd_header X-Served-By \$hostname;\n\t}"
sudo sed -i "s/server_name _;/$replacement/" /etc/nginx/sites-enabled/default
sudo service nginx restart
