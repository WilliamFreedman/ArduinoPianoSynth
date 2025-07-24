#include <Arduino.h>
#include "pitches.h"

#define BUZZER_PIN 8  // or 8 depending on your board

void waitForHost() {
  Serial.println("Waiting for host...");
  while (true) {
    if (Serial.available()) {
      char handshake = Serial.read();
      if (handshake == '!') {
        Serial.println("Host connected");
        break;
      } else {
        Serial.print("Ignored byte: ");
        Serial.println(handshake);
      }
    }
  }
}

const unsigned int note_table[8][12] = {
  // Octave 1
  {NOTE_C1,  NOTE_CS1, NOTE_D1,  NOTE_DS1, NOTE_E1,  NOTE_F1,  NOTE_FS1, NOTE_G1,  NOTE_GS1, NOTE_A1,  NOTE_AS1, NOTE_B1},
  // Octave 2
  {NOTE_C2,  NOTE_CS2, NOTE_D2,  NOTE_DS2, NOTE_E2,  NOTE_F2,  NOTE_FS2, NOTE_G2,  NOTE_GS2, NOTE_A2,  NOTE_AS2, NOTE_B2},
  // Octave 3
  {NOTE_C3,  NOTE_CS3, NOTE_D3,  NOTE_DS3, NOTE_E3,  NOTE_F3,  NOTE_FS3, NOTE_G3,  NOTE_GS3, NOTE_A3,  NOTE_AS3, NOTE_B3},
  // Octave 4
  {NOTE_C4,  NOTE_CS4, NOTE_D4,  NOTE_DS4, NOTE_E4,  NOTE_F4,  NOTE_FS4, NOTE_G4,  NOTE_GS4, NOTE_A4,  NOTE_AS4, NOTE_B4},
  // Octave 5
  {NOTE_C5,  NOTE_CS5, NOTE_D5,  NOTE_DS5, NOTE_E5,  NOTE_F5,  NOTE_FS5, NOTE_G5,  NOTE_GS5, NOTE_A5,  NOTE_AS5, NOTE_B5},
  // Octave 6
  {NOTE_C6,  NOTE_CS6, NOTE_D6,  NOTE_DS6, NOTE_E6,  NOTE_F6,  NOTE_FS6, NOTE_G6,  NOTE_GS6, NOTE_A6,  NOTE_AS6, NOTE_B6},
  // Octave 7
  {NOTE_C7,  NOTE_CS7, NOTE_D7,  NOTE_DS7, NOTE_E7,  NOTE_F7,  NOTE_FS7, NOTE_G7,  NOTE_GS7, NOTE_A7,  NOTE_AS7, NOTE_B7},
  // Octave 8
  {NOTE_C8,  NOTE_CS8, NOTE_D8,  NOTE_DS8, 0,        0,        0,        0,        0,        0,        0,        0}
};



void setup() {
  Serial.begin(9600);
  while (!Serial);
  waitForHost();
  Serial.println("Arduino ready");
  pinMode(BUZZER_PIN, OUTPUT);
}

unsigned int new_tone = 0;
unsigned int current_tone = 0;


void loop() 
{
  if (current_tone != new_tone)
  {
    if (new_tone == 0)
    {
      noTone(BUZZER_PIN);
    }
    else
    {
      tone(BUZZER_PIN, new_tone);
    }
    current_tone = new_tone;
  }

  if (Serial.available() >= 2) 
  {
    char note_code = Serial.read();
    char octave = Serial.read();


    // If it's the stop signal
    if (note_code == 'X' && octave == 'X') 
    {
      new_tone = 0;
    }
    else
    {
      int index = -1;
      switch (note_code) {
        case 'C': index = 0; break;
        case 'c': index = 1; break;
        case 'D': index = 2; break;
        case 'd': index = 3; break;
        case 'E': index = 4; break;
        case 'F': index = 5; break;
        case 'f': index = 6; break;
        case 'G': index = 7; break;
        case 'g': index = 8; break;
        case 'A': index = 9; break;
        case 'a': index = 10; break;
        case 'B': index = 11; break;
      }

      if (index >= 0 && octave >= 0 && octave <= 7) {
        new_tone = note_table[octave][index];
      } else {
        Serial.println("Invalid note or octave received");
        new_tone = 0;
      }
    }
  }
}

