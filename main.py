import tkinter as tk
from tkinter import filedialog, messagebox
import rrTkinterLib as rr # biblioteca personalizada de interface
from PIL import Image, ImageTk
import cv2 as cv
import visao
import time
import numpy as np
import os

class AboutWindow(tk.Frame): # aqui teremos os widgets da tela
    def __init__(self, master=None): 
        super().__init__(master)
        self.master = master
        self.pack() # tipo do layout
        self.master.title('Sobre o projeto...')

        temp = 'INSTITUTO FEDERAL CATARINENSE - IFC\nCampus Luzerna\n\n\n\
Estacionamento Inteligente: Utiliza visão computacional para verificar o status \
da vagas de estacionamento. \n\n\n \
Autores: Ricardo Antonello, Arildo Valmorbida Junior, Julia Valmorbida e Juliana Valmorbida.  \
\nContato: ricardo@antonello.com.br   \n\n \
Agradecimentos: Edital 09/2017 IFC/Luzerna. Instituto Federal Catarinense Campus Luzerna.'
        self.textoPrincipal = tk.Label(self, text=temp)
        #self.textoPrincipal.pack(side="top")
        self.textoPrincipal.pack(pady=50, padx=50)
        self.quit = rr.Button(self, text="Sair", command=self.master.destroy)
        self.quit.focus_force()
        self.quit.pack(side="bottom", pady=30, padx=30) # left, right, bottom, top
        self.grab_set()
    
    def __del__(self): 
        print('Janela Help destruída...')
        self.grab_release()
     
        
