# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 02:03:31 2018

@author: Nicolas
"""
import math
from numpy import linalg as LA
import numpy as np
#el modelo ocupado debe estar seteado con min count 1 o sino no agregara palabras nuevas por aparecer una vez
def cos_angle(u,v):
    norm_u= LA.norm(u)
    norm_v= LA.norm(v)
    norm_u_v= LA.norm(u-v)
    x= norm_u*norm_v
    out= 0.5*((norm_u/norm_v)+(norm_v/norm_u)- (math.pow(norm_u_v,2.0)/(x)))
    return out
    
    