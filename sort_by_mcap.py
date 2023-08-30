#!/usr/bin/env python3
# pip3 install yfinance

import os
import sys
import yfinance as yf

def bailmsg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	exit(1)

def sort_list(symb_list):
	mcap_list = []
	mcap_dict = {}
	for symb in symb_list:
		print(f'Gathering financials for {symb} ...')
		res = yf.Ticker(symb)
		if 'marketCap' not  in res.info:
			print(f'{symb} has no marketCap object')
			exit(0)
		mcap = res.info['marketCap']
		mcap_list.append(mcap)
		mcap_dict[str(mcap)] = symb
	mcap_list.sort(reverse=True)
#	print(mcap_list)
	print("Sorted by marketCap:")
	for m in mcap_list:
		symb = mcap_dict[str(m)]
#		print(f'{symb}: {m}')
		print(f'{symb}', end=',')

if __name__ == '__main__':
	symbols_env = os.getenv('SYMBOLS')
	if symbols_env is None: bailmsg('Set SYMBOLS')

	symb_list = symbols_env.split(',')
	sort_list(symb_list)
