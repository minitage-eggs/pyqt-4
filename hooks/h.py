import os
import re
import shutil
import subprocess
import sys
from distutils.sysconfig import get_python_lib


def which(program, environ=None, key = 'PATH', split = ':'):
    if not environ:
        environ = os.environ
    PATH=environ.get(key, '').split(split)
    for entry in PATH:
        fp = os.path.abspath(os.path.join(entry, program))
        if os.path.exists(fp):
            return fp
        if (sys.platform.startswith('win') or sys.platform.startswith('cyg'))  and os.path.exists(fp+'.exe'):
            return fp+'.exe'
    raise IOError('Program not fond: %s in %s ' % (program, PATH)) 


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

def h(options, buildout, opts):
    """Patch Makefile to point to our site packages."""
    cwd = os.getcwd()
    md = options['compile-directory']
    c = os.path.join(md, 'configure.py')
    os.chdir(md)
    qmake = get_qmake()
    opts = ' '.join(opts.split())
    py = buildout['buildout']['executable']
    if not  py.startswith('/'):
        py = which(py)
    includes = os.path.join(sys.prefix, 'includes')
    lib = os.path.join(sys.prefix, 'lib')
    sp = get_python_lib()
    sip = os.path.join(get_python_lib(), 'sip')
    qsci = os.path.join(get_python_lib(), 'qsci')
    bins = os.path.join(sys.prefix, 'bin')
    opts += " -d %s" % sp
    opts += " -b %s" % bins
    opts += " -n %s" % qsci
    cmd = [py, c, opts]
    if qmake:
        cmd.extend(['-q', qmake])
    scmd = ' '.join(cmd)
    print "Running: %s" % scmd
    ret = os.system(scmd)
    if ret > 0: raise Exception,('Cannot confiure')
    os.chdir(cwd)

def h_27(options,buildout):
    """Patch Makefile to point to our site packages."""
    opts = ' '.join(options['configure-options'].split())
    h(options, buildout, opts)  
# vim:set ts=4 sts=4 et  :
