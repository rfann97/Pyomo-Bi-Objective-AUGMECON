# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:53:24 2021

@author: Ruadhan Fanning
"""

import pyomo.environ as pe
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# min f1 = TPC 
# max f2 = SSPV 
# st    Demand 
#       Capcity 
#       Quality 
#       Delivery
#       Storage Capcity
#       Binary and non-negative rules

# Data related to products and suppliers
products = ([50000, 0.95, 0.03, 0.38, 0.0012, 0.01], [50000, 0.95, 0.03, 0.101, 0.0005, 0.021])
suppliers = ([[25000,35000], [0.72, 0.504], [0.01, 0.01], [0.95, 0.95], 4, 2.5, 20, 480, 0.9056], [[30000,30000], [0.78, 0.52], [0.01, 0.01], [0.95, 0.95], 4, 2.4, 40, 480, 0.8039])

# Number of products and suppliers
I = range(len(products))
J = range(len(suppliers))

# Create Model
model = pe.ConcreteModel()

# Decsion Variables
model.x = pe.Var(I, J, domain = pe.Integers)
model.y = pe.Var(J, domain = pe.Binary)

# Total Production Cost function equation
ProductCost = sum(model.x[i, j] * suppliers[j][1][i] for j in J for i in I)
SupSelectCost = sum(model.y[j]*suppliers[j][4] for j in J)
VarSupCost = sum(model.x[i, j] * suppliers[j][5] for j in J for i in I)
HoldCost = sum(model.x[i, j] * suppliers[j][1][i] * products[i][5] / 2 for j in J for i in I)
TransCost = sum((suppliers[j][6] * model.x[i, j] * products[j][3])/(suppliers[j][7]) for j in J for i in I)

TotalCost = ProductCost + SupSelectCost + VarSupCost + HoldCost + TransCost

# SSPV function equation
SusScore = sum(model.x[i, j] * suppliers[j][8] for i in I for j in J) 

# Model Constraints
model.demand = pe.ConstraintList()
for i in I:
    lhs1 = sum(model.x[i, j] for j in J)
    rhs1 = products[i][0]
    model.demand.add(lhs1 == rhs1)

model.delivery = pe.ConstraintList()
for i in I:
    lhs2 = sum((model.x[i, j]) * (1-suppliers[j][3][i]) for j in J)
    rhs2 = (1-products[i][1])*products[i][0]
    model.delivery.add(lhs2 <= rhs2)

model.quality = pe.ConstraintList()
for i in I:
    lhs3 = sum(model.x[i, j]*suppliers[j][2][i] for j in J)
    rhs3 = products[i][2] * products[i][0]
    model.quality.add(lhs3 <= rhs3)
  
model.capacity = pe.ConstraintList()
for i in I:
    for j in J:
        lhs4 = (model.x[i, j])
        rhs4 = (suppliers[j][0][i])
        model.capacity.add(lhs4 <= rhs4)
    
model.storage = pe.ConstraintList()
lhs5 = sum(model.x[i, j]*products[i][4] for i in I for j in J)
rhs5 = 100
model.storage.add(lhs5 <= rhs5)

model.binC = pe.ConstraintList()
for j in J:
    lhs6 = model.y[j]*sum(products[i][0] for i in I)
    rhs6 = sum(products[i][0] for i in I)
    model.binC.add(lhs6 == rhs6)

# TPC + SSPV objective function creation
model.SSPV = pe.Var()
model.TPC = pe.Var()

model.SSPV_C = pe.Constraint(expr = model.SSPV == SusScore)
model.TPC_C = pe.Constraint(expr = model.TPC == TotalCost)

model.SSPV_O = pe.Objective(expr = model.SSPV, sense = pe.maximize)
model.TPC_O = pe.Objective(expr = model.TPC, sense = pe.minimize)

model.SSPV_O.deactivate()

#Conventional LP Payoff Table
ConPayoffTable = []

solver = pe.SolverFactory('cplex')
solver.solve(model);

print( '(X11 , X21) = (' + str(pe.value(model.x[0,0])) + ', ' + str(pe.value(model.x[1,0])) + ')')
print( '(X12 , X22) = (' + str(pe.value(model.x[0,1])) + ', ' + str(pe.value(model.x[1,1])) + ')')
print( 'TPC = ' + str(pe.value(model.TPC)) )
print( 'SSPV = ' + str(pe.value(model.SSPV)) )


SSPV_NIS = pe.value(model.SSPV)
TPC_PIS = pe.value(model.TPC)

model.SSPV_O.activate()
model.TPC_O.deactivate()

# Creating Conventional payoff table
ConPayoffTable.append({'Objective Function':"Min TPC",\
                                'TPC': round(pe.value(model.TPC)),\
                                'SSPV': round(pe.value(model.SSPV),2),\
                                'X[1][1]': round(pe.value(model.x[0, 0])),\
                                'X[2][1]': round(pe.value(model.x[1, 0])),\
                                'X[1][2]': round(pe.value(model.x[0, 1])),\
                                'X[2][2]': round(pe.value(model.x[1, 1]))})

solver.solve(model);
print( '(X11 , X21) = (' + str(pe.value(model.x[0,0])) + ', ' + str(pe.value(model.x[1,0])) + ')')
print( '(X12 , X22) = (' + str(pe.value(model.x[0,1])) + ', ' + str(pe.value(model.x[1,1])) + ')')
print( 'TPC = ' + str(pe.value(model.TPC)) )
print( 'SSPV = ' + str(pe.value(model.SSPV)) )

SSPV_PIS = pe.value(model.SSPV)
TPC_NIS = pe.value(model.TPC)

# Creating Conventional payoff table
ConPayoffTable.append({'Objective Function':"Max SSPV",\
                                'TPC': round(pe.value(model.TPC)),\
                                'SSPV': round(pe.value(model.SSPV),2),\
                                'X[1][1]': round(pe.value(model.x[0, 0])),\
                                'X[2][1]': round(pe.value(model.x[1, 0])),\
                                'X[1][2]': round(pe.value(model.x[0, 1])),\
                                'X[2][2]': round(pe.value(model.x[1, 1]))})

# Creating payoff table obtained by a conventional LP optimizer
ConPayoffTable_df = pd.DataFrame.from_dict(ConPayoffTable)

print('Each iteration will keep SSPV lower than some values between SSPV_min and SSPV_max, so ['       + str(SSPV_NIS) + ', ' + str(SSPV_PIS) + ']')
l = 25
r = (SSPV_PIS - SSPV_NIS)
step = (r / l)
steps = list(np.arange(SSPV_NIS,SSPV_PIS, step)) + [SSPV_PIS]

TPC_PIS_r = round(TPC_PIS)
TPC_NIS_r = round(TPC_NIS)
SSPV_PIS_r = round(SSPV_PIS,2)
SSPV_NIS_r = round(SSPV_NIS,2)

# apply augmented Epsilon-Constraint

# Min TPC + delta*epsilon
# st SSPV - s = e  

model.del_component(model.TPC_O)
model.del_component(model.SSPV_O)

model.e = pe.Param(initialize=0, mutable=True)

model.delta = pe.Param(initialize=0.00001)

model.s = pe.Var(within = pe.NonNegativeReals)

model.TPC_O = pe.Objective(expr = model.TPC - model.delta * model.s, sense=pe.minimize)

model.C_e = pe.Constraint(expr = model.SSPV - model.s == model.e)

TPC_l = []
SSPV_l = []
x11_l = [] #P1S1
x21_l = [] #P2S1
x12_l = [] #P1S2
x22_l = [] #P2S2

for s in steps:
    model.e = s
    solver.solve(model);
    TPC_l.append(pe.value(model.TPC))
    SSPV_l.append(pe.value(model.SSPV))
    x11_l.append(pe.value(model.x[0,0]))
    x21_l.append(pe.value(model.x[1,0]))
    x12_l.append(pe.value(model.x[0,1]))
    x22_l.append(pe.value(model.x[1,1]))

plt.plot(x11_l, x21_l, 'bo--', label = 'Efficient solutions')
plt.ylabel('X21')
plt.xlabel('X11')
plt.title('Solutions for Supplier 1')
plt.grid(True)
plt.show()

plt.plot(x12_l, x22_l,'go--', label = 'Efficient solutions')
plt.ylabel('X22')
plt.xlabel('X12')
plt.title('Solutions for Supplier 2')
plt.grid(True)
plt.show()

plt.plot(TPC_l, SSPV_l, 'ro--', label = 'Pareto front')
plt.ylabel('SSPV');
plt.xlabel('TPC');
plt.legend()
plt.grid(False)
plt.text(310000, 85000, 'Feasible domain', bbox=dict(boxstyle="square", facecolor = 'white', edgecolor = 'white'))
plt.text(309400, 86000, 'Infeasible domain', bbox = dict(boxstyle="square", facecolor = 'white', edgecolor = 'white'))
plt.annotate('Single optimisation - Min TPC',
            xy=(TPC_PIS, SSPV_NIS), xycoords = 'data',
            xytext=(309400, SSPV_NIS), textcoords = 'data',
            arrowprops = dict(arrowstyle="->"))
plt.annotate('Single optimisation - Max SSPV',
            xy=(TPC_NIS, SSPV_PIS), xycoords = 'data',
            xytext=(309600, SSPV_PIS), textcoords = 'data',
            arrowprops = dict(arrowstyle="->",))
plt.show() 

# Rounding TPC and SSPV solutions
TPC_r = [round(num) for num in TPC_l]    
SSPV_r = [round(num,2) for num in SSPV_l]

TPC_a = []

for i in range(len(TPC_l)):
    if TPC_l[i] <= TPC_PIS:
        TPC_a.append(1)
    elif TPC_l[i] < TPC_NIS:
        a = (TPC_NIS - TPC_l[i])/(TPC_NIS - TPC_PIS)
        TPC_a.append(a)
    else:
        TPC_a.append(0)

SSPV_a =[]

for i in range(len(SSPV_l)):
    if SSPV_l[i] < SSPV_NIS:
        SSPV_a.append(0)
    elif SSPV_l[i] < SSPV_PIS:
        a = (SSPV_l[i] - SSPV_NIS)/(SSPV_PIS - SSPV_NIS)
        SSPV_a.append(a)
    else:
        SSPV_a.append(1)
        
TVSP_l_a = []
TVSP_l_c = []
TVSP_l_e = []

for i in range(len(TPC_a)):
    a = 0.4*TPC_a[i] + 0.6*SSPV_a[i]
    TVSP_l_a.append(a)
    c = 0.5*TPC_a[i] + 0.5*SSPV_a[i]
    TVSP_l_c.append(c)
    e = 0.6*TPC_a[i] + 0.4*SSPV_a[i]
    TVSP_l_e.append(e)
    
# Rounding solutions    
TVSP_r_a = [round(num,3) for num in TVSP_l_a]
TVSP_r_c = [round(num,3) for num in TVSP_l_c]
TVSP_r_e = [round(num,3) for num in TVSP_l_e]
x11_l_r = [round(num) for num in x11_l] 
x21_l_r = [round(num) for num in x21_l] 
x12_l_r = [round(num) for num in x12_l] 
x22_l_r = [round(num) for num in x22_l] 

results = {
    'Min TPC': TPC_r,
    'Max SSPV': SSPV_r,
    'X11': x11_l_r,
    'X21': x21_l_r,
    'X12': x12_l_r,
    'X22': x22_l_r,
    'TVSP w1 = 0.4': TVSP_r_a,
    'TVSP w1 = 0.5': TVSP_r_c,
    'TVSP w1 = 0.6': TVSP_r_e,
    }

pd.set_option("display.max_rows", None, "display.max_columns", None) 
results_df = pd.DataFrame.from_dict(results)
print(results_df)


with pd.ExcelWriter('SSSOA Results Rounded.xlsx') as writer:
     ConPayoffTable_df.to_excel(writer, sheet_name='Sheet1')
     results_df.to_excel(writer, sheet_name='Sheet2')
