import openai
openai.api_key = "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"
import os
import azure.cognitiveservices.speech as speechsdk
import random
import nltk
import subprocess
import psutil
from datetime import date
from datetime import time
import datetime
import pygame
import requests
import time
import locale
import speech_recognition as sr
from speech_recognition import Microphone
import speech_recognition as sr
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyglet
from ytmusicapi import YTMusic
ytmusic = YTMusic("oauth.json")
import webbrowser as wb
import pyautogui
import threading
import sounddevice as sd
import numpy as np





pygame.mixer.init() #inicia o mixer para tocar musicas
rec = sr.Recognizer()
playlistId = "PLnLvW2VxOj45gHh3Glk50j8Jbep6GjFym"

#logo a baixo ficam as credenciais da ibm do recurso de fala da Bia
# Insira suas credenciais de API aqui
authenticator = IAMAuthenticator('j135NguO5L1O9zE8_S72qotGXI-prxqtxKCFNEmAq7WH')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
#infelizmente a api da ibm atingiu seu limite vou tentar agora com a api da elven labs
#acho que vou ter que pagar mesmo
# Insira a URL do serviço aqui
#text_to_speech.set_service_url('https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/4777386e-dbc6-4d66-a3ea-fc77d73ffc69')

#aqui esta a conecção da elvenlabs
CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

headers = {
  "Accept": "audio/mp3",
  "Content-Type": "application/json",
  "xi-api-key": "8bc5e0b6e6e14ebd7a965f763c7acc42"
}


      #print(textoo)

# Criar um objeto SpeechConfig com a chave e a região do serviço de fala
#speech_key, service_region = "fd8e2e6bcecf403e81922508b2fd8d66", "brazilsouth"
#speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Criar um objeto SpeechConfig com a chave e a região do serviço de fala

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# pt-BR-BrendaNeural
# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='pt-BR-FranciscaNeural' 
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


#essa variavel a baixo é uma variavel global que recebe o valor digitado pelo usuario e é tratada na função generate_texto
#por hora toda a parte de conecimento e dialogo com o usuario é feita por meio da api chatgpt, somente a voz é vinda da microsoft

# Define a chave da API
api_key = "98ac791f57e28461be048ff83d738ab7"
# Define a URL base da API
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# Define o nome da cidade
city_name = "Fortaleza"
# Define o idioma
lang = "pt-BR"
# Constrói a URL completa com os parâmetros
complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&lang=" + lang
# Faz a requisição à API
response = requests.get(complete_url)
        # Verifica se a requisição foi bem sucedida
if response.status_code == 200:
            # Converte a resposta em um dicionário Python
            data = response.json()

             # Acessa os dados do clima atual
            main = data["main"]
            weather = data["weather"][0]

            # Extrai as informações desejadas
            temp = main["temp"] - 273.15 # Converte de Kelvin para Celsius
            pressure = main["pressure"]
            humidity = main["humidity"]
            description = weather["description"]
else:
            # Imprime uma mensagem de erro na tela
              print(f"Erro ao fazer a requisição: {response.status_code}")


#o bloco acima se comunica por meio de uma chave API com o site openweather pra obter o status do clima atual da cidade de fortaleza



#frases para saudações
sauds = ["Oi", "Oi chefe!", "Já é hora de trabalhar?", "Oi, pensei que não te veria mais!", "Vamos pesquisar algo?",
         "Vamos pesquisar algo hoje?", "Vamos trabalhar!", "Oi chefinho!", "Oi chefiho o que quer pesquisar hoje?"]

#frases para contuações de dialogos
conti = ["Estou aqui", "Sim!",
         "Oi chefe!", "Oi chefe, estou aqui!", "Prossiga!",
         "pode dizer chef!"]

#frases de confirmacoa de comandos
confcomand =["Cláro!", "Você que manda!", "É pra já", "Já estou fazendo isso", "Pronto, já providenciei", "Ok"]


#prompt = input(speech_synthesizer.speak_text_async(random.choice(sauds)).get())
#speech_synthesizer.speak_text_async(random.choice(sauds)).get()
chatgpt_model = "gpt-3.5-turbo" #@param ["gpt-3.5-turbo", "gpt-4"]

chatgpt_system = "You are my virtual assistant female, and friend, you have a slightly acidic sense of humor, you always call me chefe, your responses shouldn't take long and you don't use emojis in your messages and your name is Bia" #@param {type:"string"}
messages = []
def get_gpt4_response(prompt):
    global messages 
    messages.append({"role": "system", "content": chatgpt_system})
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=messages
    )
    #return response.choices[0].message.content
    messages.append(response['choices'][0]['message'])
    return response['choices'][0]['message']['content']


