import datetime
import json
import os
import math

__author__ = 'pf'

def std(X):
    xbar = sum(X) / float(len(X))
    return math.sqrt(sum((x - xbar)**2 for x in X)/(len(X) - 1))

def mean(array):
    return float(sum(array))/len(array)


def strongtype(method):
    """
    Decorator for strong-typing methods.

    Usage:

    >>> @strongtype
    ... def foo(a, b = int, c = float):
    ...     print a, type(a)
    ...     print b, type(b)
    ...     print c, type(c)
    ...
    ... foo(a ='1',  c= 3, b = 32)
    1 <type 'str'>
    32 <type 'int'>
    3.0 <type 'float'>

    """

    import inspect
    args, varargs, keywords, defaults = inspect.getargspec(method)

    nargs = len(args) - len(defaults) # number of normal arguments in the method definition

    types = dict((_kw, _type) for _kw, _type in zip(args[nargs:], defaults)) # a dictionary holding the (arg_name, type) mapping

    def new_method(*cur_args, **cur_kwargs):

        # assume that if cur_args contains more elements than nargs then the remainder of it (cur_args[nargs:]) contains keyword arguments
        # that were not stated explicitly. For example, if the definition of the method is "def foo(a, b = int)" a call like "foo('1','2')" would map the
        # value '2' to the definition of argument "b".
        cur_args = list(cur_args[:nargs]) + [types[_kw](_val) for _kw, _val in zip(args[nargs:], cur_args[nargs:])]

        method(*cur_args,
            **dict((_kw, types.get(_kw, lambda x: x)(_val)) # cast the keyword arguments
            for _kw, _val in cur_kwargs.items()))

    return new_method

    
def revcomp(sequence):
    """ Reverse complement of the sequence"""
    return ''.join(revcomp.rc_dict.get(c, c) for c in reversed(sequence.upper()))
revcomp.rc_dict = {'A' : 'T', 'T' : 'A', 'G' : 'C', 'C' : 'G'}

def logf(msg, logfname = None):
    if not hasattr(logf, 'logfile'):
      logf.logfile = open(logfname, 'w')
    logf.logfile.write((msg if isinstance(msg, str) else json.dumps(msg)) +'\n')

global_stime = datetime.datetime.now()
def elapsed(msg = None):
    print "[%s]" % msg if msg is not None else "+", "Last:" , datetime.datetime.now() - elapsed.stime, '\tTotal:', datetime.datetime.now() - global_stime
    elapsed.stime = datetime.datetime.now()

elapsed.stime = datetime.datetime.now()


def partial_overlap(s1, e1, s2, e2):
    return s1 <= e2 and s2 <= e1 #and min(e1, e2) - max(s1, s2) >= 10

def total_overlap(s1, e1, s2, e2):
    return s1 <= s2 and e1 >= e2 or s2 <= s1 and e2 >= e1


# set a reasonable defaults
def find_location(program):
    """ Finds the location of the executable 'program' by looking it up in the system path """
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        if is_exe(os.path.join(path, program)):
            return path

    return None
    
    

def error(msg):
    """ Prints an error message and exits """
    print 'ERROR: %s' % msg
    exit(1)
