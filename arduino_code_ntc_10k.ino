const int ntcWiderstand = 10000; // NTC-Widerstand mit 10 kOhm
const int MAX_ANALOG_VALUE = 1023;
//An welchem analogen Pin der NTC-Widerstand angeschlossen ist
#define PIN A0 
void printValue(String text, float value, String text2="");
void setup(void) {
  //beginnen der seriellen Kommunikation
  Serial.begin(9600); 
//An welchem Digital Pin der Raspberry angeschlossen ist
  pinMode(2, OUTPUT); //Setzt den Digitalpin 2 als Outputpin
}
//Beginn der Schleife
void loop(void) {
  float value = analogRead(PIN);
  printValue("analog Wert: ", value);
 
  // Konvertieren des analogen Wertes in ein Widerstandswert
  value = (MAX_ANALOG_VALUE / value)- 1; 
  value = ntcWiderstand / value;
  printValue("NTC-Widerstands Wert: ", value, " Ohm");
//if abfrage des NTC-Widerstands Wertes 
//bei über 106250.01 high Signal an D2
//bei unter 106250.01 low Signal an D2
  if (value > 106250.01){
     digitalWrite(2, HIGH);
  }
  else
     digitalWrite(2, LOW);

//warte 1000 ms (1sek)
  delay(1000);
}
//Drucke im Online Monitor jede Sekunde den Betrag des analog Wertes und den NTC-Widerstands Wert
void printValue(String text, float value, String text2=""){
  Serial.print(text);
  Serial.print(value); 
  Serial.println(text2);
}
  

  
