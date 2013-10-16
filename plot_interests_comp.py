from helpers import *
from sys import argv

results = readSurvey('Form_Responses.csv', 'index.txt')

df = results[(results['Programming_language'] == 'Yes') | (
        (results['Programming_language'] == 'Plan to') & (results['Computer_time'] > 55))]
df = df[df.columns[17:43]]
title = "Total interest points by computational people (n={})".format(str(len(df)))

plotInterestPoints(df-1, title, argv[1])

