import tkinter as tk

#CORES podem ser no formato #self['bg']='#FFFF00'

FONTE = ('Helvetica','12','bold')
FONTE = ('Helvetica','12')

class Label(tk.Label):
    def __init__(self, master, text='Label não definido', bg=None, fg=None, font=None, height=None, width=None):
        #inicializa pai com mesmos argumentos
        super().__init__(master=master, text=text, fg=fg, bg=bg, font=font, height=height, width=width) 
        self['fg']='darkgreen' if fg==None else fg 
        self['bg']='white' if bg==None else bg
        self['font']=FONTE if font==None else font
        self['borderwidth']=0
        self['padx']=30
        self['pady']=30
        #self['image']='/ifc_logo.png'

class Entry(tk.Entry):
    def __init__(self, master, show=None, bg=None, fg=None, font=None, height=None, width=None):
        #inicializa pai com mesmos argumentos
        super().__init__(master=master, show=show, fg=fg, bg=bg, font=font, height=height, width=width) 
        self['fg']='darkgreen' if fg==None else fg
        self['font']=FONTE if font==None else font
        #self['borderwidth']=10
        #self['image']='/ifc_logo.png'
        self['selectborderwidth']=1
        self['selectbackground']='yellow'
        self['selectforeground']='green'

class Button(tk.Button):
    def __init__(self, master, text='Texto não definido', bg=None, fg=None, font=None, height=None, width=None, command=None):
        #inicializa pai com mesmos argumentos
        super().__init__(master=master, text=text, fg=fg, bg=bg, font=font, height=height, width=width, command=command) 
        self['fg']='white' if fg==None else fg
        self['bg']='green' if bg==None else bg
        self['font']=FONTE if font==None else font
        #self['borderwidth']=5
        #self['width']=10 if width==None else width
        #self['height']=2 if height==None else height
        #self['padx']=10
        #self['pady']=10
        self['activebackground']='yellow'
        self['activeforeground']='green'