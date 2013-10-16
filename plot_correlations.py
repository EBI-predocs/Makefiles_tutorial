from helpers import *
from sys import argv

results = readSurvey('Form_Responses.csv', 'index.txt')

df = results[results.columns[17:43]]
df = df.replace(np.NaN, 0, inplace=False)
title = "Difference in preferences between two topics (n={})".format(str(len(df)))

plotCorrelations(df, title, argv[1])

