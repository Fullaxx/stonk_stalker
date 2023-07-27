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

def gen_html_table(cp, mp, tm, tbl):
	table_name,symbols = tbl.split('=')
	symb_list = symbols.split(',')

	html = '<table>'

	html += '<tr>'
	html += f'<th>{table_name}</th>'
	for symb in symb_list:
		thclass = None
		if(tm[symb] > 0): thclass='up'
		if(tm[symb] < 0): thclass='down'
		if thclass: html += f'<th class={thclass}>{symb}</th>'
		else: html += f'<th>{symb}</th>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>$</td>'
	for symb in symb_list:
		price = float(mp[symb])
		price_rounded = round(price, 2)
		price_formatted = "{:0.2f}".format(price_rounded)
		html += f'<td>{price_formatted}</td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>%</td>'
	for symb in symb_list:
		tdclass = None
		move_formatted = "{:0.2f}".format(tm[symb])
		move_str = '+' + str(move_formatted) if tm[symb] > 0 else str(move_formatted)
		if(tm[symb] >= 5): tdclass='pos_five'
		elif(tm[symb] >= 4): tdclass='pos_four'
		elif(tm[symb] >= 3): tdclass='pos_three'
		elif(tm[symb] >= 2): tdclass='pos_two'
		elif(tm[symb] >= 1): tdclass='pos_one'
		elif(tm[symb] > 0): tdclass='pos_small'
		elif(tm[symb] <= -5): tdclass='neg_five'
		elif(tm[symb] <= -4): tdclass='neg_four'
		elif(tm[symb] <= -3): tdclass='neg_three'
		elif(tm[symb] <= -2): tdclass='neg_two'
		elif(tm[symb] <= -1): tdclass='neg_once'
		elif(tm[symb] < 0): tdclass='neg_small'
		if tdclass: html += f'<td class={tdclass}>{move_str}%</td>'
		else: html += f'<td>{move_str}%</td>'
	html += '</tr>'

	html += '<tr>'
	html += '<td>Close</td>'
	for symb in symb_list:
		price = float(cp[symb])
		price_rounded = round(price, 2)
		price_formatted = "{:0.2f}".format(price_rounded)
		html += f'<td>{price_formatted}</td>'
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
		html += '<link rel=stylesheet href=dashboard-dark.css>'
	else:
		html += '<link rel=stylesheet href=dashboard.css>'
	html += '</head>'
	return html

def gen_html(cp, mp, tm, tables_list):
	tz = timezone('US/Eastern')
	now = datetime.now(tz)
	now_str = now.strftime("%c")
	html = '<html>'
	html += gen_html_head()
	html += '<body>'
	html += '<center>'
	html += '<h2>' + now_str + ' US/Eastern</h2>'
	for tbl in tables_list:
		html += gen_html_table(cp, mp, tm, tbl)
	html += '</br><a href=https://github.com/Fullaxx/stonk_stalker>GitHub</a>'
	html += '</center>'
	html += '</body>'
	html += '</html>'
	write_html_to_file(html, 'index.html')

def load_prices(cp, mp, tm, symb_list, tables_list, initialized):
	for symb in symb_list:
		res = yf.Ticker(symb)
#		cp[symb] = str(res.info['regularMarketPreviousClose'])
		cp[symb] = str(res.info['previousClose'])
		mp[symb] = str(res.info['currentPrice'])
		diff = float(mp[symb]) - float(cp[symb])
		move_pct = 100 * (diff / float(cp[symb]))
		tm[symb] = round(move_pct, 2)
		print(symb + ': ' + mp[symb])
		if initialized:
			gen_html(closePrice, marketPrice, tickerMotion, tables_list)

if __name__ == '__main__':
	symb_list = []
	closePrice = {}
	marketPrice = {}
	tickerMotion = {}
	wwwdir = os.getenv('WWWDIR')
	if wwwdir is not None: os.chdir(wwwdir)
	ticker_tables = os.getenv('TICKER_TABLES')
	if ticker_tables is None: bailmsg('Set TICKER_TABLES')
	tables_list = ticker_tables.split(';')
	for tbl in tables_list:
		symbols = tbl.split('=')[1]
		symb_list += symbols.split(',')
	load_prices(closePrice, marketPrice, tickerMotion, symb_list, tables_list, 0)
	while True:
		load_prices(closePrice, marketPrice, tickerMotion, symb_list, tables_list, 1)
		time.sleep(1)
