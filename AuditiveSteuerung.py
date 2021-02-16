#!/usr/bin/env python3
import vosk                                                         #Importiere Vosk STT-Engine
from vosk import KaldiRecognizer                                    #Von dem Modul Vosk Lade KaldiRecognizer  
import os                                                           #Importierte Betriebssystem
import pyaudio                                                      #Importiere pyaudio python Audioausgabe
import json                                                         #JSON Funktion zur Decodierung
import pyttsx3                                                      #Text-to-Speech Engine
from gpiozero import LED, Button                                    #Von dem Modul GPIOZERO lade die Funktion LED und Button   
from time import sleep                                              #Von dem Modul Time lade die Funktion sleep  
                                           
model = vosk.Model("model")                                         #Objekt der Klasse Model von Vosk wird agelegt Namens "model"
rec = KaldiRecognizer(model, 44100)                                 #Einstellung Mikrophon abtastrate
p = pyaudio.PyAudio()                                               #Pyaudio Objekt wird angelegt

#/// Zuweisung der SST Engine Vosk wir initialisiert
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,     #Vorbereiten des Streams mit PyAudio auf Channel 1 mit 
                input=True, frames_per_buffer=22050)                #Abtastrate 441100Hz und Signalaufteilung in 22050 Teile
stream.start_stream()                                               #Starten des Aufnahmestreams

#/// Zuweisung der TTS Engine pyttsx3 wird initialisiert
pi_mouth = pyttsx3.init()
pi_mouth2 = pyttsx3.init()

voice_id = "german"                                                 #Änderungs der Sprachausgabe auf Deutsch über die Zuordnung
pi_mouth.setProperty('voice', voice_id)                             #voice_id = Deutsch

#/// Zuweisung und Bennenung der GPIOS
power = LED(25) 
oneCup = LED(5)
twoCup = LED(6)
water = Button(23)
heat = Button(24)

#/// Abschaltung der folgenden GPIOS
power.off()
oneCup.off() 
twoCup.off() 

#/// Initialisierung der Progammes
print("\033[0;32m...::: initialized :::...\033[0m")                 #\033Schriftfarbe = Grün
pi_mouth2.say(" ich bin jetzt bereit. Wie lauten ihre Wünsche?")    #pi_mouth2.say Sprachausgabe des Begrüßungstext
pi_mouth2.runAndWait()                                              #warten auf Spracheingaben

