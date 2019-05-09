# Smart-Attendance-Tracker

## Code Structure

In this repository, we have two folders: attendance_tracker and dashboard. The code in attendance_tracker is meant 
to be downloaded and run on the Odroid-XU4Q board. The code in dashboard is meant to be downloaded and run on 
an AWS EC2 instance. The attendance_tracker code utilizes a webcam to take photos of students walking by and runs
these images through three computer vision models (facial detection, facial tilting, and facial recognition). Multiple
threads are utilized to make sure the preprocessing and facial recognition processes do not interrupt the image captures.
Once a student is recognized, an LED lights up notifying the student that their face was detected. Afterwards, a name.txt file 
is created with the student's name (ex: Priyank Varshney) and is sent as a POST request to our backend. The backend processes 
this data, updates the MySQL database, and displays the udpated information on the web UI. 


## Setup

To setup the Smart Attendance Tracker you will first need to purchase an Odroid-XU4Q Single Board Computer, 
a compatible webcam (check their website for a list of webcams), a USB-A hub, a USB keyboard, and a USB mouse. 

Plug in all the peripherals into the board, plug in power, and boot up the board.

Once the OS is installed, you want to git clone this repository in an easily accessible directory. 
All the dependencies needed to setup the Smart Attendance Tracker are in the installDeps.sh script and
the requirements.txt file.

To install the dependencies, run the following commands:

```
sudo chmod +x installDeps.sh
./installDeps.sh
pip3 install -r requirements.txt
```

Once that's complete, git clone this repository from Github that will allow us to access the GPIO pins on the board:
```
cd ~/Documents/
git clone https://github.com/jfath/RPi.GPIO-Odroid
```

Note: Please clone this in Documents. Otherwise, you will have to change some paths in the code. 


To setup the blinker, you will need to make the circuit located on this link: https://ibb.co/88JPtFX. The circuit requires stepping up the voltage from 1.6v(odroid output) to 5V (LED light input) in order to turn on the LED. Once the circuit is complete, change directory into the repo RPI.GPIO-Odroid and run "sudo python build clean" followed by "sudo python setup.py build" on the terminal. This will begin installing and linking the GPIO pins to python software allowing control. 


To start the facial recognition process, run 
```
./recognizeVideo.sh
```
and mount the system at an easily accessible area.

To update the model, create a folder named "dataset" in the attendance_tracker/... directory and create folders with
the naming criteria "*first name*_*Last Name*. Ex: 'Albert_Zarate'. Add photos of students in each of these folders
and make sure there are at least 15 photos of each student. Once that is complete, please run the following command:
```
./trainModel.sh
```

To setup the dashboard, create an EC2 instance on AWS and follow the following instructions to set it up: https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html. Once you've set it up, SSH into the newly 
made instance and git clone our repository. Once complete, install the dependencies using:
```
pip3 install -r requirements.txt
```
Afterwards, set up the sql tables and run the apache server using ``` sudo apachectl start ``` 

## Demo Video
Link: https://www.youtube.com/watch?v=2fnWXmVOWr8
