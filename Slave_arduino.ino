#include <Servo.h>
#include <Wire.h>

// arm 2
Servo myServo21;
Servo myServo22;

// arm 1
Servo myServo11;
Servo myServo12;

// arm 3
Servo myServo31;
Servo myServo32;

const int stopValue = 1500;

// ----- Non‑blocking servo state -----
enum ServoState { IDLE, MOVING };

// arm2
ServoState state1 = IDLE;
ServoState state2 = IDLE;
unsigned long servo1EndTime = 0;
unsigned long servo2EndTime = 0;
int servo1Direction = 0;  // 1 = forward, 2 = reverse
int servo2Direction = 0;

// arm1
ServoState state3 = IDLE;
ServoState state4 = IDLE;
unsigned long servo3EndTime = 0;
unsigned long servo4EndTime = 0;
int servo3Direction = 0;   // 1 = forward, 2 = reverse
int servo4Direction = 0;

// ----- I2C received data (volatile for ISR) -----
volatile bool newCommand = false;
volatile int  receivedCmd = 0;
volatile int  receivedTime = 0;

void setup() {
  // Enable internal pull‑ups (may help, but not required for this fix)
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);

  Serial.begin(9600);
  Wire.begin(8);
  Wire.onReceive(receiveEvent);

  // arm 2 servo motors
  myServo21.attach(3, 900, 2100);
  myServo22.attach(5, 900, 2100);
  myServo21.writeMicroseconds(stopValue);
  myServo22.writeMicroseconds(stopValue);

  // arm 1 servo motors
  myServo11.attach(9, 900, 2100);
  myServo12.attach(10, 900, 2100);
  myServo11.writeMicroseconds(stopValue);
  myServo12.writeMicroseconds(stopValue);



  Serial.println("Slave ready. ");
}

void loop() {
  // ----- Process new I2C commands immediately -----
  if (newCommand) {
    newCommand = false;

    char cmd = receivedCmd;
    int timeMs = receivedTime;

    switch (cmd) {
      // arm2 Servo 1
      case 1:  // forward + duration
        myServo21.writeMicroseconds(1470);
        servo1EndTime = millis() + timeMs;
        servo1Direction = 1;
        state1 = MOVING;
        break;
      case 2:  // reverse + duration
        myServo21.writeMicroseconds(1530);
        servo1EndTime = millis() + timeMs;
        servo1Direction = 2;
        state1 = MOVING;
        break;
      case 3:  // stop immediately
        myServo21.writeMicroseconds(stopValue);
        state1 = IDLE;
        servo1Direction = 0;
        break;

      // arm2 Servo 2
      case 4:
        myServo22.writeMicroseconds(1470);
        servo2EndTime = millis() + timeMs;
        servo2Direction = 1;
        state2 = MOVING;
        break;
      case 5:
        myServo22.writeMicroseconds(1530);
        servo2EndTime = millis() + timeMs;
        servo2Direction = 2;
        state2 = MOVING;
        break;
      case 6:
        myServo22.writeMicroseconds(stopValue);
        state2 = IDLE;
        servo2Direction = 0;
        break;


      // Arm1 Servo1
      case 'q':
        myServo11.writeMicroseconds(1470);
        servo3EndTime = millis() + timeMs;
        servo3Direction = 1;
        state3 = MOVING;
        break;
      case 'g':
        myServo11.writeMicroseconds(1530);
        servo3EndTime = millis() + timeMs;
        servo3Direction = 2;
        state3 = MOVING;
        break;
      case 'b':
        myServo11.writeMicroseconds(stopValue);
        state3 = IDLE;
        servo3Direction = 0;
        break;

      // Arm1 Servo2
      case 'y':
        myServo12.writeMicroseconds(1470);
        servo4EndTime = millis() + timeMs;
        servo4Direction = 1;
        state4 = MOVING;
        break;
      case 'h':
        myServo12.writeMicroseconds(1530);
        servo4EndTime = millis() + timeMs;
        servo4Direction = 2;
        state4 = MOVING;
        break;
      case 'n':
        myServo12.writeMicroseconds(stopValue);
        state4 = IDLE;
        servo4Direction = 0;
        break;




        

      // Emergency stop both
      case 0:
        myServo21.writeMicroseconds(stopValue);
        myServo22.writeMicroseconds(stopValue);
        state1 = IDLE;
        state2 = IDLE;
        servo1Direction = 0;
        servo2Direction = 0;
        break;
    }
  }

  // ----- Non‑blocking servo timeout checks -----
  unsigned long now = millis();

  if (state1 == MOVING && now >= servo1EndTime) {
    myServo21.writeMicroseconds(stopValue);
    state1 = IDLE;
    servo1Direction = 0;
    Serial.println("Servo1 stopped.");
  }

  if (state2 == MOVING && now >= servo2EndTime) {
    myServo22.writeMicroseconds(stopValue);
    state2 = IDLE;
    servo2Direction = 0;
    Serial.println("Servo2 stopped.");
  }
  
  if (state3 == MOVING && now >= servo3EndTime) {
  myServo11.writeMicroseconds(stopValue);
  state3 = IDLE;
  servo3Direction = 0;
  Serial.println("Servo11 stopped.");
  }

  // Arm1 Servo2 (new)
  if (state4 == MOVING && now >= servo4EndTime) {
    myServo12.writeMicroseconds(stopValue);
    state4 = IDLE;
    servo4Direction = 0;
    Serial.println("Servo12 stopped.");
  }

  // Other tasks can go here without blocking
}

// I2C Interrupt Handler (always returns quickly)
void receiveEvent(int bytes) {
  // Handle BOTH 1‑byte and 3‑byte commands
  if (bytes == 1) {
    // Stop command (no duration)
    receivedCmd = Wire.read();
    receivedTime = 0;   // No time needed
    newCommand = true;
  }
  else if (bytes >= 3) {
    // Timed command: cmd + high + low
    receivedCmd = Wire.read();
    byte high = Wire.read();
    byte low  = Wire.read();
    receivedTime = word(high, low);
    newCommand = true;
  }
  // Ignore any other byte counts (or you could read them anyway)
}