
- main control loop has a sleep. this should be moved deeper into the controller for the appropriate states operation.
- the distance_score and vision_count used to detect motion/vision for a duration of time are compared against hard-coded values. These values should be:
    1. not hard-coded
    2. set to appropriate values that are calculated depending on the fequency of state udpates.   
- the camera process does not have propper logging setup it. Simply calling getLogger would conflict with the main process. 
- the OPEN state operation has lots of overlap with the verifying process. having the OPEN process switch back and forth with the VERIYFING process would cause unneccesary complexity. but duplicating the code is not preffered. maybe separate the common functionality into a function/util. 
- currently, the camera process captures and process a single frame at a time when the controller signals that it needs to check for a dog. The controller, then keeps a vision score that adjusts depending on the duration of the dog in the frame. this functionality is duplicated in the VERIFYING and OPEN state. It might be beneficial to transfer this vision duration to the camera process, and the controller just signals the process when to sleep and when to run. There are several options for this camera communication:
    1. Current Impl:
        - Controller: 
        requests the camera to process a single frame and respond with a binary DOG_DETECTED or DOG_NOT_DETECTED
        - Camera Process impl:
        continuously checks the queue for a command(waits on empty queue). Use match case for each command type. The command to check for a dog will capture a single frame, run the cv model on that frame, and respond to the main process that the frame either had a dog in it or didn't. 
        - Pros:
            - simple. 
            - 
