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

class surface_object():
	def __init__(self):
		self.surfaces = []
		self.kind = []

	def add_B_spline(self, cp, n, m, deru=2, derv=2, deg1=3, deg2=3, knot1=[], knot2=[]):
		self.surfaces.append(B_spline_surface(cp, n, m, deru, derv, deg1, deg2, knot1, knot2))
		self.kind.append('B_spline')

	def add_NURBS(self, cp, weight, n, m, deru=2, derv=2, deg1=3, deg2=3):
		self.surfaces.append(NURBS_curve(cp, weight, n, m, deru, derv, deg1, deg2))
		self.kind.append('NURBS')

	def plot_data(self, n=100):
		fig = plt.figure()
		ax = plt.axes(projection='3d')
		for x in self.surfaces:
			x.plot_data(ax,n)
		plt.show()