#///Beginn der Programmschleife
while True:             

    data = stream.read(11025, exception_on_overflow=False)          #Lesen des Aufnahmestreams mit 11025       
    if len(data) == 0:                                              #When Daten Länge =0 dann unterbreche den schleifendurchlauf (wenn nichts gesagt wird)
        break

    need_speak = False                                              #Zustandvariable = Es muss nichts gesagt werden                                          

    if rec.AcceptWaveform(data):                                    #Wenn etwas Aufgenommen wurde mach weiter (Kaldi Speichert dieses im JSON Format)
        you = json.loads(rec.Result())["text"]                      #Decodiere den Aufgenommen JSON-Code zu einem Python String 
        msg = you                                                   #Zurodnungs msg=you
        
        if "manfred" in you:                                        #Wenn der name Mannfred in der Spracheingabe vorkommt 
            msg = "was kann ich für dich tun?"                      #Sprachausgabe Antwortet mit dem " " Inhalt
            need_speak = True                                       #Zustandvariable = Es muss etwas gesagt werden    
          
            if "hallo" in you:                                  
                print("Hallo, wie gehts es dir mein Meister und Gebieter?")
                msg = "Hallo, wie gehts es dir mein Meister und Gebieter?"
                need_speak = True
                
            if "einen kaffee" in you:                               #Wenn "einen kaffee" im gesprochenen vorkommt
                power.on()                                          #Setze GPIO.power auf Zustand 1
                sleep(0.5)                                          #Warte 0,5 Sekunden
                power.off()                                         #Setze GPIO.power auf Zustand 0         
                if water.is_active == False:                        #wenn Button water Zutsand 0 hat 
                    sleep(0.5)                                      #Warte 0,5 Sekunden                
                    power.on()                                      #Setze GPIO.power auf Zustand 1 
                    sleep(0.5)                                      #Warte 0,5 Sekunden  
                    power.off()                                     #Setze GPIO.power auf Zustand 0
                    msg = "Der Wasserbehälter ist Leer"             #Antworte "Der Wasserbehälter ist Leer"
                    need_speak = True                               #Zustandvariable = Es muss etwas gesagt werden   
                else:                                               #Ansonsten
                    pi_mouth2.say("ich Heize die maschine auf")     #Antworte "ich Heize die maschine auf"
                    pi_mouth2.runAndWait()                          #Sprachausgabe wartet auf Anweisungen
                    sleep(2.0)                                      #warte 2 Sekunden
                    while heat.is_active == True:                   #solange Button heat Zustand 1 hat warte in der schleife
                        sleep(2.0)                                  #Warte 2 Sekunden
                    oneCup.on()                                     #Setze GPIO.onecup auf Zustand 1  
                    sleep(0.5)                                      #Warte 0,5 Sekunden
                    oneCup.off()                                    #Setze GPIO.onecup auf Zustand 0
                    pi_mouth2.say("Ich koche jetzt den Kaffee")     #Antworte "Ich koche jetzt den Kaffee"
                    pi_mouth2.runAndWait()                          #Sprachausgabe wartet auf Anweisungen
                    sleep(23)                                       #Warte 23 Sekunden solange der Kaffee gekocht wird
                    power.on()                                      #Setze GPIO.power auf Zustand 1
                    sleep(0.5)                                      #Warte 0,5 Sekunden
                    power.off()                                     #Setze GPIO.power auf Zustand 0
                    msg = "der Kaffee ist fertig"                   #Antworte "der Kaffee ist fertig" 
                    need_speak = True                               #Zustandvariable = Es muss etwas gesagt werden  
                    
            if "zwei kaffee" in you:                                #Ablauf für zwei Tassen Kaffee  
                power.on()
                sleep(0.5)
                power.off()
                if water.is_active == False:
                    sleep(0.5) 
                    power.on()
                    sleep(0.5)
                    power.off()
                    msg = "Der Wasserbehälter ist Leer"
                    need_speak = True
                else:
                    pi_mouth2.say("ich Heize die maschine auf")
                    pi_mouth2.runAndWait()
                    sleep(2.0)
                    while heat.is_active == True:
                        sleep(2.0)
                    twoCup.on()
                    sleep(0.5)
                    twoCup.off()
                    pi_mouth2.say("Ich koche jetzt den Kaffee")
                    pi_mouth2.runAndWait()
                    sleep(23)
                    power.on()
                    sleep(0.5)
                    power.off()
                    msg = "der Kaffee ist fertig"
                    need_speak = True
                
            if "wiedersehen" in you:                                 #Wenn "wiedersehen" im gesprochenen vorkommt
                msg = "Dankeschön"                                   #Antworte "Dankeschön"
                print("\033[0;32myou:\033[0m " + you)                #print das gesprochene Wort (you) in Grün  
                print("\033[0;35mpi:\033[0m " + msg)                 #print die Antwort (msg) in Lila
                pi_mouth.say(msg)                                    #Antworte "Sage die Antwort (msg)"
                pi_mouth.runAndWait()                                #Sprachausgabe wartet auf Anweisungen
                break                                                #break beendet die Schleife und das Script beendet sich

            print("\033[0;32myou:\033[0m " + you)                    #print das gesprochene Wort (you) in Grün      
            print("\033[0;35mpi:\033[0m " + msg)                     #print die Antwort (msg) in Lila
            if need_speak == True:                                   #Zustandvariable = Es wurde was gesagt
                pi_mouth.say(msg)                                    #Antworte "Sage die Antwort (msg)"
                pi_mouth.runAndWait()                                #Sprachausgabe wartet auf Anweisungen
