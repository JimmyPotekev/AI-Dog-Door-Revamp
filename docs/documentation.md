# 🧩 System Architecture Overview

## 📦 Objects / Class Managers

### 🚪 DogDoorController
- Main controller of **door state, behavior, and operation**
- FSM
- High level control
- Does NOT perform work, simply reads flags/status/events, and controlls accordingly
- Owns:
  - DogDoorHardware

---

### DogDoorHardware
- Contains:
  - Cameras
  - Sensors
  - Servos

### 📷 Camera
- System includes:
  - 2 cameras (inside + outside)
- Each camera should:
  - Run in its own **process or thread**
  - Contain an **ImageProcessor**
- Design considerations:
  - Keep abstract (allow hardware swapping)
  - Consider multiprocessing tools:
    - `Value`
    - `Array`
    - `SharedMemory`
- Avoid opening door on a single frame, maybe require N positive frame within a time window.
or use a score that rises on detection, and decays otherwise.

---

### 🧠 ImageProcessor
- Takes frames from Camera
- Runs **object recognition model**
- Performance considerations:
  - Use multiprocessing shared memory:
    - `Value`
    - `Array`
    - `SharedMemory`

---

### ⚙️ Servo
- Has a **PWM range**
- Uses **enums** for position control
- Consider defining as an interface:
  - Enables both **C++ and Python implementations**

---

### 📡 Sensor
- Current setup:
  - 2 ultrasonic sensors (inside + outside)
- Design goals:
  - Keep abstract for flexibility
- Consider interface-based design:
  - Supports multiple implementations (C++ / Python)
- Minimum proximity duration instead of a single data point. Similar idea to camera.


---

### 📝 Logger
- Runs in its own **thread**
- Modes:
  - **Production**
    - Log level = Warning
    - Uses real hardware components
  - **Debug**
    - Log Level = Debug
    - Uses real hardware components
  - **Test**
    - Log level = Info
    - Uses dummy or mock components. No hardware used.

---

### Threads
- Threads should only do work and provide information. They should NOT modify the FSM state. 
- FSM remains master controller, a random threads should not modify this. 
- A thread can perform a task.
- A thread can retrieve information and signal to the controller that an event happened.
- A thread can queue events. The controller checks this queue. 

---

# 🔄 Main Operation Logic

## Description

The underlying principle/operation of this automated door system is an FSM(finite state machine). It has predefined modes of operation. Transitions between modes are dependent on data collected and processed by the external sensors. 

**States**
- IDLE - Polls for distance. If distance < some threshold for some duration of time, transition to verifying dog detection
- VERIFYING - Runs object recognition to detect a dog.
- OPEN - Opens the door and 
- CLOSING - Turns off camera and transitions back to IDLE. 

**Config:**
Upon running the program, it starts with the initilization setup to configure the system. First the logger, then hardware, then the systems state. 

**Operation:**
The 

## 🚀 Initialization
- Initialize all system components:
  - Logger
  - DogDoorController
  - DogDoorHardware
  - Cameras
  - Sensors
  - Servos

---

## 🔁 Main Loop

```pseudo
starts in IDLE mode
loop:
    match(controller mode):
      case IDLE:
        while true:
          check_distance()
          if distance < threshold:
            distance_score ++
          else:
            distance_score -- (if distance isn't already 0)
          
          if distance_score > 5:
            break

          sleep(0.1) // 10Hz frequency 

        transition_to(OPEN)

      case VERIFYING:
        while (time_duration < timeout)
          if dog_is_in_frame():
            transition_to(OPEN)
            break
  
        transition_to(CLOSING)

      case OPEN:
        while(time_duration < timeout)
          detect_dog()
          if dog_detected:
            reset time_duration
        
        transition_to(CLOSING)

      case CLOSING:
        turn_off_camera()
        transition_to(IDLE)
