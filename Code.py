import playsound
import wikipedia
from datetime import datetime
import os
import webbrowser
import re
import pygame
import wolframalpha
import requests
import pyaudio
import datetime
import speech_recognition as sr
from pytz import timezone
from gtts import gTTS
import re
from pyowm import OWM

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    file = 'audio.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
def listen():
    r = sr.Recognizer()
    text=''
    with sr.Microphone() as source:
        print("speak")
        speak("Speak...")
        audio = r.listen(source, phrase_time_limit = 3)
        try:
            text= r.recognize_google(audio, language ='en-US')
            text=text.lower()
            print("You : ", text)
        except :
            pass
            
        return text
    
def wish():
    hour = datetime.datetime.now()
    hour= (hour.astimezone(timezone('Asia/kolkata'))).hour
    print(hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")
    speak("how can i help u")

def control(query):
        import RPi.GPIO as GPIO
        from time import sleep
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
        if common(query,[["led","on"]])==True:
            GPIO.output(8, GPIO.HIGH)
            print("led is turned on")
            speak("led is turned on")
        if common(query,[["led","off"]])==True:
            GPIO.output(8, GPIO.LOW)
            print("led is turned off")
            speak("led is turned off")
        if common(query,[["buzzer","on"],["play","sound"]])==True:
            GPIO.output(3, GPIO.LOW)
            print("buzzer is turned on")
            speak("buzzer is turned on")
        if common(query,[["buzzer","off"],["stop","sound"]])==True:
            GPIO.output(3, GPIO.LOW)
            print("buzzer is turned off")
            speak("buzzer is turned off")
             
def search(text):
    try:
        results = wikipedia.summary(text, sentences=2)
        print(results)
        speak(results)
    except:
        pass
    return 0
    
def calculate(query):
    app_id = "TH57PT-W4XYVTEY5L"
    client = wolframalpha.Client(app_id) 
    indx = query.lower().split().index("calculate") 
    query = query.split()[indx + 1:] 
    res = client.query(' '.join(query))
    try:
        answer = next(res.results).text
        print(answer)
        speak(answer)
    except:
        pass
    return 0

def note(text):
    fd=os.open("py.txt",os.O_RDWR|os.O_CREAT)
    line = text
    b = str.encode(line)
    try:
        os.write(fd, b)
        os.close(fd)
        print("note created on desktop,thank u")
        speak("note created on desktop,thank u")
    except:
        pass
    return 0

def location(text):
    indx=0
    if "location" in text:
        indx = text.lower().split().index("location")
    elif "map" in text:
        indx = text.lower().split().index("map")
    text = text.split()[indx + 1:]
    location = text[1]
    try:
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
    except :
        pass
    return 0
    
def browse(text):
    reg_ex = re.search('open (.+)',text)
    if reg_ex:
        domain = reg_ex.group(1)
        print(domain)
        url = 'https://www.'+ domain +'.com'
        print(url)
        try:
            webbrowser.open(url)
            print("you have opened "+text+" succesfully")
            speak("you have opened "+text+" succesfully")
        except:
            pass
        return 0
    
def weather(text):
    reg_ex = re.search(' weather in (.*)', text)
    if reg_ex:
        try:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            print('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
            speak('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
        except:
            pass
        return 0
        
def date():
    time = datetime.datetime.now()
    time = time.astimezone(timezone('Asia/kolkata'))
    print('todays date is %d day %s month %d year'%(time.day,time.month,time.year))
    speak('todays date is %d day %s month %d year'%(time.day,time.month,time.year))

def time():
    hour=datetime.datetime.now()
    hour=(hour.astimezone(timezone('Asia/kolkata')))
    print('Current time is %d hours %d minutes' % (hour.hour, hour.minute))
    speak('Current time is %d hours %d minutes' % (hour.hour, hour.minute))

def substring(text,matchlist):
    res = [ele for ele in matchlist if(ele in text)]
    s=bool(res)
    return s
    
def common(text,matchlist):
    s=False
    for i in range(len(matchlist)):
        res = [all([k in text for k in matchlist[i]])]
        if res[0]==True:
            s=True
    return s

if __name__ == "__main__":
    wish()
    while True:
        query=listen()
        print(query)
        if query == "":
            continue
        elif common(query,[["who","you"],["describe","yourself"],["give","introduction"]])==True:
            speak("Hello, I am  Your personal Assistant.I am here to make your life easier")
        elif common(query,[["created","you"],["made","you"],["your","inventor"]])==True:
            speak("I am created by Ritesh singh")
        elif common(query,[["how","you"],["whats","going"],["everything","fine"]])==True:
            speak("ya i am fine , hope u r alo same ")
        elif common(query,[["when","invented","you"],["birthday","your"],["you","created"]])==True:
            speak("my birthday is on 5 november 2019")
        elif common(query,[["goodbye"],["sleep",],["exit"]])==True:
            speak("ok bye , have a nice day . meet u again ")
            break
        elif substring(query,["location","map"])==True:
            location(query)
        elif substring(query,["led","buzzer","motor"])==True:
            control(query)
        elif substring(query,["calculate"])==True:
            calculate(query)
        elif substring(query,["reminder","note","write","create file"])==True:
            print("what do u want to note down ?")
            text=listen()
            note(text)
        elif substring(query,["browse","open","play","start"])==True:
            query=query.replace("browse","open")
            query=query.replace("play","open")
            query=query.replace("start","open")
            browse(query)
        elif common(query,[["what","time"],["current","time"],["clock","status"]])==True:
            time()
        elif common(query,[["today","date"],["day","year"],["current","date"]])==True:
            date()
        elif substring(query,["weather in"])==True:
            weather(query)
        else:
            search(query)