def dialog(texto): 
  #t_microfone = threading.Thread(target=texto)
  saudacoes = random.choice(conti)
  data = {
    "text": saudacoes,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
  response = requests.post(url, json=data, headers=headers)
  with open('saudacoes.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

  music = pyglet.media.load('saudacoes.mp3')
  music.play()
      
  try:

      variavel = True
      fechamento = ["ok", "Ok obrigado", "Ok valeu", "Tá certo" "valeu", "Valeu Bia", "Tchau Bia",
                     "Tá bom então", "Blz", "Beleza", "Obrigado", "Beleza então", "Então depois a gente conversa mais",
                     "Então tá", "obrigado"]

      # prompt = "você é uma assistente atenciosa e com um humor um pouco acido e que me chama de chef, seu nome é Bia"
      while variavel:
        try:    
          with sr.Microphone() as mic2:
            rec.adjust_for_ambient_noise(mic2)
            print("Pronta pra conversar chef!\n")
            audio = rec.listen(mic2)
            #time.sleep(40)
            texto = rec.recognize_google(audio, language="pt-BR")
            print(texto)
            
            if texto == "Ok obrigado" or texto == "Valeu": #verifica se o que eu falei pelo microfone foi as frases para encerrar o loop de conversa e volta para o loop principal
              desp = "Ok chéfe, se precisar de algo, estarei aqui!"
              with open('despConversas.mp3', 'wb') as audio_file:
                audio_file.write(
                  text_to_speech.synthesize(
                  desp,
                  rate_percentage=22100,
                  voice='pt-BR_IsabelaV3Voice',
                  accept='audio/mp3'
                    ).get_result().content
                  )
    
                music = pyglet.media.load('despConversas.mp3')
                music.play()
                #pyglet.app.run()
                time.sleep(3)

                variavel = False
            else:
              txt = get_gpt4_response(prompt=texto)
              data = {
                "text": txt,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                  "stability": 0.5,
                  "similarity_boost": 0.5
                  }
                }
              response = requests.post(url, json=data, headers=headers)
              with open('conversas.mp3', 'wb') as f:
                  for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
              #sd.default.device = None
              music = pyglet.media.load('conversas.mp3')
              music.play()
              #sd.wait(music)
              time.sleep(45)
              
        except:
          print("Não entendi")
  except:
    speech_synthesizer.speak_text_async("Desculpe chefe. mas parece que houve um problema!").get()
    print("nao")
     
def cria_pasta(texto):
  try:
     pas=input(speech_synthesizer.speak_text_async("Em qual pasta quer que eu salve seu arquivo?").get())
     Nomear = input(speech_synthesizer.speak_text_async("Como devo nomear seu arquivo?").get()) 
     if not os.path.exists(pas):
      speech_synthesizer.speak_text_async(random.choice(confcomand)).get()
      os.makedirs(pas)
     c=os.path.join(pas, Nomear) 
     open(c, "x")
     speech_synthesizer.speak_text_async("Pronto. salvei seu arquivo! Deseja mais alguma coisa?")
  except:
    speech_synthesizer.speak_text_async("Desculpe chefe mas acho que deu algo errado!").get()
    
    
def abrir(texto):
    try:
      disco = "D:\\Users\\natan\\OneDrive\\Documentos\\ProjetoBia"
      speech_synthesizer.speak_text_async("Qual o nome da pasta e do arquivo que devo abrir?").get()
      p = input("...\n")
      a = input("...\n")
      cam = os.path.join(disco,p,a)
      speech_synthesizer.speak_text_async("Pronto chefe!")
      pross =  subprocess.Popen(["start", cam], shell=True)
      pross.wait(timeout=2000)
      input()
      if input == "Ok":
        pross.kill()
       
    except:
        speech_synthesizer.speak_text_async("chefe, algo deu errado")
        
        
        
        
        
#essa função da CPU ainda precisa de revisão
def cpu(texto):
  try:
    speech_synthesizer.speak_text_async(random.choice(confcomand)).get()
    CPU = psutil.cpu_percent(interval=1, percpu=True)
    percent = CPU.percent
    speech_synthesizer.speak_text_async(f"A CPU está atualmente com {percent}% de uso.").get()
  except:
    speech_synthesizer.speak_text_async("Desculpe chef, estou tendo problemas pra executar esse comando, depois, se puder dar uma olhada no meu codigo fonte, eu ficaria agradecida!").get()
    
def bateria(texto): 
  try: 
    #speech_synthesizer.speak_text_async(random.choice(confcomand)).get() 
    BATERIA = psutil.sensors_battery()#porcentagem da bateria
    percent = BATERIA.percent
    power = BATERIA.power_plugged
    txBateria = f"Estamos com aproximadamente{percent}% de bateria!"
    
    saudacoes = random.choice(conti)
    data = {
     "text": txBateria,
     "model_id": "eleven_multilingual_v2",
     "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
        }
      }
  
    response = requests.post(url, json=data, headers=headers)
    with open('bateria.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

    music = pyglet.media.load('bateria.mp3')
    music.play()
    sd.wait()
    if percent >= 100 and power == True:
      speech_synthesizer.speak_text_async("Acho que já pode tirar o carregador da tomada!")
    else:
      if percent <= 20:
        speech_synthesizer.speak_text_async(f"Hummm, chef... talvez seja hora de me conectar na tomada!")
  except:
     speech_synthesizer.speak_text_async("Desculpe chef, estou tendo problemas pra executar esse comando. depois, se puder dar uma olhada no meu codigo fonte, eu ficaria agradecida!").get()
    #cabFORCE = psutil.sensors_battery()#se bateria esta na tomada
    
def memoria(texto):
  try:
    speech_synthesizer.speak_text_async(random.choice(confcomand)).get() 
    MEMORIA = psutil.swap_memory()#percentual de uso da memoria
    percent = MEMORIA.percent
    speech_synthesizer.speak_text_async(f"Estamos com aproximadamente{percent}% de espaço em uso no disco.").get()
  except:
     speech_synthesizer.speak_text_async("Desculpe chef, estou tendo problemas pra executar esse comando, depois, se puder dar uma olhada no meu codigo fonte, eu ficaria agradecida!").get()
     
def rede(texto):
  try:
    speech_synthesizer.speak_text_async(random.choice(confcomand)).get()    
    REDE = psutil.net_connections()
    r = REDE.stauts
    speech_synthesizer.speak_text_async(r).get()
  except:
     speech_synthesizer.speak_text_async("Desculpe chef, estou tendo problemas pra executar esse comando, depois, se puder dar uma olhada no meu codigo fonte, eu ficaria agradecida!").get()

def horas(texto):
  #speech_synthesizer.speak_text_async(random.choice(confcomand)).get()#fala a hora atual
  tatual = datetime.datetime.now().time().strftime("%H"+"horas e "+"%M"+"minutos")
  #speech_synthesizer.speak_text_async(f"São exatamente{tatual}, chef!").get()
  Txthora = f"São exatamente {tatual}"
  saudacoes = random.choice(conti)
  data = {
    "text": Txthora,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
  response = requests.post(url, json=data, headers=headers)
  with open('horas.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

  music = pyglet.media.load('horas.mp3')
  music.play()
  sd.wait()
def dsemana(texto):
    #speech_synthesizer.speak_text_async(random.choice(confcomand)).get()#fala o dia da semana como uma string ex: segunda-feira
    locale.setlocale(locale.LC_ALL, "pt-BR")
    d = date.today()
    nomeDia = d.strftime("%A")
    txDsemana = f"Hoje é {nomeDia}, chef!"
      # Salve o arquivo de áudio gerado
    saudacoes = random.choice(conti)
    data = {
    "text": txDsemana,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
    response = requests.post(url, json=data, headers=headers)
    with open('dia_semana.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

    music = pyglet.media.load('dia_semana.mp3')
    music.play()
    sd.wait()
    
def data(texto):
    speech_synthesizer.speak_text_async(random.choice(confcomand)).get() #fala a data em números
    dh = date.today()
    txData = f"Hoje é {dh}"
      # Salve o arquivo de áudio gerado
    saudacoes = random.choice(conti)
    data = {
    "text": txData,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
    response = requests.post(url, json=data, headers=headers)
    with open('data.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

    music = pyglet.media.load('data.mp3')
    music.play()
    sd.wait()
    
def musicas(texto):
  #depois lembrar de colocar musicas em uma lista
  #essa função esta com um problema de logica depois lembrar de concertar isso
  #speech_synthesizer.speak_text_async(random.choice(confcomand))
  
  #depois que eu pedir para tocar alguma coisa no loop principal, logo em seguida
  #ela executa a função musicas, e utilizando a biblioteca ytmusicapi
  #procura a musica que eu pedir pelo microfone,
  #se a musica não estiver na minha playlist la no youtubemusic ela vai adicionar
  #caso contrario ela apenas toca a musica, enquanto isso o microfone fica ligado esperando a frase de 
  #efeito para parar todo o processo.
  
  pergunta = ["O que você quer escutar hoje?", "O que eu devo tocar chefe?",
              "vai de quê hoje?", "é só me dizer o nome da música!", "beleza, mas... Qual o nome da música chef?",
              "é pra já!"]
  
  
  data = {
    "text": random.choice(pergunta),
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
  response = requests.post(url, json=data, headers=headers)
  with open('P_musica.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

  music = pyglet.media.load('P_musica.mp3')
  music.play()
  sd.wait()
  try:
        with sr.Microphone() as mic:
            rec.adjust_for_ambient_noise(mic)
            print("Fale a musica\n")
            audio = rec.listen(mic)
            texto = rec.recognize_google(audio, language="pt-BR")
            print(texto)
            
            #playlistId = ytmusic.create_playlist("Minhas", "Musicas para a bia acessar") caso eu queria criar um comando para criar novas playlists

            search_results = ytmusic.search(texto.lower())
            ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

            playlist_URL = f"https://music.youtube.com/watch?v={search_results[0]['videoId']}&list={playlistId}"
            wb.open_new(playlist_URL)         
  except:
      print("Aguardando nome da musica...\n")
  
  #variavel  = True
  #while variavel:

     #try:
        #with sr.Microphone() as mic:
          #  rec.adjust_for_ambient_noise(mic)
          #  print("Devo parar a musica?\n")
           # audio = rec.listen(mic)
           # texto = rec.recognize_google(audio, language="pt-BR")
           # print(texto)
        #if texto == "para a musica" or texto == "para a música":
                #variavel = False
                #break
                #pyautogui.hotkey('ctrl', 'w')
                #pygame.mixer.music.stop()
          
    # except:
       # print("Aguardando...\n")

def parar_musica(texto):
  
  navegador = pyautogui.getWindowsWithTitle("Google Chrome")[0].activate()
  #navegador[0].close()
  pyautogui.hotkey('alt', 'f4')
  pyautogui.sleep(3)
  pyautogui.hotkey('Enter')
      
def alarme(texto):
  #antes o alarme estava confifgurado para tocar e aparecer em uma janela mas como ela sera
  #totalmente por voz então vou modificar para funcionar de acordo
  Program_Alarm = "Ok, é só me dizer as horas e os minutos, para que eu programe seu alarme!"
  # Salve o arquivo de áudio gerado
  
  data = {
    "text": Program_Alarm,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
  response = requests.post(url, json=data, headers=headers)
  with open('alarme.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

  music = pyglet.media.load('alarme.mp3')
  music.play()
  sd.wait()
  #horas
  with sr.Microphone() as mic2:
            rec.adjust_for_ambient_noise(mic2)
            print("Fale a hora chef!\n")
            audio = rec.listen(mic2, timeout=150)
            #time.sleep(40)
            hora = rec.recognize_google(audio, language="pt-BR")
            print("Adicionado", hora)
            
  time.sleep(3)
  
  #minutos         
  with sr.Microphone() as mic2:
            rec.adjust_for_ambient_noise(mic2)
            print("Fale os minutos chef!\n")
            audio = rec.listen(mic2, timeout=150)
            #time.sleep(40)
            minuto = rec.recognize_google(audio, language="pt-BR")
            print("Adicionado", minuto)

    # Define o horário do alarme
  alarm_hour = int(hora) # 10 horas
  alarm_minute = int(minuto) # 30 minutos
  
  print("Alarme criado com sucesso!")

  # Cria uma variável para controlar o loop principal
  running = True

  #  Cria uma variável para indicar se o alarme está ativo ou não
  alarm_on = False

  while running:
    # liga o microfone e verifica se eu disse alguma frase e se a frase dita foi a que esta programada para cancelar o alarme
    # caso seja ela desliga o alrame caso contrario o loop continua
    # futuramente estou pensando em colocar alguma musica para tocar mas primeiro preciso fazer mais testes
    #for event in pygame.event.get():
    
    # Obtém a hora atual do sistema
    now = datetime.datetime.now()

    # Formata a hora atual em uma string no formato HH:MM:SS
    current_time = now.strftime('%H:%M:%S')
      
    # Verifica se a hora atual é igual ao horário do alarme
    if now.hour == alarm_hour and now.minute == alarm_minute:
        # Ativa o alarme
          alarm_on = True
    
    # Se o alarme estiver ativo, toca o som e desenha um textoo na tela
    if alarm_on:
      repetir = 3
      for num in repetir:
        tx_Acorda = f"Oi chef, vamos acordar! o clima em {city_name}, é de {temp:.2f} °C, a umidade está em {humidity}%"
        saudacoes = random.choice(conti)
        data = {
        "text": tx_Acorda,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
          "stability": 0.5,
            "similarity_boost": 0.5
              }
            }
  
        response = requests.post(url, json=data, headers=headers)
        with open('Acorda.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        music = pyglet.media.load('Acorda.mp3')
        music.play()
        sd.wait()
      with sr.Microphone() as mic2:
            rec.adjust_for_ambient_noise(mic2)
            print("Desligar alarme?!\n")
            audio = rec.listen(mic2, timeout=150)
            #time.sleep(40)
            textoA = rec.recognize_google(audio, language="pt-BR")
            print(textoA)
      if textoA == "acordei" or textoA == "Acordei" or textoA == "desligar" or textoA == "Desligar":
        running = False

    # Espera um segundo antes de repetir o loop
    time.sleep(30)

def clima(texto):
  tempo = datetime.time().hour
  speech_synthesizer.speak_text_async(random.choice(confcomand)).get()
  txtTempo = f"O clima em {city_name}, é de {temp:.2f} °C, a humidade está em aproximadamente {humidity} %"
  # Salve o arquivo de áudio gerado
   
  data = {
    "text": txtTempo,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
    }
  
  response = requests.post(url, json=data, headers=headers)
  with open('saudacoes.mp3', 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)

  music = pyglet.media.load('saudacoes.mp3')
  music.play()
  sd.wait()
  
    

    
def lista_compras(texto):
  speech_synthesizer.speak_text_async("O que você deseja adicionar na lista?").get()
  listaDEcompras = []
  
  variavelV = True
  while variavelV:
          texto1 = input("Adicione:\n")
          listaDEcompras.append(texto1)
          
          if texto1.lower() == "pronto":
            variavelV = False
            speech_synthesizer.speak_text_async("Pronto chef! Criei sua lista de compras.")
            #print(listaDEcompras)
            with open("lista_de_compras.texto", "w") as arquivo:
                  for texto1 in listaDEcompras:
                    arquivo.write(texto1)
#criando classes para armazenar minhas informações pessoais, posteriormente posso pensar em implementar
#um banco de dado para armazenar tais infomações de forma mais segura

def ler_lista_compras(texto):
  arquivo = open("lista_de_compras.texto", "r")
  linhas = arquivo.readlines()
  speech_synthesizer.speak_text_async(f"Chef... Os produtos que estão na sua lista de compras são : {linhas}")
  arquivo.close()

  
  
  
class chef():
  Meunome="Natã"
  SobreNome="Fernandes"
  UltimoNome="Silva"
  Minhaidade="23"
  dataNascimento="14 do 11 de 1999"
  CPF = "087, 482, 663, 29"
  Nindentidade="2009011342 - 4"
  senhaNubank="2061"
  senhaC6="2061"
  senhaValeAlimentacao="9745"
  emailPrincipal="natecofernandes@gmail.com"
  senhaEmailPrincipal="natafernandes1"
  telefone="85 9 99616540"


# Definir uma lista de pares de textoo e classe para treinar o classificador
train_data = [
    ("Bia", "dialog"),
    ("ei", "dialog"),
    ("quer", "dialog"),
    ("conversar", "dialog"),
    ("conversa", "dialog"),
    ("Bia me tira uma duvida", "dialog"),
    ("Bia ta acordada", "dialog"),
    ("acorda", "dialog"),
    ("Biazinha acorda", "dialog"),
    ("to com uma duvida", "dialog"),
    ("vamos conversar", "dialog"),
    ("Bia vamos", "dialog"),
    ("Bia ta ai", "dialog"),
    ("vamos pesquisar", "dialog"),
    ("pesquise", "dialog"),
    ("pesquisa uma coisa pra mim", "dialog"),
    ("Bia pesquisa uma coisa pra mim", "dialog"),
    ("Bia da uma olhada em uma coisa pra mim", "dialog"),
    ("Bia olha uma coisa pra mim", "dialog"),
    ("Bia crie uma pasa pra mim", "cria_pasta"),
    ("Bia preciso de uma pasta", "cria_pasta"),
    ("Bia quero uma pasta", "cria_pasta"),
    ("por favor crie uma pasta pra mim", "cria_pasta"),
    ("preciso de uma pasta agora", "cria_pasta"),
    ("Bia pasta agora por favor", "cria_pasta"),
    ("Bia faz uma pasta pra mim por favor", "cria_pasta"),
    ("pasta", "cria_pasta"),
    ("quero uma pasta", "cria_pasta"),
    ("quero uma pasta agora", "cria_pasta"),
    ("quero uma pasta agora por favor", "cria_pasta"),
    ("pasta por favor", "cria_pasta"),
    ("Bia pasta", "cria_pasta"),
    ("Bia pasta agora", "cria_pasta"),
    ("Biazinha uma pasta por favor", "cria_pasta"),
    ("Biazinha uma pasta", "cria_pasta"),
    ("Biazinha pasta", "cria_pasta"),
    ("agora quero que voce crie uma pasta", "cria_pasta"),
    ("criar uma pasta", "cria_pasta"),
    ("agora preciso de uma pasta", "cria_pasta"),
    ("criar pasta", "cria_pasta"),
    ("crie uma pasta", "cria_pasta"),
    ("Bia agora quero que voce crie uma pasta", "cria_pasta"),
    ("preciso de um arquivo", "cria_pasta"),
    ("Bia preciso de um arquivo", "cria_pasta"),
    ("Bia cria um arquivo", "cria_pasta"),
    ("Bia cria um arquivo pra mim", "cria_pasta"),
    ("Bia arquivo", "cria_pasta"),
    ("Bia arquivo agora", "cria_pasta"),
    ("Bia abra um arquivo pra mim", "abrir"),
    ("Bia abra uma pasta pra mim", "abrir"),
    ("Bia abra uma pasta pra mim agora", "abrir"),
    ("Bia abrir pasta agora", "abrir"),
    ("Bia abrir pasta", "abrir"),
    ("Bia abrir arquivo", "abrir"),
    ("Bia abrir arquivo agora", "abrir"),
    ("abrir arquivo", "abrir"),
    ("abrir pasta", "abrir"),
    ("Bia abrir arquivo por favor", "abrir"),
    ("abrir", "abrir"),
    ("abra", "abrir"),
    ("abra uma pasta", "abrir"),
    ("criar arquivo", "cria_pasta"),
    ("como vai a cpu", "CPU"),
    ("cpu", "CPU"),
    ("informe sobre a cpu", "CPU"),
    ("informacoes da cpu", "CPU"),
    ("quero saber da cpu", "CPU"),
    ("informe cpu", "CPU"),
    ("cpu como esta", "CPU"),
    ("cpu como esta?", "CPU"),
    ("me fale como esta a cpu", "CPU"),
    ("quero informacoes da cpu", "CPU"),
    ("como esta o estado da cpu", "CPU"),
    ("mostre cpu", "CPU"),
    ("mostre a cpu", "CPU"),
    #BATERIA
    ("Bia olha o nivel da bateria", "BATERIA"),
    ("olha o nivel da bateria", "BATERIA"),
    ("nivel da bateria", "BATERIA"),
    ("Bia nivel da bateria", "BATERIA"),
    ("como vai a bateria?", "BATERIA"),
    ("como vai a bateria", "BATERIA"),
    ("estado da bateria", "BATERIA"),
    ("mostre a bateria", "BATERIA"),
    ("mostre o nivel da bateria", "BATERIA"),
    ("bateria", "BATERIA"),
    ("quero ver a bateria", "BATERIA"),
    ("quero ver o nivel da bateria", "BATERIA"),
    ("Bia", "BATERIA"),
    ("como estamos", "BATERIA"),
    ("de", "BATERIA"),
    ("Bia olhe o nivel de energia pra mim", "BATERIA"),
    ("Bia olhe o nivel da bateria pra mim", "BATERIA"),
     #memoria
    ("memoria", "MEMORIA"),
    ("estado da memoria", "MEMORIA"),
    ("memoria em dico", "MEMORIA"),
    ("como ta a porcentagem da memoria", "MEMORIA"),
    ("espaco em disco", "MEMORIA"),
    ("qual o espaco em disco", "MEMORIA"),
    ("mostre o espaco em disco", "MEMORIA"),
    ("mostre o espaco livre em disco", "MEMORIA"),
    #rede
    ("rede", "REDE"),
    ("status da rede", "REDE"),
    ("estamos conectados", "REDE"),
    #horas
    ("Bia que horas sao agora", "horas"),
    ("horas", "horas"),
    ("Bia que horas e", "horas"),
    ("Bia me diz que horas sao", "horas"),
    ("Bia horas por favor", "horas"),
    ("Bia horas", "horas"),
    ("que horas sao", "horas"),
    ("que horas sao agora", "horas"),
    ("Bia diz pra mim que horas sao", "horas"),
    ("horas", "horas"),
    #dia da semana
    ("Bia que dia e hoje", "dsemana"),
    ("que dia e hoje", "dsemana"),
    ("Bia diz pra mim que dia e hoje", "dsemana"),
    ("qual o dia de hoje Bia", "dsemana"),
    ("diz pra mim que dia e hoje"),
    ("que dia e hoje mesmo em", "dsemana"),
    ("que dia e hoje mesmo", "dsemana"),
    ("que dia e hoje mesmo em Bia", "dsemana"),
    ("que dia e hoje Bia", "dsemana"),
    #data
    ("que data e hoje Bia", "data"),
    ("Bia qual a data de hoje", "data"),
    ("Bia que data e hoje", "data"),
    ("Bia a gente ta em que dia", "data"),
    ("Bia que data a gente ta", "data"),
    ("que data e hoje", "data"),
    ("Bia a data de hoje por favor", "data"),
    ("Bia data", "data"),
    ("data", "data"),
    #chamada de classes para consulta de dados pessoais
    ("Bia qual número do meu cpf", "cpf"),
    ("Bia meu cpf", "cpf"),
    ("Bia diz o número do meu cpf", "cpf"),
    ("Bia diz o número do meu cpf por favor", "cpf"),
    ("Bia como e o número do meu cpf", "cpf"),
    ("Bia como e o número do meu cpf mesmo", "cpf"),
    ("qual o número do meu cpf em", "cpf"),
    ("Bia diz ai o número do meu cpf", "cpf"),
    ("meu cpf", "cpf"),
    ("cpf", "cpf"),
    ("Bia qual a minha idade", "idade"),
    ("Bia qual o número da minha identidade", "númeroIndentidade"),
    ("ei Bia me diz o número da minha indentidade", "númeroIndentidade"),
    ("beleza diz o número da minha identidade", "númeroIndentidade"),
    ("número da minha indentidade", "númeroIndentidade"),
    ("Bia qual o número do meu telefone", "telefone"),
    ("Bia me diz o número do meu telefone", "telefone"),
    ("qual o número do meu telefone Bia", "telefone"),
    ("qual o número do meu telefone", "telefone"),
    ("me diz o número do meu telefone", "telefone"),
    ("Bia me diz o número do meu telefone", "telefone"),
    ("Bia qual minha senha do nubank", "senhaNu"),
    ("Bia minha senha do nubank", "senhaNu"),
    ("ei Bia qual a minha senha do nubank", "senhaNU"),
    ("qual minha senha do nubank", "senhaNU"),
    ("ei Bia diz ai qual minha senha do nubank", "senhaNU"),
    ("senha do nubank", "senhaNU"),
    ("Bia qual minha senha do c6", "senhac6"),
    ("Bia minha senha do c6", "senhac6"),
    ("ei Bia qual a minha senha do c6", "senhac6"),
    ("Bia qual meu email", "email"),
    ("Bia qual a senha do meu email", "email"),
    ("ei Bia qual a senha do meu email", "email"),
    ("Bia qual a senha do meu vale", "senhaVale"),
    ("Bia a senha do meu vale", "senhaVale"),
    ("Bia qual a senha do meu vale alimentacao", "senhaVale"),
    ("Bia qual minha idade mesmo", "idade"),
    ("Bia tu sabe minha idade", "idade"),
    ("ei Bia diz minha idade", "idade"),
    #tocar musicas
    ("Bia toca uma musica pra gente", "musicas"),
    ("Bia baixa a agulha", "musicas"),
    ("vai Bia toca alguma coisa pra gente", "musicas"),
    ("Bia toca uma musica", "musicas"),
    ("Bia toca uma musica", "musicas"),
    ("musicas", "musicas"),
    ("Bia musica", "musicas"),
    ("Bia musica agora", "musicas"),
    ("ei Bia toca uma musica ai", "musicas"),
    ("Bia da o play", "musicas"),
    ("ei Bia da o play ai", "musicas"),
    ("Bia play", "musicas"),
    ("musica", "musicas"),
    ("Musica", "musicas"),
    ("Beleza toca uma música aí", "musicas"),
    ("solta o som aí bia", "musicas"),
    ("Solta o som bia", "musicas"),
    #para a musica
    ("para essa musica bia", "parar_musica"),
    ("ta bom bia", "parar_musica"),
    ("tá bom bia", "parar_musica"),
    ("sem som", "parar_musica"),
    ("chega de musica", "parar_musica"),
    ("bia chega de musica", "parar_musica"),
    ("chega de musica por hoje", "parar_musica"),
    ("chega de música por hojé", "parar_musica"),
    ("bia chega de música por hoje", "parar_musica"),
    ("parar musica", "parar_musica"),
    ("pare a musica", "parar_musica"),
    ("bia pare a musica", "parar_musica"),
    ("bisa pare a música", "parar_musica"),
    #alarme
    ("ei Bia defina um alarme pra mim", "alarme"),
    ("Bia alarme", "alarme"),
    ("alarme", "alarme"),
    ("Bia cria um alarme pra mim pode ser", "alarme"),
    ("Bia preciso de um alarme", "alarme"),
    ("ei Bia preciso de um alarme", "alarme"),
    ("ei Bia alarme", "alarme"),
    ("Bia defina um alarme pra mim"),
    ("Bia vou acordar cedo amaha preciso de um alarme"),
    ("ei Bia vou acordar cedo amaha preciso de um alarme"),
    ("vou acordar cedo amanha", "alarme"),
    ("vou acordar cedo amanha preciso de um alarme", "alarme"),
    ("Bia vou acordar cedo amanha, preciso de um alarme", "alarme"),
    ("Bia tu pode me acordar amanha", "alarme"),
    ("ei Bia tu pode me acordar amanha", "alarme"),
    ("Bia defina um alarme pra amanha pode ser", "alarme"),
    ("Bia voce pode me acordar amanha", "alarme"),
    ("Bia queria que voce me acordasse amanha pode ser", "alarme"),
    ("ei Bia eu queria que tu me acordasse amanha", "alarme"),
    ("ei Bia eu queria que tu me acordasse amanha pode ser", "alarme"),
    ("alarme", "alarme"),
    ("Bia alarme", "alarme"),
    #clima
    ("clima", "clima"),
    ("Clima", "clima"),
    ("Bia como ta o clima", "clima"),
    ("Bia o clima", "clima"),
    ("como ta o clima agora", "clima"),
    ("como ta o clima", "clima"),
    ("ei Bia como ta o clima", "clima"),
    ("ei Bia como ta o clima agora", "clima"),
    ("Bia como ta o tempo", "clima"),
    ("Bia fala sobre o tempo", "clima"),
    ("ei Bia como ta o tempo agora", "clima"),
    ("Bia e o tempo", "clima"),
    ("ei Bia como ta o tempo agora aqui", "clima"),
    ("Bia como ta o tempo la fora", "clima"),
    ("ei Bia como ta o tempo por aqui"),
    ("Bia como ta o tempo la fora em", "clima"),
    ("Bia como ta o tempo la fora hoje", "clima"),
    ("eita que hoje tá pegando fogo quantos graus tá fazendo", "clima"),
    ("Bia quantos graus tá fazendo lá fora", "clima"),
    ("quantos graus tá fazendo lá fora em", "clima"),
    ("quantos graus tá fazendo lá fora", "clima"),
    ("quantos graus tá fazendo lá fora Bia", "clima"),
    
    
    #lista de compras
    ("lista de compras", "lista_compras"),
    ("Bia preciso de uma lista de compras", "lista_compras"),
    ("lista de compras Bia", "lista_compras"),
    ("Bia vamos as compras", "lista_compras"),
    ("Bia crie uma lista de compras pra mim", "lista_compras"),
    ("preciso de uma lista de compras", "lista_compras"),
    #ler lista de compras
    ("Bia o que tem na lista de compras", "ler_lista_compras"),
    ("ei Bia o que tem na minha lista de compras", "ler_lista_compras"),
    ("Bia fala pra mim o que tem na minha lista de compras", "ler_lista_compras"),
    ("o que tem na lista de compras", "ler_lista_compras"),
    ("diz pra mim o que tem na lista de compras", "ler_lista_compras"),
    ("Bia fala pra mim o que tem na minha lista de compras", "ler_lista_compras"),
    ("Bia le pra mim a lista de compras por favor", "ler_lista_compras"),
    ("Bia o que tem na lista de compras em", "ler_lista_compras")
]

# Definir uma lista de pares de textoo e classe para testar o classificador
test_data = [
     ("Bia", "dialog"),
    ("Bia me tira uma duvida", "dialog"),
    ("Bia ta acordada", "dialog"),
    ("acorda", "dialog"),
    ("Biazinha acorda", "dialog"),
    ("to com uma duvida", "dialog"),
    ("vamos conversar", "dialog"),
    ("Bia vamos", "dialog"),
    ("Bia ta ai", "dialog"),
    ("vamos pesquisar", "dialog"),
    ("pesquise", "dialog"),
    ("pesquisa uma coisa pra mim", "dialog"),
    ("Bia pesquisa uma coisa pra mim", "dialog"),
    ("Bia da uma olhada em uma coisa pra mim", "dialog"),
    ("Bia olha uma coisa pra mim", "dialog"),
    ("Bia crie uma pasa pra mim", "cria_pasta"),
    ("Bia preciso de uma pasta", "cria_pasta"),
    ("Bia quero uma pasta", "cria_pasta"),
    ("por favor crie uma pasta pra mim", "cria_pasta"),
    ("preciso de uma pasta agora", "cria_pasta"),
    ("Bia pasta agora por favor", "cria_pasta"),
    ("Bia faz uma pasta pra mim por favor", "cria_pasta"),
    ("pasta", "cria_pasta"),
    ("quero uma pasta", "cria_pasta"),
    ("quero uma pasta agora", "cria_pasta"),
    ("quero uma pasta agora por favor", "cria_pasta"),
    ("pasta por favor", "cria_pasta"),
    ("Bia pasta", "cria_pasta"),
    ("Bia pasta agora", "cria_pasta"),
    ("Biazinha uma pasta por favor", "cria_pasta"),
    ("Biazinha uma pasta", "cria_pasta"),
    ("Biazinha pasta", "cria_pasta"),
    ("agora quero que voce crie uma pasta", "cria_pasta"),
    ("criar uma pasta", "cria_pasta"),
    ("agora preciso de uma pasta", "cria_pasta"),
    ("criar pasta", "cria_pasta"),
    ("crie uma pasta", "cria_pasta"),
    ("Bia agora quero que voce crie uma pasta", "cria_pasta"),
    ("preciso de um arquivo", "cria_pasta"),
    ("Bia preciso de um arquivo", "cria_pasta"),
    ("Bia cria um arquivo", "cria_pasta"),
    ("Bia cria um arquivo pra mim", "cria_pasta"),
    ("Bia arquivo", "cria_pasta"),
    ("Bia arquivo agora", "cria_pasta"),
    ("Bia abra um arquivo pra mim", "abrir"),
    ("Bia abra uma pasta pra mim", "abrir"),
    ("Bia abra uma pasta pra mim agora", "abrir"),
    ("Bia abrir pasta agora", "abrir"),
    ("Bia abrir pasta", "abrir"),
    ("Bia abrir arquivo", "abrir"),
    ("Bia abrir arquivo agora", "abrir"),
    ("abrir arquivo", "abrir"),
    ("abrir pasta", "abrir"),
    ("Bia abrir arquivo por favor", "abrir"),
    ("abrir", "abrir"),
    ("abra", "abrir"),
    ("abra uma pasta", "abrir"),
    ("criar arquivo", "cria_pasta"),
    ("como vai a cpu", "CPU"),
    ("cpu", "CPU"),
    ("informe sobre a cpu", "CPU"),
    ("informacoes da cpu", "CPU"),
    ("quero saber da cpu", "CPU"),
    ("informe cpu", "CPU"),
    ("cpu como esta", "CPU"),
    ("cpu como esta?", "CPU"),
    ("me fale como esta a cpu", "CPU"),
    ("quero informacoes da cpu", "CPU"),
    ("como esta o estado da cpu", "CPU"),
    ("mostre cpu", "CPU"),
    ("mostre a cpu", "CPU"),
    #BATERIA
    ("nivel da bateria", "BATERIA"),
    ("Bia ol nivel da bateria", "BATERIA"),
    ("como vai a bateria?", "BATERIA"),
    ("como vai a bateria", "BATERIA"),
    ("estado da bateria", "BATERIA"),
    ("mostre a bateria", "BATERIA"),
    ("mostre o nivel da bateria", "BATERIA"),
    ("bateria", "BATERIA"),
    ("quero ver a bateria", "BATERIA"),
    ("quero ver o nivel da bateria", "BATERIA"),
     #memoria
    ("memoria", "MEMORIA"),
    ("estado da memoria", "MEMORIA"),
    ("memoria em dico", "MEMORIA"),
    ("como ta a porcentagem da memoria", "MEMORIA"),
    ("espaco em disco", "MEMORIA"),
    ("qual o espaco em disco", "MEMORIA"),
    ("mostre o espaco em disco", "MEMORIA"),
    ("mostre o espaco livre em disco", "MEMORIA"),
    #rede
    ("rede", "REDE"),
    ("status da rede", "REDE"),
    ("estamos conectados", "REDE"),
     #horas
    ("Bia que horas sao agora", "horas"),
    ("horas", "horas"),
    ("Bia que horas e", "horas"),
    ("Bia me diz que horas sao", "horas"),
    ("Bia horas por favor", "horas"),
    ("Bia horas", "horas"),
    ("que horas sao", "horas"),
    ("que horas sao agora", "horas"),
    ("Bia diz pra mim que horas sao", "horas"),
    ("horas", "horas"),
    #dia da semana
    ("Bia que dia e hoje", "dsemana"),
    ("que dia e hoje", "dsemana"),
    ("Bia diz pra mim que dia e hoje", "dsemana"),
    ("qual o dia de hoje Bia", "dsemana"),
    ("diz pra mim que dia e hoje"),
    ("que dia e hoje mesmo em", "dsemana"),
    ("que dia e hoje mesmo", "dsemana"),
    ("que dia e hoje mesmo em Bia", "dsemana"),
    ("que dia e hoje Bia", "dsemana"),
    #data
    ("que data e hoje Bia", "data"),
    ("Bia qual a data de hoje", "data"),
    ("Bia que data e hoje", "data"),
    ("Bia a gente ta em que dia", "data"),
    ("Bia que data a gente ta", "data"),
    ("que data e hoje", "data"),
    ("Bia a data de hoje por favor", "data"),
    ("Bia data", "data"),
    ("data", "data"),
   #chamada de classes para consulta de dados pessoais
    ("Bia qual número do meu cpf", "cpf"),
    ("Bia meu cpf", "cpf"),
    ("Bia diz o número do meu cpf", "cpf"),
    ("Bia diz o número do meu cpf por favor", "cpf"),
    ("Bia como e o número do meu cpf", "cpf"),
    ("Bia como e o número do meu cpf mesmo", "cpf"),
    ("Bia qual a minha idade", "idade"),
    ("número da minha indentidade", "númeroIndentidade"),
    ("Bia qual o número da minha identidade", "númeroIndentidade"),
    ("ei Bia me diz o número da minha indentidade", "númeroIndentidade"),
    ("beleza diz o número da minha identidade", "númeroIndentidade"),
    ("Bia qual o número do meu telefone", "telefone"),
    ("Bia me diz o número do meu telefone", "telefone"),
    ("qual o número do meu telefone Bia", "telefone"),
    ("qual o número do meu telefone", "telefone"),
    ("me diz o número do meu telefone", "telefone"),
    ("Bia me diz o número do meu telefone", "telefone"),
    ("Bia qual minha senha do nubank", "senhaNu"),
    ("Bia minha senha do nubank", "senhaNu"),
    ("ei Bia qual a minha senha do nubank", "senhaNU"),
    ("Bia qual minha senha do c6", "senhac6"),
    ("Bia minha senha do c6", "senhac6"),
    ("ei Bia qual a minha senha do c6", "senhac6"),
    ("Bia qual meu email", "email"),
    ("Bia qual a senha do meu email", "senhaemail"),
    ("ei Bia qual a senha do meu email", "senhaemail"),
    ("Bia qual a senha do meu vale", "senhaVale"),
    ("Bia a senha do meu vale", "senhaVale"),
    ("Bia qual a senha do meu vale alimentacao", "senhaVale"),
    ("Bia qual minha idade mesmo", "idade"),
    ("Bia tu sabe minha idade", "idade"),
    ("ei Bia diz minha idade", "idade"),
    #tocar musicas
    ("Bia toca uma musica pra gente", "musicas"),
    ("Bia baixa a agulha", "musicas"),
    ("vai Bia toca alguma coisa pra gente", "musicas"),
    ("Bia toca uma musica", "musicas"),
    ("Bia toca uma musica", "musicas"),
    ("musicas", "musicas"),
    ("Bia musica", "musicas"),
    ("Bia musica agora", "musicas"),
    ("ei Bia toca uma musica ai", "musicas"),
    ("Bia da o play", "musicas"),
    ("ei Bia da o play ai", "musicas"),
    ("Bia play", "musicas"),
    ("toca alguma coisa ai", "musicas"),
    ("da o play ai vai", "musicas"),
    ("musica", "musicas"),
    ("baixa a agulha ai", "musicas"),
    ("baixa a agulha ai menina", "musicas"),
    #parar musicas
    ("para essa musica bia", "parar_musica"),
    ("ta bom bia", "parar_musica"),
    ("tá bom bia", "parar_musica"),
    ("sem som", "parar_musica"),
    ("chega de musica", "parar_musica"),
    ("bia chega de musica", "parar_musica"),
    ("chega de musica por hoje", "parar_musica"),
    ("chega de música por hojé", "parar_musica"),
    ("bia chega de música por hoje", "parar_musica"),
    ("parar musica", "parar_musica"),
    ("pare a musica", "parar_musica"),
    ("bia pare a musica", "parar_musica"),
    ("bisa pare a música", "parar_musica"),
    #alarme
    ("ei Bia defina um alarme pra mim", "alarme"),
    ("Bia alarme", "alarme"),
    ("alarme", "alarme"),
    ("Bia cria um alarme pra mim pode ser", "alarme"),
    ("Bia preciso de um alarme", "alarme"),
    ("ei Bia preciso de um alarme", "alarme"),
    ("ei Bia alarme", "alarme"),
    ("Bia defina um alarme pra mim"),
    ("Bia vou acordar cedo amaha preciso de um alarme"),
    ("vou acordar cedo amanha", "alarme"),
    ("vou acordar cedo amanha preciso de um alarme", "alarme"),
    ("ei Bia vou acordar cedo amanha, preciso de um alarme", "alarme"),
    ("Bia voce pode me acordar amanha", "alarme"),
    ("Bia queria que voce me acordasse amanha pode ser", "alarme"),
    ("ei Bia eu queria que tu me acordasse amanha", "alarme"),
    ("ei Bia eu queria que tu me acordasse amanha pode ser", "alarme"),
    ("alarme", "alarme"),
    ("Bia alarme", "alarme"),
    #clima
    ("clima", "clima"),
    ("Clima", "clima"),
    ("Bia como ta o clima", "clima"),
    ("Bia o clima", "clima"),
    ("como ta o clima agora", "clima"),
    ("como ta o clima", "clima"),
    ("ei Bia como ta o clima", "clima"),
    ("ei Bia como ta o clima agora", "clima"),
    ("Bia como ta o tempo", "clima"),
    ("Bia fala sobre o tempo", "clima"),
    ("ei Bia como ta o tempo agora", "clima"),
    ("Bia e o tempo", "clima"),
    ("ei Bia como ta o tempo agora aqui", "clima"),
    ("Bia como ta o tempo la fora", "clima"),
    ("ei Bia como ta o tempo por aqui"),
    ("Bia como ta o tempo la fora em", "clima"),
    ("Bia como ta o tempo la fora hoje", "clima"),
    ("eita que hoje tá pegando fogo quantos graus tá fazendo", "clima"),
    ("Bia quantos graus tá fazendo lá fora", "clima"),
    ("quantos graus tá fazendo lá fora em", "clima"),
    ("quantos graus tá fazendo lá fora", "clima"),
    ("quantos graus tá fazendo lá fora Bia", "clima"),
    
    
    #lista de compras
    ("lista de compras", "lista_compras"),
    ("Bia preciso de uma lista de compras", "lista_compras"),
    ("lista de compras Bia", "lista_compras"),
    ("Bia vamos as compras", "lista_compras"),
    ("Bia crie uma lista de compras pra mim", "lista_compras"),
    ("preciso de uma lista de compras", "lista_compras"),
    #ler lista de compras
    ("Bia o que tem na lista de compras", "ler_lista_compras"),
    ("ei Bia o que tem na minha lista de compras", "ler_lista_compras"),
    ("Bia fala pra mim o que tem na minha lista de compras", "ler_lista_compras"),
    ("o que tem na lista de compras", "ler_lista_compras"),
    ("diz pra mim o que tem na lista de compras", "ler_lista_compras"),
    ("Bia fala pra mim o que tem na minha lista de compras", "ler_lista_compras"),
    ("Bia le pra mim a lista de compras por favor", "ler_lista_compras"),
    ("Bia o que tem na lista de compras em", "ler_lista_compras")
]

# Definir uma função para extrair as características do textoo
def extract_features(texto):
  # Definir uma lista de palavras-chave para cada classe
  keywords = {
      "dialog": ["Bia", "oi Bia", "quero", "pesquisa", "pesquisar", "acorde", "acordada", "ta", "?",
                 "vamos", "agora", "acorde", "ola", "Ola", "oi", "Bia",
                 "Oi Bia", "faz", "fazer", "uma", "um"],
      
      
      "criar_pasta": ["pasta", "Pasta", "criar", "Criar", "crie", "para",
                      "pra", "mim", "para", "Para", "Pra", "Bia", "oi", "Bia",
                      "Oi", "agora", "faz", "fazer", "uma", "um", "arquivo", "cria",
                      "agora", "preciso"],
      
      
      "abrir": ["Bia", "pasta", "arquivo", "abrir", "agora", "por",
                "favor", "abra","um", "uma", "preciso"],
      
      
       "MEMORIA": ["quanto", "memoria", "por", "cento", "por cento", "qual",
                  "porcentagem", "olha", "a", "quero", "olhe", "pra",
                  "para", "eu", "mim", "quero", "acho", "que", "memory",
                  "disco", "espcaco", "espaço", "em", "quantos", "quantas",
                  "Bia", "Bia", "minha", "sua", "nossa"],
       
       
      "BATERIA": ["nivel", "menos", "e", "mais", "ou", "por", "cento", "porcentagem",
                  "quanto", "esta", "a", "bateria", "como", "energia", "estamos",
                  "de", "carga", "util", "como", "vai", "vida", "battery", "energy", 
                  "diga", "qual", "quais", "Bia", "Bia", "minha", "sua", "nossa"],
      
      
      "REDE": ["estamos", "conexcao", "conectados", "?", "conecção", "status",
               "da", "rede", "informe", "Bia", "a", "como", "qual", "quanto", "quantos",
               "internet", "estao", "estão", "conectamos", "estavamos", "estaremos",
               "ou", "sim", "ou", "nao", "não", "Bia", "minha", "sua", "nossa"],
      
      
      "CPU": ["Bia", "Bia", "como", "cpu", "estado", "estamos", "informe", "informacao",
              "informação", "informações", "da", "minha", "nossa", "sua", "cpu", "dados",
              "leia", "olhe", "por", "favor", "a"],
      
      
      "horas": ["horas", "que", "Bia", "diz", "pra", "para", "mim", "as",
                "que horas", "sao", "e", "é"],
      
      
      "dsemana": ["que", "dia", "Bia", "hoje", "qual", "estamos", "em", "o", "a", "de"],
      
      
      "data": ["que", "Bia", "data", "e", "hoje", "estamos", "em", "qual", "a", "o", "de"],
      
      
      "cpf": ["qual", "cpf", "Bia", "ei"],
      
      
      "idade": ["Bia", "minha", "diz", "qual", "idade"],
      
      
      "númeroIndentidade": ["Bia", "qual", "número", "da", "indentidade"],
      
      
      "telefone": ["meu", "Bia", "número", "de", "do", "qual", "meu"],
      
      
      "senhaNu": ["Bia", "qual", "senha", "minha", "nubank"],
      
      
      "senhac6": ["Bia", "qual", "senha", "minha", "c6"],
      
      
      "email": ["Bia", "qual", "email", "meu"],
      
      
      "senhaemail": ["Bia", "senha", "do", "email", "meu"],
      
      
      "senhaVale": ["Bia","senha", "vale", "do", "meu", "qual"],
      
      
      "musicas": ["Bia", "ei", "toca", "tocar", "toque", "baixa", "agulha", "da", "o", "play",
                  "uma", "musica", "musicas", "agora", "alguma", "coisa", "aí", "música", "beleza",
                  "Beleza", "solta", "som"],
      
      "parar_musica": ["bia", "Bia", "parar", "musica", "música", "chega", "de",
                       "ta", "tá", "bom", "som", "sem", "pare", "essa", "para",
                       "ai", "aí", "vai"],
      
      
      "alarme": ["Bia", "ei", "alarme", "preciso", "de", "um", "uma",
                 "pra", "mim", "agora", "amanha", "acordar", "cedo", "defina",
                 "define", "criar", "crie", "para", "pra", "eu", "pode", "ser",
                 "acordasse", "acorde"],
      
      
      "clima": ["como", "Bia", "clima", "tempo", "la", "fora", "ei", "me",
                "diz", "o", "hoje", "em", "clima", "Clima"],
      
      "lista_compras": ["lista", "de", "compras", "Bia", "preciso",
                        "de", "uma", "agora"],
      
      "ler_lista_compras": ["mostre", "o", "que", "tem", "lista", "na", "compras", 
               "ei", "Bia", "me", "mostra", "pra", "mim", "minha", "ei"]
  }
  # Inicializar um dicionário vazio para armazenar as características
  features = {}
  # Para cada classe, verificar se o textoo contém alguma das palavras-chave e atribuir um valor booleano à característica correspondente
  for classe in keywords:
    for word in keywords[classe]:
      features[f"contains({word})"] = word in texto.lower()
  # Retornar o dicionário de características
  return features

# Usar a função nltk.classify.apply_features para aplicar a função extract_features aos dados de treinamento e teste
train_set = nltk.classify.apply_features(extract_features, train_data)
test_set = nltk.classify.apply_features(extract_features, test_data)

# Usar a função nltk.NaiveBayesClassifier.train para treinar um classificador bayesiano ingênuo com o conjunto de treinamento
classifier = nltk.NaiveBayesClassifier.train(train_set)

# Usar a função nltk.classify.accuracy para avaliar a acurácia do classificador com o conjunto de teste
accuracy = nltk.classify.accuracy(classifier, test_set)
print("Acurácia do classificador:", accuracy)

# Usar a função nltk.classify.ClassifierI.show_most_informative_features para mostrar as características mais informativas para o classificador
classifier.show_most_informative_features()

# Definir uma variável de controle para o loop while
continuar = True
 
 #coletaLixo = True
     

# Iniciar um loop while que se repete até o usuário digitar "sair"
while continuar:  
          
    # Pedir ao usuário que digite um textoo ou "sair" para encerrar o programa
    #with sr.Microphone() as mic:
  try: 
    sd.default.device = None 
   
    with sr.Microphone() as mic:
            rec.adjust_for_ambient_noise(mic)
            print("Aguardando comandos...\n")
            audio = rec.listen(mic)
            #time.sleep(50)
            texto = rec.recognize_google(audio, language="pt-BR")
            print(texto)
    #time.sleep(15)
    sd.default.device = None 
  # Verificar se o usuário digitou "sair"
    if texto == "sair":
    # Mudar a variável de controle para False para sair do loop
      continuar = False
    # Imprimir uma mensagem de despedida
      speech_synthesizer.speak_text_async("Ok. Qualquer coisa é só chamar!").get()
  # Caso contrário, continuar com o programa
    else:
    # Usar a função nltk.classify.ClassifierI.classify para classificar o textoo digitado pelo usuário
      classe = classifier.classify(extract_features(texto))
    # Imprimir a classe predita pelo classificador
      print("A classe predita pelo classificador é:", classe)
    # Verificar se a classe é "contar_palavras"
      if classe == "dialog":
      # Chamar a função contar_palavras com o textoo digitado pelo usuário
        #speech_synthesizer.speak_text_async(random.choice(conti)).get()
        dialog(texto)
    # Verificar se a classe é "identificar_entidades"
      elif classe == "cria_pasta":
        speech_synthesizer.speak_text_async(random.choice(confcomand))
        cria_pasta(texto)
      if classe == "abrir":
        speech_synthesizer.speak_text_async(random.choice(confcomand))
        abrir(texto)
      else:
        if classe =="CPU":
          cpu(texto)
        else:
          if classe == "MEMORIA":
            memoria(texto)
          else:
            if classe == "REDE":
              rede(texto)
            else:
              if classe == "BATERIA":
                bateria(texto)
              else:
                if classe == "horas":
                  horas(texto)
                else:
                  if classe == "dsemana":
                    dsemana(texto)
                  else:
                    if classe == "data":
                      data(texto)
                    else:
                      if classe == "cpf":
                        speech_synthesizer.speak_text_async(f"Chef, o número do seu CPF é {chef.CPF}").get()
                      else:
                        if classe == "idade":
                            speech_synthesizer.speak_text_async(f"Chef, sua idade é {chef.Minhaidade}. de acordo com o que você me disse!").get()
                        else:
                          if classe == "númeroIndentidade":
                            speech_synthesizer.speak_text_async(f"Chef, o número da sua indentidade é {chef.Nindentidade}").get()
                          else:
                            if classe == "telefone":
                              speech_synthesizer.speak_text_async(f"Chef, o seu número é {chef.telefone}").get()
                            else:
                              if classe  == "senhaNu":
                                speech_synthesizer.speak_text_async(f"Chef, sua senha do Nubank é {chef.senhaNubank}").get()
                              else:
                                if classe == "senhac6":
                                  speech_synthesizer.speak_text_async(f"Chef, sua senha do C6 bank é {chef.senhaC6}").get()
                                else:
                                  if classe =="email":
                                    speech_synthesizer.speak_text_async(f"Chef, seu email é {chef.emailPrincipal}").get()
                                  else:
                                    if classe == "senhaemail":
                                      speech_synthesizer.speak_text_async(f"Chef, a senha do seu email é {chef.senhaEmailPrincipal}").get()
                                    else:
                                      if classe == "senhaVale":
                                        speech_synthesizer.speak_text_async(f"Chef, a senha do seu vale alimentação é {chef.senhaValeAlimentacao}").get()
                                      else:
                                        if classe == "musicas":
                                          musicas(texto)
                                        else:
                                          if classe == "alarme":
                                            alarme(texto)
                                          else:
                                            if classe == "clima":
                                              clima(texto)
                                            else:
                                              if classe == "lista_compras":
                                                lista_compras(texto)
                                              else:
                                                if classe == "ler_lista_compras":
                                                  ler_lista_compras(texto)
                                                else:
                                                    if classe == "parar_musica":
                                                      parar_musica(texto)
                                                    
  except:
      print("fale chef...")