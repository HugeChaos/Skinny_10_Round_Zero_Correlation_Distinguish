#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "Chaos"
import copy
from gurobipy import *


class ZeroCorrelation(object):
    def __init__(self, total_round, perm, bv, ev):
        self.TR = total_round
        self.word = 16
        self.perm = perm
        self.bv = bv
        self.ev = ev
        self.file = "ZC_model.lp"
        self.Counter = 0

    def ObjectFunction(self):
        f = open(self.file, 'a')
        f.write("Minimize\n\n")
        f.close()

    def CreateVar(self, var, rou):
        return [var + "_" + str(rou) + "_" + str(i) for i in range(0, self.word)]

    def ConstraintByBranchCopy(self, var1, var2, var3):
        f = open(self.file, "a")
        f.write(var1 + " + " + var2 + " - " + var3 + " >= 0\n")
        f.write(var1 + " + " + var3 + " - " + var2 + " >= 0\n")
        f.write(var2 + " + " + var3 + " - " + var1 + " >= 0\n")
        f.close()

    def ConstraintByEqual(self, var1, var2):
        f = open(self.file, "a")
        f.write(var1 + " - " + var2 + " = 0\n")
        f.close()

    def ConstraintByP(self, var1, var2, aux_var):
        self.ConstraintByBranchCopy(var1[1], var1[2], aux_var)
        self.ConstraintByEqual(var1[3], var2[0])
        self.ConstraintByBranchCopy(var1[0], aux_var, var2[1])
        self.ConstraintByEqual(var1[1], var2[2])
        self.ConstraintByBranchCopy(var1[3], aux_var, var2[3])

    def ConstraintsByPLayer(self, var1, var2):
        for j in range(0, 4):
            V1 = copy.deepcopy([var1[4 * i + j] for i in range(0, 4)])
            V2 = copy.deepcopy([var2[4 * i + j] for i in range(0, 4)])
            t = "v" + str(self.Counter)
            self.ConstraintByP(V1, V2, t)
            self.Counter += 1

    def ConstraintsByNibblePerm(self, var):
        res = ["" for i in range(0, len(var))]
        for i in range(0, len(var)):
            res[i] = var[self.perm[i]]
        return res

    def ConstraintsByBeginVector(self):
        f = open(self.file, "a")
        X = self.CreateVar("x", 0)
        for i in range(0, self.word):
            f.write(X[i] + " = " + str(self.bv[i]) + "\n")
        f.close()

    def ConstraintsByEndVector(self):
        f = open(self.file, "a")
        X = self.CreateVar("x", self.TR)
        for i in range(0, self.word):
            f.write(X[i] + " = " + str(self.ev[i]) + "\n")
        f.close()

    def Binary(self):
        f = open(self.file, "a")
        f.write("Binary\n")
        for rou in range(0, self.TR + 1):
            for i in range(0, self.word):
                f.write("x_" + str(rou) + "_" + str(i) + "\n")
        for i in range(0, self.Counter):
            f.write("v" + str(i) + "\n")
        f.write("END")
        f.close()

    def ModelMake(self):
        if os.path.exists(self.file):
            os.remove(self.file)
        self.ObjectFunction()
        X = self.CreateVar("x", 0)
        f = open(self.file, "a")
        f.write("Subject To\n")
        f.close()
        self.ConstraintsByBeginVector()
        for rou in range(0, self.TR):
            X1 = self.CreateVar("x", rou + 1)
            XX = self.ConstraintsByNibblePerm(X1)
            self.ConstraintsByPLayer(X, XX)
            X = X1
        self.ConstraintsByEndVector()
        self.Binary()

    def ModelSolve(self):
        m = read(self.file)
        m.optimize()
        if m.Status == 3:
            return True
        else:
            return False
