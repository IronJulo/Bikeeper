

apt update 
apt upgrade -y 
apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt get update
apt get install docker-ce docker-ce-cli containerd.io -y 
usermod -aG docker $USER
# install docker compose after
curl -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose