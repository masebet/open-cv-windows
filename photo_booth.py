# USAGE
# python photo_booth.py --output output

# import the necessary packages
from __future__ import print_function
from pyimagesearch.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time


# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
time.sleep(2.0)


pba = PhotoBoothApp(vs)
pba.root.mainloop()