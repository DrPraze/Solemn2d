from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from TkinterDnD2 import *
#from glob import glob #for testing purposes
import pygame
from time import sleep
import os
import smtplib, ssl
from tkinter import ttk

root = TkinterDnD.Tk()
pygame.init()
images = []
class Skeleton:
    global pic
    menuBar = Menu(root)
    FileMenu = Menu(menuBar, tearoff = 0)
    ToolMenu = Menu(menuBar, tearoff = 0)
    HelpMenu = Menu(menuBar, tearoff = 0)

    try:
        Pic = PhotoImage(file = "skeleton.png")
        pic = Label(root, image = Pic)
        pic.place(x = 230, y = 100)
    except:pass
    sound_track = ''
    def __init__(self):
        root.geometry('850x600')
        root.title("Untitled - Skeleton 2D 1.0")
        root.resizable(False, False)
        root.config(bg = 'white')
        root.wm_iconbitmap("skeleton.png")
        
        self.FileMenu.add_command(label = "Open Image", command = self.Open_image)
        self.FileMenu.add_command(label = "Import Sound", command = self.import_sound)
        self.FileMenu.add_command(label = "New project", command = self.New)
        self.FileMenu.add_command(label = "Open project", command = self.Open)
        self.FileMenu.add_command(label = "Save Project", command = self.save)
        self.FileMenu.add_command(label = "Export", command = None)
        self.FileMenu.add_command(label = "Exit", command = root.destroy)
        
        self.HelpMenu.add_command(label = "About ", command = self.About)
        self.HelpMenu.add_command(label = "How to use", command = self.Use)
        self.HelpMenu.add_command(label = "Rate Us", command =  self.Rate)
        self.HelpMenu.add_command(label = "Send Feedback", command = self.SendFeedback)
        self.HelpMenu.add_command(label = "Sponsor Us", command = None)
        
        self.ToolMenu.add_command(label = "Play", command = None)
        self.ToolMenu.add_command(label = "Pause", command = None)
        self.ToolMenu.add_command(label = "Animate", command = Animate)
        self.ToolMenu.add_command(label = "Stop", command = None)

        self.menuBar.add_cascade(label = "File", menu = self.FileMenu)
        self.menuBar.add_cascade(label = "Tools", menu = self.ToolMenu)
        self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)
        root.config ( menu = self.menuBar)

        self.widgets()
        file = None

    def Valid_pic(self, filename):
        with open(filename, 'rb') as img:
            img.seek(163)
            v = img.read(2)
            height = (v[0] <<8) + a[1]
            v = img.read(2)
            width = (v[0] <<8) + v[1]
            return list(width, height)

    def Open_image(self):
        try:
            self.file = askopenfilename()
        except FileNotFoundError:pass
        if self.file == " ":
            self.file = None
        else:
            try:
                f = open(self.file)
                lb.insert(END, f)
                images.append(f)
            except FileNotFoundError: showinfo("Error", "hey you didn't open nothing!")

    def New(self):
        root.title("Untitled - Skeleton 2D 1.0")
        self.file = None
        lb.delete(0, END)

    def Open(self):
        self.file = askopenfilename(defaultextension = " .txt", filetypes = [("Text Documents" , "*.txt") ])
        if self.file == " ":
            self.file = None
        else:
            root.title (os.path.basename(self.file).replace('.txt', '  ') + " - Skeleton 2D 1.0")
            try:
                file = open(self.file, "r")                   
                lb.insert(END, file)
                #file.close()
            except FileNotFoundError:
                showinfo("ALERT", "Hey, you didn't open a file")

    def save(self):        
        self.file = asksaveasfilename(initialfile = 'Untitled', defaultextension = " .txt", filetypes = [("All Files", "*.*"), ("Text Documents", "* .txt")])
        if self.file == '':
            self.file == None
        else:
           root.title(os.path.basename(self.file).replace('.txt', '  ') + "- Skeleton 2D 1.0")
           with open(self.file, 'w+', encoding = 'utf-8') as f:
               progress_ = lb.get(0, END)
               for i in progress_:
                   f.write(i + "\n")
               f.close()
               #music =

    def SendFeedback(self):
        pop = Tk()
        pop.geometry("280x250")
        pop.resizable(False, False)
        pop.title("Send Feedback")
        label = Label(pop, text = "Enter your email", fg = "black")
        label.place(x = 10, y = 0)
        entry = Text(pop, width = 25, height = 0)
        entry.place(x = 10, y = 40)
        label1 = Label(pop, text = "Enter your email password", fg = "black")
        label.place(x = 10, y = 50)
        entry1 = Text(pop, width = 25, height = 0)
        entry1.place(x = 10, y = 80)
        label2 = Label(pop, text = "Enter your feedback", fg = "black")
        label2.place(x =10, y = 100)
        entry2 = Text(pop, width = 25, height = 5)
        entry2.place(x = 10, y = 120)
        #this is just testing model, would be upgraded soon
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = entry.get(0.0, END)  # user address
        receiver_email = "praisejames011@gmail.com" 
        password = entry1.get(0.0, END)
        message = entry2.get(0.0, END)
        context = ssl.create_default_context()
        def Send():
            pop.destroy
            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
            except Exception as e:
                showerror("Error", e)
        button = Button(pop, text = "Send", command = Send)
        button.pack()

    def About(sefl):showinfo('About', ' C. Copyleft: Novasofts Incorporations')

    def Use(self):
        showinfo("How to use", "")

    def Rate(self):
        pop = Tk()
        pop.geometry('300x200')
        pop.resizable(False, False)
        pop.title("Rate Us")
        star = PhotoImage(file = "star1.png")
        star_ = PhotoImage(file = "star2.png")
        def rate1():btn1.config(image =star_)
        def rate2():
            btn1.config(image = star_)
            btn2.config(image = star_)
        def rate3():
            btn1.config(image = star_)
            btn2.config(image =star_)
            btn3.config(image = star_)
        def rate4():
            btn1.config(image = star_)
            btn2.config(image =star_)
            btn3.config(image = star_)
            btn4.config(image = star_)
        def rate5():
            btn1.config(image =star_)
            btn2.config(image = star_)
            btn3.config(image = star_)
            btn4.config(image = star_)
            btn5.config(image = star_)

        btn1 = Button(pop, image = star, command = rate1)
        btn2 = Button(pop, image = star, command = rate2)
        btn3 = Button(pop, image = star, command = rate3)
        btn4 = Button(pop, image = star, command = rate4)
        btn5 = Button(pop, image = star, command = rate5)
        btn1.place(x = 8, y = 10)
        btn2.place(x = 20, y = 10)
        btn3.place(x = 40, y = 10)
        btn4.place(x = 60, y = 10)
        btn5.place(x = 80, y = 10)
        
        
    def import_sound(self):
        try:
            self.sound_track == pygame.mixer.music.load(askopenfilename())
            self.sound.config(text = self.sound_track)
        except Exception as e:
            showerror("An Error Occured", f"{e}")

    def widgets(self):
        fps_label = Label(root, text = "fps", bg = '#000', font = ("Helvetica", 15), fg = "white")
        fps_label.place(x = 380, y = 20)
        self.sound = Label(root, text = self.sound_track, font= ("Calibri", 20), bg = "black", fg = "white")
        self.sound.place(x = 100, y = 480)

