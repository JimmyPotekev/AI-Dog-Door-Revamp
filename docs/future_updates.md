# Future Updates
RogersFergus

## 🛠️Mechanical 

### 🔒Door lock
Issue: 
Currently, there is nothing stopping the doors from being forcefully opened or closed. This could happen from a person, animal, or strong wind. 

Solution:


## ⚡Hardware/Electrical

### Servo Power Toggle

Issue: 
Currently, the servos are always powered. Some states, like IDLE, do not use the servos at all. This can cause unnecessary "passive" or "leakage" power consumption, especially if the system is used for extended periodsd of time (as most household applicances do). 

Solution:
- Option A 
    - Add a logic enable switch on the power board for the servos. This can be toggled from a GPIO pin on the Raspberrypi board. 

## 💻Firmware


## Features


### IOT System Monitoring & Control

Issue:
Currently, the system operates entirely on its own, independent of human input. It might be nice to have a server or web address for someone to check the systems status, health. Maybe even put it in a lock down or night time mode. Have scheduled operation windows. 

## System Level

### Outdoor Half of the Door System
Issue: the system is currently being implemented only considering the indoor portion of the door. So no outdoor, sensor, camera, or servos. 

