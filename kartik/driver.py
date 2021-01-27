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
from curve_object import *
from analytic_curves import *

def generate_circle():
	a = np.zeros((25,3))
	for i in range(5):
		for j in range(5):
			a[i*5+j,0] = i-2;
			a[i*5+j,1] = j-2;
			a[i*5+j,2] = np.sqrt(50-(i-2)**2-(j-2)**2);
	np.save('circle_data',a);
def gen():
	h = 20; w = 20; curr = 0; deg=3;
	a = np.zeros((h*w,3))
	for i in np.linspace(np.pi/4,3*np.pi/4,h):
		for j in np.linspace(np.pi/4,3*np.pi/4,w):
			a[curr,0] = np.cos(i)
			a[curr,1] = np.sin(i)*np.cos(j)
			a[curr,2] = np.sin(i)*np.sin(j)
			curr = curr+1
	np.save('sphere1.npy',a);
	we = np.ones((h*w,1))
	np.save('weight_one.npy', we)
	knt1 = np.linspace(0.1, 0.9, h-deg)
	knt2 = np.linspace(0.1, 0.9, h-deg)
	np.save('knot1.npy',knt1); np.save('knot2.npy',knt2)
def gen2():
	h = 20; w = 20; curr = 0; deg=3;
	a = np.zeros((h*w,3))
	for i in np.linspace(-np.pi,np.pi,h):
		for j in np.linspace(-np.pi,np.pi,w):
			a[curr,0] = i
			a[curr,1] = j
			a[curr,2] = np.sin(3*i)*np.cos(3*j)
			curr = curr+1
	np.save('general1.npy',a);
	we = np.ones((h*w,1))
	np.save('weight_one.npy', we)
	knt1 = np.linspace(0.1, 0.9, h-deg)
	knt2 = np.linspace(0.1, 0.9, h-deg)
	np.save('knot1.npy',knt1); np.save('knot2.npy',knt2)

fig = plt.figure();ax = plt.axes(projection='3d')

# b = NURBS_curve(np.load('helix.npy'), np.ones((1,15)));b.plot_data();plt.show()
# b = B_spline(np.load('helix.npy'));b.plot_data(ax);plt.show()

# b = curve_object()
# b.add_B_spline(np.load('helix.npy'))
# b.add_B_spline(np.load('helix.npy')*2)
# b.add_B_spline(np.load('circle_data.npy'))
# b.plot_data()

ar = np.array([[1,0,0], [1.4142,1.4142,0],[0,1,0]])
b = circular_arc(ar)
b.plot_data(ax)
plt.show()

