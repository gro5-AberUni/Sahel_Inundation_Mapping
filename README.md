# Profound changes in wetland extent across the Sahel and East Africa (2014–2024) drive ecological shifts and human vulnerability

**Authors:** Andy Hardy, Gregory Oakes, Peter Bunting, Mori Diallo, Lorentzo Gaffi, Lammert Hilarides, Edmund Kuto, Boubacar Youssouf, Christopher Taylor

## Abstract

Historically defined by climate variability and recurrent droughts, the Sahel-East Africa region has undergone a profound hydrological shift, yet the regional impact of recent extreme climatic events remains poorly understood. Using high-frequency 30 m Landsat analysis, we reconstruct a decade of inundation dynamics (2014–2023) across this trans-continental domain, revealing an 86% surge in wetland extent. 

This expansion represents a large-scale transition from ephemeral to seasonal wetlands, likely triggered by the record-breaking positive Indian Ocean Dipole in late 2019 affecting much of East Africa, and a more northerly latitude of the Intertropical Convergence Zone during recent Sahelian rainy seasons. We identify focal areas of extreme expansion in inundated area that intersect directly with major capital cities, refugee camps, and critical agricultural schemes. These results demonstrate that short-term climatic shocks can permanently reset regional flood baselines, necessitating an urgent re-evaluation of flood vulnerability and water management across the Sahel and East Africa.

## Data Processing Scripts

This repository contains the scripts used to generate the bi-monthly classified products used within this study, as well as the post-classification refinement applied to the imagery.

### TropWet Spectral Unmixing

`tropWetUnmix.ipynb`

This notebook is to be used in Google Colab, and uses Google Earth Engine to collect Landsat imagery over a given tile, and for a given year/month and performs linear spectral unmixing, using the Endmembers described in Hardy et al., (2026 - Submitted). These are then exported to a Google Drive location.

*Note: You need to change the GEE project on line 3 to your project, and by default, the line to submit a GEE task is commented out. Uncomment the last line to allow for data to be exported.*

### Fuzzy Classification 

`fuzzy.py` **and** `perform_analysis_opt.py`

The `fuzzy.py` file contains the functions to apply fuzzy class membership based on lower and upper bounds of membership. 

The file `perform_analysis_opt.py` performs the actual classification on the output images produced in GEE by the `tropWetUnmix.ipynb` notebook. The unmixed image is defined in the script, and the fuzzy rulebase is applied to that image to produce a multiclass output as described in Hardy et al, (2026 - Submitted) supplementary methods document. The upper and lower bounds of fuzzy membership are defined through Bayesian Optimisation ([Nogueira, 2014](https://github.com/bayesian-optimization/BayesianOptimization))

### Post Classification Refinement

`./Post_Classification_Refinement/`

The scripts used for post-classification refinement are included in this directory and should be run in the following order:

* 01_waterFrequency_RIOS_TS.py

In addition, auxiliary datasets are required to run the post-classification process, which can be found on Zenodo at the following location:

`https://zenodo.org/uploads/19705779`

## References and Software Dependencies

* Hardy, A., Oakes, G., Bunting, P., Diallo, M., Gaffi, L., Hilarides, L., Kuto, E., Youssouf, B., & Taylor, C. (2026). *Profound changes in wetland extent across the Sahel and East Africa (2014–2024) drive ecological shifts and human vulnerability* [Manuscript submitted for publication].

* Hardy, A., Oakes, G., & Ettritch, G. (2020). Tropical wetland (TropWet) mapping tool: The automatic detection of open and vegetated waterbodies in Google Earth engine for tropical wetlands. *Remote Sensing*, 12(7), 1182.

* Bunting, P., Clewley, D., Lucas, R. M., & Gillingham, S. (2014). The Remote Sensing and GIS Software Library (RSGISLib). *Computers and Geosciences*, 62, 216–226.

* Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18–27.

* Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., Fernández del Río, J., Wiebe, M., Peterson, P., ... Oliphant, T. E. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2

* Gillingham, S., & Flood, N. (2014). *Raster I/O Simplification (RIOS)*. https://www.rioshome.org/en/latest/index.html

* Nogueira, F. (2014). *Bayesian Optimization: Open source constrained global optimization tool for Python*. GitHub. https://github.com/bayesian-optimization/BayesianOptimization
