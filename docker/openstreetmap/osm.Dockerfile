FROM klokantech/tileserver-gl
WORKDIR /data/
RUN wget "https://data.maptiler.com/download/WyJiZmZkZmM5NS1lMTVlLTRmYjgtYWFkZC1lNzM5MGQ1NjAxOTciLCItMSIsODcwMl0.YDZ1Fg.Nv-IPsVI3gWKe4TWwDYRJkgBy2k/maptiler-osm-2017-07-03-v3.6.1-france_centre.mbtiles?usage=personal" --output-document=centre.mbtiles
