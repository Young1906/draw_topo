# Sample data: 
_URL = "https://gist.githubusercontent.com/anonymous/d8975f76f5bcde7bd455/raw/831239b213fc29462db68f33caad3f05c57c0eff/topoplot_sample_data.csv"


import pandas as pd 
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

class Topo():
    def __init__(self, Sig):
        '''
        Sig: R^{nx3} including X, Y cordinate of electrode + signal strength
        n : number of channel
        '''
        self.Sig = Sig
        self.gridz = None
        self.points = None
        self.values = None
        self.grid_x = None
        self.grid_y = None

    def _mgrid(self, padding=.1, resolution = 1000j, _method = 'linear'):
        
        x_min, x_max, y_min, y_max = np.min(Sig[:,0]), np.max(Sig[:,0]), \
            np.min(Sig[:,1]), np.max(Sig[:,1]), 
        
        dimX = x_max - x_min
        dimY = y_max - y_min

        x_min = x_min - dimX * padding
        x_max = x_max + dimX * padding
        y_min = y_min - dimY * padding
        y_max = y_max + dimY * padding


        grid_x, grid_y = np.mgrid[x_min:x_max:resolution, \
            y_min:y_max:resolution]

        points = Sig[:, 0:2]
        values = Sig[:,2]

        grid_z = griddata(points, values, (grid_x, grid_y), method=_method)

        self.gridz = grid_z.T
        self.points = points
        self.values = values,
        self.bound = (x_min, x_max, y_min, x_max)
        self.grid_x ,self.grid_y  = grid_x, grid_y

        return 0 

    def plot(self):
        self._mgrid()
        plt.imshow(self.gridz, self.bound, alpha = .5 )
        plt.contourf(self.gridx, self.grid_y, self.gridz, alpha = .5)
        plt.colorbar()
        plt.show()




if __name__ == "__main__":
    df = pd.read_csv(_URL)
    Sig = df[['x','y', 'signal']].values

    T = Topo(Sig)
    T.plot()


