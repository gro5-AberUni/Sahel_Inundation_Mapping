import glob
import os

listCmds = []

# targetThreshold = 'GT0'
# year = '2023'
#2018,2019,2020,2021,2022,
for year in [2014,2015,2016,2017,2018]:
    for i in [1,3,5,7,9,11]:
        classImg = os.path.abspath(glob.glob('./Class/{0}/Sahel_Classified*Month-{1}-{2}*{0}*Lvl2.tif'.format(year,i,i+1))[0])
        print(classImg)

        inunImg = os.path.abspath('./Sahel_Inun_Count_2014-2018_GT0-Bin_Clumps_SelectedClumps.tif')

        outputImg = classImg.replace('.tif','_Lvl3_Inun_Refinement.tif')

        cmd = 'python 07_apply_Inun_TS_Refinement.py -i {0} -s {1} -o {2}\n'.format(classImg,inunImg,outputImg)

        listCmds.append(cmd)

        print(listCmds)


with open('recodeInunRefinementJob.sh', 'w') as f:
    for cmd in listCmds:
        f.write(cmd)
