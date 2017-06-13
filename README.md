## Mapping LOFAR

This repository contains files for making maps of LOFAR. Tools required are
 
 * Python (with packages `pandas`, `pyproj`)
 * Jupyter
 * QGIS
 * Inkscape

The coordinates all come from the [LOFAR repository](https://svn.astron.nl/LOFAR). Locally, I convert it to a PostGIS database to bring it to QGIS, but it requires some extra work. It can be done through plain CSV as well.

Basemaps are from [PDOK](https://www.pdok.nl/) (publieke data op de kaart).