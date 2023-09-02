#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from imageai.Detection import ObjectDetection, VideoObjectDetection
from tkinter import *
from PIL import ImageTk,Image
from customtkinter import *
from tkVideoPlayer import TkinterVideo 
import os.path
import threading


class My_Command_Frame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.button_img_recog = CTkButton(self, text="Image Recognition", command=process_img)
        self.button_img_recog.place(relx=0.5, rely=0.2, anchor="center")
        
        self.button_vid_recog = CTkButton(self, text="Video Recognition",
                                          command=lambda:(threading.Thread(target=process_video).start(),
                                                         show_loading()))
        self.button_vid_recog.place(relx=0.5, rely=0.4, anchor="center")
        
        self.button_reset = CTkButton(self, text="Reset", command=reset)
        self.button_reset.place(relx=0.5, rely=0.6, anchor="center")
        
        self.button_quit = CTkButton(self, text="Quit", command=master.destroy)
        self.button_quit.place(relx=0.5, rely=0.8, anchor="center")

        

class App(CTk):
    def __init__(self):
        super().__init__()
        
        self.focus()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        app_w = 1400
        app_h = 700
        
        x = (screen_w/2) - (app_w/2)
        y = (screen_h/2) - (app_h/2)
        
        self.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
        self.title("Object Recognition")

        self.command_frame = My_Command_Frame(master=self, height=700, width=350, border_width=0.5)
        self.command_frame.place(relx=1, rely=0.5, anchor="e")
        
        self.label_main = CTkLabel(master=self, text="Please select an option.", font=('Helvetica',24))
        self.label_main.place(relx=0.3, rely=0.5, anchor="w")

        self.label_sub = CTkLabel(master=self, text="", font=('Helvetica',20))
        

class Splash_art(CTkToplevel):
    def __init__(self):
        super().__init__()
        
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        app_w = 700
        app_h = 350
        
        x = (screen_w/2) - (app_w/2)
        y = (screen_h/2) - (app_h/2)
        
        self.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
        self.overrideredirect(True)
        
        splash_main = CTkLabel(master=self, text="Processing the video.", font=('Helvetica',24))
        splash_main.place(relx=0.5, rely=0.425, anchor="center")
        
        splash_sub = CTkLabel(master=self, text="Please wait, this may take a while.")
        splash_sub.place(relx=0.5, rely=0.65, anchor="center")
        
        self.focus()
        

def show_loading():
    global loading
    root.withdraw()
    loading = Splash_art()
    loading.mainloop()
    

def process_img():
    global objs
    
    file = filedialog.askopenfilename(filetypes=[('*.jpg', '*.jpg')])
    if file == "":
        reset()
    else:
        recognizer = ObjectDetection()  

        path_input = file
        path_model = "./Models/yolov3.pt"   
        path_output = "./Output/newimage.jpg"

        recognizer.setModelTypeAsYOLOv3() 
        recognizer.setModelPath(path_model)

        recognizer.loadModel()   
        recognition = recognizer.detectObjectsFromImage(  
            input_image = path_input,  
            output_image_path = path_output  
            )  

        object_list = []  
        for eachItem in recognition:  
            if float(eachItem["percentage_probability"])>75:
                if eachItem["name"] not in object_list:
                    object_list.append(eachItem["name"])

        objs = ", ".join(object_list)

        show_img(path_output)
    
    
def show_img(image_path):
    global lst_string
    
    image_selected=CTkImage(dark_image=Image.open(image_path),size=(900, 450))
    
    root.label_main.configure(text="", image=image_selected)
    root.label_main.place(relx=0.04, rely=0.4, anchor="w")
    
    objects_in_img = "In this image there are "+objs+"."
    
    root.label_sub.configure(text=objects_in_img)
    root.label_sub.place(relx=0.2, rely=0.8, anchor="w")


'''def process_frame(frame_number, output_array, output_count):
    

    global lst_string
    frames_to_skip = 15 
    lst = []
    if frame_number % (frames_to_skip + 1) == 0:
        for obj in output_array:
            if obj not in lst:
                lst.append(obj["name"])
        
        lst_string = "In this Video there are:" + ", ".join(lst) + "."'''

def process_video():
    
    execution_path = os.getcwd()
    path_input = filedialog.askopenfilename(filetypes=[('*.mp4', '*.mp4')])

    if path_input == "":
        reset()
        loading.destroy()
        root.deiconify()
        root.focus()
    else:
        detector = VideoObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("./Models/yolov3.pt")
        detector.loadModel()

        video_path = detector.detectObjectsFromVideo(input_file_path=path_input,
                                                     output_file_path=os.path.join(execution_path, "traffic_detected")
                                                     ,frames_per_second=30,
                                                     detection_timeout=180,
                                                    log_progress=True)

        loading.destroy()
        #print(lst_string)
        play_video(video_path)


def play_video(video_path):
    
    app = CTkToplevel()
    
    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()
        
    app_w = 1400
    app_h = 700
        
    x = (screen_w/2) - (app_w/2)
    y = (screen_h/2) - (app_h/2)
        
    app.geometry(f"{app_w}x{app_h}+{int(x)}+{int(y)}")
    app.focus()

    video_player = TkinterVideo(master=app, scaled=True)
    video_player.pack(expand=True, fill='both')
    video_player.load(video_path)

    play_button = CTkButton(master=app, text="Play", command=lambda:(video_player.play()))
    play_button.pack(padx=100, side="left", fill="x")
    
    reset()
    
    destroy_button = CTkButton(master=app, text="Quit", command=lambda:(root.deiconify(),root.focus(),app.destroy()))
    destroy_button.pack(padx=100, side="right", fill="x")

    app.mainloop()


def reset():
    
    root.label_sub.place_forget()
    root.label_main.configure(text="Please select an option.", image="")
    root.label_main.place(relx=0.3, rely=0.5, anchor="w")
    

root = App()
root.mainloop()


# In[ ]:




