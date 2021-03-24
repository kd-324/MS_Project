import re; import numpy as np;

import pdb
# pdb.set_trace()

class read_step_file:
	def __init__(self, filename):
		self.filename = filename
		self.points = {}
		self.spline_data = []
		self.surface_data = []
		self.extract_cp()
		# self.extract_b_spline()
		self.extact_b_spline_surface()

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
			
			self.spline_data.append({'deg': deg, 'cp': np.array(cp), 'knot': np.array(knot)/max(knot)})

	def extact_b_spline_surface(self):
		f = open(self.filename); surfaces = []
		cnt = -1
		for line in f:
			data = re.search("#\\d+=B_SPLINE_SURFACE_WITH_KNOTS[(]\'(.*)\',(\\d+),(\\d+),[(]([(].*[)])[)],(.*),(.*),(.*),(.*),[(](.*)[)],[(](.*)[)],[(](.*)[)],[(](.*)[)],(.*)[)]", line)
			if(data):
				surfaces.append(data)

		for x in surfaces:
			degu = int(x.group(2))
			degv = int(x.group(3))
			cnt = cnt+1
 
			cp = []
			var = re.findall("[#\\d,]{2,}",x.group(4))
			# var = re.findall("(?#\\d+,)+#\\d+", x.group(4))
			for temp in var:
				var2 = re.findall("\\d+", temp)
				cp.append([self.points[x] for x in var2])
			multiplicityu = re.findall("\\d+",x.group(9))
			distinct_knotu = re.findall("-?\\d+.?\\d*E?-?\\d*",x.group(11))
			multiplicityv = re.findall("\\d+",x.group(10))
			distinct_knotv = re.findall("-?\\d+.?\\d*E?-?\\d*",x.group(12))
			n = len(multiplicityu); knotu = []
			for i in range(n):
				for j in range(int(multiplicityu[i])):
					knotu.append(float(distinct_knotu[i]))
			m = len(multiplicityv); knotv = []
			for i in range(m):
				for j in range(int(multiplicityv[i])):
					knotv.append(float(distinct_knotv[i]))

			knotu = (np.array(knotu)-min(knotu))/(max(knotu)-min(knotu))
			knotv = (np.array(knotv)-min(knotv))/(max(knotv)-min(knotv))
				          
			self.surface_data.append({'degu': degu, 'degv': degv, 'cp': np.array(cp), 'knotu': knotu, 'knotv': knotv})

#129401=B_SPLINE_SURFACE_WITH_KNOTS('',3,3,((#129402,#129403,#129404,#129405,#129406,#129407),(#129408,#129409,#129410,#129411,#129412,#129413),(#129414,#129415,#129416,#129417,#129418,#129419),(#129420,#129421,#129422,#129423,#129424,#129425),(#129426,#129427,#129428,#129429,#129430,#129431),(#129432,#129433,#129434,#129435,#129436,#129437),(#129438,#129439,#129440,#129441,#129442,#129443),(#129444,#129445,#129446,#129447,#129448,#129449)),.UNSPECIFIED.,.F.,.F.,.U.,(4,1,1,1,1,4),(4,1,1,4),(0.,1.21469910103,2.42939820107,3.6440973021,4.85879640214,6.07349550317),(0.,1.07111128502,2.14222256904,3.21333385306),.UNSPECIFIED.)	
