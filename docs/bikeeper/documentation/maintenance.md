# Maintenance

Maintain is very easy, just update ! 

To maintain bikeeper : 
- update your linux (`apt update -y && apt upgrade -y`)
- update docker image to lasted
- inspect logs (`docker logs container_name`)
- monitor your disk free space `df -h /` and `df -h | awk '{print $5 " " $6}' | sort -n | tail -5`
- Clean log ```for I in `ls "/var/log/*.log"`;do >"$I";done```
- Check internet connectivity `ping 8.8.8.8`
- Inspect Process performances `htop`   
If you have any issues email a Bikeeper developpers.