
V4L2LOOPBACK_VER = $(shell \
	apt-cache policy v4l2loopback-dkms | sed -n 2p | cut -d" " -f 4)

VID_WIDTH  = 640
VID_HEIGHT = 480


all: $(TARGET)

setup-devices:
	@echo "- Using v4l2loopback version: $(V4L2LOOPBACK_VER)"
	@echo "- Inserting module..."
	@if (lsmod | grep v4l2loopback > /dev/null); then sudo rmmod v4l2loopback; fi
	@sudo modprobe v4l2loopback \
		devices=2 exclusive_caps=1,1 video_nr=5,6 \
	    card_label="Gst VideoTest","OpenCV Camera"
	@sleep 1
	@echo "- Ready. Available devices:\n"
	@v4l2-ctl --list-devices -d5

start-gst-camera:
	gst-launch-1.0 videotestsrc ! v4l2sink device=/dev/video5

start-opencv-cam:
	./virtual-cam.py 

open-gst-sink:
	gst-launch-1.0 v4l2src device=/dev/video6 ! videoconvert ! xvimagesink

open-vlc-sink:
	vlc v4l2:///dev/video6

run:
	./virtual-cam.py s
	sleep 3
	#vlc v4l2:///dev/video6


# another helper rules
install-deps:
	sudo apt install \
	   v4l2loopback-dkms \
       v4l2loopback-utils \
       gstreamer1.0-tools \
	   gstreamer1.0-plugins-good \
	   libopencv-dev \
	   build-essential
	@echo "\n\nNOTE: you may need to also install vlc, chromium, "
	@echo "      google-chrome and/or cheese."

