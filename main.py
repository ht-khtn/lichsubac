from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty, ListProperty, DictProperty
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

Builder.load_file("lichsu.kv")


class Stage1(Widget):

    data = {
        "Cuộc kháng chiến chống quân xâm lược Triệu Đà thất bại dẫn tới hậu quả gì?" : 
        [
            "2000 năm Bắc thuộc",
            "80 năm Pháp thuộc",
            "2 thập niên Minh thuộc" 
        ],
        "Vào đầu thế kỉ XX, nước tư bản chủ nghĩa nào đã ảnh hưởng vào cuộc vận động giải phóng dân tộc Việt Nam là chủ yếu?":
        [
            "Nhật",
            "Nga",
            "Pháp"
        ],
        "Ở giai đoạn đầu thế kỉ XX, các cuộc vận động giải phóng đân tộc Việt Nam đi theo hình thức nào là chủ yếu?":
        [
            "vô sản",
            "dân chủ tư sản",
            "dân chủ vô sản"
        ]
    }
    true_data = [0,0,1]
    data_keys = list(data.keys())
    data_size = len(data_keys)
    final_result = ""
    
    video = ObjectProperty(None)
    quiz = ObjectProperty(None)
    back_btn = ObjectProperty(None)
    skip_btn  = ObjectProperty(None)
    question = ObjectProperty(None)
    answer = ObjectProperty(None)
    answer1 = ObjectProperty(None)
    answer2 = ObjectProperty(None)
    answer3 = ObjectProperty(None)
    ans_list = ReferenceListProperty(answer1,answer2,answer3)
    next_btn = ObjectProperty(None)
    result = ObjectProperty(None)
    result_status = ObjectProperty(None)
    score_is = ObjectProperty(None)
    score = ObjectProperty(None)

    def reset_quiz(self):
        self.progress = 0
        self.chosen_ans = 0
        self.curques = 0
        self.true_ans_count = 0
        self.next_btn.text = "Nộp"
        self.next_btn.disabled = False
    
    def reset_video(self):
        self.video.state = "stop"
        self.video.state = "play"
        self.video.opacity = 1
        self.quiz.opacity = 0
        self.skip_btn.opacity = 1
        self.skip_btn.background_normal = "next_btn.png"
        self.skip_status = 0
        self.next_btn.disabled = True 
        self.result.opacity = 0
        
    def skip(self):
        if self.skip_status == 0:
            self.skip_status = 1
            self.video.state = "stop"
            self.video.opacity = 0
            self.quiz.opacity = 1
            self.skip_btn.background_normal = "pre_btn.png"
            self.reset_quiz()
            self.show_quiz(0)
        else:
            self.reset_video()
        
    def choose(self,instance,value):
        print(instance,value)
    
    def show_quiz(self, n):
        self.curques = n
        self.question.text = f"{self.data_keys[n]}"
        answer_data = self.data[self.data_keys[n]]
        for i in range(3):
            self.ans_list[i].text = answer_data[i]
            self.ans_list[i].color = (0,0,0,1)

    def on_choose(self,n):
        self.chosen_ans = n

    def on_click(self):
        if self.progress % 2 != 0 and self.curques < self.data_size-1:
            self.next_btn.text = "Nộp"
            self.show_quiz(self.curques+1)
        elif self.curques < self.data_size-1:
            self.next_btn.text = "Câu hỏi tiếp theo"
            self.show_corect_ans()
        elif self.progress == -1:
            self.final_result = f"{self.true_ans_count} / {self.data_size}"
            self.show_result()
        else:
            self.next_btn.text = "Kết thúc bài làm"
            self.show_corect_ans()
            self.progress = -2
        self.progress += 1
    
    def show_corect_ans(self):
        true_ans = self.true_data[self.curques]
        self.ans_list[true_ans].color = (0,1,0,1)
        if self.chosen_ans == true_ans:
            self.true_ans_count += 1
        else:
            self.ans_list[self.chosen_ans].color = (1,0,0,1)

    def show_result(self):
        self.quiz.opacity = 0
        self.next_btn.disabled = True
        self.score.text = self.final_result
        self.result.opacity = 1


class TnlsUI(Widget):
    
    stage_area = ObjectProperty(None)
    
    opened_stage = NumericProperty(1)
    
    def create(self):
        for i in range(30):
            if i < self.opened_stage:
                btn = Button(text = f"{i+1}", background_color = (1,1,1,1))
            else:
                btn = Button(text = f"{i+1}", background_color = (1,1,1,0.5))
            btn.bind(on_press = self.parent.goto_stage)
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
            
    def showUI(self,ui):
        if self.curui:
            self.fadeout.start(self.curui)
            self.curui.x -= 1000
            if self.curui in self.stage:
                self.curui.video.state = "stop"
        if ui in self.stage:
            ui.reset_video()
        ui.x += 1000
        self.fadein.start(ui)
        self.curui = ui
    
    def goto_stage(self,obj):
        if obj.background_color == [1,1,1,1]:
            self.showUI(self.stage[int(obj.text)-1])
    

class LichSuApp(App):
    
    title = "Lịch Sử"
    
    def build(self):
        self.icon = "app_icon.png"
        return MainGUI()
        
if __name__ == '__main__':
    LichSuApp().run()