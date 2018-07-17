"""Global Controller Algorithms
	v0.1 - July 2018
	Thomas Navidi

	This module contains the algorithms for the global cloud controller
"""

import numpy as np

class Global_Controller(object):
	"""
	main controller object
	"""

	def __init__(self, network, forecaster, GCtime, lookAheadTime, GCscens, sellFactor, V_weight, Vtol, ramp_weight):
		#network and forecaster are objects from the corresponding files
		# Set parameters
		"""
		sellFactor = 1 # 0 means selling is not profitable
		V_weight = 10000 # tuning parameter for voltage penalties
		Vtol = .005 # tolerance bound on voltage penalties
		GCtime = 24 # run period of algorithm
		lookAheadTime = 24
		GCscens = 1 #Try just 1 scenario
		ramp_weight = 10000 # make large to prioritize ramp following
		"""

		self.network=network, self.forecaster=forecaster
		self.GCtime=GCtime, self.lookAheadTime=lookAheadTime, self.GCscens=GCscens
		self.sellFactor=sellFactor, self.V_weight=V_weight, self.Vtol=Vtol, self.ramp_weight=ramp_weight

		self.t_idx = 0


	def runStep(self, t_idx=np.nan):

		# get variables from self for readability
		if np.isnan(t_idx):
			t_idx = self.t_idx
		GCtime = self.GCtime
		lookAheadTime = self.lookAheadTime
		nodesStorage = self.network.battnodes
		GCscens = self.GCscens

		#Get forecasts and scenarios
		pForecast = self.forecaster.netPredict(self.network.netDemandFull, t_idx, GCtime + lookAheadTime)
		rForecast = self.forecaster.rPredict(self.network.rDemandFull, t_idx, GCtime + lookAheadTime)
		if GCscens > 1:
			sScenarios = self.forecaster.scenarioGen(nodesStorage, pForecast[nodesStorage,:], pMeans, pCovs, GCscens)
		else:
			

		#Get data from network
		netDemand, rDemand, pricesCurrent = self.network.returnData(t_idx, GCtime + lookAheadTime)

		storageNum = len(nodesStorage)
