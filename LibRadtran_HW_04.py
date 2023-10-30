import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import os     

directory = 'instert working directory'

os.chdir(directory)

Names = ['wavelength','direct horizontal irradiance',
         'diffuse downward horizontal irradiance',
         'diffuse upward horizontal irradiance (reflected)','uavgdirect',
         'uavgdiffuse downward','uavgdiffuse upward']

SZAs = ["10", "40", "70", "85"]

for SZA in SZAs:
    
    filenames = [f for f in os.listdir(directory+"/Data_partA") if f.startswith(SZA) and f.endswith('.out')]
    ref_files = [f for f in filenames if f.endswith('00.out')][0]
    filenames.remove(ref_files)
    data_ref = pd.read_csv(ref_files, header=None, names=Names,  delimiter = r'\s+')
    data_ref[data_ref < 0] = np.nan
    data_ref['global horizontal irradiance'] = data_ref['direct horizontal irradiance'] + data_ref['diffuse downward horizontal irradiance']

    for file in filenames:
        data =  pd.read_csv(file, header=None, names=Names,  delimiter = r'\s+')
        data[data < 0] = np.nan
        b = re.split('[a .]',file)[1]
        b_title = '.'.join(b)
        data['global horizontal irradiance'] = data['direct horizontal irradiance'] + data['diffuse downward horizontal irradiance']
        ratio_GHI_Direct = data['direct horizontal irradiance']/data_ref['direct horizontal irradiance']
        ratio_GHI_Diffuse = data['diffuse downward horizontal irradiance']/data_ref['diffuse downward horizontal irradiance']
        ratio_GHI = data['global horizontal irradiance']/data_ref['global horizontal irradiance']       
        fig = plt.figure(figsize = (14, 8), dpi = 150)
        plt.plot(data_ref['wavelength'],ratio_GHI_Direct,'.', markersize=7, label='GHI Direct Ratio')
        plt.plot(data_ref['wavelength'],ratio_GHI_Diffuse,'.', markersize=7, label='GHI Diffuse Ratio')
        plt.plot(data_ref['wavelength'],ratio_GHI,'.', markersize=7, label='GHI Ratio') 
        plt.xlabel('Wavelength', fontsize=16)
        plt.ylabel('Ratios', fontsize=16)       
        plt.title('b='+b_title+'&'+'SZA='+SZA, fontsize=16)
        plt.legend(loc='center left',
         ncol=1, fancybox=True, shadow=True,bbox_to_anchor=(1 , 0.9),prop={'size':12})
        plt.tight_layout()
        plt.savefig("Graphs/Fig_SZA" + SZA + "_b_" + b+".png", format="png", dpi=150, bbox_inches="tight")
        plt.close()