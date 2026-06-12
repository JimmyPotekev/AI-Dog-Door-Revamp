
- main control loop has a sleep. this should be moved deeper into the controller for the appropriate states operation.
- the distance_score and vision_count used to detect motion/vision for a duration of time are compared against hard-coded values. These values should be:
    1. not hard-coded
    2. set to appropriate values that are calculated depending on the fequency of state udpates.   
- the camera process does not have propper logging setup it. Simply calling getLogger would conflict with the main process. 
- the OPEN state operation has lots of overlap with the verifying process. having the OPEN process switch back and forth with the VERIYFING process would cause unneccesary complexity. but duplicating the code is not preffered. maybe separate the common functionality into a function/util. 
- currently, the camera process captures and process a single frame at a time when the controller signals that it needs to check for a dog. The controller, then keeps a vision score that adjusts depending on the duration of the dog in the frame. this functionality is duplicated in the VERIFYING and OPEN state. It might be beneficial to transfer this vision duration to the camera process, and the controller just signals the process when to sleep and when to run. There are several options for this camera communication:
    1. Current Impl:
        - Controller: 
        requests the camera to process a single frame increments or decrements the vision score based on this frame. dog is considered detected when the vision score is above the threshold.
        - Camera Process impl:
        continuously checks the queue for a command(waits on empty queue). Use match case for each command type. The command to check for a dog will capture a single frame, run the cv model on that frame, and respond to the main process that the frame either had a dog in it or didn't. 
        - Pros:
            - less need for IPC or synchronization 
            - 
        - Cons:
            - camera process sleeps a lot
            - possibly less performance
            - may defeat the purpose of being in a separate process if the main process just wait for camera process

    2. Constant Decection
        - Controller:
        Checks camera process status if there is a dog in the frame that very moment. increments or decrements the vision score based on this frame. dog is considered detected when the vision score is above the threshold.
        - Camera Process:
        While object recognition is enabled(depending on FSM state) the camera process continusouly captures a frame, processes it for detection, and updates the camera state specifying whether or not there is currently a dog in the frame.   
        - Pros:
            - Actual parallelism, camera process only needs to sleep when the controller isn't looking for a dog. 
        - Cons:
            - will need more synchronization and semaphores. 
            - might get confusing between the use of queue and semaphore. 

    3. Constant detection + duration check
        - controller: 
        similar to option 2, except is just checks the dog detected status once and leaves the vision score to the camera process.
        - camera process: 
        similar to option 2, continusously scans for dog updating its dog detected flag. Here, the dog detected flag is set based on the vision score. the score starts at 0 and is incremented for each frame a dog is detected. there is a max ceiling for which this score and be incremented to. for each frame a dog is not detected, the score is decremented. the min floor for the score is 0. there is a range between the specified threshold and max score where the dog is considered detected. once the score drops below this range, the dog is considered not in the frame. 
        - Pros:
            - makes controller logic simpler
            - reduces duplication between OPEN and VERIFYING states.
        - Cons:
            - more complex implementation.
            - unsure how this will affect detection accuracy

- Main and Camera process IPC consists of an input queue, and output queue, each of size 1. These queue communicate with the CameraComm enums. These single queues are useful for their blocking properties which limits the need to synchronization primitves, but it may be very tight bottle neck for performance. 