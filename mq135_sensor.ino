#define anInput A0
#define co2Zero 0

void setup() {
  pinMode(anInput, INPUT);
  Serial.begin(9600);
}

void loop() {
  int co2now[10];
  int co2raw = 0;
  int co2ppm = 0;
  int zzz = 0;

  for (int x = 0; x < 10; x++) {
    co2now[x] = analogRead(A0);
    delay(200);
  }

  for (int x = 0; x < 10; x++) {
    zzz = zzz + co2now[x];
  }

  co2raw = zzz / 10;
  co2ppm = co2raw - co2Zero;
  Serial.print(co2ppm);
  delay(50);
}
