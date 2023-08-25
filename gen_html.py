#!/usr/bin/env python3
# pip3 install yfinance

import os
import sys
import json
import time
from pytz import timezone
from datetime import datetime
import yfinance as yf

def bailmsg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	exit(1)

def write_to_file(text, filename):
	with open(filename, 'w') as f: f.write(text)

def gen_html_table(tbl):
	table_name,symbols = tbl.split('=')
	symb_list = symbols.split(',')

	html = '<table>'

	html += '<tr>'
	html += f'<th><u>{table_name}</u></th>'
	for symb in symb_list:
		html += f'<th id={symb}_th><a href=https://finance.yahoo.com/quote/{symb}>{symb}</a></th>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>$</td>'
	for symb in symb_list:
		html += f'<td id={symb}_currentPrice></td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>%</td>'
	for symb in symb_list:
		html += f'<td id={symb}_move></td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>Close</td>'
	for symb in symb_list:
		html += f'<td id={symb}_previousClose></td>'
	html += '</tr>'

	mc_toggle = os.getenv('DISPLAY_MARKET_CAP')
	if (mc_toggle is not None) and (mc_toggle == '1'):
		html += '<tr>'
		html += '<td>MCap</td>'
		for symb in symb_list:
			html += f'<td id={symb}_cap></td>'
		html += '</tr>'

	fpe_toggle = os.getenv('DISPLAY_FPE_RATIO')
	if (fpe_toggle is not None) and (fpe_toggle == '1'):
		html += '<tr>'
		html += '<td>FPE</td>'
		for symb in symb_list:
			html += f'<td id={symb}_forwardPE></td>'
		html += '</tr>'

	pst12_toggle = os.getenv('DISPLAY_PST12_RATIO')
	if (pst12_toggle is not None) and (pst12_toggle == '1'):
		html += '<tr>'
		html += '<td>PST12</td>'
		for symb in symb_list:
			html += f'<td id={symb}_priceToSalesTrailing12Months></td>'
		html += '</tr>'

	html += '</table>'
	html += '</br>'
	return html

def gen_html_head(json_update_interval):
	html = '<head>'
	html += '<title>Stonk Stalker</title>'
	if os.getenv('DARKMODE'):
		html += '<link rel="stylesheet" href="static/dashboard-dark.css">'
	else:
		html += '<link rel="stylesheet" href="static/dashboard.css">'
	html += '<script src="static/jquery-3.7.0.min.js"></script>'
	html += '<script src="static/symbols.js"></script>'
	html += '<script>$(document).ready(function(){ time_init(); });</script>'
	html += '<script>$(document).ready(function(){ symbol_init(' + json_update_interval + '); });</script>'
	html += '</head>'
	return html

def gen_html_body():
	html = '<body>'
	html += '<center>'
	html += '<h2>Stonk Stalker</h2>'
	html += '<h3><div id="time"></div></h3>'
	for tbl in tables_list:
		html += gen_html_table(tbl)
	html += '<a href="https://github.com/Fullaxx/stonk_stalker">Source Code on GitHub</a>'
	html += '</center>'
	html += '</body>'
	return html

def gen_index_html(tables_list, json_update_interval):
	html = '<!DOCTYPE html>'
	html += '<html lang="en">'
	html += gen_html_head(json_update_interval)
	html += gen_html_body()
	html += '</html>'
	write_to_file(html, 'index.html')

def delete_if_exists(stock_d, key):
	if key in stock_d:
		del stock_d[key]

def load_market_data(symb_list, marketdb):
	for symb in symb_list:
		symb_data = {}
		res = yf.Ticker(symb)
		delete_if_exists(res.info, 'companyOfficers')
		delete_if_exists(res.info, 'longBusinessSummary')
		marketdb[symb] = res.info
		market_str = json.dumps(marketdb)
		filename = f'market.json'
		print(f'Writing {filename} ...')
		write_to_file(market_str, filename)

# This function is pretty generic and could use some better logic to determine an active trading session
def trading_is_active():
	active = False
	tz = timezone('US/Eastern')
	now = datetime.now(tz)
	day = now.strftime("%a")
	hour = int(now.strftime("%H"))
	if (day == 'Sun'): return False
	if (day == 'Sat'): return False
	if ((hour >= 9) and (hour <= 16)):
		active = True
	return active

if __name__ == '__main__':
	wwwdir = os.getenv('WWWDIR')
	if wwwdir is not None: os.chdir(wwwdir)

	ticker_tables = os.getenv('TICKER_TABLES')
	if ticker_tables is None: bailmsg('Set TICKER_TABLES')

	json_update_interval = os.getenv('JSON_UPDATE')
	if json_update_interval is None: json_update_interval = '1000'

	symb_list = []
	tables_list = ticker_tables.split(';')
	for tbl in tables_list:
		symbols = tbl.split('=')[1]
		symb_list += symbols.split(',')

	marketdb = {}
	gen_index_html(tables_list, json_update_interval)
	while True:
		load_market_data(symb_list, marketdb)
		sleep_time = 1 if trading_is_active() else 30
		time.sleep(sleep_time)
