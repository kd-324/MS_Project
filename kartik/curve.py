import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import pdb
from abc import ABC, abstractmethod


class curve(ABC):
	def __init__(self, der_req):
		ABC.__init__(self)
		self.der_req = der_req
  # Given a parameter, it will return function value
	@abstractmethod
	def evaluate(self, u):
		pass

	# It computes derivatives upto der_req. Note 0th derivative is function value
	@abstractmethod
	def evaluate_derivatives(self, u):
		pass

	# For plotting the curve
	@abstractmethod
	def plot_data(self):
		pass
