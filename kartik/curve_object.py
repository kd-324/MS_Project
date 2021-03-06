import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb 

from beizer_curves import *
from B_spline import *
from B_spline_surface import *
from NURBS_surface import *
from NURBS_curve import *
from curve import *
from analytic_curves import *

class curve_object():
	def __init__(self):
		self.curves = []
		self.kind = []

	def add_beizer(self, cp):
		self.curves.append(beizer_curves(cp))
		self.kind.append('beizer')

	def add_line(self, cp):
		self.curves.append(line(cp))
		self.kind.append('line')

	def add_B_spline(self, cp, der_req=2, deg=3, knot=[]):
		self.curves.append(B_spline(cp, der_req, deg, knot=[]))
		self.kind.append('B_spline')

	def add_NURBS(self, cp, weight, der_req=2, deg=3):
		self.curves.append(NURBS_curve(cp, weight, der_req, deg))
		self.kind.append('NURBS')

	def add_polygon(self, cp):
		n = cp.shape[0]
		for i in range(n-1):
			self.curves.append(line(cp[i:i+2,:]))
			self.kind.append('line')
		self.curves.append(line(np.array([cp[0,:],cp[n-1,:]])))
		self.kind.append('line')

	def plot_data(self):
		fig = plt.figure()
		ax = plt.axes(projection='3d')
		for x in self.curves:
			x.plot_data(ax)
		plt.show()