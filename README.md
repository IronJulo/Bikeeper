
# Bikeeper

  

## What is it? 💡
Bikeeper is a school project ".........."


## Run 🚀
According to our documentation your can start this project by multiples ways.
### Manually 
You can manually start the Flask website. But we use docker for our database (MariaDB), openstreepmap tiles server, ngnix reverse proxy, grafana. All of this services can be started by executing some small script. 
For exemple : in docker folder run  `sh mariadb.sh` to install mariadb. 
All docker scripts look likes to this : 

```shell
docker run \
  --name bikeeperdb \
  -e=MYSQL_USER=teambikeeper \
  -e=MYSQL_PASSWORD=bikeeper \
  -e=MARIADB_RANDOM_ROOT_PASSWORD=no \
  -e=MYSQL_ROOT_PASSWORD=bikeepersu \
  -p 3306:3306 \
  -d mariadb/server:10.3 \
  --log-bin \
  --binlog-format=MIXED 
```
|Name | Script |Comments|
|--|--|--|
| MariaDB | docker/mariadb.sh | Simple Mariadb server to store flask website data.  |
| Grafana | docker/grafana/grafana.sh | Need few additionals steps: run `grafana-pluging.sh` to install plugings|
|TileServerGL|docker/openstreetmap/osm-server.sh||
|Ngnix|docker/ngnix/ngnix.sh|Reverse proxy to allow flask and grafana to iframe a chart (CORS issues)|


### Docker 
Install docker and docker compose with `docker-setup.sh` script.
After run `docker-compose up` to start the project. 

  
  
## Development 🔨 :

## Screenshots 📸 

 
## 👷 Authors  :
| Name | Email|
|--|--|
| **Andrew Mary Huet de Barochez** | @etu.univ-orleans.fr |
| **Jules Brossier** | jules.brossier@etu.univ-orleans.fr |
| **Xavier Lemaire**| xavier.lemaire@etu.univ-orleans.fr |
| **Kevin Talland**| kevin.talland@etu.univ-orleans.fr |
| **Dorian Hardy**| dorian.hardy@etu.univ-orleans.fr|
| **Nicolas Pasquet**| @etu.univ-orleans.fr |
| **Fabien Billauld**| @etu.univ-orleans.fr |
| **Mathieu Ramel**| @etu.univ-orleans.fr |