#!/usr/bin/env python3
# pip3 install yfinance

import os
import sys
import time
from pytz import timezone
from datetime import datetime
import yfinance as yf

def bailmsg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
	exit(1)

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

def write_html_to_file(html, filename):
	with open(filename, 'w') as f: f.write(html)

def write_loading_to_file(filename):
	tz = timezone('US/Eastern')
	now = datetime.now(tz)
	now_str = now.strftime("%c")
	html = '<html>'
	html += '<head>'
	html += '<meta http-equiv=refresh content=1; URL=/>'
	html += '</head>'
	html += '<body>'
	html += '<center>'
	html += '<h2>Loading Ticker Data ...</h2>'
	html += '<h3>' + now_str + ' US/Eastern</h3>'
	html += '</center>'
	html += '</body>'
	html += '</html>'
	write_html_to_file(html, filename)

def gen_html_table(cp, mp, tm, mcap, tbl):
	table_name,symbols = tbl.split('=')
	symb_list = symbols.split(',')

	html = '<table>'

	html += '<tr>'
	html += f'<th><u>{table_name}</u></th>'
	for symb in symb_list:
		thclass = ''
		if(tm[symb] > 0): thclass=' class=up'
		if(tm[symb] < 0): thclass=' class=down'
		html += f'<th{thclass}><a href=https://finance.yahoo.com/quote/{symb}>{symb}</a></th>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>$</td>'
	for symb in symb_list:
		html += f'<td>{mp[symb]}</td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>%</td>'
	for symb in symb_list:
		tdclass = None
		move_formatted = "{:0.2f}".format(tm[symb])
		move_str = '+' + str(move_formatted) if tm[symb] > 0 else str(move_formatted)
		if(tm[symb] >= 8): tdclass='pos_eight'
		elif(tm[symb] >= 7): tdclass='pos_seven'
		elif(tm[symb] >= 6): tdclass='pos_six'
		elif(tm[symb] >= 5): tdclass='pos_five'
		elif(tm[symb] >= 4): tdclass='pos_four'
		elif(tm[symb] >= 3): tdclass='pos_three'
		elif(tm[symb] >= 2): tdclass='pos_two'
		elif(tm[symb] >= 1): tdclass='pos_one'
		elif(tm[symb] > 0): tdclass='pos_small'
		elif(tm[symb] <= -8): tdclass='neg_eight'
		elif(tm[symb] <= -7): tdclass='neg_seven'
		elif(tm[symb] <= -6): tdclass='neg_six'
		elif(tm[symb] <= -5): tdclass='neg_five'
		elif(tm[symb] <= -4): tdclass='neg_four'
		elif(tm[symb] <= -3): tdclass='neg_three'
		elif(tm[symb] <= -2): tdclass='neg_two'
		elif(tm[symb] <= -1): tdclass='neg_one'
		elif(tm[symb] < 0): tdclass='neg_small'
		if tdclass: html += f'<td class={tdclass}>{move_str}%</td>'
		else: html += f'<td>{move_str}%</td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>Close</td>'
	for symb in symb_list:
		html += f'<td>{cp[symb]}</td>'
	html += '</tr>'

	mc_toggle = os.getenv('DISPLAY_MARKET_CAP')
	if (mc_toggle is not None) and (mc_toggle == '1'):
		html += '<tr>'
		html += '<td>MCap</td>'
		for symb in symb_list:
			html += f'<td>{mcap[symb]}</td>'
		html += '</tr>'

	html += '</table>'
	html += '</br>'
	return html

def gen_html_head():
	html_refresh_val = 3 if trading_is_active() else 10
	r = os.getenv('HTMLREFRESH')
	if r is not None: html_refresh_val = int(r)
	html = '<head>'
	if html_refresh_val > 0:
		html += f'<meta http-equiv=refresh content={html_refresh_val}; URL=/>'
	if os.getenv('DARKMODE'):
		html += '<link rel=stylesheet href=static/dashboard-dark.css>'
	else:
		html += '<link rel=stylesheet href=static/dashboard.css>'
	html += '</head>'
	return html

def gen_html(cp, mp, tm, mcap, tables_list):
	tz = timezone('US/Eastern')
	now = datetime.now(tz)
	now_str = now.strftime("%c")
	html = '<html>'
	html += gen_html_head()
	html += '<body>'
	html += '<center>'
	html += '<h2><a href=https://github.com/Fullaxx/stonk_stalker>Stonk Stalker</a></h2>'
	html += '<h3>' + now_str + ' US/Eastern</h3>'
	for tbl in tables_list:
		html += gen_html_table(cp, mp, tm, mcap, tbl)
#	html += '</br><a href=https://github.com/Fullaxx/stonk_stalker>GitHub</a>'
	html += '</center>'
	html += '</body>'
	html += '</html>'
	write_html_to_file(html, 'index.html')

def convert_market_cap(yfmcap):
	if (yfmcap >= 1e12):
		value = yfmcap/1e12
		units = 'T'
	elif (yfmcap >= 1e9):
		value = yfmcap/1e9
		units = 'B'
	else:
		value = yfmcap/1e6
		units = 'M'
	val_rounded = round(value, 1)
	mc_str = "{:0.1f}".format(val_rounded) + units
	return mc_str

def calc_symb_move(cp, mp, symb):
	diff = float(mp[symb]) - float(cp[symb])
	move_pct = 100 * (diff / float(cp[symb]))
	return round(move_pct, 2)

def format_price(p):
	r = round(float(p), 2)
	return "{:0.2f}".format(r)

def load_prices(cp, mp, tm, mcap, symb_list, tables_list, initialized):
	for symb in symb_list:
		res = yf.Ticker(symb)
#		cp[symb] = str(res.info['regularMarketPreviousClose'])
		cp[symb] = format_price(res.info['previousClose'])
		mp[symb] = format_price(res.info['currentPrice'])
		mcap[symb] = convert_market_cap(res.info['marketCap'])
		tm[symb] = calc_symb_move(cp, mp, symb)
		print(symb + ': ' + mp[symb])
		if initialized:
			gen_html(closePrice, marketPrice, tickerMotion, mcap, tables_list)

if __name__ == '__main__':
	symb_list = []
	closePrice = {}
	marketPrice = {}
	tickerMotion = {}
	marketCap = {}
	wwwdir = os.getenv('WWWDIR')
	if wwwdir is not None: os.chdir(wwwdir)
	ticker_tables = os.getenv('TICKER_TABLES')
	if ticker_tables is None: bailmsg('Set TICKER_TABLES')
	tables_list = ticker_tables.split(';')
	for tbl in tables_list:
		symbols = tbl.split('=')[1]
		symb_list += symbols.split(',')
	write_loading_to_file('index.html')
	load_prices(closePrice, marketPrice, tickerMotion, marketCap, symb_list, tables_list, 0)
	while True:
		load_prices(closePrice, marketPrice, tickerMotion, marketCap, symb_list, tables_list, 1)
		time.sleep(1)
