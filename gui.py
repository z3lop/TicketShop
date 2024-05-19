from tkinter import Tk, Label, Frame, Entry, Button, BooleanVar, DoubleVar, Menu, messagebox, END, X
from tkinter.font import Font
from tkinter.ttk import Spinbox, Checkbutton, Separator, Treeview, Scrollbar
from ttkbootstrap import Style
import re

import ticket_shop
import loginData
import manageDropbox

class windows(Tk):
  def download_button(self):
    manageDropbox.dropbox_download_file()
    messagebox.showinfo("Info", "Datei wurde runtergeladen")

  def upload_button(self):
    manageDropbox.dropbox_upload_file()
    messagebox.showinfo("Info", "Datei wurde hochgeladen")
  
  def menubar(self):
    self.menubar = Menu(self)
    self.add_users = Menu(self.menubar, tearoff=0)
    self.files = Menu(self.menubar, tearoff=0)

    self.menubar.add_cascade(label="Datein", menu =self.files)
    self.menubar.add_cascade(label='Tickets', menu = self.add_users)
    
    self.files.add_command(label = 'Neu (überschreiben)')
    self.files.add_command(label = 'Öffnen', command = lambda: self.show_frame(ShowDataFrame))

    self.files.add_separator()

    self.files.add_command(label = "Dropbox", command= lambda: self.show_frame(DropBoxScreen))
    self.files.add_command(label = 'Herunterladen', command = self.download_button)
    self.files.add_command(label = 'Hochladen', command = self.upload_button)

    self.add_users.add_command(label= "Tickets anlegen", command = lambda: self.show_frame(MainPage))
  
  def __init__(self, *args, **kwargs):
    Tk.__init__(self, *args, **kwargs)
    # Adding a title to the window
    self.wm_title("Test Application")
    style = Style(theme='darkly')
    
    # creating a frame and assigning it to container
    container = Frame(self, height=720, width=1280)
    self.geometry('640x360')
    # specifying the region where the frame is packed in root
    container.pack(side="top", fill="both", expand=True)

    # configuring the location of the container using grid
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.menubar()
    self.config(menu=self.menubar)

    # We will now create a dictionary of frames
    self.frames = {}
    # we'll create the frames themselves later but let's add the components to the dictionary.
    for F in (MainPage, SidePage, DropBoxScreen, ShowDataFrame):
        frame = F(container, self)

        # the windows class acts as the root window for the frames.
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    # Using a method to switch frames
    self.show_frame(MainPage)
  
  def show_frame(self, cont):
    # cont is a children class of the main window
    frame = self.frames[cont]
    # raises the current frame to the top
    frame.tkraise()
		
