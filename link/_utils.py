import os
import json

import warnings

from itertools import izip, chain, repeat
# -*- coding: utf-8 -*-

"""
link.utils
~~~~~~~~~~~~

Commonly used utility functions in the link code

:copyright: (c) 2013 by David Himrod
:license: Apache2, see LICENSE for more details.

"""

def load_json_file(file_name):
    """
    given a file name this function will json decode it and
    return a dictionary
    
    Raises exception if the file does not exist
    """
    data = open(file_name, 'r').read()

    try:
        return json.loads(data)
    except Exception as e:
        raise ValueError("Error json decoding file: %s error: %s" % (file_name,
                                                                     e.message))

def list_to_dataframe(rows, names):
    """
    Turns a rows of data into a dataframe and gives them the column names
    specified

    :params rows: the data you want to put in the dataframe
    :params names: the column names for the dataframe
    """
    from pandas import DataFrame
    try:
        import pandas._tseries as lib
    except ImportError:
        import pandas.lib as lib

    if isinstance(rows, tuple):
        rows = list(rows)

    columns = dict(zip(names, lib.to_object_array_tuples(rows).T))

    for k, v in columns.iteritems():
        columns[k] = lib.convert_sql_column(v)

    return DataFrame(columns, columns=names)

def array_pagenate(n, iterable, padvalue=None):
    """
    takes an array like [1,2,3,4,5] and splits it into even chunks.  It will
    pad the end with your default value to make fully even.  
    """
    return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)

def deprecated(func):
    '''
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    '''
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func
 
