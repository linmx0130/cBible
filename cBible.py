#!/usr/bin/python2
# -*- coding: utf-8 -*-

import wx
import os
def delhtm(file1,file2):
    f1=open(file1,"r")
    f2=open(file2,"w")
    for t in f1:
        if t[0]!='<' :
            f2.write(t)
    f1.close()
    f2.close()
def del2(file1,file2):
    f1=open(file1,"r")
    f2=open(file2,"w")
    mark=False
    for t in f1:
        if mark:
            mark=False
            f2.write(t)
        if len(t)>2:
            if (t[1]==':')or(t[2]==':') :
                f2.write(t)
                mark=True
    f1.close()
    f2.close()

class DownloadWindow(wx.Frame):
    def OnOKBtn(self,event):
        self.textlabel.SetLabel("正在下载《"+self.inftu[0]+"》，请稍后。。。")
        self.OKBtn.Disable()
        self.CanBtn.Disable()
        os.mkdir("bible/"+self.name)
        for i in range(1,self.inftu[1]+1):
            self.processlabel.SetLabel("Processing: "+str(i)+" / "+str(self.inftu[1]))
            os.system("wget http://www.ccctspm.org/bibleonline/hgb/%s/%s%d.htm -O bible/%s/%d.htm"%(self.name,self.name,i,self.name,i))
            os.system("iconv -f gbk -t utf-8 bible/%s/%d.htm -obible/%s/%d.txt"%(self.name,i,self.name,i))
            delhtm("bible/%s/%d.txt"%(self.name,i),"bible/%s/%d.bil"%(self.name,i))
            del2("bible/%s/%d.bil"%(self.name,i),"bible/%s/%d.txt"%(self.name,i))
            os.remove("bible/%s/%d.htm"%(self.name,i))
            os.remove("bible/%s/%d.bil"%(self.name,i))
    def OnCanBtn(self,event):
        self.Destroy()
    def __init__(self,parent,title,dname,inftu):
        wx.Frame.__init__(self,parent,title=title,size=(450,170))
        self.name=dname
        self.inftu=inftu
        self.bkg=wx.Panel(self)
        self.box=wx.BoxSizer(wx.VERTICAL)
        self.btnbox=wx.BoxSizer()
        self.textlabel=wx.StaticText(self.bkg,wx.NewId(),"您打算阅览的《"+inftu[0]+"》尚未下载，希望现在下载吗？")
        self.processlabel=wx.StaticText(self.bkg,wx.NewId(),name="")
        self.OKBtn=wx.Button(self.bkg,label="现在下载")
        self.CanBtn=wx.Button(self.bkg,label="取消下载")
        self.Bind(wx.EVT_BUTTON,self.OnOKBtn,self.OKBtn)
        self.Bind(wx.EVT_BUTTON,self.OnCanBtn,self.CanBtn)
        self.box.Add(self.textlabel,proportion=0,flag=wx.ALL,border=5)
        self.box.Add(self.processlabel,proportion=0,flag=wx.ALL,border=5)
        self.btnbox.Add(self.OKBtn,proportion=0,flag=wx.ALL,border=5)
        self.btnbox.Add(self.CanBtn,proportion=0,flag=wx.ALL,border=5)
        self.box.Add(self.btnbox)
        self.bkg.SetSizer(self.box)
        self.Show(True)

class MainWindow ( wx.Frame ) :
    index={}
    loadedname=""
    def askdownload(self,name):
        downf=DownloadWindow(self,"下载经文",name,self.index[name])
    def loadinfact(self,name,chap):
        self.loadedname=name
        self.contents.Clear()
        try:
            f=open(r"bible/"+name+r"/%d.txt"%chap,"r")
            txt=""
            for t in f:
                txt+=t
            f.close()
            self.nowChap.SetValue(str(chap))
            self.contents.SetValue(txt)
        except IOError:
            self.askdownload(name)
    def loadBible(self,event,name):
        self.loadinfact(name,1)
        text="正在阅读《"+self.index[name][0]+"》，共"+str(self.index[name][1])+"章"
        self.StatusBar.PushStatusText(text)
    def getIndex(self):
        retmenu=wx.Menu()
        new_menu=wx.Menu()
        old_menu=wx.Menu()
        index_fh=open(r"bible/index","r")
        for buf in index_fh:
            (dirname,filetotal,title,timemark)=buf.split("|")
            if timemark=="1\n":
                menu_t=new_menu
            else :
                menu_t=old_menu
            btn=menu_t.Append(wx.NewId(),title )
            self.Bind(wx.EVT_MENU, lambda evt, tmp=dirname:self.loadBible(evt,tmp), btn)
            self.index[dirname]=[title,int(filetotal)]
        index_fh.close()
        retmenu.AppendMenu(wx.NewId(),"新约",new_menu)
        retmenu.AppendMenu(wx.NewId(),"旧约",old_menu)
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
        wx.Frame.__init__(self, parent, title=title,size=(800,500))
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
    app=wx.App(False)
    frame= MainWindow(None, "cBible")
    app.MainLoop()
