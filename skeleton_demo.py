from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
#from TkinterDnD2 import *
from glob import glob #for testing purposes
import pygame
from time import sleep
import os
from tkinter import ttk
from PIL import ImageTk
from tooltip import *
from scrollimage import ScrollableImage
from animator import anime

#root = TkinterDnD.Tk()
root = Tk()
pygame.init()

class Skeleton:
    menuBar = Menu(root)
    FileMenu = Menu(menuBar, tearoff = 0)
    ToolMenu = Menu(menuBar, tearoff = 0)
    HelpMenu = Menu(menuBar, tearoff = 0)
    #images = ['imgs/super.png']
    sound_track = None
    images = []
    def __init__(self):
        root.geometry('850x600')
        root.title("Untitled - Skeleton 2D Beta")
        root.config(bg = 'white')
        try:root.wm_iconbitmap("skeleton.png")
        except:pass
        self.FileMenu.add_command(label = "Open Image", command = self.Open_image)
        self.FileMenu.add_command(label = "Import Sound", command = self.comingsoon)
        self.FileMenu.add_command(label = "New project", command = self.New)
        self.FileMenu.add_command(label = "Open project", command = self.Open)
        self.FileMenu.add_command(label = "Save Project", command = self.save)
        self.FileMenu.add_command(label = "Export", command = self.comingsoon)
        self.FileMenu.add_command(label = "Exit", command = root.destroy)
        
        self.HelpMenu.add_command(label = "About ", command = self.About)
        self.HelpMenu.add_command(label = "How to use", command = self.Use)
        self.HelpMenu.add_command(label = "Rate Us", command =  self.comingsoon)
        self.HelpMenu.add_command(label = "Send Feedback", command = self.comingsoon)
        self.HelpMenu.add_command(label = "Sponsor Us", command = self.comingsoon)
        
        self.ToolMenu.add_command(label = "Play", command = self.comingsoon)
        self.ToolMenu.add_command(label = "Pause", command = self.comingsoon)
        self.ToolMenu.add_command(label = "Animate", command = self.Animate)
        self.ToolMenu.add_command(label = "Stop", command = self.comingsoon)

        self.menuBar.add_cascade(label = "File", menu = self.FileMenu)
        self.menuBar.add_cascade(label = "Tools", menu = self.ToolMenu)
        self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)

        self.widgets()
        root.config(menu = self.menuBar)
        root.bind('<F1>', lambda x:[self.Use])
        self.file = None
        img = PhotoImage('imgs\\super.png')
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450)
        self.img_win.place(x = 100, y = 100)

        self.FPS = IntVar()
        fps_label = ttk.LabelFrame(root, text = "fps", width = 100, height = 53)
        fps_label.place(x = 340, y = 7)
        self.fps = Spinbox(fps_label, from_ = 1, to = 150, width  = 10, bd= 2, textvariable = self.FPS)
        self.fps.place(x = 10, y = 2)
        create_Tip(self.fps, "Set the frames per second")
    
    def comingsoon(self):#for coming soon features that are not yet included
        showinfo("HAHA, see you", "i'm still working on it, coming soon")

    def get_pic_size(self, filename):
        with open(filename, 'rb') as img:
            img.seek(163)
            a = img.read(2)
            height = (a[0] <<8) + a[1]
            v = img.read(2)
            width = (v[0] <<8) + v[1]
            print(width)
            print(height)
            return [width, height]

    def Open_image(self):
        try:
            self.file = askopenfilename(title = "Open image - Skeleton2D Beta")
        except FileNotFoundError:pass
        if self.file == '':
            self.file = None
        else:
            try:
                f = open(self.file, 'w+')
                self.images.append(f)
                self.n = self.images.index(f)
            except Exception as e:showinfo("An Error Occured", e)

    def New(self):
        root.title("Untitled - Skeleton2D Beta")
        self.file = None
        self.images = []

    def Open(self):
        self.file = askopenfilename(title = "Open recent project - Skeleton2D Beta", defaultextension = " .spf", filetypes = [("Skeleton2D Primary Format" , "*.spf") ])
        if self.file == '':
            self.file = None
        else:
            root.title(os.path.basename(self.file).replace('.top', '') + " - Skeleton2D Beta")
            try:
                file = open(self.file, "r")
                self.images  = eval(file)
                #file.close()
            except FileNotFoundError:
                showinfo("ALERT", "Hey, you didn't open a file")

    def save(self):        
        self.file = asksaveasfilename(title = "Save Project - Skeleton2D Beta", initialfile = 'Untitled', defaultextension = " .spf", filetypes = [("Skeleton2D Primary Format", "* .spf")])
        if self.file == '':
            self.file == None
        else:
           root.title(os.path.basename(self.file).replace('.top', '') + "- Skeleton2D Beta")
           with open(self.file, 'w+') as f:
               data = str(self.images)
               f.write(data)
               f.close()

    def About(self):showinfo('About', " C. Copyleft: Praise' desktop")

    def Use(self):showinfo("How to use...", "I'll explain soon... just remind me")
       
    def Animate(self):
        #progressing()
        fps_ = self.FPS.get()
        #work = anime()
        images = self.images
        anime.animate(images, float(1/fps_))
        try:
            pygame.mixer.music.play(-1)
        except Exception as e:
            showerror("Error", e)
        #====================TEST===========================
        #images = []
        #for i  in glob("*.jpg"):
            #images.append(i)
        #for i in images:
            #anime.animate(images, 1)
        #=================END OF REGION=====================


    def hidefile(self, filename):
        import win32file, win32con, win32api
        flags = win32file.GetFileAttributesW(filename)
        win32file.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN|flags)
    
    def widgets(self):
        class Btn(Button):
            def __init__(self, master, **kw):
                Button.__init__(self, master = master, **kw)
                self.defaultBackground = self["background"]
                self.config(relief = GROOVE)
                self.bind("<Enter>", self.on_enter)
                self.bind("<Leave>", self.on_leave)

            def on_enter(self, e): self['background'] = self['activebackground']
            def on_leave(self, e): self['background'] = self.defaultBackground

        progress_bar = ttk.Progressbar(root, orient = 'horizontal', length = 486, mode = 'determinate')
        progress_bar.place(x = 270, y = 620)
        #lb.drop_target_register(DND_FILES)
        #lb.dnd_bind('<<Drop>>', file_in)
        #lb.bind("<Button-3>", lambda x:remove(lb))

        toolbar = Canvas(root, width = 400000, height = 70).pack()

        frame = ttk.LabelFrame(root, text = "Tools", width = 300, height = 53)
        frame.place(x = 20, y = 7)

        btn0 = Btn(frame, text = "Prev", width = 5, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = None)
        btn0.place(x=30, y=1, anchor = 'nw')
        create_Tip(btn0, "Go to previous frame")
        btn1 = Btn(frame, text = "Next", width = 5, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF',  activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = None)
        btn1.place(x=100, y=1, anchor = 'nw')
        create_Tip(btn1, "Go to the next frame")
        btn2 = Btn(frame, text = "Animate", width = 7, height = 0, font = ("Calibri", 12), bg = "#000", foreground = '#fff', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.Animate)
        btn2.place(x = 200, y = 1, anchor = 'nw')
        create_Tip(btn2, "View animation preview")

        self.img_win = ScrollableImage(root, image = None, scrollbarwidth = 16, width = 700, height = 450)
        self.img_win.place(x = 100, y = 100)

if __name__=='__main__':
    Skeleton()
    root.mainloop()
