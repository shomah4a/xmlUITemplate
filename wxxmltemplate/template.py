#-*- coding:utf-8 -*-

from lxml import etree
import wx



def title(s):

    return s[0].upper() + s[1:]



stringEval = lambda x: x


def pythonEval(s):

    return eval(s)



evalTable = dict(str=stringEval,
                 py=pythonEval)



def evalAttr(s):

    s = s.split(':', 1)

    if len(s) == 1:
        return s

    else:
        func = evalTable.get(s[0])

        if func is None:
            raise ValueError('Invalid eval type "%s"' % s[0])

        return func(s[1])    



class XMLTemplate(dict):

    def __init__(self, filelike=None, xmlstr=None):

        if filelike:
            parsed = etree.parse(filelike)
        elif xmlstr:
            parsed = etree.fromstring(xmlstr)

        self._parse(parsed)


    def _parse(self, tree, parent=None, parm={}):

        print tree.tag

        tag = title(tree.tag)
        attr = tree.attrib

        cls = getattr(wx, tag)

        name = attr.get('name')

        argd = dict((str(k), evalAttr(v))
                    for k, v in attr.iteritems()
                    if k != 'name')

        ctrl = cls(parent=parent, **argd)

        if name:
            self[name] = ctrl

        self._parseChild(tree, ctrl, {})


    def _parseChild(self, tree, parent, parm):

        for child in tree.getchildren():
            self._parse(child, parent, parm)


    def __getattr__(self, attr):

        if attr in self:
            return self[attr]

        err = "'%s' object has no attribute '%s'" % (self.__class__.__name__,
                                                     attr)
        raise AttributeError, err
 
