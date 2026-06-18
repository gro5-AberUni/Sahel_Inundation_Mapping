import numpy as np
from osgeo import gdal
from osgeo import osr
import gc
import glob
import os
import rsgislib
from rios import applier
from rsgislib import imageutils

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs(True)
#
listFiles = []
for yr in [2014,2015,2016,2017,2018]:
    #listFiles = []
    for mth in [1,3,5,7,9,11]:
        print(yr)
        print(mth)
        img = os.path.abspath(glob.glob('./Class/{2}/*Classified*Month-{0}-{1}_Year-{2}*.tif'.format(mth,mth+1,yr))[0])
        listFiles.append(img)

print(listFiles)

yr = '2014-2018'

datatype = rsgislib.TYPE_8INT
numpyDT = rsgislib.get_numpy_datatype(datatype)

progress_bar = rsgislib.TQDMProgressBar()

infiles = applier.FilenameAssociations()
infiles.inputImgs = listFiles

outfiles = applier.FilenameAssociations()
outfiles.waterSum = 'Sahel_Water_Count_{0}.tif'.format(yr)
outfiles.waterPer = 'Sahel_Water_Per_{0}.tif'.format(yr)

otherargs = applier.OtherInputs()
otherargs.npDT = np.uint8
aControls = applier.ApplierControls()
aControls.progress = progress_bar
aControls.creationoptions = rsgislib.imageutils.get_rios_img_creation_opts(
'GTIFF'
)
aControls.drivername = 'GTIFF'
aControls.omitPyramids = True
aControls.calcStats = False
aControls.windowxsize = 512
aControls.windowysize = 512

def _applyFuzzy(info, inputs, output, otherargs):
    timeStack = np.stack(inputs.inputImgs)
    timeStackValid = np.where(timeStack != 0, 1, 0)
    timeStackWater = np.where(timeStack==4,1,0)
    waterSum = np.sum(timeStackWater,axis=0)
    validSum = np.sum(timeStackValid,axis=0)

    waterPer = (waterSum/validSum)*100
    output.waterSum = waterSum.astype(np.uint8)
    output.waterPer = waterPer.astype(np.uint8)

applier.apply(
        _applyFuzzy, infiles, outfiles, otherargs, controls=aControls
    )
