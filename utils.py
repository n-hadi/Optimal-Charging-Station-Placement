import numpy as np

def distance2penalty(dist):
    #-e^(x-2.4)+1.091
    #result = -np.exp(dist - 2.4) + 1.091
    result = (np.exp(dist/1000) - 1) / (1 - np.exp(2.5)) + 1
    return result if result > 0 else 0

def getPenaltyMx(distance_mx):
 for j, demand_location in enumerate(distance_mx):
  for k, distance in enumerate(demand_location):
   distance_mx[j][k] = distance2penalty(distance)
 return distance_mx

 