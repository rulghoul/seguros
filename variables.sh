#!/bin/bash

export SECRET_KEY="k$^m!=dp7ah&0_(9&0!b(47thue*@2x)u=883w3)1*pt8ae(i="
echo $SECRET_KEY
export SEGUROS_ALLOWED_HOSTS=http://localhost:1337,localhost,127.0.0.1
echo $SEGUROS_ALLOWED_HOSTS
export SEGUROS_SQL_ENGINE=django.db.backends.postgresql
echo $SEGUROS_SQL_ENGINE
export SEGUROS_SQL_DATABASE=seguros
echo $SEGUROS_SQL_DATABASE
export SEGUROS_SQL_USER=seguros
echo $SEGUROS_SQL_USER
export SEGUROS_SQL_PASSWORD=Kenqsduldc843
echo $SEGUROS_SQL_PASSWORD
export SEGUROS_SQL_HOST=db
echo $SEGUROS_SQL_HOST
export SEGUROS_SQL_PORT=5432
echo $SEGUROS_SQL_PORT
export SEGUROS_REDIS="redis://127.0.0.1:6379"
echo $SEGUROS_REDIS


# docker run --name postgresql-seguro --env=POSTGRES_USER=raulperez --env=POSTGRES_PASSWORD=425tsdfg3452345 --env=POSTGRES_DB=seguros --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/16/bin --env=GOSU_VERSION=1.17 --env=LANG=en_US.utf8  --volume=/var/lib/postgresql/data  -p 5432:5432 --restart=no --runtime=runc -d postgres