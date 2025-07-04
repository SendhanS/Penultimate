#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  102
#define SERVOMAX  491

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);

  // Initial 90° position for all servos
  for (int i = 0; i < 6; i++) {
    pwm.setPWM(i, 0, angleToPulse(90));
  }
  Serial.println("Ready to receive servo angles...");
}

void loop() {
  static String input = "";

  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      input.trim();
      Serial.println("Received: " + input);

      int angles[6];
      int index = 0;
      char *token = strtok((char*)input.c_str(), ",");

      while (token != nullptr && index < 6) {
        angles[index++] = atoi(token);
        token = strtok(nullptr, ",");
      }

      if (index == 6) {
        for (int i = 0; i < 6; i++) {
          int pulse = angleToPulse(angles[i]);
          pwm.setPWM(i, 0, pulse);
        }
      } else {
        Serial.println("Invalid data received.");
      }

      input = ""; // clear for next line
    } else {
      input += c; // build input string
    }
  }
}

