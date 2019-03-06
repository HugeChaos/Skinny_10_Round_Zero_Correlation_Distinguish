#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "Chaos"
import PermSet
import ModelBuild
import time


def F_2_16_VectorCreat(W):
    return [[a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15] \
            for a0 in [0, 1] for a1 in [0, 1] for a2 in [0, 1] for a3 in [0, 1] \
            for a4 in [0, 1] for a5 in [0, 1] for a6 in [0, 1] for a7 in [0, 1]
            for a8 in [0, 1] for a9 in [0, 1] for a10 in [0, 1] for a11 in [0, 1] \
            for a12 in [0, 1] for a13 in [0, 1] for a14 in [0, 1] for a15 in [0, 1] \
            if (a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10 + a11 + a12\
                + a13 + a14 + a15) in range(1, W + 1)]


if __name__ == '__main__':
    PS = PermSet.ps16
    p_count = 1
    for ps in PS:
        t1 = time.time()
        file_name = "zeroCorrelationL%d.txt" % p_count
        f = open(file_name, "a")
        f.write("For Permutation " + str(ps) + ", The Zero Correlation Linear Result As Follows:\n")
        f.close()
        BV = F_2_16_VectorCreat(1)
        EV = F_2_16_VectorCreat(1)
        zeroCorrelation_round = 0
        flagToRoundPlusPlus = True
        while flagToRoundPlusPlus:
            flagToRoundPlusPlus = False
            zeroCorrelation_round += 1
            for bv in BV:
                for ev in EV:
                    yx = ModelBuild.ZeroCorrelation(zeroCorrelation_round, ps, bv, ev)
                    yx.ModelMake()
                    flagToRoundPlusPlus = yx.ModelSolve()
                    if flagToRoundPlusPlus:
                        break
                if flagToRoundPlusPlus:
                    break
        f = open(file_name, "a")
        zeroCorrelation_round = zeroCorrelation_round - 1
        f.write("\n" + "*" * 50 + "\n")
        f.write("The Longest Correlation Linear Round is %d. \n" % zeroCorrelation_round)
        f.write("\n" + "*" * 50 + "\n")
        f.write("The Distinguish as Follows:\n")
        f.close()
        for bv in BV:
            for ev in EV:
                yx = ModelBuild.ZeroCorrelation(zeroCorrelation_round, ps, bv, ev)
                yx.ModelMake()
                flagToRoundPlusPlus = yx.ModelSolve()
                if flagToRoundPlusPlus:
                    f = open(file_name, "a")
                    f.write(str(bv) + " ---> X <--- " + str(ev) + "\n")
                    f.close()
        t2 = time.time()
        f = open(file_name, "a")
        f.write("\n" + "#" * 50 + "\n")
        f.write("The Total Run Time is " + str(t2 - t1) + "\n")
        f.close()
        p_count += 1
