#!/usr/bin/python

minDist = 100

for minDist in range (100,250,50):
    for parm1 in range (1,20,4):
        for parm2 in range (1,20,4):
            for minSize in range (2,30,4):
                for maxSize in range (2,30,2):
                    fname = str(minDist) + "-" + str(parm1) + "-" + str(parm2)
                    fname += "-" + str(minSize) + "-" + str(maxSize)
                    print fname
