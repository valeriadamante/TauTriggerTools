from ROOT import *
from array import array
gROOT.SetBatch(True)
from math import sqrt
from helperfunctions import * 
from setFitParam2017 import *

filename = "../data/tauTriggerEfficiencies2017_final_etauESshift_test.root"
file = TFile.Open(filename, "r")


triggers = ["ditau", "mutau", "etau"]
types = ["DATA", "MC"]
WPs = ["vlooseTauMVA", "looseTauMVA", "mediumTauMVA", "tightTauMVA", "vtightTauMVA", "vvtightTauMVA"]
tauDMs = ["dm0", "dm1", "dm10"]

isDMspesific = True

gStyle.SetFrameLineWidth(1)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.15)
gStyle.SetPadTopMargin(0.09)
gStyle.SetPadRightMargin(0.05)

outputname = "tauTriggerFitResults_2017_test.root"
outputfile = TFile( "../data/"+outputname, 'recreate')

# efficiency calculation after filling the histograms for 3 different triggers for each WPs of DATA and MC
for ipath, trigger in enumerate(triggers):

	for WPind, wp in enumerate(WPs):
		f1 =[]
		h_errBandDM68 = [[], []]
		g_errBandDM68 = [[], []]
		for idm, DM in enumerate(tauDMs):
			h_errBandDM68.append([])
			g_errBandDM68.append([])
			for index, typ in enumerate(types):
				histoname = "histo_" + typ + "_" + wp + "_" + trigger
				h_errBandDM68[idm].append(TH1F(histoname+ "_" + DM +"_CL68","histo of 0.68 confidence band", 480, 20, 500))
				g_errBandDM68[idm].append(TGraphErrors())
		
		for index, typ in enumerate(types):
			
			f1.append(TF1( 'f1'+typ, '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*([4])' ))
			if(index ==0):
				f1[index].SetLineColor( kBlue)
			else:
				f1[index].SetLineColor( kRed)
			f1[index].SetParName( 0, "alpha" )
			f1[index].SetParName( 1, "n" )
			f1[index].SetParName( 2, "simga" )
			f1[index].SetParName( 3, "x0" )
			f1[index].SetParName( 4, "scale" )
			f1[index].SetParName( 5, "y-rise" )

			f2 = [[],[]]
                for idm, DM in enumerate(tauDMs):
                        f2.append([])
                        for index, typ in enumerate(types):
                                f2[idm].append(TF1( 'f2_'+ DM  +"_" + typ, '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3]\
)*([4])' ))
                                if(idm ==0): f2[idm][index].SetLineColor( kBlue )
                                elif(idm ==1): f2[idm][index].SetLineColor( kRed )
                                elif(idm ==2): f2[idm][index].SetLineColor( kGreen+3 )
                                if( isDMspesific):
                                        if index==0: f2[idm][0].SetLineColor( kBlue )
                                        elif index==1: f2[idm][1].SetLineColor( kRed )
                                f2[idm][index].SetParName( 0, "alpha" )
                                f2[idm][index].SetParName( 1, "n" )
                                f2[idm][index].SetParName( 2, "simga" )
                                f2[idm][index].SetParName( 3, "x0" )
                                f2[idm][index].SetParName( 4, "scale" )
                                f2[idm][index].SetParName( 5, "y-rise" )

		g_errBand68 = []
		h_errBand68 = []
		
		for index, typ in enumerate(types):
			
			gEfficiency = TGraphAsymmErrors()
			gEfficiency = file.Get(trigger +"_gEfficiency_" + wp +"_"+ typ)
					
			fitparam = setFitParam(f1, f2, index, 0)
			print "trigger", trigger
			if(trigger == "ditau"): fitparam.setDiTauFitParameters()
			if(trigger == "mutau"): fitparam.setMuTauFitParameters()
			if(trigger == "etau"): fitparam.setETauFitParameters()

			h_errBand68.append(TH1F(histoname+"_CL68","histo of 0.68 confidence band", 480, 20, 500))
			g_errBand68.append(TGraphErrors())
			
			print "Fit is performed for", trigger, "trigger in", wp ,"WP for", typ 
			print "Fit parameters:", f1[index].GetParameter(0), f1[index].GetParameter(1), f1[index].GetParameter(2), f1[index].GetParameter(3), f1[index].GetParameter(4), f1[index].GetParameter(5)    
			
			fit_result = gEfficiency.Fit('f1'+ typ, 'S')
			
			funct = functions(gEfficiency, "histo_" + trigger + "ErrorBand_" + wp +"_"+ typ, idm, index, f1, h_errBand68[index], g_errBand68[index], fit_result, 0.68)
			
			h_errBand68[index], g_errBand68[index] = funct.getConfidenceInterval() 

			# Set the title of the histograms/graphs and their axes
			gEfficiency.SetTitle(trigger +"Path_" + wp +"_"+ typ)
			gEfficiency.GetYaxis().SetTitle("Efficiency")
			gEfficiency.GetXaxis().SetTitle("Offline p_{T}^{#tau} [GeV]")

			h_errBand68[index].SetTitle(trigger +"Path_" + wp +"_"+ typ)
			h_errBand68[index].GetYaxis().SetTitle("Efficiency")
			h_errBand68[index].GetXaxis().SetTitle("Offline p_{T}^{#tau} [GeV]")
			g_errBand68[index].SetTitle(trigger +"Path_" + wp +"_"+ typ)
			g_errBand68[index].GetYaxis().SetTitle("Efficiency")
			g_errBand68[index].GetXaxis().SetTitle("Offline p_{T}^{#tau} [GeV]")
			
			# write the histograms/graphs into the output ROOT file after the fit
			gEfficiency.Write(trigger +"_gFitEfficiency_" + wp +"_"+ typ)
			h_errBand68[index].Write(trigger  + "_herrorBand_"  + wp +"_"+ typ)
			g_errBand68[index].Write(trigger + "_gerrorBand_"+ wp +"_"+ typ)
	
			#======== Relative error of the fit: "fit +/- error/ fit " ===================
			relativeErrorUP = TGraphAsymmErrors()
			relativeErrorDown = TGraphAsymmErrors()
			relativeErrorUP, relativeErrorDown = funct.createRelativeErrors()

			relativeErrorUP.Write(trigger  +"_relativeErrorUp_" + wp + "_"+ typ )
			relativeErrorDown.Write(trigger + "_relativeErrorDown_"+   wp +"_"+ typ	)
	
			# per DM efficiencies
			for idm, DM in enumerate(tauDMs):
				
				gEfficiencyDM = TGraphAsymmErrors()
				gEfficiencyDM = file.Get(trigger +"_gEfficiency_" + wp +"_"+ typ +"_"+ DM)
			
				fitparam2 = setFitParam(f1, f2, index, idm)
				print "wp", wp
				if(trigger == "ditau"): 
					if(DM =="dm0" or DM =="dm1"): 
						fitparam2.setDiTauFitParametersDM0DM1()
					elif(DM =="dm10"):
						if(wp=="tightTauMVA"): fitparam2.setDiTauFitParametersDM10_tightWP()
						elif(wp=="vtightTauMVA"): fitparam2.setDiTauFitParametersDM10_vtightWP()
						elif(wp=="vvtightTauMVA"): fitparam2.setDiTauFitParametersDM10_vvtightWP()
						elif(wp=="mediumTauMVA"): fitparam2.setDiTauFitParametersDM10_mediumWP()
						elif(wp=="looseTauMVA"): fitparam2.setDiTauFitParametersDM10_looseWP()
						elif(wp=="vlooseTauMVA"): fitparam2.setDiTauFitParametersDM10_vlooseWP()
						
				if(trigger == "mutau"): 
					if(DM =="dm0" or DM =="dm1"): 
						fitparam2.setMuTauFitParametersDM0DM1()
					elif(DM =="dm10"):
						if(wp=="tightTauMVA"): fitparam2.setMuTauFitParametersDM10_tightWP()
						elif(wp=="vtightTauMVA"): fitparam2.setMuTauFitParametersDM10_vtightWP()
						elif(wp=="vvtightTauMVA"): fitparam2.setMuTauFitParametersDM10_vvtightWP()
						elif(wp=="mediumTauMVA"): fitparam2.setMuTauFitParametersDM10_mediumWP()
						elif(wp=="looseTauMVA"): fitparam2.setMuTauFitParametersDM10_looseWP()
						elif(wp=="vlooseTauMVA"): fitparam2.setMuTauFitParametersDM10_vlooseWP()
						
				if(trigger == "etau"): 
					if(DM =="dm0"): 
						fitparam2.setETauFitParametersDM0()
					elif(DM =="dm1"): 
						fitparam2.setETauFitParametersDM1()
					elif(DM =="dm10"):
						if(wp=="tightTauMVA"): fitparam2.setETauFitParametersDM10_tightWP()
						elif(wp=="vtightTauMVA"): fitparam2.setETauFitParametersDM10_vtightWP()
						elif(wp=="vvtightTauMVA"): fitparam2.setETauFitParametersDM10_vvtightWP()
						elif(wp=="mediumTauMVA"): fitparam2.setETauFitParametersDM10_mediumWP()
						elif(wp=="looseTauMVA"): fitparam2.setETauFitParametersDM10_looseWP()
						elif(wp=="vlooseTauMVA"): fitparam2.setETauFitParametersDM10_vlooseWP()

							
				print "Fit is performed for", trigger, "trigger in", wp ,"WP for", typ , " per DM", DM
				print "Fit parameters:", f2[idm][index].GetParameter(0), f2[idm][index].GetParameter(1), f2[idm][index].GetParameter(2), f2[idm][index].GetParameter(3), f2[idm][index].GetParameter(4), f2[idm][index].GetParameter(5)    
							
				fit_result2 = gEfficiencyDM.Fit('f2_'+ DM +"_" + typ, 'S')
				functDM = functions(gEfficiencyDM, "histo_" + trigger + "_" + wp +"_"+ typ, idm, index, f2[idm] , h_errBandDM68[idm][index], g_errBandDM68[idm][index], fit_result2, 0.68)
				h_errBandDM68[idm][index], g_errBandDM68[idm][index] = functDM.getConfidenceInterval()


				gEfficiencyDM.Write(trigger +"_gFitEfficiency_"+ wp +"_" + typ +"_"+ DM)
				if(int(fit_result2) !=0): h_errBandDM68[idm][index].Fill(0)
				h_errBandDM68[idm][index].Write( trigger  + "_herrorBand_" + wp +"_" + typ +"_"+ DM)
				g_errBandDM68[idm][index].Write( trigger  + "_gerrorBand_" + wp +"_" + typ +"_"+ DM)


		# Getting Scale Factors
		SF = TGraphAsymmErrors()
		SFerror = TH1F()
		functSF = functions(gEfficiency, "histo_" + trigger + "ErrorBand_" + wp +"_"+ typ, idm, index, f1, h_errBand68, g_errBand68, fit_result, 0.68) 
			
		SFerror = functSF.getScaleFactorError()
		SF = functSF.getScaleFactor()
		SF.Write(trigger + '_ScaleFactor_' + wp)
		SFerror.Write(trigger + '_ScaleFactorUnc_' + wp)
		
		# Getting Scale Factors per decay mode
		for idm, DM in enumerate(tauDMs):
			SFdm = TGraphErrors()
			SFdmerror = TH1F()
			functDMSF = functions(gEfficiency, "histo_" + trigger + "ErrorBand_" + wp +"_"+ typ, idm, index, f2[idm], h_errBandDM68[idm], g_errBandDM68[idm], fit_result2, 0.68) 
			
			SFdmerror = functDMSF.getScaleFactorError()
			SFdm = functDMSF.getScaleFactor()
			SFdm.Write(trigger + "_ScaleFactor_" + wp + '_' + DM)
			SFdmerror.Write(trigger + '_ScaleFactorUnc_' + wp + '_' + DM)
			

outputfile.Close()
print "The output ROOT file has been created: ../data/" + outputname

