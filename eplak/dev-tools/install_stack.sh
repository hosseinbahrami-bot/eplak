#!/bin/bash
set -x
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends php-cli php-mysql php-mbstring php-xml mariadb-server mariadb-client
php -v
which mysqld mariadbd
echo "INSTALL_DONE"
