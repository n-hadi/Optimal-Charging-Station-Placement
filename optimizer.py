#!/usr/bin/env python3.11

import gurobipy as gp
from gurobipy import GRB
from utils import getPenaltyMx
from data import demand_mx, distance_mx

d = demand_mx
p = getPenaltyMx(distance_mx)

demands = range(len(distance_mx)) 
cstations = range(len(distance_mx[0])) #charging stations

cpu = 15000 #cost per unit
budget = 120000
capacity = 9

try:
    m = gp.Model("ChargingStationProblem")

    z = m.addVars(demands,cstations, lb=0, ub=1, name="gedeckte Nachfrage") #(6)
    x = m.addVars(cstations, vtype=GRB.BINARY, name="Aufstellungsvariable") #(7)
    
    m.setObjective(sum(d[j]*z[j,k]*p[j][k] for j in demands for k in cstations), GRB.MAXIMIZE) #(1)

    m.addConstrs(sum(d[j]*z[j,k] for j in demands) <= capacity for k in cstations) #(2)
    
    m.addConstrs(sum(z[j,k] for k in cstations) <= 1 for j in demands) #(3)

    m.addConstrs(z[j,k] <= x[k] for j in demands for k in cstations) #(4)

    m.addConstr(sum(cpu*x[k] for k in cstations) <= budget) #(5)

    m.optimize()

    for v in m.getVars():
        print(f"{v.VarName} = {v.X}")
    
    demand_covered = 0
    for key, var in z.items():
        if "gedeckte Nachfrage" in var.VarName:
            demand_covered += demand_mx[key[0]]*var.X
    print(f"Gedeckte NF absolut: {demand_covered}/{sum(demand_mx)} = {demand_covered*100/sum(demand_mx)}%")
    print(f"Zielwert = {m.ObjVal}")

        
except gp.GurobiError as e:
    print(f"Error code {e.errno}: {e}")

except AttributeError as e:
    print("Encountered an attribute error")
    print(e)