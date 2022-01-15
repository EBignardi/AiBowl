#include <Servo.h>
#include "SR04.h"

#include <stdio.h>
#define TRIG_PIN 12
#define ECHO_PIN 11
Servo myservo;
int l=0;
int flag;
int pos = 0;
int qtcibo=0;
int led;
enum states{ S1,S2,S3,S4,S5,stato1, stato2, stato3, stato4};

SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;
int cont;
int contatore;
int incomingByte;
int lastbyte;
states currentstate;
states futurestate;
states cs;
states fs;
void setup() {
  cont=0;
  flag=0;
  led=13;
  pinMode(led, OUTPUT);
  cs=stato1;
  fs=stato1;
  contatore=200;
  currentstate=S1;
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(0);
}
void loop(){
  
  if (cs==stato1){
      a=sr04.Distance();
      if (int(a)<50){
        cont=cont+1;
      }
      if (cont==500){
        fs=stato2;
        cont=0;
      }
  }
  if (cs==stato2){
    Serial.write(0xff);
    Serial.write(0x01);
    Serial.write(0x00);
    Serial.write(0xfe);
    fs=stato3;
  }
  if(cs==stato3){ 
    if (Serial.available()>0){
    //Attesa di una comunicazione da seriale (255 01 00 254)--> (255 02 qt 254) (255 03 00 254)
    incomingByte = Serial.read();
    futurestate=S1;
    if (incomingByte==0xff) futurestate=S2;
    if (currentstate==S2 && incomingByte==0x02) futurestate=S4;
    if (currentstate==S2 && incomingByte==0x03) futurestate=S5;
    if (currentstate==S5) fs=stato1;
    if (currentstate==S4) {
        lastbyte=Serial.read();
        if (lastbyte==0xfe){fs=stato4;}
        else {fs=stato1;}
    }
    currentstate=futurestate;
    }
    delay(10);
  }
  cs=fs;
  if(cs==stato4){
      int contat=int(incomingByte);
      while (contat>0){
      for (pos = 0; pos <= 90; pos += 1) { 
        myservo.write(pos);              
        delay(15);    
      }
      for (pos = 90; pos >= 0; pos -= 1) { 
        myservo.write(pos);              
        delay(15);                       
      }
      contat=contat-1;
     }

    fs=stato1;
  }
   
}
