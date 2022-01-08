/*

*/

const float OUT_PIN = A4;

void setup() {
    Serial.begin(9600);
}

void loop() {
    Serial.println(analogRead(OUT_PIN));
}
