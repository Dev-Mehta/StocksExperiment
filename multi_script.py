# Import Libaries
import imp
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from os import listdir
import os
tickers = listdir(os.getcwd() + "\\data")

for ticker in tickers:
	# Read data
	# ticker = ticker.upper()
	# df = yf.Ticker(ticker + '.NS').history(period='max', interval="1wk",actions=False)
	# df.to_csv(ticker +".csv")
	path = os.getcwd() + f"\\data\\{ticker}"
	df = pd.read_csv(path)
	df.reset_index()
	df.set_index('Date')

	df['boringCandle'] = (abs(df['Open']-df['Close']) / abs(df['High']-df['Low']) < 0.5)
	df['greenExcitingCandle'] = (abs(df['Open']-df['Close'])/abs(df['High']-df['Low']) > 0.5) & (df['Open']<df['Close'])
	df['redExcitingCandle'] = (abs(df['Open']-df['Close'])/abs(df['High']-df['Low']) > 0.5) & (df['Open']>df['Close'])

	# %%
	# Make patterns out of candles
	# demand zones
	"""
	Demand zone patterns
	drop base rally - base candle 1
	rally base rally - base candle 1
	drop base rally - base candle 2
	rally base rally - base candle 2 
	"""
	df['ds_dbr_base1'] = df['redExcitingCandle'].shift(2) & df['boringCandle'].shift(1) & df['greenExcitingCandle']
	df['ds_rbr_base1'] = df['greenExcitingCandle'].shift(2) & df['boringCandle'].shift(1) & df['greenExcitingCandle']
	df['ds_dbr_base2'] = df['redExcitingCandle'].shift(3) & df['boringCandle'].shift(2) & df['boringCandle'].shift(1) & df['greenExcitingCandle']
	df['ds_rbr_base2'] = df['greenExcitingCandle'].shift(3) & df['boringCandle'].shift(2) & df['boringCandle'].shift(1) & df['greenExcitingCandle']
	df['ds_dbr_x3_base1'] = df['redExcitingCandle'].shift(4) & df['boringCandle'].shift(3) & df['greenExcitingCandle'].shift(2) & df['greenExcitingCandle'].shift(1) & df['greenExcitingCandle']

	# supply zones
	"""
	Demand zone patterns
	rally base drop - base candle 1
	drop base drop - base candle 1
	rally base drop - base candle 2
	drop base drop - base candle 2 
	"""
	df['ss_rbd_base1'] = df['greenExcitingCandle'].shift(2) & df['boringCandle'].shift(1) & df['redExcitingCandle']
	df['ss_dbd_base1'] = df['redExcitingCandle'].shift(2) & df['boringCandle'].shift(1) & df['redExcitingCandle']
	df['ss_rbd_base2'] = df['greenExcitingCandle'].shift(3) & df['boringCandle'].shift(2) & df['boringCandle'].shift(1) & df['redExcitingCandle']
	df['ss_dbd_base2'] = df['redExcitingCandle'].shift(3) & df['boringCandle'].shift(2) & df['boringCandle'].shift(1) & df['redExcitingCandle']

	# %%
	# Get base candles out of patterns - which will be later used to find proximal and distal line
	df_ds_dbr_base1 = df.iloc[df.iloc[np.where(df['ds_dbr_base1'] == True)].index - 1]
	df_ds_rbr_base1 = df.iloc[df.iloc[np.where(df['ds_rbr_base1'] == True)].index - 1]
	df_ds_dbr_x3_base1 = df.iloc[df.iloc[np.where(df['ds_dbr_x3_base1'] == True)].index - 3]
	df_ss_rbd_base1 = df.iloc[df.iloc[np.where(df['ss_rbd_base1'] == True)].index - 1]
	df_ss_dbd_base1 = df.iloc[df.iloc[np.where(df['ss_dbd_base1'] == True)].index - 1]
	df_ss_rbd_base1_cmp = df.iloc[np.where(df['ss_rbd_base1'] == True)]
	df_ss_dbd_base1_cmp = df.iloc[np.where(df['ss_dbd_base1'] == True)]
	df_ds_dbr_base1_cmp = df.iloc[np.where(df['ds_dbr_base1'] == True)]
	df_ds_rbr_base1_cmp = df.iloc[np.where(df['ds_rbr_base1'] == True)]

	df_ds_dbr_base2_boringCandle1 = df.iloc[df.iloc[np.where(df['ds_dbr_base2'] == True)].index - 2]
	df_ds_dbr_base2_boringCandle2 = df.iloc[df.iloc[np.where(df['ds_dbr_base2'] == True)].index - 1]
	df_ds_rbr_base2_boringCandle1 = df.iloc[df.iloc[np.where(df['ds_rbr_base2'] == True)].index - 2]
	df_ds_rbr_base2_boringCandle2 = df.iloc[df.iloc[np.where(df['ds_rbr_base2'] == True)].index - 1]

	df_ss_rbd_base2_boringCandle1 = df.iloc[df.iloc[np.where(df['ss_rbd_base2'] == True)].index - 2]
	df_ss_rbd_base2_boringCandle2 = df.iloc[df.iloc[np.where(df['ss_rbd_base2'] == True)].index - 1]
	df_ss_dbd_base2_boringCandle1 = df.iloc[df.iloc[np.where(df['ss_dbd_base2'] == True)].index - 2]
	df_ss_dbd_base2_boringCandle2 = df.iloc[df.iloc[np.where(df['ss_dbd_base2'] == True)].index - 1]

	df_ss_rbd_base2 = df.iloc[np.where(df['ss_rbd_base2'] == True)]
	df_ss_dbd_base2 = df.iloc[np.where(df['ss_dbd_base2'] == True)]

	# %%
	# Get color of base candle
	df_ds_dbr_base1['greenBoringCandle'] = df_ds_dbr_base1['Open'] < df_ds_dbr_base1['Close']
	df_ds_rbr_base1['greenBoringCandle'] = df_ds_rbr_base1['Open'] < df_ds_rbr_base1['Close']
	df_ds_dbr_base2_boringCandle1['greenBoringCandle'] = df_ds_dbr_base2_boringCandle1['Open'] < df_ds_dbr_base2_boringCandle1['Close']
	df_ds_dbr_base2_boringCandle2['greenBoringCandle'] = df_ds_dbr_base2_boringCandle2['Open'] < df_ds_dbr_base2_boringCandle2['Close']
	df_ds_rbr_base2_boringCandle1['greenBoringCandle'] = df_ds_rbr_base2_boringCandle1['Open'] < df_ds_rbr_base2_boringCandle1['Close']
	df_ds_rbr_base2_boringCandle2['greenBoringCandle'] = df_ds_rbr_base2_boringCandle2['Open'] < df_ds_rbr_base2_boringCandle2['Close']
	df_ds_dbr_x3_base1['greenBoringCandle'] = df_ds_dbr_x3_base1['Open'] < df_ds_dbr_x3_base1['Close']

	df_ss_rbd_base1['greenBoringCandle'] = df_ss_rbd_base1['Open'] < df_ss_rbd_base1['Close']
	df_ss_dbd_base1['greenBoringCandle'] = df_ss_dbd_base1['Open'] < df_ss_dbd_base1['Close']
	df_ss_rbd_base2_boringCandle1['greenBoringCandle'] = df_ss_rbd_base2_boringCandle1['Open'] < df_ss_rbd_base2_boringCandle1['Close']
	df_ss_rbd_base2_boringCandle2['greenBoringCandle'] = df_ss_rbd_base2_boringCandle2['Open'] < df_ss_rbd_base2_boringCandle2['Close']
	df_ss_dbd_base2_boringCandle1['greenBoringCandle'] = df_ss_dbd_base2_boringCandle1['Open'] < df_ss_dbd_base2_boringCandle1['Close']
	df_ss_dbd_base2_boringCandle2['greenBoringCandle'] = df_ss_dbd_base2_boringCandle2['Open'] < df_ss_dbd_base2_boringCandle2['Close']

	# %%
	"""
	Find Base 1 Demand Zones - Proximal Line and Distal Line
	"""
	dbrProximalLine = []
	dbrDistalLine = []
	for i in range(0,len(df_ds_dbr_x3_base1)):
		df_x = df_ds_dbr_x3_base1.iloc[i]
		if df_x['greenBoringCandle']:
			dbrProximalLine.append(df_x['Close'])
		else:
			dbrProximalLine.append(df_x['Open'])
		dbrDistalLine.append(df_x['Low'])
	df_ds_dbr_x3_base1['proximalLine'] = dbrProximalLine
	df_ds_dbr_x3_base1['distalLine'] = dbrDistalLine

	dbrProximalLine = []
	dbrDistalLine = []
	rbrProximalLine = []
	rbrDistalLine = []
	for i in range(0,len(df_ds_dbr_base1)):
		df_x = df_ds_dbr_base1.iloc[i]
		if df_x['greenBoringCandle']:
			dbrProximalLine.append(df_x['Close'])
		else:
			dbrProximalLine.append(df_x['Open'])
		dbrDistalLine.append(df_x['Low'])
	for i in range(0,len(df_ds_rbr_base1)):
		df_x = df_ds_rbr_base1.iloc[i]
		if df_x['greenBoringCandle']:
			rbrProximalLine.append(df_x['Close'])
		else:
			rbrProximalLine.append(df_x['Open'])
		rbrDistalLine.append(df_x['Low'])
	df_ds_dbr_base1['proximalLine'] = dbrProximalLine
	df_ds_dbr_base1['distalLine'] = dbrDistalLine
	df_ds_rbr_base1['proximalLine'] = rbrProximalLine
	df_ds_rbr_base1['distalLine'] = rbrDistalLine

	# %%
	"""
	Finding Base 1 Supply Zones - Proximal and Distal Line
	"""

	rbdProximalLine = []
	rbdDistalLine = []
	dbdProximalLine = []
	dbdDistalLine = []
	for i in range(0,len(df_ss_rbd_base1)):
		df_x = df_ss_rbd_base1.iloc[i]
		if not df_x['greenBoringCandle']:
			rbdProximalLine.append(df_x['Close'])
		else:
			rbdProximalLine.append(df_x['Open'])
		rbdDistalLine.append(df_x['High'])
	for i in range(0,len(df_ss_dbd_base1)):
		df_x = df_ss_dbd_base1.iloc[i]
		if not df_x['greenBoringCandle']:
			dbdProximalLine.append(df_x['Close'])
		else:
			dbdProximalLine.append(df_x['Open'])
		dbdDistalLine.append(df_x['High'])
	df_ss_rbd_base1['proximalLine'] = rbdProximalLine
	df_ss_rbd_base1['distalLine'] = rbdDistalLine
	df_ss_dbd_base1['proximalLine'] = dbdProximalLine
	df_ss_dbd_base1['distalLine'] = dbdDistalLine

	# %%
	"""
	Finding Base 2 Demand Zones - Proximal Line and Distal Line
	"""
	dbrProximalLine2 = []
	dbrDistalLine2 = []
	rbrProximalLine2 = []
	rbrDistalLine2 = []
	for i in range(0,len(df_ds_dbr_base2_boringCandle1)):
		df_x_1 = df_ds_dbr_base2_boringCandle1.iloc[i]
		df_x_2 = df_ds_dbr_base2_boringCandle2.iloc[i]
		if df_x_1['greenBoringCandle'] and df_x_2['greenBoringCandle']:
			if df_x_1['Close'] > df_x_2['Close']:
				dbrProximalLine2.append(df_x_1['Close'])
			else:
				dbrProximalLine2.append(df_x_2['Close'])
		elif df_x_1['greenBoringCandle'] and (not df_x_2['greenBoringCandle']):
			if df_x_1['Close'] > df_x_2['Open']:
				dbrProximalLine2.append(df_x_1['Close'])
			else:
				dbrProximalLine2.append(df_x_2['Open'])
		elif (df_x_1['greenBoringCandle'] == False) and df_x_2['greenBoringCandle']:
			if df_x_1['Open'] > df_x_2['Close']:
				dbrProximalLine2.append(df_x_1['Open'])
			else:
				dbrProximalLine2.append(df_x_2['Close'])
		else:
			if df_x_1['Open'] > df_x_2['Open']:
				dbrProximalLine2.append(df_x_1['Open'])
			else:
				dbrProximalLine2.append(df_x_2['Open'])
		if int(df_x_1['Low']) < int(df_x_2['Low']):
			dbrDistalLine2.append(int(df_x_1['Low']))
		else:
			dbrDistalLine2.append(int(df_x_2['Low']))
	for i in range(0,len(df_ds_rbr_base2_boringCandle1)):
		df_x_1 = df_ds_rbr_base2_boringCandle1.iloc[i]
		df_x_2 = df_ds_rbr_base2_boringCandle2.iloc[i]
		if df_x_1['greenBoringCandle'] and df_x_2['greenBoringCandle']:
			if df_x_1['Close'] > df_x_2['Close']:
				rbrProximalLine2.append(df_x_1['Close'])
			else:
				rbrProximalLine2.append(df_x_2['Close'])
		elif df_x_1['greenBoringCandle'] and (not df_x_2['greenBoringCandle']):
			if df_x_1['Close'] > df_x_2['Open']:
				rbrProximalLine2.append(df_x_1['Close'])
			else:
				rbrProximalLine2.append(df_x_2['Open'])
		elif (df_x_1['greenBoringCandle'] == False) and df_x_2['greenBoringCandle']:
			if df_x_1['Open'] > df_x_2['Close']:
				rbrProximalLine2.append(df_x_1['Open'])
			else:
				rbrProximalLine2.append(df_x_2['Close'])
		else:
			if df_x_1['Open'] > df_x_2['Open']:
				rbrProximalLine2.append(df_x_1['Open'])
			else:
				rbrProximalLine2.append(df_x_2['Open'])
		if int(df_x_1['Low']) < int(df_x_2['Low']):
			rbrDistalLine2.append(int(df_x_1['Low']))
		else:
			rbrDistalLine2.append(int(df_x_2['Low']))
	df_ds_dbr_base2_boringCandle1['proximalLine'] = dbrProximalLine2
	df_ds_dbr_base2_boringCandle1['distalLine'] = dbrDistalLine2
	df_ds_rbr_base2_boringCandle1['proximalLine'] = rbrProximalLine2
	df_ds_rbr_base2_boringCandle1['distalLine'] = rbrDistalLine2

	# %%
	"""
	Finding Base 2 Supply Zones - Proximal and Distal Line
	"""
	rbdProximalLine2 = []
	rbdDistalLine2 = []
	dbdProximalLine2 = []
	dbdDistalLine2 = []
	for i in range(0,len(df_ss_rbd_base2_boringCandle1)):
		df_x_1 = df_ss_rbd_base2_boringCandle1.iloc[i]
		df_x_2 = df_ss_rbd_base2_boringCandle2.iloc[i]
		if (not df_x_1['greenBoringCandle']) and (not df_x_2['greenBoringCandle']):
			if df_x_1['Close'] < df_x_2['Close']:
				rbdProximalLine2.append(df_x_1['Close'])
			else:
				rbdProximalLine2.append(df_x_2['Close'])
		elif (not df_x_1['greenBoringCandle']) and (df_x_2['greenBoringCandle']):
			if df_x_1['Close'] < df_x_2['Open']:
				rbdProximalLine2.append(df_x_1['Close'])
			else:
				rbdProximalLine2.append(df_x_2['Open'])
		elif (df_x_1['greenBoringCandle']) and (not df_x_2['greenBoringCandle']):
			if df_x_1['Open'] < df_x_2['Close']:
				rbdProximalLine2.append(df_x_1['Open'])
			else:
				rbdProximalLine2.append(df_x_2['Close'])
		else:
			if df_x_1['Open'] < df_x_2['Open']:
				rbdProximalLine2.append(df_x_1['Open'])
			else:
				rbdProximalLine2.append(df_x_2['Open'])
		if int(df_x_1['High']) > int(df_x_2['High']):
			rbdDistalLine2.append(int(df_x_1['High']))
		else:
			rbdDistalLine2.append(int(df_x_2['High']))

	for i in range(0,len(df_ss_dbd_base2_boringCandle1)):
		df_x_1 = df_ss_dbd_base2_boringCandle1.iloc[i]
		df_x_2 = df_ss_dbd_base2_boringCandle2.iloc[i]
		if (not df_x_1['greenBoringCandle']) and (not df_x_2['greenBoringCandle']):
			if df_x_1['Close'] < df_x_2['Close']:
				dbdProximalLine2.append(df_x_1['Close'])
			else:
				dbdProximalLine2.append(df_x_2['Close'])
		elif (not df_x_1['greenBoringCandle']) and (df_x_2['greenBoringCandle']):
			if df_x_1['Close'] < df_x_2['Open']:
				dbdProximalLine2.append(df_x_1['Close'])
			else:
				dbdProximalLine2.append(df_x_2['Open'])
		elif (df_x_1['greenBoringCandle']) and (not df_x_2['greenBoringCandle']):
			if df_x_1['Open'] < df_x_2['Close']:
				dbdProximalLine2.append(df_x_1['Open'])
			else:
				dbdProximalLine2.append(df_x_2['Close'])
		else:
			if df_x_1['Open'] < df_x_2['Open']:
				dbdProximalLine2.append(df_x_1['Open'])
			else:
				dbdProximalLine2.append(df_x_2['Open'])
		if int(df_x_1['High']) > int(df_x_2['High']):
			dbdDistalLine2.append(int(df_x_1['High']))
		else:
			dbdDistalLine2.append(int(df_x_2['High']))
	df_ss_rbd_base2_boringCandle1['proximalLine'] = rbdProximalLine2
	df_ss_rbd_base2_boringCandle1['distalLine'] = rbdDistalLine2
	df_ss_dbd_base2_boringCandle1['proximalLine'] = dbdProximalLine2
	df_ss_dbd_base2_boringCandle1['distalLine'] = dbdDistalLine2

	# %%
	"""Removing Tested Demand Zones"""
	df_ds_dbr_base1_list = df_ds_dbr_base1.values.tolist()
	df_ds_dbr_x3_base1_list = df_ds_dbr_x3_base1.values.tolist()
	df_ds_rbr_base1_cmp_list = df_ds_rbr_base1_cmp.values.tolist()[::-1]
	df_ds_dbr_base1_cmp_list = df_ds_dbr_base1_cmp.values.tolist()[::-1]
	df_ds_rbr_base1_list = df_ds_rbr_base1.values.tolist()
	df_ds_dbr_base2_boringCandle1_list = df_ds_dbr_base2_boringCandle1.values.tolist()
	df_ds_rbr_base2_boringCandle1_list = df_ds_rbr_base2_boringCandle1.values.tolist()
	df_ds_dbr_base1_list = df_ds_dbr_base1_list[::-1]
	df_ds_rbr_base1_list = df_ds_rbr_base1_list[::-1]
	df_ds_dbr_x3_base1_list = df_ds_dbr_x3_base1_list[::-1]
	df_ds_dbr_base2_boringCandle1_list = df_ds_dbr_base2_boringCandle1_list[::-1]
	df_ds_rbr_base2_boringCandle1_list = df_ds_rbr_base2_boringCandle1_list[::-1]
	zoneTested = []
	df.Date = pd.to_datetime(df.Date)
	linesToDrawStrong = []
	for dz in df_ds_dbr_x3_base1_list:
		proximalLine = dz[19]
		distalLine = dz[20]
		index = dz[0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.Low <= proximalLine)) == 0:
			linesToDrawStrong.append([index,proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ds_dbr_x3_base1['zoneTested'] = zoneTested
	zoneTested= []
	linesToDraw = []
	for i in range(0, len(df_ds_dbr_base1_list)):
		dz = df_ds_dbr_base1_list[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ds_dbr_base1_cmp_list[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.Low <= proximalLine)) == 0:
			linesToDraw.append([index,proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ds_dbr_base1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ds_rbr_base1_list)):
		dz = df_ds_rbr_base1_list[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ds_rbr_base1_cmp_list[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.Low <= proximalLine)[0]) == 0:
			linesToDraw.append([index,proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ds_rbr_base1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ds_dbr_base2_boringCandle1_list)):
		dz = df_ds_dbr_base2_boringCandle1.iloc[i]
		dz2 = df_ds_dbr_base2_boringCandle2.iloc[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = dz2[0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.Low <= proximalLine)[0]) == 0:
			linesToDraw.append([index,proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ds_dbr_base2_boringCandle1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ds_rbr_base2_boringCandle1_list)):
		dz = df_ds_rbr_base2_boringCandle1.iloc[i]
		dz2 = df_ds_rbr_base2_boringCandle2.iloc[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = dz2[0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.Low <= proximalLine)[0]) == 0:
			linesToDraw.append([index,proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ds_rbr_base2_boringCandle1['zoneTested'] = zoneTested

	# %%
	"""Removing Tested Supply Zones"""
	df_ss_rbd_base1_list = df_ss_rbd_base1.values.tolist()
	df_ss_dbd_base1_list = df_ss_dbd_base1.values.tolist()
	df_ss_rbd_base1_list_cmp = df_ss_rbd_base1_cmp.values.tolist()
	df_ss_dbd_base1_list_cmp = df_ss_dbd_base1_cmp.values.tolist()
	df_ss_rbd_base2_boringCandle1_list = df_ss_rbd_base2_boringCandle1.values.tolist()
	df_ss_dbd_base2_boringCandle1_list = df_ss_dbd_base2_boringCandle1.values.tolist()
	df_ss_rbd_base1_list = df_ss_rbd_base1_list[::-1]
	df_ss_dbd_base1_list = df_ss_dbd_base1_list[::-1]
	df_ss_rbd_base1_list_cmp = df_ss_rbd_base1_list_cmp[::-1]
	df_ss_dbd_base1_list_cmp = df_ss_dbd_base1_list_cmp[::-1]
	df_ss_rbd_base2_boringCandle1_list = df_ss_rbd_base2_boringCandle1_list[::-1]
	df_ss_dbd_base2_boringCandle1_list = df_ss_dbd_base2_boringCandle1_list[::-1]
	zoneTested = []
	df.Date = pd.to_datetime(df.Date)
	linesToDrawSZ = []
	for i in range(0,len(df_ss_rbd_base1_list)):
		dz = df_ss_rbd_base1_list[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ss_rbd_base1_list_cmp[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.High >= proximalLine)[0]) == 0:
			print("Zone found")
			linesToDrawSZ.append([dz[0],proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ss_rbd_base1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ss_dbd_base1_list)):
		dz = df_ss_dbd_base1_list[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ss_dbd_base1_list_cmp[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.High >= proximalLine)[0]) == 0:
			linesToDrawSZ.append([dz[0],proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ss_dbd_base1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ss_rbd_base2_boringCandle1_list)):
		dz = df_ss_rbd_base2_boringCandle1.iloc[i]
		dz2 = df_ss_rbd_base2_boringCandle2.iloc[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ss_rbd_base2.iloc[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.High >= proximalLine)[0]) == 0:
			linesToDrawSZ.append([dz2[0],proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ss_rbd_base2_boringCandle1['zoneTested'] = zoneTested
	zoneTested = []	
	for i in range(0,len(df_ss_dbd_base2_boringCandle1_list)):
		dz = df_ss_dbd_base2_boringCandle1.iloc[i]
		dz2 = df_ss_dbd_base2_boringCandle2.iloc[i]
		proximalLine = dz[19]
		distalLine = dz[20]
		index = df_ss_dbd_base2.iloc[i][0]
		index = pd.to_datetime(index)
		dz_sub = df.loc[df.Date > index]
		if len(np.where(dz_sub.High >= proximalLine)[0]) == 0:
			linesToDrawSZ.append([dz2[0],proximalLine, distalLine])
			zoneTested.append(False)
		else:
			zoneTested.append(True)
	df_ss_dbd_base2_boringCandle1['zoneTested'] = zoneTested

	# %%
	"""
	Plotting Figure
	"""
	df_dz = pd.DataFrame(linesToDraw)
	df_dz.rename(columns={0:"Date", 1:"proximalLine", 2:"distalLine"}, inplace=True)
	df_dz = df_dz.set_index('Date').sort_index()
	proximalLineLatest = df_dz.tail(1).proximalLine.values[0]
	distalLineLatest = df_dz.tail(1).distalLine.values[0]
	date = df_dz.tail(1).index.values[0]
	proximalLineLatest, distalLineLatest
	entry = round(proximalLineLatest) + 1 
	sl = round(distalLineLatest) - 1
	target = entry + ((entry - sl) * 3)
	linesToDraw.pop()
	fig = go.Figure(data=go.Candlestick(x=df['Date'], open=df['Open'], close=df['Close'], low=df['Low'], high=df['High']))
	for row in linesToDrawSZ:
		fig.add_shape(type="rect",line=dict(color="red", width=2),x0=df.Date.min(), y0=row[2], x1=df.Date.max(), y1=row[1], fillcolor='red', opacity=0.5)
	for row in linesToDraw:
		fig.add_shape(type="rect",line=dict(color="green", width=2),x0=row[0], y0=row[1], x1=df.Date.max(), y1=row[2], fillcolor='green', opacity=0.3)
	for row in linesToDrawStrong:
		fig.add_shape(type="rect",line=dict(color="orange", width=2),x0=row[0], y0=row[1], x1=df.Date.max(), y1=row[2], fillcolor='orange', opacity=0.6)
	fig.update_layout(margin={"t":25, "b":0, "l":0, "r":2})
	fig.add_shape(type="rect",line=dict(color="red", width=2),x0=pd.to_datetime(date).date(), y0=entry, x1=df.Date.max(), y1=sl, fillcolor='red', opacity=0.3)
	fig.add_shape(type="rect",line=dict(color="green", width=2),x0=pd.to_datetime(date).date(), y0=entry+2, x1=df.Date.max(), y1=target, fillcolor='green', opacity=0.3)
	fig.write_html(f"output/{ticker}.html")
	print(f"Done for {ticker}")