from samplemethod import *

if __name__=="__main__":
    
    logic = sys.argv[1]
    outputfile = sys.argv[2]
    vlogic = getvlogic(logic)
    llogic = getllogic(vlogic)
    samples = rsample(llogic,10)
    sample = samples[0]
    masks = indexmask(vlogic)
    
    roundlimit = 300000
    res = set()
    count = 0
    while True:
        roundoutput = []
        count+=1
        print(count)
        vlogic = getvlogic(logic)
        llogic = getllogic(vlogic)
        samples = rsample(llogic,roundlimit)
        for i in range(len(samples)):
            tempvals = evalmask(samples[i],masks)
            if len(np.unique(tempvals)) != len(tempvals):
                continue
            tempord = tuple(np.argsort(tempvals))
            #print(tempord)
            if tempord not in res:
                tempstr = str(tempord)+': '+str(samples[i])
                roundoutput.append(tempstr)
                res.add(tempord)

        with open(outputfile,'a+') as file:
            for i in range(len(roundoutput)):
                file.write(roundoutput[i]+'\n')
        with open('logfile','a+') as file:
            file.write(str(len(res))+'\n')
