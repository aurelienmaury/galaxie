#!/usr/bin/env python
# -*- coding: utf-8 -*-
#<!-- http://fr.wikiversity.org/wiki/Vocabulaire_fran%C3%A7ais/Dire_l%27heure -->

import getopt
import sys
import time
import locale
locale.setlocale(locale.LC_ALL,'')

version = '1.0'
verbose = False
output_filename = 'default.out'
date = False
clock = False
day = False
daynum = False
month = False
year = False

#Multilansupport
text_hour = 'heure'
text_minute = 'minute'
text_and = 'et'
text_extact = 'pile'
text_midnight = 'minuit'
text_lunchtime = 'midi'
text_one = 'une'

#print 'ARGV      :', sys.argv[1:]

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:v', ['output=', 
                                                             'verbose',
                                                             'version=',
                                                             'date',
                                                             'clock',
                                                             'day',
                                                             'daynum',
                                                             'month',
                                                             'year'
                                                             ])
#print 'OPTIONS   :', options


for opt, arg in options:
    if opt in ('-o', '--output'):
        output_filename = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg
    elif opt == '--date':
        date = True
    elif opt == '--clock':
        clock = True
    elif opt == '--day':
        day = True
    elif opt == '--daynum':
        daynum = True
    elif opt == '--month':
        month = True
    elif opt == '--year':
        year = True


def print_date():
    #Day of the week - Exemple: samedi
    A=str(time.strftime('%A'))
    #Day number of the month - Exemple: 4 or 31 
    e=str(time.strftime('%e'))
    #Month name as plain text - Exemple: janvier
    B=str(time.strftime('%B'))
    #Year number
    Y=str(time.strftime('%Y'))

    #Note: month_num_to_text_fr(e) -> Tranlate a number to full language tipe - Exemple: 1 will b tranlate as "premier"
    print A + ' ' + month_num_to_text_fr(e) + ' ' + B + ' ' + Y


def print_clock():
    #Reproduse Speech clock
    temp = ''

    H=int(time.strftime('%H'))
    M=int(time.strftime('%M'))
   
    if H == 0:
        temp = temp + text_midnight + ' '
    if H == 1:
        temp = temp + text_one + ' ' +  text_hour + ' '
    if H == 12:
        temp = temp + text_lunchtime + ' '
    if H > 1 and not H == 12:
        temp = temp + str(H) + ' ' +  text_hour + 's' + ' '

    # Add "and"
    if not M  == 0:
        temp = temp + text_and + ' '

    if M == 0:
        temp = temp + text_extact + ' '
    if M == 1:
        temp = temp + text_one + ' ' + text_minute + ' '
    if M > 1:
        temp = temp + str(M) + ' ' + text_minute + 's' + ''

    print temp

def print_day():
    temp=time.strftime('%A')
    print temp

def print_daynum():
    temp=time.strftime('%e %B')
    print temp

def print_month():
    temp=time.strftime('%B')
    print temp

def print_year():
    temp=time.strftime('%Y')
    print temp
    
def month_num_to_text_fr(e):
    if e == 0 or e == 00:
        return e
    elif e == '1' or e == '01' or e == ' 1':
        e = 'premier'
    elif e == '2' or e == '02' or e == ' 2':
        e = 'deux'
    elif e == '3' or e == '03' or e == ' 3':
        e = 'trois'
    elif e == '4' or e == '04' or e == ' 4':
        e = 'quatre'
    elif e == '5' or e == '05' or e == ' 5':
        e = 'cinq'
    elif e == '6' or e == '06' or e == ' 6':
        e = 'six'
    elif e == '7' or e == '07' or e == ' 7':
        e = 'sept'
    elif e == '8' or e == '08' or e == ' 8':
        e = 'huit'
    elif e == '9' or e == '09' or e == ' 9':
        e = 'neuf'
    elif e == '10':
        e = 'dix'
    elif e == '11':
        e = 'onze'
    elif e == '12':
        e = 'douze'
    elif e == '13':
        e = 'treize'
    elif e == '14':
        e = 'quatorze'
    elif e == '15':
        e = 'quinze'
    elif e == '16':
        e = 'seize'
    elif e == '17':
        e = 'dix sept'
    elif e == '18':
        e = 'dix huit'
    elif e == '19':
        e = 'dix neuf'
    elif e == '20':
        e = 'vinght'
    elif e == '21':
        e = 'vinght et un'
    elif e == '22':
        e = 'vinght deux'
    elif e == '23':
        e = 'vinght trois'
    elif e == '24':
        e = 'vinght quatre'
    elif e == '25':
        e = 'vinght cinq'
    elif e == '26':
        e = 'vinght six'
    elif e == '27':
        e = 'vinght spet'
    elif e == '28':
        e = 'vinght huit'
    elif e == '29':
        e = 'vinght neuf'
    elif e == '30':
        e = 'trente'
    elif e == '31':
        e = 'trente et un'
    return e

if date:
    print_date()

if clock:
    print_clock()

if day:
    print_day()

if daynum:
    print_daynum()


if month:
    print_month()

if year:
    print_year()
