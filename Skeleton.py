from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from TkinterDnD2 import *
from glob import glob
import pygame, os
from time import sleep
from tkinter import ttk
from tooltip import *
from PIL import ImageTk, ImageDraw, ImageOps
try:
    import Image
except ImportError:
    from PIL import Image
from scrollimage import ScrollableImage
from animator import anime
import smtplib, ssl
import cv2, time
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import librosa
from tkinter.colorchooser import askcolor

root = TkinterDnD.Tk()
pygame.init()
class Main:
    menuBar = Menu(root)
    FileMenu = Menu(menuBar, tearoff = 0)
    ToolMenu = Menu(menuBar, tearoff = 0)
    HelpMenu = Menu(menuBar, tearoff = 0)
    sound_track = None
    images = [sound_track, 'imgs\\skeleton.jpg']
    File = "Untitled"
    def __init__(self):
        root.geometry('900x650')
        root.title("Untitled - Solemn2D 1.0")
        root.config(bg = 'white')
        try:root.wm_iconbitmap("imgs\\logo.ico")
        except:pass
        self.FileMenu.add_command(label = "Open Image", command = self.Open_image)
        self.FileMenu.add_command(label = "Import Sound", command = self.FetchSound)
        self.FileMenu.add_command(label = "New project    Ctrl+N", command = self.New)
        self.FileMenu.add_command(label = "Open project   Ctrl+O", command = self.Open)
        self.FileMenu.add_command(label = "Save Project   Ctrl+S", command = self.save)
        self.FileMenu.add_command(label = "SaveAs", command = self.SaveAs)
        self.FileMenu.add_command(label = "Export", command = self.export)
        self.FileMenu.add_command(label = "Exit           Ctrl+Q", command = self._quit_)
        
        self.HelpMenu.add_command(label = "About ", command = self.About)
        self.HelpMenu.add_command(label = "How to use  F1", command = self.Use)
        self.HelpMenu.add_command(label = "Version ", command = self.version)
        self.HelpMenu.add_command(label = "Send Feedback", command = self.feedback)
        
        self.ToolMenu.add_command(label = "Next Frame", command = self.next_frame)
        self.ToolMenu.add_command(label = "Previous Frame", command = self.prev_frame)
        self.ToolMenu.add_command(label = "Delete Current Frame", command = self.del_frame)
        self.ToolMenu.add_command(label = "Duplicate Frame", command = self.duplicate)
        self.ToolMenu.add_command(label = "Preview       F5", command = self.Animate)

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
        # root.bind('<Motion>', lambda:self.coord())
        root.bind('<ButtonRelease-1>', lambda x:[self.update_frame()])

        root.protocol('WM_DELETE_WINDOW', self._quit_)

        self.file = None
        self.n = 1

        self.FPS = IntVar()
        fps_label = ttk.LabelFrame(root, text = "fps", width = 100, height = 53)
        fps_label.place(x = 375, y = 7)
        self.fps = Spinbox(fps_label, from_ = 1, to = 150, width  = 10, bd= 2, textvariable = self.FPS)
        self.fps.place(x = 10, y = 2)
        create_Tip(self.fps, "Set the frames per second")

    def _quit_(self):
        if askokcancel("Exit", "Are you sure you want to quit?"):
            root.destroy()
            pygame.quit()

    def coord(self):
        x, y = root.winfo_pointerx(), root.winfo_pointery()
        return x, y

    def update_frame(self):
        if self.coord()[0]>= 775 and self.coord()[1] >= 100:#work on this area
            self.n = self.navFrame.get()
            self.img_win.del_canvas()
            try:
                img = Image.open(self.images[self.n])
            except:
                pass
            try:
                img = ImageTk.PhotoImage(img)
                self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = self.line_width)
                self.img_win.place(x = 130, y = 100)
                self.img_win.setup(self.line_width, self.pen_button)
            except UnboundLocalError:
                pass

    def comingsoon(self):showinfo("Very Sorry", "This feature is not available for this version of the app,\n you can check for the latest verison with the\n version button in the help menu")

    def Open_image(self): 
        try:
            self.file = askopenfilename(title = "Open image - Solemn2D 1.0", defaultextension = " .top", filetypes = [("All Files", "*.*")])
        except FileNotFoundError:pass
        if self.file == '':
            self.file = None
        else:
            try:
                self.images.append(self.file)
                self.n = self.images.index(self.file)
                self.img_win.del_canvas()
                img = Image.open(self.file)
                img = ImageTk.PhotoImage(img)
                self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450)
                self.img_win.place(x = 130, y = 100)
                self.img_win.setup(self.line_width, self.pen_button)
                self.update_nav()
            except Exception as e:
                showinfo("An Error Occured", e)

    def New(self):
        root.title("Untitled - Solemn2D 1.0")
        self.file = None
        self.images = [self.sound_track, 'imgs\\skeleton.jpg']
        self.img_win.del_canvas()
        img = Image.open('imgs\\skeleton.jpg')
        img = ImageTk.PhotoImage(img)
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450)
        self.img_win.place(x = 130, y = 100)
        self.img_win.setup(self.line_width, self.pen_button)
        self.update_nav()

    def Open(self):
        self.File = askopenfilename(title = "Open recent project - Solemn2D 1.0", defaultextension = " .top", filetypes = [("Tuple Of Pics" , "*.top") ])
        if self.File == '' or self.File == None:
            self.File = None
        else:
            root.title(os.path.basename(self.File).replace('.top', '') + " - Solemn2D 1.0")
            try:
                file = open(self.File, "r")
                file = file.read()
                self.images = eval(file)
                # print(self.images)
                # file.close()
                self.update_nav()
            except FileNotFoundError:
                showinfo("ALERT", "Hey, you didn't open a file")

    def save(self):         
        if not os.path.exists(self.File):
            self.File = asksaveasfilename(title = "Save Project - Solemn2D 1.0", initialfile = 'Untitled.top', defaultextension = " .top", filetypes = [("Tuple Of Pics", "* .top")])
            if self.File == '':
                self.File == "Untitled"
            else:
                root.title(os.path.basename(self.File).replace('.top', '') + "- Solemn2D 1.0")
                with open(self.File, 'w+') as f:
                    data = str(self.images)
                    f.write(data)                                                                                                                                                                                                                           
                    f.close()
        else:
            with open(self.File, 'w+') as f:
                f.truncate()
                f.write(str(self.images))
                f.close

    def SaveAs(self):
        self.File = askopenfilename(title = "Solemn2D 1.0 - Save As")
        if self.File == '':
            self.File == "Untitled"
        else:
            root.title(os.path.basename(self.File).replace('.top', '') + "- Solemn2D 1.0")
            with open(self.File, 'w+') as f:
                data = str(self.images)
                f.write(data)
                f.close()

    def About(self):showinfo('About Solemn2D', "Made by Praise James a.k.a ... nevermine\n Special thanks to: stackoverflow.com,\n pixabay.com for images\n Send Feedback with the send feedback\n button to help us improve Solemn2D")

    def Use(self):
        file = open('how.txt', 'r')
        showinfo("How to use", file.read())
       
    def Animate(self):
        pygame.init()
        self.progressing()
        showinfo("Success", "Animation ready for preview")
        fps_ = self.FPS.get()
        images = self.images
        anime.animate(images, float(1/fps_))
        #====================TEST===========================
        #images = [i for i in glob('*.jpg')]
        #anime.animate(images, 1)
        #=================END OF REGION=====================

    def hidefile(self, filename):
        import win32file, win32con, win32api
        flags = win32file.GetFileAttributesW(filename)
        win32file.SetFileAttributes(filename, win32con.FILE_ATTRIBUTE_HIDDEN|flags)
    
    def file_in(self, e):
        try:
            e = root.tk.splitlist(e.data)[0]
            self.images.append(e)
            self.n = self.images.index(e)
            self.img_win.del_canvas()
            img = Image.open(e)
            img = ImageTk.PhotoImage(img)
            self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = 10)
            self.img_win.place(x = 130, y = 100)
            self.update_nav()
        except Exception as E:
            showinfo("An Error Occured", E)
       
    def widgets(self):
        global progress_bar, img_, Frame
        try:self.track = AudioSegment.from_mp3(self.images[0])
        except:pass
        class Sound:
            """class for sound editing"""
            def __init__(self):
                try:
                    self.track = AudioSegment.from_mp3(self.images[0])
                except:pass
                # stack and queue are arrays used for the undo/redo functionality. 
                self.queue = []
                self.stack = []
    
            def save(self):
                save_path = asksaveasfilename(initialdir = "/home/", title = "Where do you want to save the modified file?", filetypes = (("mp3 files","*.mp3"), ("all files","*.*")))
                self.track.export(save_path, bitrate = "320k",format = "mp3")
        
            def reverse(self):
                self.stack.append(self.track)
                self.track = self.track.reverse()
                self.images[0] = self.track

            def checkLength(self):return self.track.duration_seconds

            def mergeTracks(self):
                self.stack.append(self.track)
                self.filePath = askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
                self.mergeTrack = AudioSegment.from_mp3(self.filePath)
                self.track = self.track + self.mergeTrack

            def gapMerge(self):
                self.stack.append(self.track)
                self.filePath = tkFileDialog.askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
                self.mergeTrack = AudioSegment.from_mp3(self.filePath)
                self.track = self.track + AudioSegment.silent(duration = 10000) + self.mergeTrack

            def repeat(self):
                self.stack.append(self.track)
                self.track = self.track*2
        
            def overlay(self):
                self.stack.append(self.track)
                self.filePath = askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
                self.overlayTrack = AudioSegment.from_mp3(self.filePath)
                self.track = self.track.overlay(self.overlayTrack)

            def undo(self):
                self.queue.insert(0, self.track)
                self.track = self.stack.pop()
    
            def redo(self):
                self.stack.append(self.track)
                self.track = self.queue[0]
                self.queue.pop(0)
        
        class Btn(Button):
            def __init__(self, master, **kw):
                Button.__init__(self, master = master, **kw)
                self.defaultBackground = self["background"]
                self.config(relief = GROOVE)
                self.bind("<Enter>", self.on_enter)
                self.bind("<Leave>", self.on_leave)

            def on_enter(self, e): self['background'] = self['activebackground']
            def on_leave(self, e): self['background'] = self.defaultBackground

        status_bar = Frame(root, width= 4000, height = 60)
        status_bar.place(x = 0, y = root.winfo_height())
        progress_bar = ttk.Progressbar(status_bar, orient = 'horizontal', length = 168, mode = 'determinate')
        progress_bar.place(x = 800, y = 7)#place(x = 670, y = 500)
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.file_in)

        toolbar = Canvas(root, width = 400000, height = 80).pack()

        frame = ttk.LabelFrame(root, text = "Tools", width = 340, height = 60)
        frame.place(x = 20, y = 7)

        btn0 = Btn(frame, text = "Prev", width = 7, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.prev_frame)
        btn0.place(x=30, y=1, anchor = 'nw')
        create_Tip(btn0, "Go to previous frame")
        btn1 = Btn(frame, text = "Next", width = 7, height = 0, font = ('Calibri', 12), bg = '#000', foreground = '#FFF',  activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.next_frame)
        btn1.place(x=100, y=1, anchor = 'nw')
        create_Tip(btn1, "Go to the next frame")
        btn2 = Btn(frame, text = "Delete", width = 7, height = 0, font = ("Calibri", 12), bg = "#000", foreground = '#fff', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.del_frame)
        btn2.place(x = 180, y = 1, anchor = 'nw')
        create_Tip(btn2, "delete the current frame")
        btn3 = Btn(frame, text = "Preview", width = 7, height = 0, font = ("Calibri", 12), bg = "#000", foreground = '#fff', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5,borderwidth = "2", command = self.Animate)
        btn3.place(x = 258, y = 1, anchor = 'nw')
        create_Tip(btn3, "View animation preview")

        img = Image.open('imgs\\skeleton.jpg')
        img = ImageTk.PhotoImage(img)
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = 10)
        self.img_win.place(x = 130, y = 100)
        self.img_win.save('test.png')

        Frame = ttk.LabelFrame(root, text = "Extras", width = 350, height = 60)
        Frame.place(x = 500, y = 7)
        drawbtn = Button(Frame, text = "Sketch", width = 5, command = self.drawimage)
        drawbtn.place(x = 5, y = 5)
        create_Tip(drawbtn, "Turn the current frame pic into a sketch")
        blurbtn = Button(Frame, text = "Blur", width = 5, command = self.blurimage)
        blurbtn.place(x = 60, y = 5)
        create_Tip(blurbtn, "Blur the image in the current frame")
        mirrorbtn = Button(Frame, text = "Mirror", width = 5, command = self.mirror)
        mirrorbtn.place(x = 115, y = 5)
        create_Tip(mirrorbtn, "Add mirror effect to an image")
        loop = Checkbutton(Frame, text = "loop")
        loop.place(x = 170, y = 5)
        create_Tip(loop, "Don't worry  about this \nit doesn't do anything yet")
        self.update_nav()

        def Merge(self):
            Sound.mergeTracks(self.track)
            self.durLabel['text'] = "Track Duration: " + str(int(sound.checkLength(self.tr))) + "s"
        
        def gapmerge(self):
            Sound.gapMerge(self.track)
            self.durLabel['text'] = "Track Duration: " + str(int(Sound.checkLength(askopenfilename(title = "Open another sound file for merge")))) + "s"

        def repeat(self):
            Sound.repeat(self.track)
            self.durLabel['text'] = "Track Duration: " + str(int(Sound.checkLength(self.track))) + "s"

        def overlayTrack(self):
            Sound.overlay(self.track)
            self.durLabel['text'] = "Track Duration: " + str(int(sound.checkLength(self.tr))) + "s"


        self.sound_frame = ttk.LabelFrame(root, text = "Sound", width = 130, height = 350)
        self.sound_frame.place(x = 870, y = 100)

        self.reverse = Button(self.sound_frame, text="Reverse Track", width = 16, command = lambda: Sound.reverse(self.track), relief = GROOVE)
        self.reverse.place(x=2,y=2)
        create_Tip(self.reverse, "Reverse the track(turn the\ntrack backwards)")
        merge = Button(self.sound_frame, text="Gapless Merge", width = 16, command = lambda: self.Merge(), relief = GROOVE)
        merge.place(x = 2, y=32)

        self.gapMerge = Button(self.sound_frame, text = "Merge with Gap", width = 16, command = lambda: self.gapmerge(), relief = GROOVE)
        self.gapMerge.place(x=2,y=62)
        create_Tip(self.gapMerge, "Merge two audio files together with a gap between them")

        self.repeat = Button(self.sound_frame, text = "Repeat", width = 16, command = lambda: self.repeat())
        self.repeat.place(x=2,y=92)
        create_Tip(self.repeat, "Repeat track once again")

        self.overlay = Button(self.sound_frame, text = "Overlay", width = 16, command = lambda: self.overlayTrack())
        self.overlay.place(x=2,y=122)
        create_Tip(self.overlay, "Overlay two tracks together")

        self.savesound = Button(self.sound_frame, text="Save changes", width = 16, command = lambda: Sound.save(self.track), relief = GROOVE) 
        self.savesound.place(x=2,y=152)
        create_Tip(self.savesound, "Save current changes\n made on sound")

        self.undo = Button(self.sound_frame, text = "Undo", command = lambda: sound.undo(self.track), relief = GROOVE)
        self.undo.place(x=22, y=182)
        create_Tip(self.undo, "Undo changes made on sound")

        self.redo = Button(self.sound_frame, text = "Redo", command = lambda: sound.redo(self.track), relief = GROOVE)
        self.redo.place(x=65, y=182)
        create_Tip(self.redo, "Redo changes made on sound")

        self.play = Button(self.sound_frame, text = "Play", command = self.play, relief=GROOVE)
        self.play.place(x=22, y=212)

        self.stop = Button(self.sound_frame, text = "Stop", command = self.stop, relief = GROOVE)
        self.stop.place(x =65, y=212)
        
        self.maxtempo = Button(self.sound_frame, text = "Max tempo", command = self.Max_tempo, relief = GROOVE)
        self.maxtempo.place(x=32, y=242)

        self.change_voice_label = ttk.LabelFrame(self.sound_frame, text = "Change voice", width = 140, height = 120)
        self.change_voice_label.place(x = 2, y = 272)
        self.shift = IntVar()
        self.change = Spinbox(self.change_voice_label, from_ = -150, to = 150, width  = 5, bd= 2, textvariable = self.shift)
        self.change.place(x = 2, y = 2)
        create_Tip(self.change, "Set the change rate of the voice")
        self.Change_voice = Button(self.change_voice_label, text = "Change", command = lambda :self.change_voice(self.shift))
        self.Change_voice.place(x = 70, y =2)
        self.durLabel = Label(self.sound_frame, text = "Track duration: 0")
        self.update_sound_editing_tools()

        self.image_frame = ttk.LabelFrame(root, text = "Edit Image", width = 120, height= 280)
        self.image_frame.place(x = 2, y = 100)
        self.pen_button = Button(self.image_frame, width = 12, text='pen', command=None)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.image_frame, width = 12, text='brush', command=self.brush)
        self.brush_button.grid(row=1, column=0)

        self.color = None
        self.color_button = Button(self.image_frame, width = 12, text='color', command=self.Color)
        self.color_button.grid(row=2, column=0)

        self.eraser_button = Button(self.image_frame, width = 12, text='eraser', command=None)
        self.eraser_button.grid(row=3, column=0)

        self.choose_size_button = Scale(self.image_frame, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=4, column=0)
        self.line_width = self.choose_size_button.get()
        self.img_win.setup(self.line_width, self.pen_button, color = self.color)

    def Color(self):
        self.color = askcolor(title = "select a color")[1]
        self.eraser_on = False
        self.color_button.config(bg = self.color)
        self.img_win.setup(self.line_width, self.pen_button, color = self.color)

    def brush(self):
        self.img_win.activate_button(self.brush_button)

    def change_voice(self, shift):
        y, sr = librosa.load(self.images[0])
        b = librosa.effects.pitch_shift(y, sr, n_steps = shift)
        progressing()
        sf.write(self.title+'.wav', b, sr)

    def Max_tempo(self):
        src = self.images[0]
        dst = 'in.wav'
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format = 'wav')
        data, samplerate = sf.read("in.wav")
        # print(data.shape)
        # print(samplerate)

        # plt.plot(data)
        # plt.show()
        samplerate = int(samplerate * 1.5)
        self.progressing()

        sf.write("out.wav", data, samplerate)
        os.system("out.wav")

    def stop(self):
        pygame.mixer.music.stop()
        self.play.config(text = "Play", command = self.play)
    def resume(self):
        pygame.mixer.music.unpause()
        self.play.config(text = "Pause", command = self.pause)
    def pause(self):
        pygame.mixer.music.pause()
        self.play.config(text="Resume", command = self.resume)
    def play(self):
        try:
            pygame.mixer.music.load(self.images[0])
            pygame.mixer.music.play(-1)
            self.play.config(text = "Pause", command = self.pause)
        except Exception as e:
            showerror("An error occured", e)

    def update_sound_editing_tools(self):
        if self.images[0]==None:
            self.reverse.config(state=DISABLED)
            self.savesound.config(state = DISABLED)
            self.undo.config(state=DISABLED)
            self.redo.config(state = DISABLED)
            self.repeat.config(state = DISABLED)
            self.overlay.config(state = DISABLED)
        else:
            pass

    def blurimage(self):
        img = self.images[self.n]
        if askokcancel("Warning", "Are you sure about this? \nThis would replace the image with the blurred\n one, if you want to keep it, you have to duplicate\n it, click prev and next to refresh and see the image"):
            blur = cv2.blur(cv2.imread(img), (10, 10))
            os.remove(img)
            cv2.imwrite(img, blur)
            self.images[self.n] = img

    def drawimage(self):
        img = self.images[self.n]
        if askokcancel("Warning", "Are you sure about this? \nThis would replace the image with the sketched\n one, if you want to keep it, you have to duplicate\n it, click prev and next to refresh and see the image"):
            gray = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
            smoothing = cv2.GaussianBlur(cv2.bitwise_not(gray), (21, 21), sigmaX = 0, sigmaY = 0)
            image = cv2.divide(gray, 255 - smoothing, scale = 256)
            os.remove(img)
            cv2.imwrite(img, image)
            self.images[self.n] = img

    def progressing(self):
        progress_bar['maximum'] = 100
        for i in range(101):
            sleep(0.05)
            progress_bar["value"] = i
            progress_bar.update()
        progress_bar["value"] = 0

    def next_frame(self):
        self.n += 1
        self.img_win.del_canvas()
        try:
            img = Image.open(self.images[self.n])
        except:
            pass
        try:
            img = ImageTk.PhotoImage(img)
            self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = 10)
            self.img_win.place(x = 100, y = 100)
        except UnboundLocalError:
            pass

    def prev_frame(self):
        self.n -=1
        self.img_win.del_canvas()
        try:
            img = Image.open(self.images[self.n])
        except:
            pass
        try:
            img = ImageTk.PhotoImage(img)
            self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = 10)
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
        showinfo("Version", "Solemn2D version 1.0")
        
        pop = Tk()
        pop.title('check for latest version')
        pop.geometry('150x50')
        pop.resizable(False, False)
        pop.wm_iconbitmap('imgs\\logo.ico')

        def checklatest():
            import webbrowser
            pop.destroy()
            webbrowser.open('https://sourceforge.net/projects/solemn2d/files/')
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
            except Exception as e:showerror("An Error Occured", e)

        btn = Button(pop, text = 'Send', command = send)
        btn.place(x = 170, y = 150)

        create_Tip(email, 'Enter your email here')
        create_Tip(password, 'Enter your password here')
        create_Tip(message, 'Enter your feedback')

    def FetchSound(self):
        self.images[0] = askopenfilename(title = "Open Sound Track - Solemn2D 1.0")
        try:self.track = AudioSegment.from_mp3(self.images[0])
        except:pass
        self.update_sound_editing_tools()

    def createVid(self, images, fps, title, audio):
        imgs = []
        for i in images:
            img = cv2.imread(i)
            height, width, layer = img.shape
            size = (width, height)
            imgs.append(img)
        Title = title.replace('.top', '')
        print(Title)
        output = cv2.VideoWriter(Title, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for i in range(len(imgs)):
            output.write(imgs[i])
        output.release()
        if self.images[0] is not None:
            os.popen(f'CMD /K ffmpeg -i ' + Title + ' -i ' + audio +' -map 0:0 -map 1:0 -c:v copy -c:a copy ' + title)

    def export(self):
        images = self.images[1:]
        fps = self.FPS.get()
        self.progressing()
        title = self.File.replace('.avi', '') + '.avi'
        try:
            self.createVid(images, fps, title, audio = self.images[0])
        except TypeError:
            showerror("An Error Occured", "You'll need to import an audio to export the project")
        showinfo("Success", "Your animation was exported succesfully exported to "+title)

    def duplicate(self):
        import shutil
        src = self.images[self.n]
        new = src.replace('.', '') + '(d)' + '.jpg'
        shutil.copy(src, new)
        self.images.append(new)
        self.n = self.images.index(new)
        self.img_win.del_canvas()
        img = Image.open(new)
        img = ImageTk.PhotoImage(img)
        self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 450, line_width = 10)
        self.img_win.place(x = 100, y = 100)

    def mirror(self):
        try:
            img = Image.open(self.images[self.n])
        except:pass
        image = ImageOps.mirror(img)
        im = self.images[self.n].replace('.', '') + '.jpg'
        image = image.save(im)
        self.images.append(im)

    def update_nav(self):
        self.navFrame = Scale(Frame, from_ = 1, to = len(self.images)-1, orient = HORIZONTAL)
        self.navFrame.place(x = 225, y = 0)
        create_Tip(self.navFrame, "Navigate through frames by dragging")

if __name__=='__main__':
    Main()
    root.mainloop()
