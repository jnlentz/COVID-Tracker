# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 05:19:47 2020

@author: jnlen
"""
import datetime

def toDate(iDate):
    sDate = str(iDate)
    years = sDate[0:4]
    months = sDate[4:6]
    days = sDate[6:8]
    date = years + '-' + months + '-' + days 
    return date

x = []

import csv

with open('fixed - Sheet1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        x.append(toDate(row[0]))



   
with open('fixed2 - Sheet1.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)   
    for i in x:
        l = []
        l.append(i)
        spamwriter.writerow(l)
