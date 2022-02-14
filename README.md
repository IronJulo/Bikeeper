
# Bikeeper

  

## What is it? 💡
Bikeeper is a DUT 2 project. The goal of this project is to help bikers to find their motorbike and prevent motocycle stealing. In case off falling or stealing the arduino placed on the motorbike alert his owner. 


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


### Docker 🐳
Install docker and docker compose with `docker-setup.sh` script.
After run `docker-compose up` to start the project. 



## Documentation 📄 : 


To see our project documentation clone this repo and run  `docsify serve docs` or open [page](https://ironjulo.gitlab.io/project-bikeeper/#/)
We use [docsify](https://docsify.js.org/#/) to write this documentation. 
GitLab page : `https://ironjulo.gitlab.io/project-bikeeper/#/`

API is documented, in **docs** folder open `api-documentation.pdf`

## Screenshots 📸 


![alt text](https://i.imgur.com/ZtYGXJY.png)
![alt text](https://i.imgur.com/L43L8Ny.jpg)
![alt text](https://i.imgur.com/xSDQnF2.jpg)
![alt text](https://i.imgur.com/01kRkwk.jpg)
 
## 👷 Authors  :
| Name | Email|
|--|--|
| **Andrew Mary Huet de Barochez** | andrew.mary-huet-de-barochez@etu.univ-orleans.fr |
| **Jules Brossier** | jules.brss@gmail.com |
| **Xavier Lemaire**| xavier.lemaire@etu.univ-orleans.fr |
| **Kevin Talland**| kevin.talland@etu.univ-orleans.fr |
| **Dorian Hardy**| @thegostisdead |
| **Nicolas Pasquet**| nicolas.pasquet@etu.univ-orleans.fr |
| **Fabien Billauld**| fabien.billault@etu.univ-orleans.fr |
| **Mathieu Ramel**| mathieu.ramel@etu.univ-orleans.fr |