class MainPage(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    self.pack(fill='both', expand = True)
    
    style = Style(theme='darkly')
    frame_c = Frame(self)
  
    
    used_font = Font(family = 'Calibri', size = 12, weight = 'normal')
    spinbox_font = Font(family = 'Calibri', size = 10, weight = 'normal')
    small_font = Font(family = 'Calibri', size = 8, weight = 'normal')
    

    # We use the switch_window_button in order to call the show_frame() method as a lambda function
    x = 0.2
    y = 0.1
    width = 20
    height = 20
    eat = BooleanVar()
    var2 = BooleanVar()
    var2.set(True)
    
    def font_change(event):
      #print( event.widget, event )  # See what is happening
  
      # Base size
      normal_width = 360
      normal_height = 640
  
      # Screen
      screen_width = event.width
      screen_height = event.height
  
      # Get percentage of screen size from Base size
      percentage_width = screen_width / (normal_width / 100)
      percentage_height = screen_height / (normal_height / 100)
  
      minimum_size = 8
  
      # Make a scaling factor
      scale_factor = ((percentage_width + percentage_height) / 2) / 100
  
      # Set the fontsize based on scale_factor,
      # if the fontsize is less than minimum_size
      # it is set to the minimum size
      
      # font_size is the variable to store actual size
      
      if scale_factor > minimum_size/12:
          font_size = int(12 * scale_factor)
          height = int(20 * scale_factor)
          width = int(200 * scale_factor)
      
      else:
          font_size = minimum_size
          height = 20
          width = 200
  
      used_font.configure( size = font_size )
      spinbox_font.configure(size = int(font_size*0.8))
      small_font.configure(size= int(font_size*0.7))
      
      PRENAME.place(height = height, width = width)
      NAME.place(height = height, width = width)
      MAIL.place(height = height, width = width)
      NUM.place(height = height, width = width/4)
      vegetarian.place(height = height, width = width/4)
      vegan.place(height = height, width = width/4)
      
      make_ticket.configure(font = spinbox_font)
      
      #KOMBI.place(height=height*1.5, width = width)
      #PARTY.place(height=height*1.5, width = width)
      
      style.configure('Toolbutton', font = spinbox_font, size = scale_factor*0.7)

    def toggle_options() -> None:
      if eat.get():
        frame_c.pack(fill= 'both', expand = True)
        var2.set(False)
        
      else:
        frame_c.pack_forget()
        var2.set(True)

    def value_two() -> None:
      if var2.get():
        eat.set(False)
        frame_c.pack_forget()
      else:
        frame_c.pack(fill = 'both', expand = True)
        eat.set(True)

    def set_value() -> None:
      vegetarian.configure(from_ = 0, to= NUM.get())
      vegan.configure(from_= 0, to = NUM.get())

    def set_vegan() -> None:
      max = int(NUM.get())- int(vegetarian.get())
      vegan.configure(from_ = 0, to = max)  

    def set_vege() -> None:
      max = int(NUM.get()) -int(vegan.get())
      vegetarian.configure(from_ = 0, to  = max)

    PRENAME = Entry(self, width = width, font=used_font)
    NAME = Entry(self, width = width, font = used_font)
    MAIL = Entry(self, width = width, font = used_font)
    NUM = Spinbox(self, from_ = 0, to = 10, increment=1, width = 6, command=set_value, font = spinbox_font, state='readonly')
    KOMBI = Checkbutton(self, text = 'Kombi', variable=eat, command=toggle_options, style='Toolbutton')
    PARTY = Checkbutton(self, text = 'Party', variable=var2, command=value_two, style='Toolbutton')
    
    
    var_veg = DoubleVar(value = 0)
    var_ve = DoubleVar(value = 0)
    vegetarian = Spinbox(frame_c, text = 'vegetarisch', command = set_vegan, textvariable=var_veg, font = spinbox_font, state='readonly')
    vegan = Spinbox(frame_c, text='vegan', command = set_vege, textvariable= var_ve, font = spinbox_font, state='readonly')
    
    vegetarian.place(relx = 2*x, rely = 8*y)
    vegan.place(relx= 3*x, rely = 8*y)
    label_vegetarian = Label(frame_c, text = 'vegetarisch', font = spinbox_font)
    label_vegan = Label(frame_c, text='vegan', font = spinbox_font)
    
    label_vegan.place(relx = 3*x, rely = 7.2*y)
    label_vegetarian.place(relx = 2*x, rely = 7.2*y)

    PRENAME.place(relx = 2*x, rely = y, height=height)
    NAME.place(relx=2*x, rely = 2*y, height = height)
    MAIL.place(relx = 2*x, rely = 3*y, height = height)
    NUM.place(relx = 2*x, rely = 4*y, height= height)
    KOMBI.place(relx = 2*x, rely = 5*y/0.9)
    PARTY.place(relx = 3*x, rely = 5*y/0.9)

    label_prename = Label(self, text = 'Vorname', font = used_font)
    label_name = Label(self, text = 'Name', font = used_font)
    label_mail = Label(self, text = 'E-Mail', font = used_font)
    label_num = Label(self, text = 'Ticketanzahl', font = used_font)
    
    label_prename.place(relx=x, rely=y)
    label_name.place(relx = x, rely = 2*y)
    label_mail.place(relx = x, rely = 3*y)
    label_num.place(relx= x, rely = 4*y)

    self.bind('<Configure>', font_change)

    make_ticket = Button(
      self,
      text="Ticket anlegen",
      command= lambda: self.pressButton(controller, PRENAME, NAME, MAIL, NUM, eat, var_veg, var_ve),
    )
    make_ticket.pack(side="bottom", fill=X)
    
		
  def pressButton(self, controller,PRENAME, NAME, MAIL, NUM, eat, var_veg, var_ve):
    self.collect_data(PRENAME, NAME, MAIL, NUM, eat, var_veg, var_ve)
    self.clear_entries(PRENAME, NAME, MAIL, NUM)
    frame = controller.frames[SidePage]
    frame.tkraise()
  
  def clear_entries(self, PRENAME, NAME, MAIL, NUM):
    PRENAME.delete(0, 'end')
    NAME.delete(0,'end')
    MAIL.delete(0,'end')

  def collect_data(self, PRENAME: Entry, NAME: Entry, MAIL: Entry, NUM, eat, var_veg, var_ve):
    num_ticket = int(NUM.get())
    prename = str(PRENAME.get())
    name = str(NAME.get())
    mail = str(MAIL.get())
    meal_bool = int(eat.get())
    var_ve = int(var_ve.get())
    var_veg = int(var_veg.get())
    
    df = ticket_shop.DataFrameOperations()
    if meal_bool == True:
      bool = df.add_to_df(prename, name, mail, num_ticket, meal_bool, [var_veg, var_ve])
    else:
      bool = df.add_to_df(prename, name, mail, num_ticket, meal_bool)

    if bool == True:
      df.write_to_csv()
      df.make_and_send_qr_code()
    else:
      print('Form not filled out correctly')
  
class SidePage(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)

    used_font = Font(family = 'Calibri', size = 12, weight = 'normal')
    spinbox_font = Font(family = 'Calibri', size = 10, weight = 'normal')
    small_font = Font(family = 'Calibri', size = 8, weight = 'normal')
    
    label = Label(self, text="Ticket wurde angelegt", font = used_font)
    label.pack(fill = 'none', expand= True)

    def font_change(event):
      #print( event.widget, event )  # See what is happening
  
      # Base size
      normal_width = 360
      normal_height = 640
  
      # Screen
      screen_width = event.width
      screen_height = event.height
  
      # Get percentage of screen size from Base size
      percentage_width = screen_width / (normal_width / 100)
      percentage_height = screen_height / (normal_height / 100)
  
      minimum_size = 8
  
      # Make a scaling factor
      scale_factor = ((percentage_width + percentage_height) / 2) / 100
  
      # Set the fontsize based on scale_factor,
      # if the fontsize is less than minimum_size
      # it is set to the minimum size
      
      # font_size is the variable to store actual size
      
      if scale_factor > minimum_size/12:
          font_size = int(12 * scale_factor)
          small_font_size = int(8 * scale_factor)
          medium_font_size = int(10 * scale_factor)
          height = int(20 * scale_factor)
          width = int(200 * scale_factor)
      
      else:
          font_size = minimum_size
          small_font_size = minimum_size
          medium_font_size = minimum_size
          height = 20
          width = 200
  
      used_font.configure( size = font_size )
      spinbox_font.configure(size = medium_font_size)
      small_font.configure(size = small_font_size)
      
      switch_window_button.configure(font = used_font)

    switch_window_button = Button(
        self,
        text="Zurück zur Ticketerstellung",
        command=lambda: controller.show_frame(MainPage),
        font = used_font
    )
    switch_window_button.pack(side="bottom", fill=X)

    self.bind('<Configure>', font_change)

class DropBoxScreen(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)
    used_font = Font(family = 'Calibri', size = 12, weight = 'normal')
    spinbox_font = Font(family = 'Calibri', size = 10, weight = 'normal')
    small_font = Font(family = 'Calibri', size = 8, weight = 'normal')
    
    x = 0.2
    y = 0.1

    def handle_focus_in(_):
      tmp = APP_KEY.get()
      if (tmp == 'App Key einfügen') or (tmp == "App Key vorhanden"):
        APP_KEY.delete(0, END)
        APP_KEY.config(fg='white', show = '●')
  
    def handle_focus_in_secret(_):
      tmp = APP_SECRET.get()
      if (tmp == 'App Secret einfügen') or (tmp == 'App Secret vorhanden'):
        APP_SECRET.delete(0, END)
        APP_SECRET.config(fg='white', show = '●')
    
    def font_change(event):
      #print( event.widget, event )  # See what is happening
  
      # Base size
      normal_width = 360
      normal_height = 640
  
      # Screen
      screen_width = event.width
      screen_height = event.height
  
      # Get percentage of screen size from Base size
      percentage_width = screen_width / (normal_width / 100)
      percentage_height = screen_height / (normal_height / 100)
  
      minimum_size = 8
  
      # Make a scaling factor
      scale_factor = ((percentage_width + percentage_height) / 2) / 100
  
      # Set the fontsize based on scale_factor,
      # if the fontsize is less than minimum_size
      # it is set to the minimum size
      
      # font_size is the variable to store actual size
      
      if scale_factor > minimum_size/12:
          font_size = int(12 * scale_factor)
          small_font_size = int(8 * scale_factor)
          medium_font_size = int(10 * scale_factor)
          height = int(20 * scale_factor)
          width = int(200 * scale_factor)
      
      else:
          font_size = minimum_size
          small_font_size = minimum_size
          medium_font_size = minimum_size
          height = 20
          width = 200
  
      used_font.configure( size = font_size )
      spinbox_font.configure(size = medium_font_size)
      small_font.configure(size = small_font_size)
      
      ACCESS_CODE.place(height = height, width = width)
      APP_KEY.place(height = height, width = width)
      APP_SECRET.place(height = height, width = width)
      
      separator.place(x = 0, y = 0.3*scale_factor, relheight= 1, relwidth=1)

    try:
      tmp1 = loginData.read_from_env('APP_KEY')
    except ValueError:
      tmp1 = ''
    
    try: 
      tmp2 = loginData.read_from_env('APP_SECRET')
    except ValueError:
      tmp2 = ''

    separator = Separator(self, orient ='horizontal')

    Label(self, text = 'App Key', font = spinbox_font).place(relx = x, rely = 1*y)
    APP_KEY = Entry(self, fg = "grey", font = spinbox_font)
    if tmp1 == '':
      APP_KEY.insert(0, 'App Key einfügen')
    else:
      APP_KEY.insert(0, 'App Key vorhanden')
    APP_KEY.place(relx = x, rely=1.8*y)

    Label(self, text = 'App Secret', font = spinbox_font). place(relx = x, rely = 3*y)
    APP_SECRET = Entry(self, fg = 'grey', font = spinbox_font)
    if tmp2 == '':
      APP_SECRET.insert(0, 'App Secret einfügen')
    else: 
      APP_SECRET.insert(0, 'App Secret vorhanden')
    APP_SECRET.place(relx = x, rely = 3.8*y)

    KEY_BUTTON = Button(self, text = 'speichern', command=lambda: self.save_button_app(APP_KEY), font = small_font)
    SECRET_BUTTON = Button(self, text = 'speichern', command = lambda: self.save_button_secret(APP_SECRET), font = small_font)

    KEY_BUTTON.place(relx=3*x, rely = 1.8*y)
    SECRET_BUTTON.place(relx = 3*x, rely = 3.8*y)

    ADD = Button(self, text = 'erstellen', command = loginData.get_access_code, font = small_font)
    ADD.place(relx = 3*x, rely = 6*y)
    
    ACCESS_CODE = Entry(self, show = '●',font = spinbox_font)
    Label(self, text='Access Code eingeben', font = spinbox_font).place(relx = x, rely = 5.2*y)
    ACCESS_CODE.place(relx = x, rely = 6*y)
    
    SAVE = Button(self, text = 'speichern', font = small_font, command=lambda: self.save_button_access(ACCESS_CODE))
    SAVE.place(relx = 4*x, rely = 6*y)

    switch_window_button = Button(
      self,
      text="Login Token erstellen",
      command= self.get_login_data,
      font = used_font
    )
    switch_window_button.pack(side="bottom", fill=X)


    self.bind('<Configure>', font_change)
    APP_KEY.bind('<FocusIn>', handle_focus_in)
    APP_SECRET.bind('<FocusIn>', handle_focus_in_secret)
  
  def save_button_access(self, entry):
    string = entry.get()
    string = re.sub(r"\s", '', string)
    loginData.write_to_env('ACCESS_CODE_GENERATED', string)

  def save_button_app(self, entry):
    string = entry.get()
    string = re.sub(r"\s", '', string)
    loginData.write_to_env('APP_KEY', string)
  
  def save_button_secret(self, entry):
    string = entry.get()
    string = re.sub(r"\s", '', string)
    loginData.write_to_env('APP_SECRET', string)

  def get_login_data(self):
    loginData.get_login_data()
    messagebox.showinfo('Information', 'Login Token wurde erfolgreich erstellt')

class ShowDataFrame(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent)

    df = ticket_shop.DataFrameOperations().dataframe
    cols = list(df.columns)

    tree = Treeview(self, selectmode='browse')
    
    horzscrlbar = Scrollbar(self, orient='horizontal', command = tree.xview)
    horzscrlbar.pack(side = 'bottom', fill = 'x')

    vertscrlbar = Scrollbar(self, orient='vertical', command = tree.yview)
    vertscrlbar.pack(side = 'right', fill = 'y')
    tree["columns"] = cols
    
    tree.configure(yscrollcommand=vertscrlbar.set)
    tree.configure(xscrollcommand=horzscrlbar.set)
    tree.column("#0", width=50)
    for i in cols:
        tree.column(i, width = 100,anchor="w")
        tree.heading(i, text=i, anchor='w')
    
    for index, row in df.iterrows():
        tree.insert("",0,text=index,values=list(row))
    tree.pack(side = 'top', expand = 1, fill = 'both')

