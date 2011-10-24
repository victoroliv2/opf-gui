import pyjd # this is dummy in pyjs.
from pyjamas import DOM

from pyjamas.ui.RootPanel import RootPanel, RootPanelCls, manageRootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Label import Label
from pyjamas.ui.FocusPanel import FocusPanel
from pyjamas.Canvas.GWTCanvas import GWTCanvas
from pyjamas.Canvas.ImageLoader import loadImages
from pyjamas.Canvas import Color
from pyjamas.ui.Composite import Composite
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel

#from pyjamas.Canvas2D import Canvas, CanvasImage, ImageLoadListener
from pyjamas.Timer import Timer
from pyjamas import Window
from pyjamas import log
from pyjamas.ui import Event
from pyjamas.ui import KeyboardListener
from pyjamas.ui.KeyboardListener import KeyboardHandler
from pyjamas.ui.ClickListener import ClickHandler

from pyjamas.ui.Image import Image
from pyjamas import Window

import math
import pygwt
import random

from pyjamas.HTTPRequest import HTTPRequest
from pyjamas.JSONService import JSONProxy
import urllib


try:
    # included in python 2.6...
    from json import dumps, loads
except ImportError:
    try:
        # recommended library (python 2.5)
        from simplejson import dumps, loads
    except ImportError:
        # who's the pyjs daddy?
        from pyjamas.JSONParser import JSONParser
        parser = JSONParser()
        dumps = getattr(parser, 'encode')
        loads = getattr(parser, 'decodeAsObject')
        JSONDecodeException = None

FPS = 30

class Point():
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

class Canvas(GWTCanvas):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.classify = False
        self.color = [(random.randint(0,256), random.randint(0,256), random.randint(0,256)),]
        self.PointList = []
        GWTCanvas.__init__(self, self.w, self.h)
        
        self.sinkEvents (Event.KEYEVENTS | Event.MOUSEEVENTS)
        self.clear()

        self.onTimer()
        self.resize(self.w, self.h)
        
    def clear(self):
      self.color = [(random.randint(0,256), random.randint(0,256), random.randint(0,256)),]
      self.PointList = []

    def onMouseDown(self, sender, x, y):
      rx = x + Window.getScrollLeft()
      ry = y + Window.getScrollTop()
      if self.classify:
        self.PointList.append( Point(rx, ry, -1 ) )
      else:
        self.PointList.append( Point(rx, ry, len(self.color)-1) )
        
    def onTimer(self, t=None):
        Timer(int(1000/FPS), self)
        
        self.draw()

    def draw(self):

        self.setFillStyle(Color.Color('#CCC'))
        self.fillRect(0,0,self.w,self.h)
        
        for p in self.PointList:
          if p.c >= 0:
            cl = self.color[p.c]
            self.setFillStyle(Color.Color(cl[0], cl[1], cl[2]))
            self.beginPath()
            self.arc(p.x, p.y, 8, 0, 3.1416*2, True)
            self.closePath()
            self.fill()
            self.stroke()
          else:
            self.beginPath()
            self.arc(p.x, p.y, 8, 0, 3.1416*2, True)
            self.closePath()
            self.stroke()
            self.beginPath()
            self.arc(p.x, p.y, 5, 0, 3.1416*2, True)
            self.closePath()
            self.stroke()
            
class RunHandle:
  def __init__ (self, canvas):
    self.canvas = canvas

  def onCompletion(self, response):
    if response:
      self.canvas.PointList = [Point(x,y,c) for x,y,c in loads (response)]
    else:
      print "EMPTY ANSWER"

  def onClick(self, sender):
    msg = dumps( [(p.x,p.y,p.c) for p in self.canvas.PointList] )
    HTTPRequest().asyncPost(url = "http://parati.dca.fee.unicamp.br/opfdemo",
                            postData = msg,
                            handler = self)
    print "REQUEST", msg

class ChangeLabelHandle:
  def __init__ (self, canvas):
    self.canvas = canvas

  def onClick(self, sender):
    self.canvas.classify = False
    self.canvas.color.append((random.randint(0,256), random.randint(0,256), random.randint(0,256)))

class ClassifyHandle:
  def __init__ (self, canvas):
    self.canvas = canvas

  def onClick(self, sender):
    self.canvas.classify = True

class ClearHandle:
  def __init__ (self, canvas):
    self.canvas = canvas

  def onClick(self, sender):
    self.canvas.clear()

class OPF_GUI(Composite):
  def __init__(self):
    Composite.__init__(self)

    vp = VerticalPanel(Spacing=10)
    
    self.canvas = Canvas(800, 600)
    
    handle_run      = RunHandle(self.canvas)
    handle_cg       = ChangeLabelHandle(self.canvas)
    handle_classify = ClassifyHandle(self.canvas)
    handle_clear    = ClearHandle(self.canvas)
    
    self.run      = Button("Run!",         handle_run,      StyleName='button')
    self.change   = Button("Change label", handle_cg,       StyleName='button')
    self.classify = Button("Classify",     handle_classify, StyleName='button')
    self.clear    = Button("Clear",        handle_clear,    StyleName='button')
    
    hp = HorizontalPanel(Spacing=10)
    hp.add(self.run)
    hp.add(self.change)
    hp.add(self.classify)
    hp.add(self.clear)
    
    vp.add(Label("Optimum-Path Forest Classifier Demo", StyleName='label'))
    vp.add(self.canvas)
    vp.add(hp)

    panel = FocusPanel()
    panel.add(self.canvas)
    panel.addKeyboardListener(self.canvas)
    panel.addMouseListener(self.canvas)
    panel.setFocus(True)
    
    vp.add(panel)
    
    self.initWidget(vp)
    
if __name__ == '__main__':
    c = OPF_GUI()
    panel = FocusPanel(Widget=c)
    RootPanel().add(panel)

    pyjd.run()
