/*
 * adsCMD.h
 * Library header file for adsCMD library
 */
#include "Arduino.h"

//constants define pins on Arduino 
// const int IPIN_PWDN = 2; //not required for TI demo kit
//const int PIN_CLKSEL = 6;//6;//*optional
//const int IPIN_RESET  =3;//*optional
const int PIN_START = 4;
const int IPIN_DRDY = 5;
const int IPIN_CS = 10;//10
//const int PIN_DOUT = 11;//SPI out
//const int PIN_DIN = 12;//SPI in
//const int PIN_SCLK = 13;//SPI clock

//function prototypes
void adc_wreg(int reg, int val); //write register
void adc_send_command(int cmd); //send command
int adc_rreg(int reg); //read register
