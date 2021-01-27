import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb

from B_spline import *
from curve import *

class NURBS_curve(B_spline):
	def __init__(self, cp, weight, der_req=2, deg=3):
		B_spline.__init__(self, cp,der_req, deg)
		self.weight = weight
		self.control_points *= self.weight
		self.control_points = np.append(self.control_points, self.weight, axis = 0)


	def evaluate_basis(self, u):
		[x0,basis] = B_spline.evaluate_basis(self,u)
		basis = basis[0:3] / basis[3]
		return [x0, basis]


	def evaluate(self, u):
		cp = self.control_points
		deg = self.degree
		[x0,basis] = self.evaluate_basis(u)
		sol = np.matmul(basis.T, cp[x0-deg:x0+1,0:3])
		return sol
	
	def plot_data(self, ax, n=100):
	  cnt = 0
	  data = np.zeros((n+1,3, self.der_req+1))
	  for i in np.linspace(0,1,n+1):
	      data[cnt,:,0] = self.evaluate(i)
	      cnt = cnt+1
	  
	  ax.plot3D(data[:,0,0],data[:,1,0], data[:,2,0])
	  ax.plot3D(self.control_points[0,:],self.control_points[1,:],self.control_points[2,:],'ro')