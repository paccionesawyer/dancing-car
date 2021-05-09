# Viennese Ball Dancing Robot

## Overview

This project is a final project for ME 35 - Intro to Robotics course in Spring 2021 at Tufts University taught by Prof. Chris Rogers. The project brings together various topics and ideas discussed in the class such as serial communication, image and audio processing and navigation.

## Description

The Viennese Ball is a waltz dance event for our robots in the class to celebrate the completion of a successful and enjoyable semester. To celebrate this event, we partnered up to build robots that dance around a circle to waltz songs. My partner Olif Hordofa and I, each built robots that are joined together for the dance. The primary hardwares we used in this project are Spike Primes, Raspberry Pis, Lightsensors, Microphones and Motors.

## Objectives

*   Have the two robots spin about a common center at all times while dancing
*   Have the two robots stay in a big circle with all the robots at all times while dancing
*   Start dancing with the queue stop dancing when the music stops

The basic setup simply explained is similar to that of the earth revolving around the sun while rotating about its own axis. Just as the earth revolves around the sun, our joined robot dancers needed to do the same about the center of the big white tape on the floor. At the same time, the earth rotates about its axis. Similarly, our joined robots will rotate about their common center.

## Milestones

### Milestone 0: Basic Line Following and Serial Communication

From a previous project in the class, we were able to make a robot that follows a white tape on the floor for navigation. In that project, we used light sensors to stay on the line, ultrasonic sensors to avoid collisions with other robots and motors for a straight path motion. To start off this project, as shown in the picture above we joined the robots together with a light sensor in between them. Considering one of the robots on either side as right/left sides of one complete robot, we attempted to move along the white tape in without the two robots spinning about one another.

Similarly, since we are using Raspberry Pi’s for audio detection which is then communicated to the Spike Prime to control the motors we used a serial communication setup between the two hardwares that we used in previous projects.

### Milestone 1a: Music Detection
This first aspect of this project Olif and I decided to tackle was the issue of detecting when music was actually playing. Our first iteration was to detect the audio using the a k-Nearest-Neighbors algorithm along with the built in microphone of a SEEED WIO-Terminal board. The code for which can be seen below. k-nearest neighbors (KNN) is a supervised learning algorithm which allows us to compare new data into a set of trained cases. For our project, the cases are 'Music On' and 'Music Off'. To learn more about the basics of the KNN algorithm, check out [this article](https://towardsdatascience.com/machine-learning-basics-with-the-k-nearest-neighbors-algorithm-6a6e71d01761). Unfortunately, the on-board microphone was not sensitive enough so our algorithm could not differentiate between the two cases. This posed a huge limitation on our project, so we eventually upgraded our hardware to use a Raspberry Pi microphone. The time we spent with the WIO microphone was not useless at it allowed us to get familiar with the implementation of the k-Nearest-Neighbors algorithm.

### Milestone 1b: Music Detection on Raspberry Pi
With a new microphone and a new microprocessor we again went about implementing the KNN algorithm, now in python! The code for the training has been provided below. The new microphone did a much better job of differentiating between the two cases, so we could move on to implementing the other aspects of the assignments.

### Milestone 2: Complex Line Following

Our dancing pair needed to be part of a group of 13 pairs of dancers that revolve around a big circle while spinning together to the waltz music playing. What we called the complex line following is a step-up from the simple line following in that it has complex rotation motions involved. To achieve the two rotations described above for our robots, we needed two light sensors. Both light sensors were connected to a single SPIKE Prime which we will call the “Lead” SPIKE Prime. One light sensor would be used to provide the error as it is normally in a proportional controller for a line following robot. The other light sensor would use a kNN algorithm to determine whether it crossed the line. This way we can always determine what side of the line the Lead Spike Prime is. What this allows us to do is know whether we need to speed up or slow down the Lead Spike Prime in order to stay on the line. This introduces one of the limitations of our setup as communication between the two SPIKE Primes is difficult to implement directly, and any indirect communication presents other problems like lag. Therefore we could only control the speed of the Lead Spike Prime, and the other had it’s motors set to a constant speed. This resulted in a sub-par result, as can be seen in the video below.

### Milestone 3: Reality Check

In the end we had to scale down our ambition and focus on something more realistic to complete the project in a reasonable time frame. An unfortunate situation but one we were prepared to deal with. Our end result uses a Proportional plus derivative controller to follow the line around the circle. When audio is detected by the PI, the motor on top of the car is turned on spinning our dancers.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   [Raspberry Pi 4](https://www.google.com/search?q=raspberry+pi+4&sxsrf=ALeKk03vsMgGCu7PQVxu5BVM5yzeNxULQw:1613717510216&source=lnms&tbm=shop&sa=X&ved=2ahUKEwjM7dqXrvXuAhWYWc0KHdwgBTIQ_AUoAXoECAUQAw&biw=958&bih=1087) x2

    *   Libraries
        *   [pyserial](https://pyserial.readthedocs.io/en/latest/pyserial.html) v3.4
        *   [time](https://docs.python.org/3/library/time.html) v3.7
        *   [pyaudio](https://pypi.org/project/PyAudio/) v0.2.11
        *   [wave](https://docs.python.org/3/library/wave.html) v3.4
        *   [array](https://docs.python.org/3/library/array.html) v3.9
        *   [statistics](https://docs.python.org/3/library/statistics.html) v3.4
*   A LEGO SPIKE PRIME Kit [Purchase One Here.](https://education.lego.com/en-us/products/lego-education-spike-prime-set/45678#spike%E2%84%A2-prime)

    *   The LEGO SPIKE PRIME kit IDE should be downloaded to update the firmware [here](https://education.lego.com/en-us/downloads/spike-prime/software)
        *   Once the firmware is updated you can connect via Serial Communication using Putty or [this IDE](https://github.com/chrisbuerginrogers/ME35_21)

### Installing

Simply download the files in this repository and first run the code on the WIO Terminal using the Arduino IDE. Then run the SPIKE PRIME Code in REPL or the IDE that can be found here, [SPIKE PRIME IDE](https://github.com/chrisbuerginrogers/ME35_21). To run the PI code, use the command `sudo python3 knnAudio.py`. It will then ask you to record silence 5 times, and music for 5 times. The code will then run continuously.

## Authors

*   **Sawyer Bailey Paccione** - _Raspberry PI CODE, SPIKE CODE_ - [Portfolio](http://sawyerbaileypaccione.tech/)
*   **Olif Soboka Hordofa**    - _Raspberry PI CODE, SPIKE CODE_ - [Portfolio](https://olifsoboka.wixsite.com/my-site1)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/paccionesawyer/dancing-car/blob/main/LICENSE) file for details
