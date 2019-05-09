sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential cmake pkg-config nmap net-tools

sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get -y install libatlas-base-dev gfortran
sudo apt-get -y install libgtk2.0-dev
sudo apt-get -y install python2.7-dev python3-dev
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.1.zip
unzip opencv.zip
rm opencv.zip
cd opencv-3.4.1
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.1.zip
unzip opencv_contrib.zip
rm opencv_contrib.zip
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-3.4.1/modules -D BUILD_EXAMPLES=ON ..
make -j4
sudo make install
sudo ldconfig
sudo apt-get -y update
sudo apt-get -y install sklearn
sudo apt-get -y install imutils
sudo pip3 install -r requirements.txt
