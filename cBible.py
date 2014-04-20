#!/usr/bin/python2
# -*- coding: utf-8 -*-

import wx

class MainWindow ( wx.Frame ) :
    index={}
    loadedname=""
    def loadinfact(self,name,chap):
        self.loadedname=name
        self.contents.Clear()
        f=open(r"bible/"+name+r"/%d.txt"%chap,"r")
        txt=""
        for t in f:
            txt+=t
        f.close()
        self.nowChap.SetValue(str(chap))
        self.contents.SetValue(txt)

    def loadBible(self,event,name):
        self.loadinfact(name,1)
        text="正在阅读《"+self.index[name][0]+"》，共"+str(self.index[name][1])+"章"
        self.StatusBar.PushStatusText(text)
    def getIndex(self):
        retmenu=wx.Menu()
        index_fh=open(r"bible/index","r")
        for buf in index_fh:
            (dirname,filetotal,title)=buf.split("|")
            title=title.strip('\n')
            btn=retmenu.Append(wx.NewId(),title )
            self.Bind(wx.EVT_MENU, lambda evt, tmp=dirname:self.loadBible(evt,tmp), btn)
            self.index[dirname]=[title,int(filetotal)]
        index_fh.close()
        return retmenu
    def OnToLeftBtn(self,event):
        nowchap=int(self.nowChap.GetValue())
        if (nowchap -1  >0 ):
            nowchap = nowchap -1
            self.loadinfact(self.loadedname,nowchap)

    def OnToRightBtn(self,event):
        nowchap=int(self.nowChap.GetValue())
        if (nowchap + 1 <= self.index[self.loadedname][1]):
            nowchap = nowchap +1
            self.loadinfact(self.loadedname,nowchap)

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()
        
        #build box sizer
        self.bkg=wx.Panel(self)
        self.box=wx.BoxSizer(wx.VERTICAL)

        #build the menu
        filemenu=wx.Menu()
        self.AboutBtn=filemenu.Append(wx.ID_ABOUT, u"关于(&A)", u"关于cBible")
        filemenu.AppendSeparator()
        self.ExitBtn=filemenu.Append(wx.ID_EXIT, u"退出(&X)", u"退出")
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu,u"文件(&F)")
        self.Bind(wx.EVT_MENU,self.OnAbout,self.AboutBtn)
        self.Bind(wx.EVT_MENU,self.OnClose,self.ExitBtn)
        self.SetMenuBar(menuBar)
        menuBar.Append(self.getIndex(),u"目录(&I)");
        
        #build the chapter choicer
        self.chapch=wx.BoxSizer()
        self.toLeftBtn=wx.Button(self.bkg,label="<-")
        self.Bind(wx.EVT_BUTTON,self.OnToLeftBtn,self.toLeftBtn)
        self.toRightBtn=wx.Button(self.bkg,label="->")
        self.Bind(wx.EVT_BUTTON,self.OnToRightBtn,self.toRightBtn)
        self.nowChap=wx.TextCtrl(self.bkg)
        self.chapch.Add(self.toLeftBtn,proportion=0,flag=wx.LEFT ,border=5)
        self.chapch.Add(self.nowChap,proportion=1,flag=wx.EXPAND)
        self.chapch.Add(self.toRightBtn,proportion=0,flag=wx.LEFT ,border=5)
        self.box.Add(self.chapch,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        #build the contents container
        self.contents=wx.TextCtrl(self.bkg,style=wx.TE_MULTILINE|wx.HSCROLL)
        self.contents.SetEditable(False)
        self.box.Add(self.contents,proportion=1,flag=wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT)
        
        #the last part
        self.bkg.SetSizer(self.box)
        self.Show(True)
    def OnAbout(self,event):
        dlg=wx.MessageDialog(self, u"cBible是一个简单的中文圣经工具\nAuthor:Michael Lin",caption=u"关于",style=wx.OK,pos=wx.DefaultPosition)
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self,event):
        self.Destroy()

if __name__== '__main__':
    app =wx.App(False)
    frame= MainWindow(None, "cBible")
    app.MainLoop()
