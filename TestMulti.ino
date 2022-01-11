int micro0_Pin = 2;
int micro1_Pin = 4;
int micro2_Pin = 7;

int timerL;
int timerC;
int timerR;

int tLC;
int tCR;
int tLR;

unsigned long TimeL;
unsigned long TimeC;
unsigned long TimeR;

void setup() {
  Serial.begin(9600);
  pinMode(micro0_Pin, INPUT);
  pinMode(micro1_Pin, INPUT);
  pinMode(micro2_Pin, INPUT);
}

void loop() {
  if (timerL == 0 && digitalRead(micro0_Pin) == HIGH){
    TimeL = micros();
    timerL = 1;
  }
  if (timerC == 0 && digitalRead(micro1_Pin) == HIGH){ // button pressed & timer not running already
    TimeC = micros();
    timerC = 1;
  }
  if (timerR == 0 && digitalRead(micro2_Pin) == HIGH){ // button pressed & timer not running already
    TimeR = micros();
    timerR = 1;
  }
  if (timerL*timerC*timerR==1){
    tLR=TimeL-TimeR;
    tLC=TimeL-TimeC;
    tCR=TimeC-TimeR;
    Serial.print(tLR);
    Serial.print ("\t");
    Serial.print(tLC);
    Serial.print("\t");
    Serial.println(tCR);
    delay(1000);
    timerL=0;
    timerC=0;
    timerR=0;
  }
}
