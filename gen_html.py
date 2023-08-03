#!/usr/bin/env python3
# pip3 install yfinance

import os
import sys
import json
import time
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
		html += f'<td id={symb}_price></td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>%</td>'
	for symb in symb_list:
		html += f'<td id={symb}_move></td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>Close</td>'
	for symb in symb_list:
		html += f'<td id={symb}_close></td>'
	html += '</tr>'

	mc_toggle = os.getenv('DISPLAY_MARKET_CAP')
	if (mc_toggle is not None) and (mc_toggle == '1'):
		html += '<tr>'
		html += '<td>MCap</td>'
		for symb in symb_list:
			html += f'<td id={symb}_cap></td>'
		html += '</tr>'

	html += '</table>'
	html += '</br>'
	return html

def gen_html_head(symb_list):
	html = '<head>'
	if os.getenv('DARKMODE'):
		html += '<link rel="stylesheet" href="static/dashboard-dark.css">'
	else:
		html += '<link rel="stylesheet" href="static/dashboard.css">'
	html += '<script src="static/jquery-3.7.0.min.js"></script>'
	html += '<script src="static/symbols.js"></script>'
	html += '<script>$(document).ready(function(){ time_init(); });</script>'
	html += '<script>$(document).ready(function(){ symbol_init(' + str(symb_list) +'); });</script>'
	html += '</head>'
	return html

def gen_html_body():
	html = '<body>'
	html += '<center>'
	html += '<h2><a href="https://github.com/Fullaxx/stonk_stalker">Stonk Stalker</a></h2>'
	html += '<h3><p id="time"></p></h3>'
	for tbl in tables_list:
		html += gen_html_table(tbl)
	html += '</center>'
	html += '</body>'
	return html

def gen_html(symb_list, tables_list):
	html = '<!DOCTYPE html>'
	html += '<html lang="en">'
	html += gen_html_head(symb_list)
	html += gen_html_body()
	html += '</html>'
	write_to_file(html, 'index.html')

def load_prices(symb_list, tables_list):
	for symb in symb_list:
		res = yf.Ticker(symb)
		info_str = json.dumps(res.info)
		filename = f'symbols/{symb}.json'
		print(f'Writing {filename} ...')
		write_to_file(info_str, filename)

if __name__ == '__main__':
	symb_list = []
	wwwdir = os.getenv('WWWDIR')
	if wwwdir is not None: os.chdir(wwwdir)
	os.makedirs('symbols', mode = 0o755, exist_ok = True)
	ticker_tables = os.getenv('TICKER_TABLES')
	if ticker_tables is None: bailmsg('Set TICKER_TABLES')

	tables_list = ticker_tables.split(';')
	for tbl in tables_list:
		symbols = tbl.split('=')[1]
		symb_list += symbols.split(',')

	gen_html(symb_list, tables_list)
	while True:
		load_prices(symb_list, tables_list)
		time.sleep(1)