class Btn(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master = master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e): self['background'] = self['activebackground']
    def on_leave(self, e): self['background'] = self.defaultBackground

class anime:
    pygame.init()
    def __init__(self):
        self.screen= pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Project Preview - Skeleton 2D 1.0")
        self.run()

    def animate(images, fps):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Project Preview - Skeleton 2D")
        imagelist = []
        for i in images:
            imagelist.append(i)
        for i in imagelist:
            img = pygame.image.load(i)
            screen.blit(img, [0, 0])
            sleep(fps)
            pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    Skeleton()
            pygame.display.update()
    """
    def Test(self):
        #====================TESTS===========================
        images = []
        for i  in glob("*.jpg"):
            images.append(i)
        for i in images:
            self.animate(images, fps =1)
        #==================END OF REGION===============
    """
    def run(self):
        while True:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    Skeleton()
            pygame.display.update()
            pygame.display.flip()

def Animate():
    progressing()
    root.destroy()
    fps_ = FPS.get()
    #work = anime()
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
    #==================END OF REGION===============

def file_in(e):
    file = lb.tk.splitlist(e.data)[0]
    lb.insert(END, file)
    images.append(file)

def remove(lb):
    item = lb.get(ACTIVE)
    lb.delete(ACTIVE, item)

def progressing():
    progress_bar['maximum'] = 100
    for i in range(101):
        sleep(0.05)
        progress_bar["value"] = i
        progress_bar.update()
    progress_bar["value"] = 0
    showinfo("Success", "Animation compiled successfully!")

progress_bar = ttk.Progressbar(root, orient = 'horizontal', length = 286, mode = 'determinate')
progress_bar.place(x = 270, y = 420)
frame = Frame(root)
frame.pack(side = LEFT)
FPS = IntVar()
fps = Spinbox(root, from_ = 1, to = 150, width  = 10, bd= 8,textvariable = FPS)
fps.place(x = 410, y = 20)

lb = Listbox(frame, bg = "black", fg = "white", width = 35, height = 20)
lb.pack(fill = Y, expand = 1)
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', file_in)
lb.bind("<Button-3>", lambda x:remove(lb))

btn0 = Btn(root, text = "Prev",width = 5, height = 0, font = ('Calibri', 15, 'bold', 'italic'), bg = '#000', foreground = '#FFF', activebackground = 'gold', highlightbackground = "#bce8f1", highlightthickness = 0.5, relief = RAISED, borderwidth = "2", command = None)
btn0.place(x=690, y=20, anchor = 'nw')
btn1 = Btn(root, text = "Next", width = 5, height = 0, font = ('Calibri', 15, 'bold', 'italic'), bg = '#000', foreground = '#FFF',  activebackground = 'gold', highlightbackground = "#bce8f1", highlightthickness = 0.5, relief = RAISED, borderwidth = "2", command = None)
btn1.place(x=780, y=20, anchor = 'nw')
btn2 = Btn(root, text = "Animate", width = 15, height = 0, font = ("Calibri", 15, 'bold', 'italic'), bg = "#000", foreground = '#fff', activebackground = 'gold', highlightbackground = "#bce8f1", highlightthickness = 0.5, relief = RAISED, borderwidth = "2", command = Animate)
btn2.place(x = 500, y = 20, anchor = 'nw')

#if __name__=='__main__':
Skeleton()
