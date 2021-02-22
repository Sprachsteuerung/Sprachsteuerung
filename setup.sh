sudo apt-get update                                                         #Update die Packetliste
sudo apt-get upgrade                                                        #Lade die neuen Versionen der instalierten Pakete
sudo apt install python-gpiozero libespeak1 -y
pip3 install pyttsx3  	
pip3 install vosk
pip3 install pyaudio
cd Sprachsteuerung
wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip vosk-model-small-de-0.15.zip
sudo mv vosk-model-small-de-0.15 model
git clone https://github.com/respeaker/seeed-voicecard #soundkarte microfon
cd seeed-voicecard
sudo ./install.sh
sudo ./install.sh --compat-kernel #test mit alten kernel
cd
sudo apt install audacity
sudo reboot

