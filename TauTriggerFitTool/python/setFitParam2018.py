
class setFitParam2018:

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
		
	def setDiTauFitParametersDM0_looser(self):
		self.f2[self.idm][0].SetParameter( 0, 4.0) 
		self.f2[self.idm][0].SetParameter( 1, 10.0)
		self.f2[self.idm][0].SetParameter( 2, 5.0)
		self.f2[self.idm][0].SetParameter( 3, -30.) 
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.5) 
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 7.0 ) 
		self.f2[self.idm][1].SetParameter( 3, -35.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	
	def setDiTauFitParametersDM0_tighter(self):
		self.f2[self.idm][0].SetParameter( 0, 4.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 5.0 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 2.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 5.0 )
		self.f2[self.idm][1].SetParameter( 3, -29.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM1_looser(self):
		self.f2[self.idm][0].SetParameter( 0, 4.0)
		self.f2[self.idm][0].SetParameter( 1, 5.0 )
		self.f2[self.idm][0].SetParameter( 2, 7.0 )
		self.f2[self.idm][0].SetParameter( 3, -35.)
		self.f2[self.idm][0].SetParameter( 4, 1.0)
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
                self.f2[self.idm][1].SetParameter( 0, 5.0) 
                self.f2[self.idm][1].SetParameter( 1, 10.0)
                self.f2[self.idm][1].SetParameter( 2, 7.0 )
                self.f2[self.idm][1].SetParameter( 3, -34.)
                self.f2[self.idm][1].SetParameter( 4, 1.0)
                self.f2[self.idm][1].SetParameter( 5, 1.0)

        def setDiTauFitParametersDM1_tighter(self):
                self.f2[self.idm][self.index].SetParameter( 0, 4.0)
                self.f2[self.idm][self.index].SetParameter( 1, 5.0 )
                self.f2[self.idm][self.index].SetParameter( 2, 7.0 )
                self.f2[self.idm][self.index].SetParameter( 3, -35.)
                self.f2[self.idm][self.index].SetParameter( 4, 1.0)
                self.f2[self.idm][self.index].SetParameter( 5, 1.0)


	def setDiTauFitParametersDM10_tightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)		

		self.f2[self.idm][1].SetParameter( 0, 0.5) 
		self.f2[self.idm][1].SetParameter( 1, 10.0) 
		self.f2[self.idm][1].SetParameter( 2, 0.5 ) 
		self.f2[self.idm][1].SetParameter( 3, -34.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setDiTauFitParametersDM10_vtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.3 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.2) 
		self.f2[self.idm][1].SetParameter( 1, 10.0) 
		self.f2[self.idm][1].SetParameter( 2, 2.6 ) 
		self.f2[self.idm][1].SetParameter( 3, -27.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_vvtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 2.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.5 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.2) 
		self.f2[self.idm][1].SetParameter( 1, 10.0)
 		self.f2[self.idm][1].SetParameter( 2, 2.6 )
		self.f2[self.idm][1].SetParameter( 3, -27.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_vlooseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.7) 
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 0.5 ) 
		self.f2[self.idm][1].SetParameter( 3, -34.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setDiTauFitParametersDM10_looseWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.7) 
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 0.5)
		self.f2[self.idm][1].SetParameter( 3, -31.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	
	def setDiTauFitParametersDM10_mediumWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 0.5) 
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -31.)
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
		
	def setMuTauFitParametersDM0_loose(self):
		self.f2[self.idm][0].SetParameter( 0, 1.2)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 4.1 )
		self.f2[self.idm][0].SetParameter( 3, -18.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.5)  
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 1.5 ) 
		self.f2[self.idm][1].SetParameter( 3, -21.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
	
	def setMuTauFitParametersDM0_vloose(self):
		self.f2[self.idm][0].SetParameter( 0, 1.2)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 4.1 )
		self.f2[self.idm][0].SetParameter( 3, -18.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.4)  
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 1.2 ) 
		self.f2[self.idm][1].SetParameter( 3, -21.) 
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM0_tighter(self):
		self.f2[self.idm][0].SetParameter( 0, 1.2)
		self.f2[self.idm][0].SetParameter( 1, 10.0)
		self.f2[self.idm][0].SetParameter( 2, 4.1 )
		self.f2[self.idm][0].SetParameter( 3, -18.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.2)
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 7.5 )
		self.f2[self.idm][1].SetParameter( 3, -30.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
			
	def setMuTauFitParametersDM1_looser(self):
		self.f2[self.idm][0].SetParameter( 0, 1.2) 
		self.f2[self.idm][0].SetParameter( 1, 10.0) 
		self.f2[self.idm][0].SetParameter( 2, 1.0 ) 
		self.f2[self.idm][0].SetParameter( 3, -33.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.2)
		self.f2[self.idm][1].SetParameter( 1, 10.0)
		self.f2[self.idm][1].SetParameter( 2, 4.1 )
		self.f2[self.idm][1].SetParameter( 3, -18.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setMuTauFitParametersDM1_tighter(self):
		self.f2[self.idm][0].SetParameter( 0, 2.5) 
		self.f2[self.idm][0].SetParameter( 1, 10.0 ) 
		self.f2[self.idm][0].SetParameter( 2, 0.6 )
		self.f2[self.idm][0].SetParameter( 3, -30.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.2)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 4.1 )
		self.f2[self.idm][1].SetParameter( 3, -18.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)

	def setMuTauFitParametersDM10_tighter(self):
		self.f2[self.idm][self.index].SetParameter( 0, 5.2)
		self.f2[self.idm][self.index].SetParameter( 1, 10.0 )
		self.f2[self.idm][self.index].SetParameter( 2, 7.5 )
		self.f2[self.idm][self.index].SetParameter( 3, -35.)
		self.f2[self.idm][self.index].SetParameter( 4, 1.0 )
		self.f2[self.idm][self.index].SetParameter( 5, 1.0)

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
		
	def setETauFitParametersDM0_looser(self):
		self.f2[self.idm][0].SetParameter( 0, 0.5)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 7.0 )
		self.f2[self.idm][0].SetParameter( 3, -35.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.2)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 4.0 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM0_tighter(self):
		self.f2[self.idm][0].SetParameter( 0, 0.5)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 5.3 )
		self.f2[self.idm][0].SetParameter( 3, -33.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)
		
		self.f2[self.idm][1].SetParameter( 0, 1.2)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 4.0 )
		self.f2[self.idm][1].SetParameter( 3, -25.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
			
	def setETauFitParametersDM1(self):
		self.f2[self.idm][0].SetParameter( 0, 0.8)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 5.0 )
		self.f2[self.idm][0].SetParameter( 3, -20.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 2.0 )
		self.f2[self.idm][1].SetParameter( 3, -34.)
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

		self.f2[self.idm][1].SetParameter( 0, 0.3)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 0.5 )
		self.f2[self.idm][1].SetParameter( 3, -35.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
	def setETauFitParametersDM10_vtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 0.3)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 0.7 )
		self.f2[self.idm][0].SetParameter( 3, -25.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 3.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 2.0 )
		self.f2[self.idm][1].SetParameter( 3, -34.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)	

	def setETauFitParametersDM10_vvtightWP(self):
		self.f2[self.idm][0].SetParameter( 0, 1.0)
		self.f2[self.idm][0].SetParameter( 1, 10.0 )
		self.f2[self.idm][0].SetParameter( 2, 1.0 )
		self.f2[self.idm][0].SetParameter( 3, -34.)
		self.f2[self.idm][0].SetParameter( 4, 1.0 )
		self.f2[self.idm][0].SetParameter( 5, 1.0)

		self.f2[self.idm][1].SetParameter( 0, 1.0)
		self.f2[self.idm][1].SetParameter( 1, 10.0 )
		self.f2[self.idm][1].SetParameter( 2, 1.0)
		self.f2[self.idm][1].SetParameter( 3, -34.)
		self.f2[self.idm][1].SetParameter( 4, 1.0 )
		self.f2[self.idm][1].SetParameter( 5, 1.0)
		
