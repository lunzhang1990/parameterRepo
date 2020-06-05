import random
from math import log
from math import floor
import numpy as np
from time import time
import sys

precision = 1000

def getvlogic(logic):
    vlogic = list(map(lambda x:int(x), logic.split('_')))
    return vlogic

def getllogic(vlogic):
    llogic = list(map(lambda x: int(log(x,2)), vlogic))
    return llogic

def rsample(llogic, no):
    #logic = list(map(lambda x:int(x), logic.split('_')))
    samples = []
    for i in range(no):
        temp = []
        for j in range(len(llogic)):
            fsample = random.sample(range(1,precision), llogic[j]+1)
            #fsample = [random.randint(1,precision) for _ in range(llogic[j]+1)]
            fsample[1:] = sorted(fsample[1:],reverse=True)
            temp.append(fsample)
        samples.append(temp)
    return samples

def indexmask(vlogic):
    no = np.prod(vlogic)
    l = int(log(no,2))
    pattern = '{0:0'+str(l)+'b}'
    ret = []
    for i in range(no):
        mask = pattern.format(i)
        vmask = [int(i) for i in mask]
        currmask = []
        llogic = getllogic(vlogic)
        currpos = 0
        for i in range(len(llogic)):
            temp = vmask[currpos:currpos+llogic[i]]
            currmask.append(temp)
            currpos += llogic[i]
        ret.append(currmask)
    return ret

def evalmask(sample, masks):
    ret = []
    for i in range(len(masks)):
        currval = 1
        for j in range(len(masks[i])):
            tempsum = sample[j][0]
            for k in range(len(masks[i][j])):
                tempsum+= masks[i][j][k]*sample[j][k+1]
            currval*=tempsum
        ret.append(currval)
    return ret        


