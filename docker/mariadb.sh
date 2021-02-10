docker run \
  --name bikeeperdb \
  -e=MYSQL_USER=teambikeeper \
  -e=MYSQL_PASSWORD=bikeeper \
  -e=MARIADB_RANDOM_ROOT_PASSWORD=no \
  -e=MYSQL_ROOT_PASSWORD=bikeepersu \
  -p 3306:3306 \
  -d mariadb/server:10.3 \
  --log-bin \
  --binlog-format=MIXED \
