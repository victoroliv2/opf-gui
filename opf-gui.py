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

FPS = 30

class Point():
    def __init__(self, x, y, c):
        print "new point", x, y
        self.x = x
        self.y = y
        self.c = c

class Canvas(GWTCanvas):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.PointList = []
        GWTCanvas.__init__(self, self.w, self.h)
        
        self.sinkEvents (Event.KEYEVENTS | Event.MOUSEEVENTS)
        self.clear()

        self.onTimer()
        self.resize(self.w, self.h)
        
    def clear(self):
      self.PointList = []

    def onMouseDown(self, sender, x, y):
      rx = x + Window.getScrollLeft()
      ry = y + Window.getScrollTop()
      self.PointList.append( Point(rx, ry, 0) )
      
    def onTimer(self, t=None):
        Timer(int(1000/FPS), self)
        
        self.draw()

    def draw(self):

        self.setFillStyle(Color.Color('#CCC'))
        self.fillRect(0,0,self.w,self.h)
        
        self.setFillStyle(Color.Color('#000'))
        for p in self.PointList:
            self.beginPath()
            self.arc(p.x, p.y, 5, 0, 3.1416*2, True)
            self.closePath()
            self.stroke()

class RunHandle:
  def onClick(self, sender):
    pass

class ChangeLabelHandle:
  def onClick(self, sender):
    pass

class ClearHandle:
  def onClick(self, sender):
    pass

class OPF_GUI(Composite):
  def __init__(self):
    Composite.__init__(self)

    vp = VerticalPanel()
    
    self.canvas = Canvas(800, 600)
    
    handle_run   = RunHandle()
    handle_cg    = ChangeLabelHandle()
    handle_clear = ClearHandle()
    
    self.run    = Button("Run!",         handle_run,   StyleName='button')
    self.change = Button("Change label", handle_cg,    StyleName='button')
    self.clear  = Button("Clear",        handle_clear, StyleName='button')
    
    hp = HorizontalPanel()
    hp.add(self.run)
    hp.add(self.change)
    hp.add(self.clear)
    
    vp.add(Label("Optimum-Path Forest Classifier", StyleName='label'))
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
