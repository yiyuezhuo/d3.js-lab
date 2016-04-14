# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:40:28 2016

@author: yiyuezhuo
"""
import pickle
import os

class System(object):
    def __init__(self,endog,exog,arg,endog_map=None,arg_bind=None):
        self.endog=endog
        self.exog=exog
        self.arg=arg
        self.var=endog+exog+arg
        self._endog={var.__repr__():var for var in self.endog}
        self._exog={var.__repr__():var for var in self.exog}
        self._arg={var.__repr__():var for var in self.arg}
        self._var={var.__repr__():var for var in self.var}
        self.arg_bind=arg_bind
        self.exog_bind=None
        self.endog_map=endog_map
    def _bind(self,dic):
        return {self._var[skey]:value for skey,value in dic.items()}
    def bind_arg(self,dic):
        self.arg_bind=self._bind(dic)
    def show(self):
        print('endog',*self._endog)
        print('exog',*self._exog)
        print('arg',*self._arg)
    def solve(self,exog_bind,arg_bind=None):
        if not arg_bind:
            arg_bind=self.arg_bind
        exog_bind=self._bind(exog_bind)
        return {var.__repr__():float(mapping.subs(self.arg_bind).subs(exog_bind)) for var,mapping in self.endog_map.items()}
    def dump(self,name='system_cache'):
        data=[self.endog,self.exog,self.arg,self.endog_map,self.arg_bind]
        with open(name,'wb') as f:
            pickle.dump(data,f)
    @staticmethod
    def load(name='system_cache'):
        with open(name,'rb') as f:
            args=pickle.load(f)
        obj=System(*args)
        return obj

def example():
    from model_solve2 import map_y_P_c_i_r_N_W_L1_L2_h_f,exog,endog,arg
    
    system=System(endog,exog,arg,map_y_P_c_i_r_N_W_L1_L2_h_f)
    
    arg_bind={"Ca":1000,
    "Cb":0.8,
    "ia":10000,
    "ib":5000,
    "L1a":100,
    "L1b":0.1,
    "L2a":1000,
    "L2b":500,
    "fa":0,
    "fb":1,
    "ha":1000,
    "hb":1,
    "ya":10,
    "yb":1}
    
    exog_bind={'g':100,'t':110,'kbar':100,'M':100}
    
    system.bind_arg(arg_bind)
    
    print(system.solve(exog_bind))
    system.dump()
    return system
    
def load(fname='system_cache'):
    if os.path.isfile(fname):
        return System.load(fname)
    else:
        return example()
    
print(__name__)
if __name__=='__main__':
    #system=example()
    system=load()