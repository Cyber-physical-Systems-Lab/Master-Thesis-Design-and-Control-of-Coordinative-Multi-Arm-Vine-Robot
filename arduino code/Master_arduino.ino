#include <Wire.h>
#define PUMP 13
#define PUMP2 12
const int valvePin = 2;
const int valvePin2 = 4;


const int motor1IN1 = 3;   // arm1
const int motor1IN2 = 5;   // arm1
const int motor2IN1 = 9;   // arm2
const int motor2IN2 = 10;  // arm2
const int motor3IN1 = 11;  // arm3
const int motor3IN2 = 6;   // arm3

int targetSpeed1 = 0;  // arm 1
int targetSpeed2 = 0;  // arm 2
int targetSpeed3 = 0;  // arm 3

String inputBuffer = "";

void setMotor(int in1, int in2, int speed) {
  if (speed > 0) {
    analogWrite(in1, speed);
    digitalWrite(in2, LOW);
  } else if (speed < 0) {
    digitalWrite(in1, LOW);
    analogWrite(in2, -speed);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
}

// complex input: num,num,char 
void handleComplex(int x, int y, char level) {
  switch (level) {
    case 'l':
    if (x >= 1 && x <= 11 && y >= -11 && y <= 11) {
      // (overlap zone) in area 3
      if (x >= 1 && x <= 11 && y >= -11 && y <= -1) {
        // overlap — pick closest starting point
        //float distTo1 = sqrt(pow(x - 0, 2) + pow(y - 1, 2));   // distance to (0,1)
        //float distTo2 = sqrt(pow(x - 0, 2) + pow(y - (-1), 2)); // distance to (0,-1)

        //if (distTo2 < distTo1) {
          //goto area3;  // closer to condition 2
        //}
        if (abs(x) < abs(y)) {
          goto area3;  // closer to y axis → condition 2
        }
      }

      // arm2 — area 2 and area 3
      Serial.println("area 2, low level");
      targetSpeed2 = 100;
      int durations1[] = {0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500};
      int duration1 = durations1[x];
      digitalWrite(PUMP2, HIGH);
      digitalWrite(valvePin2, LOW);
      digitalWrite(PUMP, HIGH);
      digitalWrite(valvePin, LOW);
      setMotor(motor2IN1, motor2IN2, 100);

      delay(duration1);

      digitalWrite(motor2IN1, LOW);
      digitalWrite(motor2IN2, LOW);
      targetSpeed2 = 0;
      digitalWrite(PUMP2, LOW);
      digitalWrite(valvePin2, HIGH);
      digitalWrite(PUMP, LOW);
      digitalWrite(valvePin, HIGH);
      int servoDurations[] = {0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500};
      int servoDuration = servoDurations[abs(y)];
      Wire.beginTransmission(8);
      if (y > 1)       Wire.write(1);
      else if (y < 1)  Wire.write(4);
      Wire.write(highByte(servoDuration));
      Wire.write(lowByte(servoDuration));
      Wire.endTransmission();

    } else if (x >= -11 && x <= 11 && y >= -11 && y <= -1) {
      area3:
      // arm 3 — area 3 and area 4
      Serial.println("area 3, low level");
      targetSpeed3 = 100;
      int durations2[] = {0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500};
      int duration2 = durations2[abs(y)];
      setMotor(motor3IN1, motor3IN2, 100);
      delay(duration2);
      digitalWrite(motor3IN1, LOW);
      digitalWrite(motor3IN2, LOW);
      targetSpeed3 = 0;

    } 
    else if (x >= -11 && x <= 11 && y >= 1 && y <= 11) {
      area1:
      // arm 1 — area 1 and area 2
      Serial.println("area 1, low level");
    }
    
    else {
      Serial.println("Error: values out of range.");
    }
    break;

    case 'h':
      // area 2, arm 1 and arm 2
      if (x >= 1 && x <= 11 && y >= 1 && y <= 11) {
        //targetSpeed1 = map(x, 1, 11, 0, 255);
        //targetSpeed2 = map(y, 1, 11, 0, 255);
        Serial.print("M1 speed set to: ");
        //Serial.println(targetSpeed1);
        Serial.print("M2 speed set to: ");
        //Serial.println(targetSpeed2);
      }
      // area 3, arm 2 and arm 3
      if (x >= 1 && x <= 11 && y >= -1 && y <= -11) {
        //targetSpeed1 = map(x, 1, 11, 0, 255);
        //targetSpeed2 = map(y, 1, 11, 0, 255);
        Serial.print("M1 speed set to: ");
        //Serial.println(targetSpeed1);
        Serial.print("M2 speed set to: ");
        //Serial.println(targetSpeed2);
      } else {
        Serial.println("Error: for L, both x and y must be 1 to 11.");
      }
      break;

    default:
      Serial.println("Unknown complex level.");
      break;
  }
}

// simple input parser, only num
void handleSimple(char input) {
  switch (input) {
    case '1':
      digitalWrite(PUMP2, HIGH);
      digitalWrite(valvePin2, LOW);
      digitalWrite(PUMP, HIGH);
      digitalWrite(valvePin, LOW);
      Serial.println("Pumps ON.");
      break;
    case '2':
      digitalWrite(PUMP2, LOW);
      digitalWrite(valvePin2, HIGH);
      digitalWrite(PUMP, LOW);
      digitalWrite(valvePin, HIGH);
      Serial.println("Pumps OFF.");
      break;
    case '3':
      Wire.beginTransmission(8);
      Wire.write(1);
      Wire.endTransmission();
      delay(1000);
      break;

    // Motor 1 arm 1
    case 'r':
      targetSpeed1 = 100;
      Serial.println("arm1 Forward.");
      break;
    case 'f':
      targetSpeed1 = -100;
      Serial.println("arm1 Reverse.");
      break;
    case 'v':
      targetSpeed1 = 0;
      Serial.println("arm1 Stop.");
      break;

    // Motor 2 arm 2
    case 'w':
      targetSpeed2 = 100;
      Serial.println("arm2 Forward.");
      break;
    case 's':
      targetSpeed2 = -100;
      Serial.println("arm2 Reverse.");
      break;
    case 'x':
      targetSpeed2 = 0;
      Serial.println("arm2 Stop.");
      break;

    // Motor 3 arm 3
    case 'e':
      targetSpeed3 = 100;
      Serial.println("arm3 Forward.");
      break;
    case 'd':
      targetSpeed3 = -100;
      Serial.println("arm3 Reverse.");
      break;
    case 'c':
      targetSpeed3 = 0;
      Serial.println("arm3 Stop.");
      break;

    // Both
    case 'q':
      targetSpeed1 = 0;
      targetSpeed2 = 0;
      targetSpeed3 = 0;
      Serial.println("All motor stop.");
      break;

    // arm2 Servo1
    case '5':
      Wire.beginTransmission(8);
      Wire.write(1);               // turn direction
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case '6':
      Wire.beginTransmission(8);
      Wire.write(2);
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case '7':
      Wire.beginTransmission(8);
      Wire.write(3);
      Wire.endTransmission();
      break;

    // arm 2 Servo2
    case '8':
      Wire.beginTransmission(8);
      Wire.write(4);
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case '9':
      Wire.beginTransmission(8);
      Wire.write(5);
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case '0':
      Wire.beginTransmission(8);
      Wire.write(6);
      Wire.endTransmission();
      break;


    // arm 1 Servo1
    case 't':
      Wire.beginTransmission(8);
      Wire.write('q');               // turn direction
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case 'g':
      Wire.beginTransmission(8);
      Wire.write('g');
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case 'b':
      Wire.beginTransmission(8);
      Wire.write('g');
      Wire.endTransmission();
      break;

    // arm 1 Servo2
    case 'y':
      Wire.beginTransmission(8);
      Wire.write('y');
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case 'h':
      Wire.beginTransmission(8);
      Wire.write('h');
      Wire.write(highByte(2000));  // send high byte first
      Wire.write(lowByte(2000));
      Wire.endTransmission();
      break;
    case 'n':
      Wire.beginTransmission(8);
      Wire.write('n');
      Wire.endTransmission();
      break;




      

    default:
      Serial.print("Unknown command: ");
      Serial.println(input);
      break;
  }
}

// parser for the input (num, num, char)
void parseCommand(String cmd) {
  cmd.trim();
  int firstComma = cmd.indexOf(',');
  int secondComma = cmd.indexOf(',', firstComma + 1);

  // Format: num,num,char
  if (firstComma != -1 && secondComma != -1) {
    int x = cmd.substring(0, firstComma).toInt();
    int y = cmd.substring(firstComma + 1, secondComma).toInt();
    char level = cmd.charAt(secondComma + 1);

    if (x < -255 || x > 255) {
      Serial.println("Error: x must be -255 to 255.");
      return;
    }
    if (y < -255 || y > 255) {
      Serial.println("Error: y must be -255 to 255.");
      return;
    }

    handleComplex(x, y, level);

    // Format: single char
  } else if (cmd.length() == 1) {
    handleSimple(cmd.charAt(0));

  } else {
    Serial.println("Bad format. Use: num,num,char  or  single char");
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(motor1IN1, OUTPUT);  // arm1
  pinMode(motor1IN2, OUTPUT);  // arm1
  pinMode(motor2IN1, OUTPUT);  // arm2
  pinMode(motor2IN2, OUTPUT);  // arm2
  pinMode(motor3IN1, OUTPUT);  // arm3
  pinMode(motor3IN2, OUTPUT);  // arm3
  pinMode(PUMP, OUTPUT);
  pinMode(PUMP2, OUTPUT);
  pinMode(valvePin, OUTPUT);
  digitalWrite(valvePin, HIGH);
  pinMode(valvePin2, OUTPUT);
  digitalWrite(valvePin2, HIGH);
  Wire.begin();
  Serial.println("set up ready");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (inputBuffer.length() > 0) {
        parseCommand(inputBuffer);
        inputBuffer = "";
      }
    } else {
      inputBuffer += c;
    }
  }
  
  setMotor(motor1IN1, motor1IN2, targetSpeed1);
  setMotor(motor2IN1, motor2IN2, targetSpeed2);
  setMotor(motor3IN1, motor3IN2, targetSpeed3);
  delay(10);
}