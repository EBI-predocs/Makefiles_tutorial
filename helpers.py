import sys
import pandas as pd
import pandas.io.parsers as parsers
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist

def readSurvey(fname, findex):
    results = parsers.read_csv(fname)
    results.columns = np.genfromtxt(findex, dtype='str')

    results['Computer_time'] = results['Computer_time'].astype('int')
    lookup = [ ("(5) more",5), ("-4",4), ("-3",3), ("-2",2), ("(1) less",1) ]
    for k,v in lookup:
        results.replace(k, v, inplace=True)

    return results

def plotBackground(df, title, fname):
    plt.figure(figsize=(8,8))

    labels = set(df)
    for label in labels:
        if sum(df == label) == 1:
            df.replace(label, 'Other', inplace=True)

    labels = set(df)
    fracs = [sum(df == label) for label in labels]
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title(title)
    plt.savefig(fname)

def plotInterestPoints(df, title, fname):
    n = len(df.columns)
    plt.figure()
    pts = df.sum()
    pts.sort()
    plt.barh(np.arange(n)+.1, pts)
    plt.yticks(np.arange(n)+.5, pts.keys())
    plt.title(title)
    plt.tight_layout()
    plt.ylim(0, n)
    plt.savefig(fname)

def plotCorrelations(df, title, fname):
    plt.figure()

    n = len(df.columns)
    corr = np.zeros((n,n))

    for iy,y in enumerate(df.columns):
        for ix,x in enumerate(df.columns):
            corr[iy,ix] = np.sum(np.abs(df[y]-df[x]))

    dist = pdist(corr, 'euclidean')
    link = linkage(dist, method='complete')
    leaves = leaves_list(link)
    corr = corr[:, leaves][leaves]
    colnames = df.columns[leaves]

    plt.imshow(corr, interpolation='nearest')
    plt.colorbar()
    plt.title(title)
    plt.xticks(range(n), colnames, size='small', rotation=45, ha='right')
    plt.yticks(range(n), colnames, size='small')
    plt.tight_layout()
    plt.savefig(fname)

