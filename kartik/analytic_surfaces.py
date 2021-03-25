import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb 
import math

# pdb.set_trace()

from surface import *


class cylinder(surface):
	def __init__(self, radius, height):
		self.radius = radius
		self.height = height
		surface.__init__(self, 1, 1)

	def evaluate(self, u, v):
		sol = np.zeros(3)
		sol[0] = self.radius*np.cos(u*2*np.pi)
		sol[1] = self.radius*np.sin(u*2*np.pi)
		sol[2] = self.height*v
		return sol


	def evaluate_derivatives(self, u):
		sol = np.zeros((2,2,3))
		sol[0,0,:] = self.evaluate(u,v)
		sol[1,0,:] = np.array([-self.radius*np.sin(u), self.radius*np.cos(u),0])
		sol[0,1,:] = np.array([0,0,1])
		return sol

	def plot_data(self, ax, n=100, m=100):
		cnti = 0; cntj=0;
		data = np.zeros((n+1,m+1,3))
		for i in np.linspace(0,1,n+1):
			for j in np.linspace(0,1,m+1):
				data[cnti,cntj,:] = self.evaluate(i,j)
				cntj = cntj+1
			cntj = 0
			cnti = cnti+1
		ax.plot_surface(data[:,:,0],data[:,:,1], data[:,:,2])


class plane(surface):
	def __init__(self, point, normal):
		self.point = point
		self.normal = normal
		surface.__init__(self, 1, 1)
		if(all(normal == np.array([1.,0,0]))):
			self.n1 = np.array([0,1.,0])
		else:
			self.n1 = np.array([1.,0,0])
		self.normal /= np.linalg.norm(self.normal)
		self.n1 -= self.n1.dot(self.normal)*self.normal
		self.n1 /= np.linalg.norm(self.n1)
		self.n2 = np.cross(self.n1, self.normal)
		self.n2 /= np.linalg.norm(self.n2)

	def evaluate(self, u, v):
		sol = self.point+u*self.n1+v*self.n2
		return sol

	def evaluate_derivatives(self, u, v):
		pass

	def plot_data(self, ax, n=100, m=100):
		cnti = 0; cntj=0;
		data = np.zeros((n+1,m+1,3))
		for i in np.linspace(0,1,n+1):
			for j in np.linspace(0,1,m+1):
				data[cnti,cntj,:] = self.evaluate(i,j)
				cntj = cntj+1
			cntj = 0
			cnti = cnti+1
		ax.plot_surface(data[:,:,0],data[:,:,1], data[:,:,2])


class SOR(surface):
	def __init__(self, gen_curve):
		surface.__init__(self, 1, 1)
		self.gen_curve = gen_curve

	def evaluate(self, u, v):
		sol = self.gen_curve.evaluate(u)
		r = (sol[0]**2+sol[1]**2)**0.5
		sol2 = r*(np.array([np.cos(2*np.pi*v),np.sin(2*np.pi*v),0]))
		sol2[2] = sol[2]
		return sol2

	def evaluate_derivatives(self, u, v):
		pass

	def plot_data(self, ax, n=100, m=100):
		cnti = 0; cntj=0;
		data = np.zeros((n+1,m+1,3))
		for i in np.linspace(0,1,n+1):
			for j in np.linspace(0,1,m+1):
				data[cnti,cntj,:] = self.evaluate(i,j)
				cntj = cntj+1
			cntj = 0
			cnti = cnti+1
		ax.plot_surface(data[:,:,0],data[:,:,1], data[:,:,2])


class circular_disk(surface):
	def __init__(self, radius=1):
		surface.__init__(self, 1, 1)
		self.radius = radius
		self.parts = []


	def evaluate(self, n, u, v):
		if(n==4):
			return np.array([self.radius*u-self.radius/2, self.radius*v-self.radius/2,0])
		th = np.pi*v/2-np.pi/4
		r = self.radius*u/(2*np.cos(th))+self.radius*(1-u)
		return np.array([r*np.cos(th+n*np.pi/2),r*np.sin(th+n*np.pi/2), 0])


	def evaluate_derivatives(self, u, v):
		pass


	def plot_data(self, ax, n=100, m=100):
		for k in range(5):
			cnti = 0; cntj=0;
			data = np.zeros((n+1,m+1,3))
			for i in np.linspace(0,1,n+1):
				for j in np.linspace(0,1,m+1):
					data[cnti,cntj,:] = self.evaluate(k,i,j)
					cntj = cntj+1
				cntj = 0
				cnti = cnti+1
			ax.plot_surface(data[:,:,0],data[:,:,1], data[:,:,2])


class sphere(surface):
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius
		surface.__init__(self,2,2)

	def evaluate(self, i, u, v):
		if (i<4):
			rot = np.array([[1,0,0],[0,np.cos(np.pi*i/2),np.sin(np.pi*i/2)],[0,-np.sin(np.pi*i/2),np.cos(np.pi*i/2)]])
		elif(i==4):
			rot = np.array([[np.cos(np.pi/2),0,np.sin(np.pi/2)],[0,1,0],[-np.sin(np.pi/2),0,np.cos(np.pi/2)]])
		else:
			rot = np.array([[np.cos(-np.pi/2),0,np.sin(-np.pi/2)],[0,1,0],[-np.sin(-np.pi/2),0,np.cos(-np.pi/2)]])
		u = np.pi*(u+0.5)/2; v = np.pi*(v+0.5)/2;
		ans = np.zeros(3); r = self.radius;
		ans[0] = r*np.cos(u); ans[1] = r*np.sin(u)*np.cos(v);
		ans[2] = r*np.sin(u)*np.sin(v);
		ans = np.matmul(rot, ans)
		return ans

	def evaluate_derivatives(self, u, v):
		pass

	def plot_data(self, ax, n=100, m=100):
		cnti = 0; cntj=0;
		data = np.zeros((n+1,m+1,3))
		s_i = 0
		for s_i in np.arange(6):
			for i in np.linspace(0,1,n+1):
				for j in np.linspace(0,1,m+1):
					data[cnti,cntj,:] = self.evaluate(s_i,i,j)
					cntj = cntj+1
				cntj = 0
				cnti = cnti+1
			cnti = 0; cntj=0;
			ax.plot_surface(data[:,:,0],data[:,:,1], data[:,:,2])