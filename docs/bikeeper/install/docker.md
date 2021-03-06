# Docker 

## How to start ?    

To run all services clone the repo and run `docker-compose up` .     
To stop the services type `docker-compose down` or press `ctrl+c` if your terminal is atteched to docker-compose.

## How it works ?  

Docker-compose will automatically deploy the bikeeper platform.     
It start : 
- mariadb
- grafana 
- ngnix
- flask
- openstreetmap


!> **Important** Please, replace the osm token by a new one. The token is available for one hour.  [Token](https://data.maptiler.com/downloads/tileset/osm/europe/france/centre/?wizard).   

```yaml
version: '3'
services:
  db:
    image: mariadb/server:10.3
    container_name: bikeeperbd
    expose:
      - 3306
    ports:
    - 3306:3306
    command:
      --log-bin
      --binlog-format=MIXED
    environment:
      - MYSQL_USER=teambikeeper
      - MYSQL_PASSWORD=bikeeper
      - MARIADB_RANDOM_ROOT_PASSWORD=no
      - MYSQL_ROOT_PASSWORD=bikeepersu
      - MYSQL_DATABASE=BIKEEPER
    healthcheck:
      test: "/usr/bin/mysql --user=teambikeeper --password=bikeeper --execute \"SHOW DATABASES;\""
      interval: 2s
      timeout: 20s
      retries: 10

  bikeeper-website:
    container_name: bikeeper
    depends_on:
      db:
        condition: service_healthy
    build: ./flask/
    volumes:
      - ./flask/:/usr/src/app/
    ports:
      - 8080:8080
    environment:
      PORT: 8080
      HOST: 0.0.0.0
      FLASK_DEBUG: 1

  osm:
    image: osm-bundle
    container_name: osm
    build:
      context: .
      dockerfile: ./docker/openstreetmap/osm.Dockerfile
      args:
        - MAP_TOKEN=WyJiZmZkZmM5NS1lMTVlLTRmYjgtYWFkZC1lNzM5MGQ1NjAxOTciLCItMSIsODcwMl0.YD6sPw.MEJHhB0BwjOEbCH95mX5o305m3s # get a new on here https://data.maptiler.com/downloads/tileset/osm/europe/france/centre/?wizard
    depends_on:
      db:
        condition: service_healthy
#    volumes:
#      - ./docker/openstreetmap/:/data
    ports:
      - 8989:80
    command:
      --bind 0.0.0.0
      --mbtiles /bundle/centre.mbtiles

  reverse-proxy:
    image: nginx
    container_name: nginxreverse
    depends_on:
      - grafana
      - bikeeper-website
    volumes:
      - ./docker/ngnix/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - 80:80

  grafana:
    image: grafana/grafana
    container_name: grafana
    depends_on:
      - db
    environment:
      - "GF_INSTALL_PLUGINS=grafana-worldmap-panel"
      - "GF_INSTALL_IMAGE_RENDERER_PLUGIN=true"
      - "GF_DATABASE_TYPE=mysql"
      - "GF_DATABASE_NAME=BIKEEPER"
      - "GF_DATABASE_USER=teambikeeper"
      - "GF_DATABASE_HOST=db"
      - "GF_DATABASE_PASSWORD=bikeeper"
      - "GF_ANALYTICS_REPORTING_ENABLED=false"
      - "GF_SECURITY_ADMIN_USER=admin"
      - "GF_SECURITY_ADMIN_PASSWORD:=admin"
    volumes:
      - ./docker/grafana/grafana.ini:/etc/grafana/grafana.ini
      - ./docker/grafana/grafana-storage:/var/lib/grafana
    ports:
      - 3000:3000

```