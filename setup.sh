sudo apt-get update                                                         #Update die Packetliste
sudo apt-get upgrade                                                        #Lade die neuen Versionen der instalierten Pakete
sudo apt install python-gpiozero -y
pip3 install pyttsx3  	
pip3 install vosk
pip3 install pyaudio
cd
cd AuditiveSteuerung
curl https://alphacephei.com/vosk/models/vosk-model-small-de-zamia-0.3.zip
unzip vosk-model-small-de-zamia-0.3.zip
sudo mv vosk-model-small-de-zamia-0.3 model
git clone https://github.com/respeaker/seeed-voicecard #soundkarte microfon
cd seeed-voicecard
sudo ./install.sh
sudo ./install.sh --compat-kernel #test mit alten kernel
cd
sudo apt install audacity




#https://alphacephei.com/vosk/models  1. model download 2. entpacken 3. entpackten ordner "model" nennen und aus diesem project.py starten

