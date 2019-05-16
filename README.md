# Estacionamento Inteligente: Utiliza visão computacional para verificar o status da vagas de estacionamento.
  
Autores: Ricardo Antonello, Arildo Valmorbida Junior, Julia Valmorbida e Juliana Valmorbida.  
Contato: ricardo@antonello.com.br  
Agradecimentos: Edital 09/2017 IFC/Luzerna. Instituto Federal Catarinense Campus Luzerna.  

## Instruções para instalação Ubuntu 16 (ou superior)  
sudo apt install git  
git clone https://github.com/ricardoantonello/estacionamento-inteligente.git  
cd estacionamento-inteligente  
sudo apt install python3-venv  
sudo apt install python3-tk  
python3 -m venv venv   
source venv/bin/activate  
venv/bin/pip3 install opencv-python opencv-contrib-python 

## Instruções para utilização  
cd ~/estacionamento-inteligente
source venv/bin/activate  
python main.py    

## Screenshot  
![alt text](https://github.com/ricardoantonello/eletron/blob/master/Screenshot%20from%202019-05-13%2014-27-25.png)  




