#-*- coding:utf-8 -*-

import wx

import template



class WXTemplate(template.XMLTemplate):

    def getDefaultNamespace(self):

        ns = super(WXTemplate, self).getDefaultNamespace()

        ns.update(sizer=None,
                  sizerParam={},
                  wx=wx,)

        return ns


    def _parseControl(self, tree, parent, namespace):

        ignores = ['key', 'methods']

        tag = template.title(tree.tag)
        attr = template.getAttrs(tree)

        cls = getattr(wx, tag)

        name = attr.get('key')
        calls = attr.get('methods')

        argd = template.expandAttr(attr, namespace, ignores)

        ctrl = cls(parent=parent, **argd)

        sizer = namespace.get('sizer')

        if sizer is not None:
            param = namespace.get('sizerParam')
            sizer.Add(ctrl, **param)

        if calls:
            template.callMethods(ctrl, namespace, calls)

        if name:
            self[name] = ctrl

        ns = dict(namespace,
                  here=ctrl,
                  parent=ctrl,
                  sizer=None)

        self._parseChild(tree, ctrl, namespace)


    def _parseSizer(self, tree, parent, namespace):

        ignores = ['methods']

        tag = template.title(tree.tag)
        
        attr = template.getAttrs(tree)

        calls = attr.get('methods')
        
        cls = getattr(wx, tag)

        argd = template.expandAttr(attr, namespace, ignores)

        sizer = cls(**argd)

        psizer = namespace.get('sizer')

        if psizer is not None:
            param = namespace.get('sizerParam')

            psizer.AddSizer(sizer, **param)

        else:
            parent.SetSizer(sizer)

        if calls:
            template.callMethods(ctrl, namespace, calls)

        ns = dict(namespace,
                  sizer=sizer,
                  sizerParam={})

        self._parseChild(tree, parent, ns)


    def _parseSizerParam(self, tree, parent, namespace):

        param = namespace.get('sizerParam', {})

        attr = template.getAttrs(tree)
        
        argd = template.expandAttr(attr, namespace, [])

        param.update(argd)

        namespace['sizerParam'] = param

        self._parseChild(tree, parent, namespace)
       

    def _parseTag(self, tree, parent, namespace):

        tag = tree.tag.lower()

        if 'sizerparam' == tag:
            self._parseSizerParam(tree, parent, namespace)
        elif 'sizer' in tag:
            self._parseSizer(tree, parent, namespace)
        else:
            self._parseControl(tree, parent, namespace)    


