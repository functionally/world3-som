import numpy                  as np
import numpy.random           as nr
import pandas                 as pd
import scipy.stats            as sp
import sklearn.manifold       as sm
import sklearn.preprocessing  as sk
import tensorly               as tl
import tensorly.decomposition as td

from collections import namedtuple
from warnings    import simplefilter


def read_sampled(filename, runLabel, timeLabel, size=None, sep="\t", verbose=0):

    simplefilter(action='ignore', category=FutureWarning)
    zOutput = pd.read_csv(filename, sep=sep, index_col=[runLabel, timeLabel], verbose=verbose)
    
    if verbose >= 1:
        print("Original shape:", zOutput.shape)
        print("Columns:", zOutput.columns)
        
    nRuns = zOutput.index.levels[0].size
    if verbose >= 1:
        print("Runs:", nRuns)
    
    nTimes = zOutput.index.levels[1].size
    if verbose >= 1:
        print("Times:", nTimes)

    if size is not None and size < nRuns:
        runs = nr.choice(zOutput.index.levels[0], size=size, replace=False)
        zOutput = zOutput[zOutput.index.isin(runs, level=0)]

    if verbose >= 1:
        print("Sampled shape:", zOutput.shape)

    return zOutput


def tucker_tnse(zInput, metrics, kTimes, kMetrics,
                scaler=sk.MinMaxScaler(),
                n_components=3, perplexity=30, early_exaggeration=12, learning_rate=200, n_iter=1000, min_grad_norm=1e-7, angle=0.5,
                verbose=0):
    
    zSorted = zInput.sort_index()
    zSorted.index = zSorted.index.remove_unused_levels()
    
    runs = zSorted.index.levels[0]
    nRuns = runs.size
    if verbose >= 1:
        print("Runs:", nRuns)
    
    times = zSorted.index.levels[1]
    nTimes = times.size
    if verbose >= 1:
        print("Times:", nTimes)
    
    assert zSorted.shape[0] == nRuns * nTimes

    zArray = np.array(zSorted[metrics])
    
    nMetrics = len(metrics)

    if verbose >= 2:
        print("Range before scaling:", sp.describe(zArray).minmax)
    zScaled = scaler.fit_transform(zArray)
    if verbose >= 2:
        print("Range after scaling:", sp.describe(zScaled).minmax)
    if verbose >= 3:
        print("Scaling model:", scaler)
        
    zTensor = np.reshape(zScaled, (nRuns, nTimes, nMetrics)) 
    if verbose >= 1:
        print("Tensor shape:", zTensor.shape)
        
    zCore, zFactors = td.tucker(zTensor, ranks=[nRuns, kTimes, kMetrics], verbose=verbose)
    if verbose >= 1:
        print("Core shape:", zCore.shape)
    if verbose >= 2:
        print("Factor shapes:", list(map(lambda x: x.shape, zFactors)))
        
    maxAbsDev = np.amax(abs(tl.tucker_to_tensor(zCore, zFactors) - zTensor))
    if verbose >= 1:
        print("Maximum absolute deviation:", maxAbsDev)
        
    model = sm.TSNE(n_components=n_components, perplexity=perplexity, early_exaggeration=early_exaggeration, learning_rate=learning_rate, n_iter=n_iter, min_grad_norm=min_grad_norm, angle=angle, verbose=verbose)
    if verbose >= 3:
        print("TSNE model:", model)
    zEmbedded = model.fit_transform(np.reshape(zCore, (nRuns, kTimes * kMetrics)))
    if verbose >= 1:
        print("Embedding shape:", zEmbedded.shape)
    
    return namedtuple(
        "TuckerTSNE",
        ("embedding", "mad")
    ) (
        pd.DataFrame(
            data=zEmbedded,
            index=pd.Index(data=runs, name=zSorted.index.names[0]),
            columns=["Embed " + str(i+1) for i in range(0, n_components)]
        ),
        maxAbsDev
    )


def write_joined(zOriginal, zEmbedded, filename, sep="\t", compression=None):
    
    zOutput = zOriginal.xs(max(zOriginal.index.levels[1]), level=1, drop_level=False).join(zEmbedded.embedding, how="inner")
    
    zOutput.to_csv(filename, sep=sep, compression=compression)
    
    return None


def analyze(basename, runColumn, timeColumn, outputColumns, timeCounts, metricCounts, perplexities, runCount=None, n_components=3, verbose=1):

    z = read_sampled(basename + ".tsv.gz", runColumn, timeColumn, runCount)

    for t in timeCounts:
        for m in metricCounts:
            for p in perplexities:
                print()
                print("Base name:", basename)
                print("Time dimension:", t)
                print("Metric dimension:", m)
                print("Perplexity:", p)
                ze = tucker_tnse(z, outputColumns, t, m, perplexity=p, n_components=n_components, verbose=verbose)
                write_joined(z, ze, basename + "-t=" + str(t) + "-m=" + str(m) + "-p=" + str(p) + ".tsv.gz", compression="gzip")
                print()
