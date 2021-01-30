from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
#from TkinterDnD2 import *
from glob import glob #for testing purposes
import pygame
from time import sleep
import os
from tkinter import ttk
from tooltip import *
from PIL import ImageTk
try:
    import Image
except ImportError:
    from PIL import Image
from scrollimage import ScrollableImage
from animator import anime
from time import sleep
import smtplib, ssl

#root = TkinterDnD.Tk()
root = Tk()
pygame.init()

class Skeleton:
    menuBar = Menu(root)
    FileMenu = Menu(menuBar, tearoff = 0)
    ToolMenu = Menu(menuBar, tearoff = 0)
    HelpMenu = Menu(menuBar, tearoff = 0)
    sound_track = None
    images = ['imgs\\skeleton.jpg']
    def __init__(self):
        root.geometry('850x600')
        root.title("Untitled - Skeleton2D Beta")
        root.config(bg = 'white')
        try:root.wm_iconbitmap("imgs\\logo.ico")
        except:pass
        self.FileMenu.add_command(label = "Open Image", command = self.Open_image)
        self.FileMenu.add_command(label = "Import Sound", command = self.comingsoon)
        self.FileMenu.add_command(label = "New project    Ctrl+N", command = self.New)
        self.FileMenu.add_command(label = "Open project   Ctrl+O", command = self.Open)
        self.FileMenu.add_command(label = "Save Project   Ctrl+S", command = self.save)
        self.FileMenu.add_command(label = "Export", command = self.comingsoon)
        self.FileMenu.add_command(label = "Exit           Ctrl+Q", command = self._quit_)
        
        self.HelpMenu.add_command(label = "About ", command = self.About)
        self.HelpMenu.add_command(label = "How to use  F1", command = self.Use)
        self.HelpMenu.add_command(label = "Version ", command = self.version)
        self.HelpMenu.add_command(label = "Send Feedback", command = self.feedback)
        
        self.ToolMenu.add_command(label = "Pause", command = self.comingsoon)
        self.ToolMenu.add_command(label = "Next Frame", command = self.next_frame)
        self.ToolMenu.add_command(label = "Previous Frame", command = self.prev_frame)
        self.ToolMenu.add_command(label = "Delete Current Frame", command = self.del_frame)
        self.ToolMenu.add_command(label = "Preview       F5", command = self.Animate)
        self.ToolMenu.add_command(label = "Stop", command = self.comingsoon)

        self.menuBar.add_cascade(label = "File", menu = self.FileMenu)
        self.menuBar.add_cascade(label = "Tools", menu = self.ToolMenu)
        self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)

        self.widgets()
        root.config(menu = self.menuBar)

        root.bind('<F1>', lambda x:[self.Use()])
        root.bind('<F5>', lambda x:[self.Animate()])
        root.bind('<Control-q>', lambda x:[self._quit_()])
        root.bind('<Control-n>', lambda x:[self.New()])
        root.bind('<Control-s>', lambda x:[self.save()])
        root.bind('<Control-o>', lambda x:[self.Open()])
        root.bind('<Control-i>', lambda x:[self.Open_image()])

        self.file = None
        self.n = 0

        self.FPS = IntVar()
        fps_label = ttk.LabelFrame(root, text = "fps", width = 100, height = 53)
        fps_label.place(x = 375, y = 7)
        self.fps = Spinbox(fps_label, from_ = 1, to = 150, width  = 10, bd= 2, textvariable = self.FPS)
        self.fps.place(x = 10, y = 2)
        create_Tip(self.fps, "Set the frames per second")

    def _quit_(self):
        if askokcancel("Exit", "Are you sure you want to quit?"):
            root.destroy()
    
    def comingsoon(self):#for coming soon features that are not yet included
        showinfo("Very Sorry", "This is the beta version of this app,\n you can check for the latest verison\n which should have this feature with the\n version button in the help button")

    def Open_image(self):
        try:
            self.file = askopenfilename(title = "Open image - Skeleton2D Beta", defaultextension = " .top", filetypes = [("All Files", "*.*")])
        except FileNotFoundError:pass
        if self.file == '':
            self.file = None
        else:
            try:
                #f = open(self.file, 'w+')
                self.images.append(self.file)
                self.n = self.images.index(self.file)
                self.img_win.del_canvas()
                img = Image.open(self.file)
                img = ImageTk.PhotoImage(img)
                self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 770, height = 450)
                self.img_win.place(x = 100, y = 100)
            except Exception as e:
                showinfo("An Error Occured", e)

    def New(self):
        root.title("Untitled - Skeleton2D Beta")
        self.file = None
        self.images = []
        self.img_win.del_canvas()
        img = Image.open('imgs\\skeleton.jpg')
        img = ImageTk.PhotoImage(img)
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 770, height = 450)
        self.img_win.place(x = 100, y = 100)


    def Open(self):
        self.file = askopenfilename(title = "Open recent project - Skeleton2D Beta", defaultextension = " .top", filetypes = [("Tuple Of Pics" , "*.top") ])
        if self.file == '':
            self.file = None
        else:
            root.title(os.path.basename(self.file).replace('.top', '') + " - Skeleton2D Beta")
            try:
                file = open(self.file, "r")
                file = file.read()
                self.images = eval(file)
                # print(self.images)
                # file.close()
            except FileNotFoundError:
                showinfo("ALERT", "Hey, you didn't open a file")

    def save(self):        
        self.file = asksaveasfilename(title = "Save Project - Skeleton2D Beta", initialfile = 'Untitled.top', defaultextension = " .top", filetypes = [("Tuple Of Pics", "* .top")])
        if self.file == '':
            self.file == None
        else:
           root.title(os.path.basename(self.file).replace('.top', '') + "- Skeleton2D Beta")
           with open(self.file, 'w+') as f:
               data = str(self.images)
               f.write(data)
               f.close()

    def About(self):showinfo('About', " C. Copyleft: Bullsofts Inc.\n Send Feedback with the send feedback\n button to help us improve Skeleton2D")

    def Use(self):
        file = open('how.txt', 'r')
        showinfo("How to use...", file.read())
       
    def Animate(self):
        self.progressing()
        fps_ = self.FPS.get()
        images = self.images
        anime.animate(images, float(1/fps_))
        #...play music here...
        #====================TEST===========================
        #images = [i for i in glob('*.jpg')]
        #anime.animate(images, 1)
        #=================END OF REGION=====================


    def hidefile(self, filename):
        import win32file, win32con, win32api
        flags = win32file.GetFileAttributesW(filename)
        win32file.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN|flags)
    
    def widgets(self):
        global progress_bar, img_
        class Btn(Button):
            def __init__(self, master, **kw):
                Button.__init__(self, master = master, **kw)
                self.defaultBackground = self["background"]
                self.config(relief = GROOVE)
                self.bind("<Enter>", self.on_enter)
                self.bind("<Leave>", self.on_leave)

            def on_enter(self, e): self['background'] = self['activebackground']
            def on_leave(self, e): self['background'] = self.defaultBackground

        progress_bar = ttk.Progressbar(root, orient = 'horizontal', length = 686, mode = 'determinate')
        progress_bar.place(x = 270, y = 620)
        #lb.drop_target_register(DND_FILES)
        #lb.dnd_bind('<<Drop>>', file_in)
        #lb.bind("<Button-3>", lambda x:remove(lb))

        toolbar = Canvas(root, width = 400000, height = 70).pack()

        frame = ttk.LabelFrame(root, text = "Tools", width = 340, height = 53)
        frame.place(x = 20, y = 7)

        btn0 = Btn(frame, text = "Prev", width = 5, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.prev_frame)
        btn0.place(x=30, y=1, anchor = 'nw')
        create_Tip(btn0, "Go to previous frame")
        btn1 = Btn(frame, text = "Next", width = 5, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF',  activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.next_frame)
        btn1.place(x=100, y=1, anchor = 'nw')
        create_Tip(btn1, "Go to the next frame")
        btn2 = Btn(frame, text = "Delete", width = 7, height = 0, font = ("Calibri", 12), bg = "#000", foreground = '#fff', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.del_frame)
        btn2.place(x = 180, y = 1, anchor = 'nw')
        btn3 = Btn(frame, text = "Preview", width = 7, height = 0, font = ("Calibri", 12), bg = "#000", foreground = '#fff', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.Animate)
        btn3.place(x = 258, y = 1, anchor = 'nw')
        create_Tip(btn2, "delete the current frame")
        create_Tip(btn3, "View animation preview")

        img = Image.open('imgs\\skeleton.jpg')
        img = ImageTk.PhotoImage(img)
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 770, height = 450)
        self.img_win.place(x = 100, y = 100)

    def progressing(self):
        progress_bar['maximum'] = 100
        for i in range(101):
            sleep(0.05)
            progress_bar["value"] = i
            progress_bar.update()
        progress_bar["value"] = 0
        showinfo("Success", "Animation ready for preview")

    def next_frame(self):
        self.n += 1
        self.img_win.del_canvas()
        try:
            img = Image.open(self.images[self.n])
        except IndexError:
            pass
        try:
            img = ImageTk.PhotoImage(img)
            self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 770, height = 450)
            self.img_win.place(x = 100, y = 100)
        except UnboundLocalError:
            pass

    def prev_frame(self):
        self.n -=1
        self.img_win.del_canvas()
        try:
            img = Image.open(self.images[self.n])
        except IndexError:
            pass
        try:
            img = ImageTk.PhotoImage(img)
            self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 770, height = 450)
            self.img_win.place(x = 100, y = 100)
        except UnboundLocalError:
            pass

    def del_frame(self):
        try:
            self.images.pop(self.n)
        except IndexError:
            pass
        self.prev_frame()

    def version(self):
        showinfo("Version", "Skeleton2D Beta version")
        
        pop = Tk()
        pop.title('check for latest version')
        pop.geometry('150x50')
        pop.resizable(False, False)
        pop.wm_iconbitmap('imgs\\logo.ico')

        def checklatest():
            import webbrowser
            pop.destroy()
            webbrowser.open('--link for cheking version goes here--')
        button = Button(pop, text = "check latest version", command = checklatest).pack()

    def feedback(self):
        pop = Tk()
        pop.title('Send Feedback')
        pop.geometry('400x200')
        pop.wm_iconbitmap('imgs\\logo.ico')

        email = Entry(pop, width = 30)
        email.place(x = 100, y = 25)
        password = Entry(pop, width = 30, show = '*')
        password.place(x = 100, y = 60)
        message = Entry(pop, width = 50)
        message.place(x = 50, y = 100)

        def send():
            port = 465
            email_ = email.get()
            password_ = password.get()
            message_ = message.get()
            context = ssl.create_default_context()
            pop.destroy()
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(email_, password_)
                    for i in file.readlines():
                        server.send_mail(email_, 'praisejames011@gmail.com', message_) 
            except Exception as e:
                showerror("An Error Occured", e)

        btn = Button(pop, text = 'Send', command = send)
        btn.place(x = 170, y = 150)

        create_Tip(email, 'Enter your email here')
        create_Tip(password, 'Enter your password here')
        create_Tip(message, 'Enter your feedback')

if __name__=='__main__':
    Skeleton()
    root.mainloop()
