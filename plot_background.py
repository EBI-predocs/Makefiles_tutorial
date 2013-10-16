from helpers import *
from sys import argv

results = readSurvey('Form_Responses.csv', 'index.txt')

df = results['Primary_Training']
title = "Primary training (n={})".format(str(len(df)))

plotBackground(df, title, argv[1])

