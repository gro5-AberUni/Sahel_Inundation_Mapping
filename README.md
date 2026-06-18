# Profound changes in wetland extent across the Sahel and East Africa (2014–2024) drive ecological shifts and human vulnerability

**Authors:** Andy Hardy, Gregory Oakes, Peter Bunting, Mori Diallo, Lorentzo Gaffi, Lammert Hilarides, Edmund Kuto, Boubacar Youssouf, Christopher Taylor

## Abstract

Historically defined by climate variability and recurrent droughts, the Sahel-East Africa region has undergone a profound hydrological shift, yet the regional impact of recent extreme climatic events remains poorly understood. Using high-frequency 30 m Landsat analysis, we reconstruct a decade of inundation dynamics (2014–2023) across this trans-continental domain, revealing an 86% surge in wetland extent. 

This expansion represents a large-scale transition from ephemeral to seasonal wetlands, likely triggered by the record-breaking positive Indian Ocean Dipole in late 2019 affecting much of East Africa, and a more northerly latitude of the Intertropical Convergence Zone during recent Sahelian rainy seasons. We identify focal areas of extreme expansion in inundated area that intersect directly with major capital cities, refugee camps, and critical agricultural schemes. These results demonstrate that short-term climatic shocks can permanently reset regional flood baselines, necessitating an urgent re-evaluation of flood vulnerability and water management across the Sahel and East Africa.

## Data Processing Scripts

This repository contains the scripts used to generate the bi-monthly classified products used within this study, as well as the post-classification refinement applied to the imagery.

### TropWet Spectral Unmixing

*tropWetUnmix.ipynb*

This notebook is to be used in Google Colab, and uses Google Earth Engine to collect Landsat imagery over a given tile, and for a given year/month and performs linear spectral unmixing, using the Endmembers described in Hardy et al., (2026 - Submitted). These are then exported to a Google Drive location.

*Note: You need to change the GEE project on line 3 to your project, and by default, the line to submit a GEE task is commented out. Uncomment the last line to allow for data to be exported.*

### Fuzzy Classification 

*fuzzy.py* **and** *
