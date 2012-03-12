import os
import re
import shutil
import subprocess
import sys
from minitage.core.common import which


def get_qmake():
    qmake = ''
    try:
        qmake = which('qmake-qt4')
    except:
        qmake = which('qmake')
    return qmake

def install(options,buildout):
    """Installs only the python site-packages."""
    cwd = os.getcwd()
    #os.system("""
    #          cd %s
    #          cd python
    #          make install""" % options['compile-directory'])

    for d in 'include', 'man', 'lib', 'share', 'bin':
        if os.path.exists(
            os.path.join(options['location'], d)):
            shutil.rmtree(
                os.path.join(options['location'], d))
    os.chdir(cwd)

def h(options, buildout, version, opts):
    """Patch Makefile to point to our site packages."""
    cwd = os.getcwd()
    md = options['compile-directory']
    c = os.path.join(md, 'configure.py')
    os.chdir(md)
    p = buildout['p'][version]
    qmake = get_qmake()
    cmd = [p, c, opts]
    if qmake:
        cmd.extend(['-q', qmake])
    scmd = ' '.join(cmd)
    print "Running: %s" % scmd
    ret = os.system(scmd)
    if ret > 0: raise Exception,('Cannot confiure')
    os.chdir(cwd)

def h_26(options,buildout):
    """Patch Makefile to point to our site packages."""
    opts = ' '.join(options['configure-options'].split())
    h(options, buildout, '26', opts)
def h_24(options,buildout):
    """Patch Makefile to point to our site packages."""
    opts = ' '.join(options['configure-options'].split())
    h(options, buildout, '24', opts) 
# vim:set ts=4 sts=4 et  :
