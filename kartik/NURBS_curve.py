import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import copy
import pdb

from B_spline import *
from curve import *

class NURBS_curve(B_spline):
	def __init__(self, cp, weight, der_req=2, deg=3, knot=[]):
		B_spline.__init__(self, cp,der_req, deg, knot)
		self.weight = weight
		# self.control_points_plot = copy.deepcopy(self.control_points)
		self.control_points *= self.weight
		self.control_points = np.append(self.control_points, self.weight, axis = 0)


	def translate(self, pos):
		for x in self.control_points.T:
			x[0:3] /= x[3]
			x[0:3] += pos
			x[0:3] *= x[3]


	def rotatez(self, angle):
		for x in self.control_points.T:
			x[0:3] /= x[3]
			rot = np.array([[np.cos(angle),np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
			x[0:2] = np.matmul(rot,x[0:2])
			# x[0] = x[0]*np.cos(angle)+x[1]*np.sin(angle)
			# x[1] = -x[0]*np.sin(angle)+x[1]*np.cos(angle)
			x[0:3] *= x[3]


	def evaluate(self, u):
		cp = self.control_points
		deg = self.degree
		[x0,basis] = self.evaluate_basis(u)
		# sol = np.matmul(basis.T, cp[x0-deg:x0+1,0:3])
		sol = np.matmul(cp[:,x0-deg:x0+1],basis.T)
		sol = sol[0:3]/sol[3]		
		return sol

	
	def plot_data(self, ax, n=100, show_control_points=False):
	  cnt = 0
	  data = np.zeros((n+1,3, self.der_req+1))
	  for i in np.linspace(0,1,n+1):
	      data[cnt,:,0] = self.evaluate(i)
	      cnt = cnt+1
	  
	  ax.plot3D(data[:,0,0], data[:,1,0], data[:,2,0])
	  if(show_control_points):
	  	# ax.plot3D(self.control_points_plot[0,:],self.control_points_plot[1,:],self.control_points_plot[2,:],'ro')
	  	ax.plot3D(self.control_points[0,:]/self.control_points[3,:],self.control_points[1,:]/self.control_points[3,:],self.control_points[2,:]/self.control_points[3,:],'ro')