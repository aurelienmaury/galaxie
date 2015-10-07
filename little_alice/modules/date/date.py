#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

# <!-- http://fr.wikiversity.org/wiki/Vocabulaire_fran%C3%A7ais/Dire_l%27heure -->

import getopt
import sys
import time
import locale

locale.setlocale(locale.LC_ALL, '')

version = '1.0'
verbose = False
output_filename = 'default.out'
date = False
clock = False
day = False
day_num = False
month = False
year = False
salutation = False

# Translation in hard for French
text_hour = 'heure'
text_minute = 'minute'
text_and = 'et'
text_exact = 'pile'
text_midnight = 'minuit'
text_lunchtime = 'midi'
text_one = 'une'
text_good_morning = 'bonjour'
text_good_evening = 'bonsoir'

options, remainder = getopt.gnu_getopt(
    sys.argv[1:],
    'o:v',
    {'output=',
     'verbose',
     'version=',
     'date',
     'clock',
     'day',
     'daynum',
     'month',
     'year',
     'salutation'}
)

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
        day_num = True
    elif opt == '--month':
        month = True
    elif opt == '--year':
        year = True
    elif opt == '--salutation':
        salutation = True


def print_date():
    day_of_the_week = str(time.strftime('%A'))
    day_number_of_the_month = str(time.strftime('%e'))
    month_name_as_plain_text = str(time.strftime('%B'))
    year_number = str(time.strftime('%Y'))

    # Note: month_num_to_text_fr(e) - Translate a number to full language tipe - Exemple: 1 will b tranlate as "premier"
    text_to_return = ''
    text_to_return += day_of_the_week.title()
    text_to_return += ' '
    text_to_return += month_num_to_text_fr(day_number_of_the_month).title()
    text_to_return += ' '
    text_to_return += month_name_as_plain_text.title()
    text_to_return += ' '
    text_to_return += year_number

    print text_to_return


def print_clock():
    # Reproduce Speech clock
    text_to_return = ''

    hour = int(time.strftime('%H'))
    minute = int(time.strftime('%M'))

    if hour == 0:
        text_to_return += text_midnight
        text_to_return += ' '
    if hour == 1:
        text_to_return += str(hour_num_to_text_fr(hour))
        text_to_return += ' '
        text_to_return += text_hour
        text_to_return += ' '
    if hour == 12:
        text_to_return += text_lunchtime
        text_to_return += ' '
    if hour > 1 and not hour == 12:
        text_to_return += str(hour_num_to_text_fr(hour))
        text_to_return += ' '
        text_to_return += text_hour
        text_to_return += 's'
        text_to_return += ' '

    # Add "and"
    if not minute == 0:
        text_to_return += text_and
        text_to_return += ' '

    if minute == 0:
        text_to_return += text_exact
        text_to_return += ' '
    if minute == 1:
        text_to_return = str(minute_num_to_text_fr(minute))
        text_to_return += ' '
        text_to_return += text_minute
        text_to_return += ' '
    if minute > 1:
        text_to_return += minute_num_to_text_fr(minute)
        text_to_return += ' '
        text_to_return += text_minute
        text_to_return += 's'
        text_to_return += ' '
    print text_to_return


def print_day():
    print time.strftime('%A')


def print_day_num():
    print time.strftime('%e %B')


def print_month():
    print time.strftime('%B')


def print_year():
    print time.strftime('%Y')


def print_salutation():
    hour = int(time.strftime('%H'))
    minute = int(time.strftime('%M'))

    if 0 <= hour <= 5:
        if hour == 5 and minute >= 30:
            print text_good_morning.title()
        else:
            print text_good_evening.title()
    elif 6 <= hour <= 17:
        if hour == 17 and minute >= 30:
            print text_good_evening.title()
        else:
            print text_good_morning.title()
    elif 18 <= hour <= 23:
        print text_good_evening.title()


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
        e = 'vingt et un'
    elif e == '22':
        e = 'vingt deux'
    elif e == '23':
        e = 'vingt trois'
    elif e == '24':
        e = 'vingt quatre'
    elif e == '25':
        e = 'vingt cinq'
    elif e == '26':
        e = 'vingt six'
    elif e == '27':
        e = 'vingt spet'
    elif e == '28':
        e = 'vingt huit'
    elif e == '29':
        e = 'vingt neuf'
    elif e == '30':
        e = 'trente'
    elif e == '31':
        e = 'trente et un'
    return e


def hour_num_to_text_fr(hour):
    text_to_return = ''
    hour = str(hour)
    if hour == 0 or hour == 00:
        return hour
    elif hour == '1' or hour == '01' or hour == ' 1':
        text_to_return = 'une'
    elif hour == '2' or hour == '02' or hour == ' 2':
        text_to_return = 'deux'
    elif hour == '3' or hour == '03' or hour == ' 3':
        text_to_return = 'trois'
    elif hour == '4' or hour == '04' or hour == ' 4':
        text_to_return = 'quatre'
    elif hour == '5' or hour == '05' or hour == ' 5':
        text_to_return = 'cinq'
    elif hour == '6' or hour == '06' or hour == ' 6':
        text_to_return = 'six'
    elif hour == '7' or hour == '07' or hour == ' 7':
        text_to_return = 'sept'
    elif hour == '8' or hour == '08' or hour == ' 8':
        text_to_return = 'huit'
    elif hour == '9' or hour == '09' or hour == ' 9':
        text_to_return = 'neuf'
    elif hour == '10':
        text_to_return = 'dix'
    elif hour == '11':
        text_to_return = 'onze'
    elif hour == '12':
        text_to_return = 'douze'
    elif hour == '13':
        text_to_return = 'treize'
    elif hour == '14':
        text_to_return = 'quatorze'
    elif hour == '15':
        text_to_return = 'quinze'
    elif hour == '16':
        text_to_return = 'seize'
    elif hour == '17':
        text_to_return = 'dix sept'
    elif hour == '18':
        text_to_return = 'dix huit'
    elif hour == '19':
        text_to_return = 'dix neuf'
    elif hour == '20':
        text_to_return = 'vinght'
    elif hour == '21':
        text_to_return = 'vingt et une'
    elif hour == '22':
        text_to_return = 'vingt deux'
    elif hour == '23':
        text_to_return = 'vingt trois'
    return text_to_return

