# author: Werley Cordeiro
# werleycordeiro@gmail.com

# Lib
python -m pip install --user numpy pandas scipy matplotlib # cmd

import numpy as np
import pandas as pd
# import scipy as sp
# import matplotlib.pyplot as plt
# import os

# Data
url = "https://www.dropbox.com/s/inpnlugzkddp42q/bonds.csv?dl=1"
df = pd.read_csv(url,sep=';',index_col=0);
df.head();
df.tail();

l=df.shape[0]
matu=np.array([3,6,9,12,15,18,21,24,30,36,48,60,72,84,96,108,120])
T=matu.shape[0]
lam=0.0609

# Loading matrix
# os.getcwd()
# os.chdir("")
import Nelson_Siegel_factor_loadings as Nelson_Siegel_factor_loadings 
Z = Nelson_Siegel_factor_loadings(lam=lam,matu=matu)

# Betas and Yhat

import Yhat_betas as Yhat_betas
results = Yhat_betas(Y=df,Z=Z)
results[0].head()
results[1].head()

# VAR(1) coeffient matrix
import VARcoeff as VARcoeff 
var = VARcoeff(betas=results[0],l=l) 

# Start point to DNS-baseline via Kalman filter

para = np.zeros(36)
para[0] = lam # Start point to lambda
para[1:18] = np.sqrt(np.diag(np.cov((df.values-results[1]).T))) # Start point to H
# Start point to matrix phi
para[18] = var[0,1];
para[19] = var[0,2];
para[20] = var[0,3];
para[21] = var[1,1];
para[22] = var[1,2];
para[23] = var[1,3];
para[24] = var[2,1];
para[25] = var[2,2];
para[26] = var[2,3];
# Start point to vector mu
para[27] = np.mean(results[0])[0];
para[28] = np.mean(results[0])[1];
para[29] = np.mean(results[0])[2];
# Start point to matrix Q 
res = np.empty(((results[0].shape[0]-1),results[0].shape[1]))
res[:] = np.nan
for i in range(0,results[0].shape[0]-1):
 res[i,] = np.matmul(var[:,[1,2,3]],np.array(results[0])[i,]) - np.array(results[0])[i+1,]
 
from numpy.linalg import cholesky
Q = cholesky(np.cov(res.T));
para[30] = Q[0,0];
para[31] = Q[1,0];
para[32] = Q[1,1];
para[33] = Q[2,0];
para[34] = Q[2,1];
para[35] = Q[2,2];

# see https://github.com/werleycordeiro/Kalman-Filter-Dynamic-Nelson-Siegel
