docker run -d \
  --name grafana\
  -p 3000:3000 \
  -v $(pwd)/grafana.ini:/etc/grafana/grafana.ini \
  -v $(pwd)/grafana-storage:/var/lib/grafana \
  --restart unless-stopped \
  grafana/grafana
