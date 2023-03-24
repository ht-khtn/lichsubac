from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.animation import Animation
from kivy.clock import time
from kivy.uix.label import Label

Builder.load_string('''

<Stage1>
    
    opacity: 0

<TnlsUI>
    stage_area: stage_area
    
    opacity: 0
        
    Button:
        id: back_btn
        text: "Back"
        size: 60,40
        y: root.height - 50
        x: 10
        
        on_press: root.parent.showUI(root.parent.mainui)
    
    GridLayout:
        id: stage_area
        center:root.center
        orientation: "lr-tb"
        cols: 8
        size: root.width-50, root.height-200
        padding: 10
        spacing: 20
        

<MainInterface>
    
    opacity: 0

    AsyncImage:                                          # Change Main Interface Picture here
        source: ''
        center: root.width/2, root.height/2
        size: 750,750

    Button:
        id: tnls
        center_x: root.center_x
        center_y: root.center_y + 50
        size: 300,60
        text: 'Trải nghiệm Lịch sử'
        font_size: 20
        
        on_press: root.parent.showUI(root.parent.tnlsui)
    
    Button:
        id: cckt
        center_x: root.center_x
        center_y: root.center_y - 50
        size: 300,60
        text: 'Củng cố Kiến thức'
        font_size: 20
        

<LoadInterface>
    opacity: 0
    
    AsyncImage:                                          # Change App logo here
        source: 'app_icon.png'
        size: 248,260         
        center: root.width/2, root.height/2 + 75
        
    Label:                                               # App Name here
        text: 'Thắp lửa Tuổi trẻ Việt'
        text_size: 500,90
        font_size: 50
        halign: 'center'
        color: 0,0,0,1
        center_x: root.center_x
        center_y: root.center_y - 150


<MainGUI>
    logo: logo
    mainui: main
    tnlsui: tnlsui
    
    canvas.before:
        Color:
            rgba: 1,1,1,1                                 # Change App Color here
        Rectangle:
            size: root.size
            pos: root.pos
            
    LoadInterface:
        id: logo
        pos: root.pos
        size: root.size
        
    MainInterface:
        id: main
        pos: root.x-1000,root.y
        size: root.size
        
    TnlsUI:
        id: tnlsui
        pos: root.x-1000,root.y
        size: root.size
    
    Stage1:
        id: stage1
        pos: root.x-1000,root.y
        size: root.size
    
''')

class Stage1(Widget):
    
    pass


class TnlsUI(Widget):
    
    stage_area = ObjectProperty(None)
    
    def create(self):
        for i in range(30):
            btn = Button(text = f"{i+1}")
            btn.bind(on_press = lambda x: self.parent.goto_stage(i))
            self.stage_area.add_widget(btn)
    

class LoadInterface(Widget):
    
    pass


class MainInterface(Widget):
    
    pass


class MainGUI(Widget):
    
    logo = ObjectProperty(None)
    mainui = ObjectProperty(None)
    tnlsui = ObjectProperty(None)
    
    stage1 = ObjectProperty(None)
    
    stage = ReferenceListProperty(stage1)
    
    anim_duration = 0.5
    start_anim_duration = 0.5
    
    fadein = Animation(opacity = 1, duration = anim_duration)
    fadeout = Animation(opacity = 0, duration = anim_duration)
    
    curui = None
    
    def __init__(self, *kwargs):
        super(MainGUI, self).__init__(*kwargs)
        
        self.tnlsui.create()
        
        fade = Animation(opacity = 2, duration = self.start_anim_duration) + Animation(opacity = 0, duration = self.start_anim_duration)
        fade.start(self.logo)
        fade.bind(on_complete = self.on_complete)
        self.fadein.bind(on_complete = self.on_complete)
    
    def on_complete(self,animation,widget):
        if widget == self.logo:
            self.showUI(self.mainui)
        print(widget)
            
    def showUI(self,ui):
        if self.curui:
            self.fadeout.start(self.curui)
            self.curui.x -= 1000
        ui.x += 1000
        self.fadein.start(ui)
        self.curui = ui
    
    def goto_stage(self,stage):
        print(stage)
        self.showUI(self.stage[stage])
    

class LichSuApp(App):
    
    def build(self):
        return MainGUI()
        
if __name__ == '__main__':
    LichSuApp().run()