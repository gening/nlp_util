import sys

import codecs
from os import path

if sys.version_info[0] == 2:  # python 2
    # noinspection PyCompatibility,PyUnresolvedReferences
    from ConfigParser import ConfigParser
elif sys.version_info[0] == 3:  # python 3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from configparser import ConfigParser
# SafeConfigParser supports interpolation.
# This means values can contain format strings which refer to other values in the same section,
# or values in a special DEFAULT section.
"""
For example:

[My Section]
foodir: %(dir)s/whatever
dir=frob
long: this value continues
   in the next line
   
would resolve the %(dir)s to the value of dir (frob in this case).

Note:
For Python 3.3, one can use the expression `${section:option}` in the config file.
>>> config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
Please see: https://docs.python.org/3.6/library/configparser.html
To make Python 2.7 compatible, one need: from backports import configparser
"""


def conf(conf_filename):
    config = ConfigParser()
    with codecs.open(path.join(path.dirname(__file__), 'conf', conf_filename),
                     'r', encoding='utf-8') as f:
        config.readfp(f)
    # if not config.has_section('default'):
    #    config.add_section('default')
    if not config.has_option('DEFAULT', 'data_dir'):
        data_dir = path.join(path.dirname(__file__), 'data')
        config.set('DEFAULT', 'data_dir', data_dir)
    return config
