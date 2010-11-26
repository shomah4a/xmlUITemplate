#-*- coding:utf-8 -*-

import template


def fromString(str):

    return template.XMLTemplate(xmlstr=str)



def test():

    import wx
    app = wx.App(redirect=False)
    
    ret = fromString('''<frame name="window">
  <button name="button" label="str:click me" />
</frame>''')

    print ret.window
    print ret.button

    ret.window.Show()

    app.MainLoop()

    return ret


if __name__ == '__main__':
    test()
