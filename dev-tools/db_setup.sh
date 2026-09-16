#!/bin/bash
set -x
sudo mkdir -p /run/mysqld /var/log/mysql
sudo chown -R mysql:mysql /run/mysqld /var/log/mysql
if [ ! -d /var/lib/mysql/mysql ]; then
  sudo mariadb-install-db --user=mysql --datadir=/var/lib/mysql --auth-root-authentication-method=normal
fi
sudo chown -R mysql:mysql /var/lib/mysql
echo "DB_INIT_DONE"
