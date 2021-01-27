import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb 
import math

from curve import *


class line(curve):
	def __init__(self, cp):
		self.starting_point = cp[0]
		self.ending_point = cp[1]
		curve.__init__(self, 1)

	def evaluate(self, u):
		a = self.starting_point
		b = self.ending_point
		sol = u*a+(1-u)*b
		return sol

	def evaluate_derivatives(self, u):
		a = self.starting_point
		b = self.ending_point
		sol = np.zeros((2, a.shape[1]))
		sol[0,:] = u*a+(1-u)*b
		sol[1,:] = b-a
		return sol

	def plot_data(self, ax, n=100):
		cnt = 0
		data = np.zeros((n+1,3))
		for i in np.linspace(0,1,n+1):
			data[cnt,:] = self.evaluate(i)
			cnt = cnt+1
		ax.plot3D(data[:,0],data[:,1], data[:,2])


class circular_arc(curve):
	def __init__(self, cp, der_req = 1):
		curve.__init__(self, der_req)
		self.centeroid = cp.mean(axis = 0)
		cp = cp-self.centeroid
		n = np.cross(cp[0,:],cp[1,:])
		self.n1 = cp[0,:]/np.linalg.norm(cp[0,:])
		self.n2 = np.cross(self.n1,n)
		self.n2 = self.n2/np.linalg.norm(self.n2)
		x1 = cp[1,:].dot(self.n1)
		y1 = cp[1,:].dot(self.n2)
		x2 = cp[2,:].dot(self.n1)
		y2 = cp[2,:].dot(self.n2)
		A = np.array([[x1-1,y1],[x2-1,y2]])
		B = np.array([[(x1*x1+y1*y1-1)/2],[(x2*x2+y2*y2-1)/2]])
		center = np.matmul(np.linalg.inv(A),B)
		self.centeroid = self.centeroid + center[0]*self.n1+center[1]*self.n2
		self.scale = math.atan((center[1]+y1)/(center[0]+x1))
		# if(center[0]+x1<0):
		# 	self.scale += math.pi


	def evaluate(self, u):
		u *= self.scale
		sol = self.centeroid
		sol += math.cos(u)*self.n1+math.sin(u)*self.n2
		return sol


	def plot_data(self, ax, n=100):
		cnt = 0
		data = np.zeros((n,3))
		for u in np.linspace(0,6.28,n):
			data[cnt,:] = self.evaluate(u)
			cnt += 1
		ax.plot(data[:,0], data[:,1], data[:,2])


	def evaluate_derivatives(self, u):
		pass