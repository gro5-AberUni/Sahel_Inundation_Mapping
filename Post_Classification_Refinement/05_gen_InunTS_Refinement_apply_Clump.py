import rsgislib
from rsgislib import segmentation
import rsgislib.segmentation.tiledclump
import rsgislib.imagecalc
from rsgislib import rastergis
rsgislib.imageutils.set_env_vars_lzw_gtiff_outs(True)

from osgeo import gdal
import rios
from rios import rat

import numpy as np

import pandas as pd

inunTsImg = './Sahel_Inun_Count_2014-2018.tif'
inunTS_GT0 = inunTsImg.replace('.tif','_GT0-Bin.tif')
inunTS_GT6 = inunTsImg.replace('.tif','_GT6-Bin.tif')

band_defns = list()
band_defns.append(rsgislib.imagecalc.BandDefn('b1', inunTsImg, 1))
rsgislib.imagecalc.band_math(inunTS_GT0, 'b1>0?1:0', 'GTIFF', 1, band_defns)
rsgislib.imagecalc.band_math(inunTS_GT6, 'b1>=6?1:0', 'GTIFF', 1, band_defns)

clumpsImg = inunTS_GT0.replace('.tif','_Clumps.kea')

rsgislib.segmentation.tiledclump.perform_clumping_multi_process(inunTS_GT0, clumpsImg, './tmp', 1500, 1500,'KEA', 8)

inunTS_GT6Dist = inunTS_GT6.replace('.tif','_Dist.kea')
rsgislib.imagecalc.calc_dist_to_img_vals(inunTS_GT6, inunTS_GT6Dist, 1, 1, 'KEA', out_no_data_val=-9999,unit_geo=True)

bs = []
bs.append(rastergis.BandAttStats(band=1, min_field='distMin', max_field='distMax', mean_field='distMean', std_dev_field='distStdDev'))
rastergis.populate_rat_with_stats(inunTS_GT6Dist, clumpsImg, bs)

bs = []
bs.append(rastergis.BandAttStats(band=1, min_field='CountMin', max_field='CountMax', mean_field='CountMean', std_dev_field='CountStdDev'))
rastergis.populate_rat_with_stats(inunTsImg, clumpsImg, bs)

# Open RAT
inRatFile = clumpsImg
ratDataset = gdal.Open(inRatFile)

print(inRatFile)

# Set column names
x_col_names = ['distMin','distMax','distMean','CountMax']

# Set up list to hold data
X = []

# Read in data from each column
for colName in x_col_names:
    X.append(rat.readColumn(ratDataset, colName))
    print("Reading: ", colName)
data = np.asarray(X)
dataT = pd.DataFrame(np.transpose(data),columns=x_col_names)

#### 30m (1*Pxl) = 0.000269494585235856472 ####

#### Dist 100m = 0.0026949459 ####
#### Dist 150m = 0.040424188 ####
#### Dist 250m = 0.067373646 ####
#### Dist 500m = 0.134747293 ####

dist = 0.0026949459

rastArr = np.where(dataT['distMean']>dist,np.where(dataT['CountMax']<=2,2,1),1)

rios.rat.writeColumn(clumpsImg, 'ThreshSelect', rastArr, colType=gdal.GFT_Integer)

print(dataT)

rastSelection = clumpsImg.replace('.kea','_SelectedClumps.tif')

rsgislib.rastergis.export_col_to_gdal_img(clumpsImg, rastSelection, 'GTIFF', 1, 'ThreshSelect', rat_band=1)
