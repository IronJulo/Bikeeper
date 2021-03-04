FROM klokantech/tileserver-gl

ARG MAP_TOKEN=
ENV MAP_TOKEN=$MAP_TOKEN

WORKDIR /bundle
RUN wget "https://data.maptiler.com/download/$MAP_TOKEN/maptiler-osm-2017-07-03-v3.6.1-france_centre.mbtiles?usage=personal" --output-document=centre.mbtiles

WORKDIR /data
RUN cp /bundle/centre.mbtiles .