def minute_num_to_text_fr(minute):
    text_to_return = ''
    minute = str(minute)
    if minute == 0 or minute == 00:
        text_to_return = 'zéro'
    elif minute == '1' or minute == '01' or minute == ' 1':
        text_to_return = 'une'
    elif minute == '2' or minute == '02' or minute == ' 2':
        text_to_return = 'deux'
    elif minute == '3' or minute == '03' or minute == ' 3':
        text_to_return = 'trois'
    elif minute == '4' or minute == '04' or minute == ' 4':
        text_to_return = 'quatre'
    elif minute == '5' or minute == '05' or minute == ' 5':
        text_to_return = 'cinq'
    elif minute == '6' or minute == '06' or minute == ' 6':
        text_to_return = 'six'
    elif minute == '7' or minute == '07' or minute == ' 7':
        text_to_return = 'sept'
    elif minute == '8' or minute == '08' or minute == ' 8':
        text_to_return = 'huit'
    elif minute == '9' or minute == '09' or minute == ' 9':
        text_to_return = 'neuf'
    elif minute == '10':
        text_to_return = 'dix'
    elif minute == '11':
        text_to_return = 'onze'
    elif minute == '12':
        text_to_return = 'douze'
    elif minute == '13':
        text_to_return = 'treize'
    elif minute == '14':
        text_to_return = 'quatorze'
    elif minute == '15':
        text_to_return = 'quinze'
    elif minute == '16':
        text_to_return = 'seize'
    elif minute == '17':
        text_to_return = 'dix sept'
    elif minute == '18':
        text_to_return = 'dix huit'
    elif minute == '19':
        text_to_return = 'dix neuf'
    elif minute == '20':
        text_to_return = 'vinght'
    elif minute == '21':
        text_to_return = 'vingt et une'
    elif minute == '22':
        text_to_return = 'vingt deux'
    elif minute == '23':
        text_to_return = 'vingt trois'
    elif minute == '24':
        text_to_return = 'vingt quatre'
    elif minute == '25':
        text_to_return = 'vingt cinq'
    elif minute == '26':
        text_to_return = 'vingt six'
    elif minute == '27':
        text_to_return = 'vingt spet'
    elif minute == '28':
        text_to_return = 'vingt huit'
    elif minute == '29':
        text_to_return = 'vingt neuf'
    elif minute == '30':
        text_to_return = 'trente'
    elif minute == '31':
        text_to_return = 'trente et une'
    elif minute == '32':
        text_to_return = 'trente deux'
    elif minute == '33':
        text_to_return = 'trente trois'
    elif minute == '34':
        text_to_return = 'trente quatre'
    elif minute == '35':
        text_to_return = 'trente cinq'
    elif minute == '36':
        text_to_return = 'trente six'
    elif minute == '37':
        text_to_return = 'trente spet'
    elif minute == '38':
        text_to_return = 'trente huit'
    elif minute == '39':
        text_to_return = 'trente neuf'
    elif minute == '40':
        text_to_return = 'quarante'
    elif minute == '41':
        text_to_return = 'quarante et une'
    elif minute == '42':
        text_to_return = 'quarante deux'
    elif minute == '43':
        text_to_return = 'quarante trois'
    elif minute == '44':
        text_to_return = 'quarante quatre'
    elif minute == '45':
        text_to_return = 'quarante cinq'
    elif minute == '46':
        text_to_return = 'quarante six'
    elif minute == '47':
        text_to_return = 'quarante spet'
    elif minute == '48':
        text_to_return = 'quarante huit'
    elif minute == '49':
        text_to_return = 'quarante neuf'
    elif minute == '50':
        text_to_return = 'cinquante'
    elif minute == '51':
        text_to_return = 'cinquante et une'
    elif minute == '52':
        text_to_return = 'cinquante deux'
    elif minute == '53':
        text_to_return = 'cinquante trois'
    elif minute == '54':
        text_to_return = 'cinquante quatre'
    elif minute == '55':
        text_to_return = 'cinquante cinq'
    elif minute == '56':
        text_to_return = 'cinquante six'
    elif minute == '57':
        text_to_return = 'cinquante spet'
    elif minute == '58':
        text_to_return = 'cinquante huit'
    elif minute == '59':
        text_to_return = 'cinquante neuf'
    return text_to_return


if date:
    print_date()

if clock:
    print_clock()

if day:
    print_day()

if day_num:
    print_day_num()

if month:
    print_month()

if year:
    print_year()

if salutation:
    print_salutation()
