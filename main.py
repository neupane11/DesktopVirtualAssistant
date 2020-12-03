import speech_recognition as sr
import playsound
from gtts import gTTS
import os
from time import ctime
import time
import webbrowser
import subprocess
import requests, json 
import pytemperature

def speak(text):
    text=str(text)
    tts=gTTS(text=text,lang='en')
    filename='audio.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
#speak('hello')
def take_input():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        
        #print('say something')
        audio=r.listen(source)
        voice=''
        try:
            voice=r.recognize_google(audio)
            print(voice)
        except sr.UnknownValueError: 
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')
        return voice.lower()
def there_is(commands):
    for command in commands:
        if command in voice:
            return True       
def weather_api(city):
    api_key = "e5cfcb9bc633c0e3b447493cd3a8fceb"#got from creating account with openweather api
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url) 
    # json method of response object ,convert json format data into  python format data 
    x = response.json() 
    
    # Now x contains list of nested dictionaries 
    if x["cod"] != "404": #if not error
    
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        current_temperature = y["temp"] 
        current_temperature=pytemperature.k2f(current_temperature) # Kelvin to Fahrenheit
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
    
        speak(f"the current Temperature of{city} is " +
                        str(current_temperature) + 'ferenheit'+ 'with'+str(weather_description)) 
            
    
    else: 
        speak(" City Not Found ") 
    
def my_location():
    res = requests.get('https://ipinfo.io/')#finds your location based ip address
    data = res.json()

    city = data['city']
    region=data['region']
    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]
    speak(city+region)

def calculator():
    pars=voice.split('is')[-1]
    print(pars)
    opr = pars.split()[1]
    print(opr)
    print(pars.split()[0])
    print(pars.split()[2])
    if opr == '+':
        ans=int(pars.split()[0]) + int(pars.split()[2])
        ans=round(ans,1)
        ans=str(ans)
        speak(f'{pars.split()[0]} plus {pars.split()[2]} is'+ans)
    elif opr == '-':
        ans=int(pars.split()[0]) - int(pars.split()[2])
        ans=round(ans,1)
        ans=str(ans)
        speak(f'{pars.split()[0]} minus {pars.split()[2]} is'+ans)
    elif opr == '*':
        ans=int(pars.split()[0]) * int(pars.split()[2])
        ans=round(ans,1)
        ans=str(ans)
        speak(f'{pars.split()[0]} times {pars.split()[2]} is'+ans)
    elif opr == '/' or opr== 'divide':
        ans=int(pars.split()[0]) / int(pars.split()[2])
        ans=round(ans,1)
        ans=str(ans)
        speak(f'{pars.split()[0]} divide {pars.split()[2]} is'+ans)
    elif opr == '**'or opr== 'power':
        ans=int(pars.split()[0]) ** int(pars.split()[2])
        ans=round(ans,1)
        ans=str(ans)
        speak(f'{pars.split()[0]} power {pars.split()[2]} is'+ans)
    else:
        speak("Wrong Operator")




def service(voice):
    print(voice)
    
    if there_is(['hello','hi']):
        speak('hello, how may i help you?')
    if there_is(['what is the time','tell me time','what time is it']):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak('the time is'+time)

    
    if there_is(['what is your name','tell me your name']):
        speak('i am your desktop')
    if there_is(['how are you','how you doing']):
        speak('i am doing very well,always ready to help you,thanks for asking' )
    if there_is(['open chrome']):
        speak('opening chrome')
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome %s").open("http://google.com")#path to your chrome
    if there_is(['open youtube']):#you can open any url
        search = voice.split("open")[-1]
        url = 'https://www.youtube.com/'
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search} on google')

    if there_is(['find for','search for']):#search for anything
        search = voice.split("for")[-1]
        url = f"https://google.com/search?q={search}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search} on google')    
    if there_is(['exit','bye','goodbye']):
        speak('have a good day')
        exit()
    if there_is(['shutdown my computer','turn off my computer']):
        speak("Do you wish to shutdown your computer ")
        ans=take_input()
        if ans == 'no': 
            exit() 
        else:
            speak('shutting down your computer in few seconds')
           
            os.system("shutdown /s /t 1") 
    if there_is(['restart my computer','restart computer']):
        speak("are you sure you want to restart your computer ")
        ans=take_input()
        if ans == 'no': 
            exit() 
        else:
            speak('restarting  your computer in few seconds')
           
            os.system("shutdown /r /t 1") 
    
    if there_is(['what is the weather of','what is the temperature of','tell me temperature of','what is weather condition of']):
        search=voice.split('of')[-1]
        weather_api(search)
    if there_is(['what is my location','tell me my location']):
        my_location()

    if there_is(["plus","minus","multiply",'times',"divide","power","+","-","*","/"]):
        calculator()
time.sleep(1)
speak('how may i help you')
while 1:
    print('listenning....')
    voice=take_input()
    service(voice)
