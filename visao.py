import cv2 as cv
from time import time
import numpy as np

class VideoCamera(object): 

    def __init__(self, tipo_fonte=None, config=''):
        self.tipo_fonte = tipo_fonte
        self.config = config
        self.video = None
        print('>> tipo_fonte: ', self.tipo_fonte)

        if self.tipo_fonte == 'camera':
          try: 
            cam_id=int(self.config)
            self.video = cv.VideoCapture(cam_id)
            print('>> VideoCamera USB (',cam_id,') acionada!')
          except ValueError:
            print('!! ERRO CAMERA USB')
        elif self.tipo_fonte == 'video':
          try:
            print('>> Acessando arquivo: ', self.config)
            self.video = cv.VideoCapture(self.config)
          except ValueError:
            print('!! ERRO ABRINDO ARQUIVO!')

    def __del__(self):
      try:
        self.video.release()
      except:
        print('VideoCamera.video não existe em DAO_Cameras')

    def release(self):
      try:
        self.video.release()
        print('Release acionado!')
      except:
        print('Release acionado! VideoCamera.video não existe em DAO_Cameras')

    def get_frame(self): 
      try:
        success, frame = self.video.read()
        if success:
          return True, frame
        else:
          return False, frame;    
      except:
        return False, None
      

AREAS = [  [5,    3,  85,105],
           [107,  3, 187,105],
           [209,  3, 289,105],
           [5,  130,  85,235],
           [107,130, 187,235],
           [209,130, 289,235]]

class Engine:
    
    def __init__(self):
        self.frame = None
        self.counters = []
        self.last_pixels = [] # em duas dimensoes acumula os pixels das ultimas X linhas 
        self.tamanho_media_movel = 3
        self.flag_contagem = []
        self.fgbg = cv.createBackgroundSubtractorMOG2()


    def run_frame(self, frame=None):
        #se não passar parametro fram então tenta ler o atual de DAO_Cameras
        self.frame = frame
        #self.frame_ant = frame # por enquanto não esta usando frame anterior...
        
        #Rotaciona imagem
        rows,cols,channels = frame.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        frame = cv2.warpAffine(frame,M,(cols,rows))
        
        frame=verificaVagas(i, img_clean) #vai em formato RGB

        backtorgb = cv.cvtColor(fgmask,cv.COLOR_GRAY2RGB)
        return backtorgb
    
    def config(self, frame=None):
      self.frame = frame
      for (a,b,c,d) in AREAS:
        frame=cv2.rectangle(frame.copy(),(a,b),(c,d),(0,255,0),2)
      return frame

    def save(self, image_path, frame):
      print(image_path, frame.shape)
      cv.imwrite(image_path, frame)

def retira_bordas(frame, tamanho_borda):
    #tamanho da borda em percentual da imagem
    lin = int(frame.shape[0]*(tamanho_borda/100.0))
    col = int(frame.shape[1]*(tamanho_borda/100.0))
    return frame[lin:frame.shape[0]-lin, col:frame.shape[1]-col]

def escreve(frame, texto):
    cv.putText(frame, texto, (1, 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 3, cv.LINE_AA)
    cv.putText(frame, texto, (1, 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv.LINE_AA)

def filtro_1(frame):
    frame = cv.blur(frame, (3, 3))
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #frame =  cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)   
    frame = cv.equalizeHist(frame)
    frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    return frame

def filtro_2(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.blur(frame, (3, 3))
    frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    return frame

if __name__ == '__main__':
    print("Iniciando, por favor aguarde...")
    
    vc = VideoCamera(tipo_fonte='video', arquivo='video1.mp4')
    engine = Engine()

    # Seta ROI (Region of Interest)
    #success, frame = vc.get_frame()
    #if not success:
    #    print('!! Erro acessando fonte de dados')
    #roi = cv.selectROI(frame)
    #print('>> ROI:', roi)
    roi = (851, 402, 750, 470)

    while(1):
        success, frame = vc.get_frame()
        if not success:
            break
        #frame = retira_bordas(frame, 15) # retira 10% das bordas da imagem

        # Recorta (crop) regiao selecionada
        frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        
        # Aplic filtros para melhorar a imagem
        
        frame_eq = filtro_1(frame)
        frame_1 = engine.run_frame(frame)
        frame_2 = engine.run_frame(filtro_2(frame))
        escreve(frame_eq, 'Equalizado')
        escreve(frame_1, 'Filtro 1')
        escreve(frame_2, 'Filtro 2')
        escreve(frame, 'Original')

        saida = np.vstack([np.hstack([frame, frame_eq]),np.hstack([frame_1, frame_2])])
        cv.imshow("Millikan Carga do Eletron # Autores: Madge Bianchi dos Santos, Ricardo Antonello e Thiago Tavares", saida)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    print('>> Resultados:')
    print('Velocidade média:', 33)
        
    print('>> Fim!')
