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
        text_to_return = text_to_return + text_midnight + ' '
    if hour == 1:
        text_to_return = text_to_return + text_one + ' ' + text_hour + ' '
    if hour == 12:
        text_to_return = text_to_return + text_lunchtime + ' '
    if hour > 1 and not hour == 12:
        text_to_return = text_to_return + str(hour) + ' ' + text_hour + 's' + ' '

    # Add "and"
    if not minute == 0:
        text_to_return = text_to_return + text_and + ' '

    if minute == 0:
        text_to_return = text_to_return + text_exact + ' '
    if minute == 1:
        text_to_return = text_to_return + text_one + ' ' + text_minute + ' '
    if minute > 1:
        text_to_return = text_to_return + str(minute) + ' ' + text_minute + 's' + ''

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