class MainWindow(tk.Frame): # aqui teremos os widgets da tela
    def __init__(self, toplevel): 
        super().__init__(toplevel)
        self.master = toplevel
        self.grid() # tipo do layout
        #self.master.maxsize(width=1920, height=1080)
        #self.master.minsize(width=640, height=480)
        self.master['bg']='white'
        #master.resizable(width=False, height=False)
        self.master.title('Estacionamento Inteligente')
        self.create_widgets() 

    def create_widgets(self): 
        # CRIACAO DO MENU
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Abrir vídeo", command=lambda:self.openVideo('arquivo'))
        fileMenu.add_command(label="Usar câmera", command=lambda:self.openVideo('camera'))
        fileMenu.add_separator()
        fileMenu.add_command(label="Sair", command=root.quit)
        menubar.add_cascade(label="Arquivo", menu=fileMenu)
        helpMenu = tk.Menu(menubar, tearoff=0)
        helpMenu.add_command(label="Ajuda", command=self.openAbout)
        helpMenu.add_command(label="Sobre...", command=self.openAbout)
        menubar.add_cascade(label="Ajuda", menu=helpMenu)
        # FIM DA CRIACAO DO MENU

        logo = Image.open('ifc_logo.png')
        logo_width, logo_height = logo.size
        logo = logo.resize((logo_width//2, logo_height//2), Image.ANTIALIAS) #The (250, 250) is (height, width)
        logo = ImageTk.PhotoImage(logo)
        self.lb_img = tk.Label(self.master, image=logo)
        self.lb_img['borderwidth'] = 0
        self.lb_img.photo = logo
        self.lb_img.grid(column=1, row=1, sticky='n', rowspan=1, columnspan=1, padx=1, pady=1)
        
        self.lb1 = rr.Label(self.master)
        self.lb1["text"] = "Estacionamento\nInteligente"
        self.lb1['bg']='white'
        self.lb1.grid(column=1, row=2, sticky='N', padx=1, pady=1)

        self.abrirVideo = rr.Button(self.master)
        self.abrirVideo["text"] = "Abrir Vídeo"
        self.abrirVideo["command"] = lambda:self.openVideo('arquivo')
        self.abrirVideo.grid(column=1, row=3, sticky='N', padx=1, pady=1)

        self.abrirCamera = rr.Button(self.master)
        self.abrirCamera["text"] = "Usar Câmera"
        self.abrirCamera["command"] = lambda:self.openVideo('camera')
        self.abrirCamera.grid(column=1, row=4, sticky='N', padx=1, pady=1)

        self.about = rr.Button(self.master)
        self.about["text"] = "Autores"
        self.about["command"] = self.openAbout 
        self.about.grid(column=1, row=5, sticky='N', padx=1, pady=1)

        self.quit = rr.Button(self.master, text="Sair", command=self.master.destroy)
        self.quit.grid(column=1, row=6, sticky='S', padx=1, pady=1)
        self.quit.focus_force()

        self.desliga = rr.Button(self.master, text="Desligar", command=self.turnoff)
        self.desliga.grid(column=1, row=7, sticky='S', padx=1, pady=1)
        
        self.framesCount = rr.Label(self.master, text='')
        self.framesCount.grid(column=1, row=8)

        self.lbautores = rr.Label(self.master)
        self.lbautores["text"] = "Autores: Ricardo Antonello, Arildo Valmorbida Junior, Julia Valmorbida e Juliana Valmorbida."
        self.lbautores.grid(column=2, row=8, sticky='e', padx=2, pady=2, columnspan=2)

    def turnoff(self):
        print('Desligando o sistema...')
        os.system('systemctl poweroff')

    def openAbout(self):
        #aboutWindow = AboutWindow(master=tk.Tk()) 
        #aboutWindow.mainloop() 
        self.aboutWindow = tk.Toplevel(self.master) 
        self.app = AboutWindow(self.aboutWindow) 

    def calibragem():
        # Se não tem picamera então captura da webcam
        vc = cv2.VideoCapture(0)
        vc.set(cv2.CAP_PROP_FRAME_WIDTH,320)  
        vc.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        if vc.isOpened(): # try to get the first frame
            is_capturing, frame = vc.read()
        else:
            is_capturing = False  

        # calibragem
        img_clean = 0
        cont = 0
        while is_capturing:
            try: # Lookout for a keyboardInterrupt to stop the script
                is_capturing, frame = vc.read()   
                print('Calibrando... Aguarde!')
                time.sleep(0.2)
                if cont > 0:
                    #img_clean = cv2.accumulate(frame, img_clean)
                    img_clean = frame.copy()
                else:
                    img_clean = frame.copy()
                    cont+=1
                if cont>2:
                    break
                
            except KeyboardInterrupt:
                vc.release()
            except:
                print('Erro!')
                vc.release()

    def update(self):
        try:
            success, frame = self.vc.get_frame()
            if success:
                # Aplic filtros para melhorar a imagem
                frame_eq = visao.filtro_1(frame)
                frame_1 = self.engine.run_frame(frame)
                frame_2 = self.engine.config(frame)
                visao.escreve(frame_eq, 'Equalizado')
                visao.escreve(frame_1, 'Filtro 1')
                visao.escreve(frame_2, 'Filtro 2')
                visao.escreve(frame, 'Original')
                saida = np.vstack([np.hstack([frame, frame_eq]),np.hstack([frame_1, frame_2])])
                #Converte de OpenCV para formato Tkinter no canvas
                frame = cv.cvtColor(saida, cv.COLOR_BGR2RGB)
                frame = ImageTk.PhotoImage(image = Image.fromarray(frame))    
                self.canvas.photo = frame  # IMPORTANTE: Importante salvar na instancia do canvas em .photo ou qualquer outra propriedade (tipo .xxx) para permitir a exibição
                self.canvas.itemconfig(self.image_on_canvas, image=frame)
                self.frameCounter += 1
                if self.frameCount==0:
                    self.framesCount['text'] = 'Contador de frames: %d' % self.frameCounter
                else:
                    self.framesCount['text'] = 'Contador de frames: %d/%d' % (self.frameCounter, self.frameCount)
                if self.isUpdating == True:
                    self.master.after(self.delay, self.update)
        except:
            print('Fonte de dados ausente!')
        
        
    def openVideo(self, source):
        self.frameCounter = 0
        if source == 'arquivo':
            ftypes = [('Vídeos mp4', '*.mp4'), ('All files', '*')]
            path = tk.filedialog.askopenfilename(filetypes=ftypes)
            if path == '':
                return
            print('Arquivo escolhido:', path)
            print("Iniciando, por favor aguarde...")
            try:
                self.vc.release()
                self.isUpdating = False
                time.sleep(1)
                del self.vc
            except:
                print('Fonte de dados existente foi eliminada!')
            self.vc = visao.VideoCamera('video', path)
            #exibe FPS do vídeo
            fps = self.vc.video.get(cv.CAP_PROP_FPS)
            self.delay = int(1000//fps) #velocidade de atualização da tela, ou seja, captura de um novo frame
            print("FPS do vídeo em video.get(cv.CAP_PROP_FPS): {0}".format(fps))
            print("self.delay:", self.delay)
            self.frameCount = int(self.vc.video.get(cv.CAP_PROP_FRAME_COUNT))
            print("self.frameCount do vídeo:", self.frameCount)
        elif source == 'camera':
            try:
                self.vc.release()
                self.isUpdating = False
                time.sleep(1)
                del self.vc
            except:
                print('Fonte de dados existente foi eliminada!')
            self.vc = visao.VideoCamera('camera', 0)
            self.delay = 15 # para camera um delay de 15 deve ser suficiente
            self.frameCount=0
        self.engine = visao.Engine()
        success, frame = self.vc.get_frame()
        if success:
            img_width, img_height = frame.shape[1], frame.shape[0] 
            print('Shape:', img_width, img_height)
            try:
                self.canvas.delete("all")
                self.canvas.update()
                del self.canvas
            except:
                print('Canvas antigo eliminado!')
            self.canvas = tk.Canvas(self.master, width=img_width*2, height=img_height*2, bg='white')
            self.canvas['borderwidth']=0
            self.canvas.grid(column=3, row=1, rowspan=6, padx=1, pady=1)
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW)
            # chama método update() para atualizar frames na tela 
            self.isUpdating = True
            self.update()
        else:
            messagebox.showinfo("Erro acessando fonte de dados!", "Erro acessando fonte de dados: Caso seja um arquivo de vídeo confira se o arquivo não esta corrompido. Caso seja uma câmera, confira se ela esta ligada corretamente ao computador.")            
            print('!! Erro acessando fonte de dados')
        

root = tk.Tk() # biblioteca TK permite que os widgets sejam usados
app = MainWindow(root) # app será a tela principal da aplicação 
app.mainloop() # chama loop principal que fica lendo os eventos (como click de um botao)
