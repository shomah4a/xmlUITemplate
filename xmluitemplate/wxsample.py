#-*- coding:utf-8 -*-

import wx
import os
import glob
import functools

import wxtemplate

    
def test():

    app = wx.App(redirect=False)

    wnd = wxtemplate.WXTemplate(xmlstr='''
<uitl define="aaaa python:10;
              bbbb aaaa">
  <frame key="window">
    <boxSizer orient="py: wx.VERTICAL">

      <button key="button" label="str:aaaa" />

      <sizerParam flag="py:wx.EXPAND|wx.ALL" />

      <button key="button" label="str:bbbbb" />

      <boxSizer>
        <button key="button" label="str:cccccc" />
        <button key="button" label="py: str(aaaa)" />
      </boxSizer>

    </boxSizer>
  </frame>
</uitl>
''')

    wnd.window.Show()

    samplesSelector()

    app.MainLoop()



def launch(lst, *args):

    sel = lst.GetSelection()

    if sel == wx.NOT_FOUND:
        return

    path = lst.GetClientData(sel)

    ui = wxtemplate.WXTemplate(path)

    ui.window.Show()

    print path

   

def samplesSelector():

    sampledir = os.path.join(os.path.dirname(__file__), 'samples')
    sampletmpl = os.path.join(sampledir, 'wxsamples.xml')

    sampleui = wxtemplate.WXTemplate(sampletmpl)

    items = glob.glob(os.path.join(sampledir, 'wx_*.xml'))

    print items

    lst = sampleui.lstSamples

    for item in items:
        fn = os.path.splitext(os.path.basename(item))[0]
        lst.Insert(fn, lst.GetCount(), item)

    sampleui.btnLaunch.Bind(wx.EVT_BUTTON, functools.partial(launch, sampleui.lstSamples))
    sampleui.window.Show()

    return sampleui

    

if __name__ == '__main__':
    test()

