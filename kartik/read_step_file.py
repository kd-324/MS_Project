class read_step_file:
	def __init__(self, filename):
		self.filename = filename
		self.points = {}
		self.spline_data = []
		self.extract_cp()
		self.extract_b_spline()

	def extract_cp(self):
		f = open(self.filename)
		for line in f:
			x = re.search("#(\\d+)=CARTESIAN_POINT.\'Control Point\',.(.?\\d+.?\\d*E?-?\\d*),(.?\\d+.?\\d*E?-?\\d*),(.?\\d+.?\\d*E?-?\\d*)", line)
			if(x):
				self.points[x.group(1)] = [float(x.group(2)),float(x.group(3)),float(x.group(4))]
		
	def extract_b_spline(self):
		f = open(self.filename); splines = []
		for line in f:
			data = re.search("B_SPLINE_CURVE_WITH_KNOTS[(]\'(.*)\',(\\d+),[(](.*)[)],(.*),(.*),(.*),[(](.*)[)],[(](.*)[)],(.*)[)]", line)
			if(data):
				splines.append(data)
		for x in splines:
			deg = int(x.group(2))

			cp_id = re.findall("\\d+", x.group(3)); cp = []
			for icp_id in cp_id:
				cp.append(self.points[icp_id])
			
			multiplicity = re.findall("\\d+",x.group(7))
			distinct_knot = re.findall("\\d+.?\\d*E?-?\\d*",x.group(8))
			n = len(multiplicity); knot = []
			for i in range(n):
				for j in range(int(multiplicity[i])):
					knot.append(float(distinct_knot[i]))
			
			self.spline_data.append({'deg': deg, 'cp': np.array(cp), 'knot': np.array(knot)})
