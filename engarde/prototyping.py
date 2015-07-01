
from types import BooleanType, ObjectType

from pandas import Dataframe

from slicers import ix, iloc, loc

from copy import copy

class CheckSet(object):
    def __init__(self, ret=None, raize=None, raize_msg_or_kwargs=None):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ret or (Dataframe, BooleanType, ObjectType)
        self.raize = raize or AssertionError
        if isinstance(raize_msg_or_kwargs, (str, unicode)):
            self.raize_kwargs = {'msg' : raize_msg_or_kwargs}
        else:
            assert isinstance(raize_msg_or_kwargs, dict)
            self.raize_kwargs = raize_msg_or_kwargs

    @staticmethod
    def _acheck_raize(dforig, dfcheck, dfderive, *args, **kwargs):
        
        # pull out _raize _raize_kwargs 
        
        #dologicchecklogic, raising when necessary...
        # if False:
        #     _raize(**_raize_kwargs)
        return dforig
        
    @staticmethod
    def _acheck_ret(dforig, dfcheck, dfderive, *args, **kwargs):
        
        # pull out _ret
        
        #dologicchecklogic, calculating as necessary...
        return (dforig,) # ... a function of _ret)
        
    def acheck(self, df, slc, slcd, *args, **kwargs):
        
        # pull out ...from kwargs
        #       ix = None, iloc = None, loc = None,
        #       ix_d=None, iloc_d=None, loc_d=None
        
        #detect if slc and slcd belong at the front of 
        #args, add if they do, otherwise, do something like this...
        
        # (NOTE: PSEUDO Only...)
        #df1 = df.ix|iloc|loc[self.check_slc.slc] or df
        #df2 = df.ix|iloc|loc[self.derive_slc.slc] or df

        if self.raize is not None:
            result = self._acheck_raize(df, df1, df2, *args, _raize=self.raize, _raize_kwargs=self.raize_kwargs, **kwargs)
        elif self.ret is not None:
            result = self._acheck_ret(df, df1, df2, *args, _ret=self.ret, **kwargs)
        else:
            raise Exception("Can't read your mind")
        
        return result

if __name__ == '__main__':
    class Jeff(object):
        def __init__(self):
            self.name = "McLarty"
        def amethod(self, x=5):
            print x
            return x + 1
        @staticmethod
        def amethod(self, x=5):
            print x
            return x + 1
            
    def afunc(self, x=7):
        return x + 4
        
    
    jeffsmethod = Jeff.amethod
    
    ajeffsmethod = Jeff().amethod
    
    
    def checkit(obj):
        print isinstance(obj, types.FunctionType)
        print isinstance(obj, types.UnboundMethodType)
        print isinstance(obj, types.MethodType)
    
    checkit(afunc)
    
    checkit(jeffsmethod)
    
    checkit(ajeffsmethod)
