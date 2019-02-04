## Mapping LOFAR

This repository contains files for making maps of LOFAR. Tools required are
 
 * Python (with packages `pandas`, `pyproj`)
 * Jupyter
 * QGIS
 * Inkscape

The coordinates all come from the [LOFAR repository](https://svn.astron.nl/LOFAR). Locally, I convert it to a PostGIS database to bring it to QGIS, but it requires some extra work. It can be done through plain CSV as well.

The docker command to create a postgis server is:
```
docker run --name=postgis -d -e POSTGRES_USER=dijkema -e POSTGRES_PASS=hoepla -e POSTGRES_DBNAME=lofargo -e ALLOW_IP_RANGE=0.0.0.0/0 -p 5432:5432 --restart=always kartoza/postgis
```

Basemaps are from [PDOK](https://www.pdok.nl/) (publieke data op de kaart).
