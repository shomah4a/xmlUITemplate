#-*- coding:utf-8 -*-

import sys
from lxml import etree
import abc


def loadModule(name):
    '''
    モジュール読み込み
    '''

    mod = __import__(name)

    return reduce(lambda x, y: getattr(x, y), name.split('.'), mod)



class Module(object):
    '''
    モジュール読み込むためのアレ
    '''

    def __getitem__(self, modname):

        return loadModule(modname)

    __call__ = __getitem__



def title(s):

    return s[0].upper() + s[1:]



stringEval = lambda x, ns: x



def pythonEval(s, ns):

    try:
        return eval(s, ns)
    except Exception, e:
        print >> sys.stderr, '%s: An error occured in evaluating "%s"' % (type(e).__name__, s)
        raise



evalTable = dict(str=stringEval,
                 py=pythonEval,
                 python=pythonEval)



def evalAttr(at, namespace=None):

    if namespace is None:
        namespace = globals()
    
    s = at.split(':', 1)

    if len(s) == 1:
        return at

    else:
        func = evalTable.get(s[0])

        if func is None:
            raise ValueError('Invalid eval type "%s"' % s[0])

        return func(s[1], namespace)



def evalDefines(s, namespace):

    if not s:
        return namespace

    n = namespace.copy()

    for k, v in (x.strip().split(None, 1) for x in s.split(';')):
        n[k] = evalAttr(v)

    return n



def parseNS(name, map):

    s = name.replace('{', '').split('}')

    if len(s) == 1:
        return s[0]

    ns, n = s

    return ':'.join([map.get(ns), n])



def getAttrs(et):

    mp = dict((v, k) for k, v in et.nsmap.iteritems())    

    return dict((parseNS(k, mp), v) for k, v in et.attrib.iteritems())



def expandAttr(d, ns, ignores):

    argd = dict((str(k), evalAttr(v, ns))
                for k, v in d.iteritems()
                if k.lower() not in ignores)

    return argd



def callMethods(tgt, ns, callstrings):

    uns = dict(ns,
               target=tgt,
               self=tgt)

    calls = [x.strip().split(None, 1) for x in callstrings.split(';') if x]

    print calls

    for method in ['target.%s(%s)' % (title(x[0]), x[1]) for x in calls]:
        pythonEval(method, uns)



class XMLTemplate(dict):
    '''
    Abstract class for GUI Template
    '''

    __metaclass__ = abc.ABCMeta
    

    def __init__(self, filelike=None, xmlstr=None, parent=None):

        if filelike:
            parsed = etree.parse(filelike).getroot()
        elif xmlstr:
            parsed = etree.fromstring(xmlstr)

        self._parse(parsed, parent, namespace=self.getDefaultNamespace())



    def getDefaultNamespace(self):

        ret = dict(__builtins__,
                   modules=Module(),
                   parent=None,
                   here=None,
                   sizer=None,
                   sizerParam={})

        return ret


    def _parseUITL(self, tree, parent, namespace):

        attr = getAttrs(tree)
        
        defs = attr.get('define')
        execute = attr.get('execute')

        ns = evalDefines(defs, namespace)

        if execute:
            exec execute in ns

        self._parseChild(tree, parent, ns)


    @abc.abstractmethod
    def _parseTab(self, tree, parent, namespace):
        pass
        

    def _parse(self, tree, parent=None, namespace={}):

        parseTbl = dict(uitl=self._parseUITL)

        tag = tree.tag

        parseTbl.get(tag, self._parseTag)(tree, parent, namespace)


    def _parseChild(self, tree, parent, namespace):

        for child in tree.getchildren():
            self._parse(child, parent, namespace)


    def __getattr__(self, attr):

        if attr in self:
            return self[attr]

        err = "'%s' object has no attribute '%s'" % (self.__class__.__name__,
                                                     attr)
        raise AttributeError, err
 
