# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:55:20 2016

@author: yiyuezhuo
"""

from sympy import S, Eq, solve,Symbol,simplify

'''arg'''
Ca,Cb,ia,ib,L1a,L1b,L2a,L2b=S('Ca,Cb,ia,ib,L1a,L1b,L2a,L2b'.split(','))
fa,fb,ha,hb,ya,yb=S('fa,fb,ha,hb,ya,yb'.split(','))

arg=[Ca,Cb,ia,ib,L1a,L1b,L2a,L2b,fa,fb,ha,hb,ya,yb]

'''exog'''
g,kbar,t,M=S('g,kbar,t,M'.split(','))

exog=[g,kbar,t,M]

'''endog'''
y,c,i,r,P,N,L1,L2,f,h,W=S('y,c,i,r,P,N,L1,L2,f,h,W'.split(','))
N=Symbol('N')

endog=[y,c,i,r,P,N,L1,L2,f,h,W]


'''equations function hypothesis'''
c_y_t=Eq(c,Ca+Cb*(y-t))
i_r=Eq(i,ia-ib*r)
L1_y=Eq(L1,L1a+L1b*y)
L2_r=Eq(L2,L2a-L2b*r)
f_N=Eq(f,fa+fb*N)
h_N=Eq(h,ha-hb*N)
f_h=Eq(f,h)
#y_N_kbar=Eq(y,ya+yb*N*kbar)

#equs_hypo=[c_y_t,i_r,L1_y,L2_r,h_N,y_N_kbar]

'''equations main'''
y_=Eq(y,c+i+g)
P_=Eq(P,M/(L1+L2))
f_=Eq(f,W/P)
y__=Eq(y,ya+yb*N*kbar)


'''IS curve'''

map_y_c_i=solve([c_y_t,y_,i_r],[y,c,i])

'''LM curve'''

map_y_L1_L2=solve([L1_y,L2_r,P_],[y,L1,L2])

'''total demand curve'''

map_y_r=solve([Eq(y,map_y_c_i[y]),Eq(y,map_y_L1_L2[y])],[y,r])

map_y_c_i_={key:map_y_c_i[key].subs({r:map_y_r[r]}) for key in [y,c,i]}
map_y_L1_L2_={key:map_y_L1_L2[key].subs({r:map_y_r[r]}) for key in [y,L1,L2]}

map_y_c_i_L1_L2={}
map_y_c_i_L1_L2.update(map_y_c_i_)
map_y_c_i_L1_L2.update(map_y_L1_L2_)

'''total supply curve'''

map_y_W_N_f_h=solve([f_N,h_N,f_h,f_,y__],[y,W,N,f,h],dict=True)[0]

'''do it!'''

map_y_P=solve([Eq(y,map_y_W_N_f_h[y]),Eq(y,map_y_c_i_L1_L2[y])],[y,P],dict=True)[0]

map_y_P_c_i_N_W_L1_L2_h_f={}
map_y_P_c_i_N_W_L1_L2_h_f.update(map_y_P)
#map_y_P_c_i_N_W_L1_L2_h_f[c]=map_y_c_i_L1_L2[c].subs(map_y_P)
map_y_P_c_i_N_W_L1_L2_h_f.update({key:map_y_c_i_L1_L2[key].subs(map_y_P) for key in [c,i,L1,L2]})
map_y_P_c_i_N_W_L1_L2_h_f.update({key:map_y_W_N_f_h[key].subs(map_y_P) for key in [W,N,f,h]})

map_y_P_c_i_N_W_L1_L2_h_f={key:simplify(value) for key,value in map_y_P_c_i_N_W_L1_L2_h_f.items()}

map_y_P_c_i_r_N_W_L1_L2_h_f={}
map_y_P_c_i_r_N_W_L1_L2_h_f.update(map_y_P_c_i_N_W_L1_L2_h_f)
map_y_P_c_i_r_N_W_L1_L2_h_f[r]=simplify(map_y_r[r].subs({P:map_y_P_c_i_N_W_L1_L2_h_f[P]}))