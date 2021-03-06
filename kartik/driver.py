import numpy as np;import pandas as pd;import matplotlib.pyplot as plt;from mpl_toolkits.mplot3d import Axes3D
import pdb 

from beizer_curves import *;from B_spline import *;from B_spline_surface import *;from NURBS_surface import *
from NURBS_curve import *;from curve import *;from curve_object import *;from analytic_curves import *
from surface_object import *;from analytic_surfaces import *;from read_step_file import *


# fig = plt.figure();ax = plt.axes(projection='3d')


# ar = np.genfromtxt('step_data.csv', delimiter=',')
# c = B_spline(ar)
# c.plot_data(ax)
# plt.show()

# b_spline = "B_SPLINE_CURVE_WITH_KNOTS[(]\'.*\',(%d+),[(](#\\d+,)+(#\\d+)"
# cartesian_point = "(#\\d+)=CARTESIAN_POINT.\'Control Point\',.(.?\\d+.\\d+),(.?\\d+.\\d+),(.?\\d+.\\d+)"

a = read_step_file("bottle_text.stp")
q = curve_object()
i = 0
for y in a.spline_data:
	q.add_B_spline(y['cp'], y['deg']-1, y['deg'], y['knot'])
	i = i + 1
	if(i>5):
		pass

	# q.add_B_spline(y['cp'])
q.plot_data()
