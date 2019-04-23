
class setFitParam:

	def __init__(self, f1, f2, index, idm):
		self.index = index
		self.f1 = f1
		self.f2 = f2
		self.idm = idm

	def setDiTauFitParameters(self):
		self.f1[self.index].SetParameter( 0, 0.2)
		self.f1[self.index].SetParameter( 1, 5.0 )
		self.f1[self.index].SetParameter( 2, 7.0 )
		self.f1[self.index].SetParameter( 3, -30.)
		self.f1[self.index].SetParameter( 4, 1.0 )
		self.f1[self.index].SetParameter( 5, 1.0)
		
	def setDiTauDMFitParameters(self):
		self.f2[self.idm][self.index].SetParameter( 0, 0.2)
		self.f2[self.idm][self.index].SetParameter( 1, 5.0 )
		self.f2[self.idm][self.index].SetParameter( 2, 7.0 )
		self.f2[self.idm][self.index].SetParameter( 3, -30.)
		self.f2[self.idm][self.index].SetParameter( 4, 1.0 )
		self.f2[self.idm][self.index].SetParameter( 5, 1.0)
		
	def setDiTauFitParametersDM0DM1(self):
		self.f2[self.idm][self.index].SetParameter( 0, 4.0)
		self.f2[self.idm][self.index].SetParameter( 1, 5.0 )
		self.f2[self.idm][self.index].SetParameter( 2, 7.0 )
		self.f2[self.idm][self.index].SetParameter( 3, -30.)
		self.f2[self.idm][self.index].SetParameter( 4, 1.0 )
		self.f2[self.idm][self.index].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_tightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)		

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setDiTauFitParametersDM10_vtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_vvtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.4 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setDiTauFitParametersDM10_vlooseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.3 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_looseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 2.0 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	
	def setDiTauFitParametersDM10_mediumWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.3 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	# MuTau triggers
	def setMuTauFitParameters(self):
		self.f1[self.index].SetParameter( 0, 0.2)
		self.f1[self.index].SetParameter( 1, 5.0 )
		self.f1[self.index].SetParameter( 2, 7.0 )
		self.f1[self.index].SetParameter( 3, -30.)
		self.f1[self.index].SetParameter( 4, 1.0 )
		self.f1[self.index].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM0DM1(self):
		self.f2[self.idm][self.index].SetParameter( 0, 0.5)
		self.f2[self.idm][self.index].SetParameter( 1, 5.0 )
		self.f2[self.idm][self.index].SetParameter( 2, 7.0 )
		self.f2[self.idm][self.index].SetParameter( 3, -20.)
		self.f2[self.idm][self.index].SetParameter( 4, 1.0 )
		self.f2[self.idm][self.index].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM10_vvtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.2 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setMuTauFitParametersDM10_vtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.2 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM10_tightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.2 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setMuTauFitParametersDM10_mediumWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 5.0 )
		self.f2[self.idm][0].SetParameter( 2, 2.0 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM10_looseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -28.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setMuTauFitParametersDM10_vlooseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.4 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.3 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setMuTauFitParametersDM10_vvlooseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.2 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.2 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	
	#ETau triggers	
	def setETauFitParameters(self):
		self.f1[self.index].SetParameter( 0, 1.0)
		self.f1[self.index].SetParameter( 1, 10.0 )
		self.f1[self.index].SetParameter( 2, 1.0 )
		self.f1[self.index].SetParameter( 3, -30.)
		self.f1[self.index].SetParameter( 4, 1.0 )
		self.f1[self.index].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM0(self):
		self.f2[self.idm][0].SetParameter( 0, 1.5)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 2.0 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.8 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM1(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 5.0 )
		self.f2[self.idm][0].SetParameter( 3, -20.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.8)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 5.0 )
		self.f2[self.idm][1].SetParameter( 3, -20.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM10_vlooseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 1.5)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.5)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.2 )
		self.f2[self.idm][1].SetParameter( 3, -35.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM10_looseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 2.0 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.3 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
				
	def setETauFitParametersDM10_mediumWP(self):
		self.f2[self.idm][0].SetParameter( 0, 1.5)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.5)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM10_tightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.7)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.8 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.5)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.4 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM10_vtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.3)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.7 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.3)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.3 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)	

	def setETauFitParametersDM10_vvtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.7 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.6 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	
	def setDiTauFitParametersDM10(self):
		setDiTauFitParametersDM10 = {"vvtightTauMVA": self.setDiTauFitParametersDM10_vvtightWP(),  "vtightTauMVA": self.setDiTauFitParametersDM10_vtightWP(), "tightTauMVA": self.setDiTauFitParametersDM10_tightWP(), "mediumTauMVA": self.setDiTauFitParametersDM10_mediumWP(), "looseTauMVA": self.setDiTauFitParametersDM10_looseWP(), "vlooseTauMVA": self.setDiTauFitParametersDM10_vlooseWP()} #, "vvlooseTauMVA": eTauFitParamsDM10_vvlooseWP,}
		return setDiTauFitParametersDM10
	
	def setMuTauFitParametersDM10(self):
		setMuTauFitParametersDM10 = {"vvtightTauMVA": self.setMuTauFitParametersDM10_vvtightWP(),  "vtightTauMVA": self.setMuTauFitParametersDM10_vtightWP(), "tightTauMVA": self.setMuTauFitParametersDM10_tightWP(), "mediumTauMVA": self.setMuTauFitParametersDM10_mediumWP(), "looseTauMVA": self.setMuTauFitParametersDM10_looseWP(), "vlooseTauMVA": self.setMuTauFitParametersDM10_vlooseWP()} #, "vvlooseTauMVA": eTauFitParamsDM10_vvlooseWP,}
		return setMuTauFitParametersDM10
	
	def setETauFitParametersDM10(self):
		setETauFitParametersDM10 = {"vvtightTauMVA": self.setETauFitParametersDM10_vvtightWP(),  "vtightTauMVA": self.setETauFitParametersDM10_vtightWP(), "tightTauMVA": self.setETauFitParametersDM10_tightWP(), "mediumTauMVA": self.setETauFitParametersDM10_mediumWP(), "looseTauMVA": self.setETauFitParametersDM10_looseWP(), "vlooseTauMVA": self.setETauFitParametersDM10_vlooseWP()} #, "vvlooseTauMVA": eTauFitParamsDM10_vvlooseWP,}
		return setETauFitParametersDM10
	
	
	
		
