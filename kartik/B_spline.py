import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb

from curve import *

class B_spline(curve):
    def __init__(self, cp, der_req=2, deg=3, show_cp = False):
        curve.__init__(self, der_req)
        self.degree = deg
        self.control_points = cp.T
        self.show_cp = show_cp
        n = self.control_points.shape[1]
        self.knot = [0 for i in range(0,deg)] + np.linspace(0,1,n-deg+1).tolist() + [1 for i in range(0,deg)]
        

    def find_knot(self, u):
        l = len(self.knot)
        if(u == 1):
            return l-self.degree-2
        for a in range(l):
            if(self.knot[a] > u):
                return a-1
        return l


    def evaluate_basis(self, u):
        deg = self.degree
        t0 = self.find_knot(u)
        knot = self.knot[t0-deg:t0+deg+1]
        # basis = np.zeros((0,deg+1))
        basis = [0 for t in range(0,deg+1)]
        basis[deg] = 1
        
        for i in range(1,deg+1):
            if(knot[deg-i+1]!=knot[deg+1]):
                basis[deg-i] = basis[deg-i+1]*(knot[deg+1]-u)/(knot[deg+1]-knot[deg-i+1])
            for j in range(deg-i+1,deg):
                if(knot[j]!= knot[j+i]):
                    basis[j] = basis[j]*(u-knot[j])/(knot[j+i]-knot[j])
                if(knot[j+1]!= knot[j+i+1]):
                    basis[j] += basis[j+1]*(knot[j+i+1]-u)/(knot[j+i+1]-knot[j+1])
            if(knot[deg]!=knot[deg+i]):
                basis[deg] *= (u-knot[deg])/(knot[deg+i]-knot[deg])

        return [t0, np.array(basis)]


    def evaluate(self, u):
        deg = self.degree
        [t0, basis] = self.evaluate_basis(u)
        val = self.control_points[:,t0-deg:t0+1]
        ans = val.dot(basis)
        return ans


    def evaluate_basis_derivatives(self, u):
        deg = self.degree
        t0 = self.find_knot(u)
        knot = self.knot[t0-deg:t0+deg+1]
        der_req = self.der_req
        basis = np.zeros((deg+1,deg+1), dtype=np.float64)
        basis[0][deg] = 1
    
        # evaluation of basis upto order degree
        for i in range(1,deg+1):
            if(knot[deg-i+1]!=knot[deg+1]):
                basis[i][deg-i] = basis[i-1][deg-i+1]*(knot[deg+1]-u)/(knot[deg+1]-knot[deg-i+1])
            for j in range(deg-i+1,deg):
                if(knot[j]!= knot[j+i]):
                    basis[i][j] = basis[i-1][j]*(u-knot[j])/(knot[j+i]-knot[j])
                if(knot[j+1]!= knot[j+i+1]):
                    basis[i][j] += basis[i-1][j+1]*(knot[j+i+1]-u)/(knot[j+i+1]-knot[j+1])
            if(knot[deg]!=knot[deg+i]):
                basis[i][deg] = basis[i-1][deg]*(u-knot[deg])/(knot[deg+i]-knot[deg])

        # derivative calculation
        # derivatives = np.zeros((deg+1, der_req+1),dtype=np.float64)
        derivatives = np.zeros((der_req+1, deg+1),dtype=np.float64)

        for i in range(0,deg+1):
            p = deg
            factor = p
            a = np.zeros(der_req+1, dtype=np.float64)
            a[0] = 1
            derivatives[0][i] = basis[deg][i]
            for k in range(1, der_req+1):
                if(i+1 <= deg):
                    deno1 = knot[i+deg+1]-knot[i+k]
                    if(deno1 != 0):
                        a[k] = -a[k-1]/deno1

                for j in range(k-1,0,-1):
                    deno2 = knot[deg+j-k+1+i]-knot[j+i]
                    if(deno2 != 0):
                        a[j] = (a[j]-a[j-1])/deno2
                deno2 = knot[deg-k+1+i]-knot[0+i]
                if(deno2 != 0):
                    a[0] = a[0]/deno2
                rend = min(deg+1, i+k+1)
                # derivatives[i][k] = a[0:rend-i].dot(basis[deg-k][i:rend])
                derivatives[k,i] = factor*a[0:rend-i].dot(basis[deg-k][i:rend])
                p -= 1
                factor *= p
        
        return [t0,derivatives]

    
    def evaluate_derivatives(self, u):
        deg = self.degree
        [t0, derivatives] = self.evaluate_basis_derivatives(u)
        val = self.control_points[:,t0-deg:t0+1]
        ans = val.dot(derivatives.T)
        return ans


    def plot_data(self, ax, n=100):
        cnt = 0
        data = np.zeros((n+1,3, self.der_req+1))
        for i in np.linspace(0,1,n+1):
            data[cnt] = self.evaluate_derivatives(i)
            cnt = cnt+1
        
        ax.plot3D(data[:,0,0],data[:,1,0], data[:,2,0])
        if(self.show_cp == True):
            ax.plot3D(self.control_points[0,:],self.control_points[1,:],self.control_points[2,:],'ro')