# Installation 

?> **Tip** There is 2 ways to install Bikeeper. 

## By hands 

!> **Important** If you choose this method you need to install by our own **MariaDB, Grafana, Ngnix (reverse proxy for grafana), OpenStreetMap Server Tiles**

?> **Tips** In the project repository in the docker folder some shell scripts can help you to install all required services.

## With docker  

You can use our docker-compose file. 

?> **Tips**  This script will install docker and docker-compose. Run it with sudo. Tested on ubuntu ✅ 
```shell
apt update 
apt upgrade -y 
apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt get update
apt get install docker-ce docker-ce-cli containerd.io -y 
usermod -aG docker thor
# install docker compose after
curl -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```