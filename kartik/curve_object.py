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

class curve_object():
	def __init__(self):
		self.curves = []
		self.kind = []

	def add_beizer(self, cp):
		self.curves.append(beizer_curves(cp))
		self.kind.append('beizer')

	def add_B_spline(self, cp, der_req=2, deg=3):
		self.curves.append(B_spline(cp, der_req, deg))
		self.kind.append('B_spline')

	def add_NURBS_curve(self, cp, weight, der_req=2, deg=3):
		self.curves.append(NURBS_curve(cp, weight, der_req, deg))
		self.kind.append('NURBS')

	def plot_data(self):
		fig = plt.figure()
		ax = plt.axes(projection='3d')
		for x in self.curves:
			x.plot_data(ax)
		plt.show()