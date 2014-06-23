Pieva
=====

Silicone meadow - An LED installation by Ieva Dautartaitė built in Technarium hackerspace in Vilnius, Lithuania.

![TRIAC BLOC](doc/photos/facebook_-1830532766.jpg)

The installation consists of several sections made of plywood with silicone tubes attached. Every silicone tube is illuminated by a separate addressable RBG LED.

Software/hardware stack:
 * 1k of WS2812 LEDs
 * 3 ![Fadecandy](https://github.com/scanlime/fadecandy) driver boards
 * Perlin Simplex noise generation and data structure reshaping routines written in C as a Python module
 * LED connection model definition and glue code written in Python
 * on Arch Linux ARM distro
 * on Raspberry Pi

Every section has a separate 5V switched mode power supply unit, AC power is daisy-chained. 

Data and ground connections are routed using Cat5 cable implementing a star ground topology. 

The tubes are attached using a custom 3d printed holders. 

More info, contacts, etc at: 
 * http://technarium.lt
 * http://www.degantiszmogus.lt
 * http://wemakethings.net

