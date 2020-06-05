import sys
from helpers import *
import json
import numpy as np
if __name__ == "__main__":
    logic = sys.argv[1]
    preOrderFile = sys.argv[2]
    extraRestrictionFile = sys.argv[3]
    #pattern = list(map(lambda x:int(x),logic.split('_')))
    #restrictedOrdering = list(map(lambda x: int(x),sys.argv[2:]))
    #file_no = int(sys.argv[2])
    #print(subpattern)
    pres = []
    with open(preOrderFile,'r') as file:
        line = file.readline()[:-1]
        while line:
            line = line.split(' ')
            line = list(map(lambda x: int(x), line))
            pres.append(tuple(line))
            line = file.readline()[:-1]

    #run5(logic,pres[file_no])
    #print(pres[file_no])
    for i in range(len(pres)):
        print(logic)
        run5(logic,pres[i],extraRestrictionFile,np.array([[0,0,0,0,1,-1,-1,1]]))
