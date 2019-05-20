# coding: utf-8
# Autor: Ricardo Antonello 
# Site: cv.antonello.com.br
# E-mail: ricardo@antonello.com.br

# import the necessary packages
import time
import cv2

areas = [  [5,    3,  85,105],
           [107,  3, 187,105],
           [209,  3, 289,105],
           [5,  130,  85,235],
           [107,130, 187,235],
           [209,130, 289,235]]

def texto(img, texto, coord, fonte = cv2.FONT_HERSHEY_SIMPLEX, cor=(0,0,255), tamanho=0.5, thickness=2):
    textSize, baseline = cv2.getTextSize(texto, fonte, tamanho, thickness);
    cor_background = 0
    if type(cor)==int: # se não for colorida a imagem
        cor_background=255-cor
    else:
        cor_background=(0,255,255)
    #print(cor_background)
    cv2.rectangle(img, (coord[0], coord[1]-textSize[1]-3), (coord[0]+textSize[0], coord[1]+textSize[1]-baseline), cor_background, -1)
    #cv2.putText(img, texto, coord, fonte, tamanho, cor_background, thickness+1, cv2.LINE_AA)
    cv2.putText(img, texto, coord, fonte, tamanho, cor, thickness, cv2.LINE_AA)
    return img

def subtraiArea(i1, i2, x1,y1,x2,y2):
    iA = cv2.cvtColor(i1, cv2.COLOR_RGB2GRAY) # Converte para imagem em tons de cinza
    iB = cv2.cvtColor(i2, cv2.COLOR_RGB2GRAY) 
    result = iA[y1:y2,x1:x2] - iB[y1:y2,x1:x2] # realiza a subtração na área informada
    soma_pixels_das_colunas = [sum(x) for x in zip(*result)] # soma os valores dos pixels das colunas
    return True if sum(soma_pixels_das_colunas)>800000 else False

def verificaVagas(img,img_clean):
  for (a,b,c,d) in areas:
    ocupada = subtraiArea(img,img_clean,a,b,c,d)
    temp = 'Ocupada' if ocupada else 'Livre'
    texto(img, temp, (a,b+15))
  return img

  
#####################################
## INICIO MAIN
#####################################
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
print('Bem vindo(a) ao Estacionamento Inteligente!')
print('\n\n\nSelecione a fonte da imagem:')
print('\n1. Câmera Pi')
print('2. Webcam')
op = int(input('\nOpção: '))
input('\n\n\nLimpe a área de leitura para calibrar e selecione 1 para iniciar...')

if op==1:
   ### PERGUNTA SE QUER VER AREAS DEMARCADAS
   print('\n\nSelecione:')
   print('\n1. Configurações')
   print('2. Operação')
   op = int(input('\nOpção: '))
   
   try:
     from picamera.array import PiRGBArray
     from picamera import PiCamera
     # initialize the camera and grab a reference to the raw camera capture
     camera = PiCamera()
     camera.resolution = (320, 240) #camera.resolution = (640, 480)
     camera.framerate = 32
     rawCapture = PiRGBArray(camera, size=(320, 240)) #rawCapture = PiRGBArray(camera, size=(640, 480))
      
     # allow the camera to warmup
     time.sleep(0.1)
      
     # capture frames from the camera
     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
       # grab the raw NumPy array representing the image, then initialize the timestamp
       # and occupied/unoccupied text
       image = frame.array
       i = image.copy()
       
       if op==1:
         #Mostra configuracoes de areas
         for (a,b,c,d) in areas:
           i=cv2.rectangle(i.copy(),(a,b),(c,d),(0,255,0),2)
       else:
         #verifica vagas
         i=verificaVagas(i, img_clean) #vai em formato RGB
              
       # show the frame
       cv2.imshow("Frame", i)
       key = cv2.waitKey(1) & 0xFF
       # clear the stream in preparation for the next frame
       rawCapture.truncate(0)
       # if the `q` key was pressed, break from the loop
       if key == ord("q"):
         break
   except ImportError:
     print('Não esta rodando em um Raspberry')

elif op==2: # USANDO A WEBCAM
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

  ### PERGUNTA SE QUER VER AREAS DEMARCADAS
  print('\n\nSelecione:')
  print('\n1. Configurações')
  print('2. Operação')
  op = int(input('\nOpção: '))

  while is_capturing:
     try:    # Lookout for a keyboardInterrupt to stop the script
         is_capturing, i = vc.read()   
         #Rotaciona imagem
         rows,cols,channels = i.shape
         M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
         i = cv2.warpAffine(i,M,(cols,rows))
         
         if op==1:
           #Mostra configuracoes de areas
           for (a,b,c,d) in areas:
             i=cv2.rectangle(i.copy(),(a,b),(c,d),(0,255,0),2)
         else:
           #verifica vagas
           i=verificaVagas(i, img_clean) #vai em formato RGB
                 
         window_name = "Estacionamento"
         cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
         cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

         #cv2.imshow(window_name, i[:,:,::-1]) #converte para BGR para mostrar
         cv2.imshow(window_name, i) #converte para BGR para mostrar
         key = cv2.waitKey(1) & 0xFF
         # if the `q` key was pressed, break from the loop
         if key == ord("q"):
             break
     except KeyboardInterrupt:
         vc.release()
         cv2.destroyAllWindows()
else:
  print('Opção inválida!')


        
