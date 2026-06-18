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
#2018,2019,2020,2021,2022,
listFiles = []
for yr in [2014,2015,2016,2017,2018]:
    for mth in [1,3,5,7,9,11]:
        img = os.path.abspath(glob.glob('./Class/{2}/*Classified*Month-{0}-{1}_Year-{2}*Lvl2.tif'.format(mth,mth+1,yr))[0])
        listFiles.append(img)

print(listFiles)

yr = '2014-2018'

datatype = rsgislib.TYPE_8INT
numpyDT = rsgislib.get_numpy_datatype(datatype)

progress_bar = rsgislib.TQDMProgressBar()

infiles = applier.FilenameAssociations()
infiles.inputImgs = listFiles

outfiles = applier.FilenameAssociations()
outfiles.inunSum = 'Sahel_Inun_Count_{0}.tif'.format(yr)
outfiles.inunPer = 'Sahel_Inun_Per_{0}.tif'.format(yr)

outfiles.validSum = 'Sahel_Valid_Obs_{0}.tif'.format(yr)

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
aControls.windowxsize = 255
aControls.windowysize = 255
#aControls.setNumThreads(10)
#aControls.setJobManagerType('mpi')

def _applyFuzzy(info, inputs, output, otherargs):
    timeStack = np.stack(inputs.inputImgs)
    timeStackValid = np.where(timeStack != 0, 1, 0)
    timeStackInun = np.where(timeStack==1,1,0)
    inunSum = np.sum(timeStackInun,axis=0)
    validSum = np.sum(timeStackValid,axis=0)

    inunPer = (inunSum/validSum)*100
    output.inunSum = inunSum.astype(np.uint8)
    output.inunPer = inunPer.astype(np.uint8)
    output.validSum = validSum.astype(np.uint8)


applier.apply(
        _applyFuzzy, infiles, outfiles, otherargs, controls=aControls
    )
