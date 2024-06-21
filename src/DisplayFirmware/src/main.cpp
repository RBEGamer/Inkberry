#include <Arduino.h>

//#define ARDUINO_INKPLATE_INKBERRY
#define ARDUINO_INKPLATE_INKBERRY
#include "Inkplate_INKBERRY.h"
#include "Inkplate.h" // Include Inkplate library to the sketch
Inkplate display;     // Create object on Inkplate library

// Define the delay between drawing
#define DELAY_MS 5000

void setup()
{
    display.begin();        // Init library (you should call this function ONLY ONCE)
    display.clearDisplay(); // Clear any data that may have been in (software) frame buffer.
    //(NOTE! This does not clean image on screen, it only clears it in the frame buffer inside ESP32).
    // Write text and rotate it by 90 deg. forever
    int r = 0;
    display.setTextSize(5);
    display.setTextColor(INKPLATE_INKBERRY_WHITE, INKPLATE_INKBERRY_BLACK);
    while (true)
    {
        display.setRotation(r % 4);
        display.setCursor(50, 50);
        display.clearDisplay();
        display.print("INKPLATE_INKBERRY");
        display.display();
        r++;
        delay(DELAY_MS);
    }
}

void loop()
{
    // Never here...
}

// Small function that will write on the screen what function is currently in demonstration.
void displayCurrentAction(String text)
{
    display.setTextSize(1);
    display.setCursor(2, 374);
    display.print(text);
}
