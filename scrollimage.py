from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
import io
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfile

topx, topy, botx, boty = 0, 0, 0, 0
acts = []
past = []
class ScrollableImage(Frame):
	def __init__(self, master = None, **kw):
		self.image = kw.pop('image', None)
		self.line_width = line_width = kw.pop('line_width', None)
		sw = kw.pop('scrollbarwidth', 10)
		super(ScrollableImage, self).__init__(master = master, **kw)
		self.canvas = Canvas(self, highlightthickness = 0, **kw)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)
		# Vertical and Horizontal scrollbars
		self.v_scroll = Scrollbar(self, orient='vertical', width=sw)
		self.h_scroll = Scrollbar(self, orient='horizontal',width=sw)
		# Grid and configure weight.
		self.canvas.grid(row=0, column=0, sticky='nsew')
		self.h_scroll.grid(row=1, column=0, sticky='ew')
		self.v_scroll.grid(row=0, column=1, sticky='ns')
		self.rowconfigure(0, weight=10)
		self.columnconfigure(0, weight =10)
		# Set the scrollbars to the canvas
		self.canvas.config(xscrollcommand=self.h_scroll.set,yscrollcommand=self.v_scroll.set)
		# Set canvas view to the scrollbars
		self.v_scroll.config(command=self.canvas.yview)
		self.h_scroll.config(command=self.canvas.xview)
		# Assign the region to be scrolled
		self.canvas.config(scrollregion=self.canvas.bbox('all'))
		self.canvas.bind_class(self.canvas, "<MouseWheel>", self.mouse_scroll)

		self.count = 0

	def mouse_scroll(self, evt):
		if evt.state == 0 :
			self.canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
			self.canvas.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
		if evt.state == 1:
			self.canvas.xview_scroll(-1*(evt.delta), 'units') # For MacOS
			self.canvas.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

	def change_image(self, img):
		self.canvas.create_rectangle(0, 0, 200, 300)
		self.canvas.create_image(0, 0, anchor='nw', image=img)

	def del_canvas(self):self.canvas.destroy()
	
	def clear(self):self.canvas.create_rectangle(0, 0, 2000, 2000, outline = None, fill = "white")

	def setup(self, line_width, pen, color = None):
		self.old_x = None
		self.old_y = None
		self.line_width = line_width
		self.color = "black"if color == None else color
		self.eraser_on = False
		self.active_button = pen
		self.canvas.bind('<B1-Motion>', self.paint)
		self.canvas.bind('<ButtonRelease-1>', self.reset)

	def choose_color(self):
		self.eraser_on = False
		self.color = askcolor(color=self.color)[1]

	def activate_button(self, some_button, eraser_mode=False):
		self.active_button = some_button
		self.active_button.config(relief=RAISED)
		some_button.config(relief=SUNKEN)
		self.eraser_on = eraser_mode

	def paint(self, event):
		self.line_width = self.line_width
		tag = "paint"+str(self.count)
		acts.append(tag)
		paint_color = 'white' if self.eraser_on else self.color
		if self.old_x and self.old_y:
			self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36, tags = tag)
		self.old_x = event.x
		self.old_y = event.y
		self.count += 1

	def reset(self, event):
		self.old_x, self.old_y = None, None

	def get_mouse_pos(self, event):
		global topy, topx
		topx, topy = event.x, event.y

	def update_selection(self, event):
		global shape_id
		global topy, topx, botx, boty
		botx, boty = event.x, event.y
		self.canvas.coords(shape_id, topx, topy, botx, boty)
		# self.count+=1

	def drawrect(self, color1, color2, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		# topx, topy, botx, boty = 0, 0, 0, 0
		window.config(cursor="crosshair")
		tag = "rect" + str(self.count)
		acts.append(tag)
		self.canvas.bind('<Button-1>', self.get_mouse_pos)
		shape_id = self.canvas.create_rectangle(topx, topy, topx, topy, width=linewidth, fill=color2, outline=color1, tags = tag)
		self.canvas.create_rectangle(topx, topy, topx, topy, width=linewidth, fill=color2, outline=color1, tags = tag)
		self.canvas.bind('<B1-Motion>', self.update_selection)
		self.count+=1

	def drawcircle(self, color1, color2, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		window.config(cursor="crosshair")
		tag = "circle" + str(self.count)
		acts.append(tag)
		try:self.canvas.bind('<Button-1>', self.get_mouse_pos)
		except:pass
		shape_id = self.canvas.create_oval(topx, topy, botx, boty, width=linewidth, fill=color2, outline=color1, tags=tag)
		# self.canvas.create_oval(topx, topy, botx, boty, width=linewidth, fill=color2, outline=color1, tags=tag)
		self.canvas.bind('<B1-Motion>', self.update_selection)
		self.count+=1


	def drawLine(self, color, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		window.config(cursor="crosshair")
		tag = "line" + str(self.count)
		acts.append(tag)
		self.canvas.bind('<Button-1>', self.get_mouse_pos)
		shape_id = self.canvas.create_line(topx, topy, botx, boty, width=linewidth, fill=color, tags=tag)
		self.canvas.bind('<B1-Motion>', self.update_selection)
		self.count += 1

	def save(self):
		ps = self.canvas.postscript(colormode='color')
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		f = asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[('JPG files', '*.jpg')])
		if f is None:
			return
		img.save(f, 'jpeg')
		showinfo("Successfull", "Image saved as " + str(f))

	def append_and_return(self, lst, item):
		lst.append(item)
		return item

	def _undo_(self):
		# print(self.count)
		# print(acts).,
		self.canvas.delete(self.append_and_return(past, acts.pop(self.count-1)))
		self.count -= 2

	def _redo_(self):
		past.pop()
