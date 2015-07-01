
from types import BooleanType, ObjectType

from pandas import DataFrame

from slicers import ix, iloc, loc, SliceStore

from functools import wraps
from copy import copy

def _acheck_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    try:
        _ret = kwargs['_ret']
    except KeyError:
        raise KeyError("_ret must be defined")
    
    if not isinstance(_ret, (list, tuple)):
        _ret = (_ret,)
    
    ret_specd = {'orig' : None, 'bool' : None, 'ndframe' : None, 'obj' : None}
    
    #dologicchecklogic, calculating as necessary...populating the 
    # above appropriate keys as necessary
    
    ret = [ret_specd[t] for t in _ret]
    return ret

def _acheck_raize(dforig, dfcheck, dfderive, *args, **kwargs):
    
    try:
        _raize = kwargs['_raize']
        _raize_kwargs = kwargs['_raize_kwargs']
    except KeyError:
        raise KeyError("_raize and _raize_kwargs must be defined")
    kwargs = {key : value for key, value in kwargs.iteritems() if key not in ('_raize', '_raize_kwargs')}

    #dologicchecklogic, raising when necessary...
    # or...to not duplicate code:

    _ret = ('bool',)
    result = _acheck_ret(dforig, dfcheck, dfderive, _ret=_ret, *args, **kwargs)
    
    if result:
        return dforig
    else:
        _raize(**_raize_kwargs)  

def _lop_off_head_if_slice(args, otherwise):
    if len(args) > 1:
        if isinstance(args[0], (slice, SliceStore)):
            if len(args) > 2:
                return args[0], args[1:]
            else:
                return otherwise, []
    else:
        return otherwise, []
                    
class CheckSet(object):
    def __init__(self, ret=None, raize=None, raize_msg_or_kwargs=None):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ret or ('ndframe', 'bool', 'obj')
        self.raize = raize or AssertionError
        if isinstance(raize_msg_or_kwargs, (str, unicode)):
            self.raize_kwargs = {'msg' : raize_msg_or_kwargs}
        else:
            if isinstance(raize_msg_or_kwargs, dict):
                self.raize_kwargs = raize_msg_or_kwargs
            else:
                #TODO make this better...
                self.raize_kwargs = {}
 
    def acheck(self, df, *args, **kwargs):
        
        #print self, df, args, kwargs
        
        slc, args = _lop_off_head_if_slice(args, self.check_slc)
        slcd, args = _lop_off_head_if_slice(args, self.derive_slc)    
        
        dfc = getattr(df, slc.mode)[slc.slc]
        dfd = getattr(df, slcd.mode)[slcd.slc]
        
        if self.raize is not None:
            result = _acheck_raize(df, dfc, dfd, 
                                   *args, _raize=self.raize, 
                                   _raize_kwargs=self.raize_kwargs, **kwargs)
        elif self.ret is not None:
            result = _acheck_ret(df, dfc, dfd, *args, _ret=self.ret, **kwargs)
        else:
            raise Exception("Can't read your mind")
        
        return result
    def decorator_maker(self, name, *args, **kwargs):
        def adecorator(*args, **kwargs):
            def decorate(func):
                @wraps(func)
                def wrapper(*wargs, **wkwargs):
                    result = func(*wargs, **wkwargs)
                    ans = getattr(self, name)(result, *args, **kwargs)
                    if ans:
                        result = [result] + list(ans)
                        result = tuple(result)
                    return result
                return wrapper
            return decorate
        return adecorator

acheck = CheckSet().acheck
acheck_dec = CheckSet().decorator_maker('acheck')
            
if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame(data=[1,2,3,4])
    
    acheck(df)
    
    @acheck
    def myfunc(df):
        return df + 1.0
