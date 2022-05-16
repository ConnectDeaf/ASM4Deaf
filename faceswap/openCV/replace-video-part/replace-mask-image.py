#python replace-mask-image.py <full path to GIF with filename+extention> <full path to user image filename+extention> <full path to mask filename+extention> <name of output file+extension>
import sys
import cv2
import time
import numpy as np

start_time = time.time()
# Get the webcam
cap1 = cv2.VideoCapture(sys.argv[1])
frame2 = cv2.imread(sys.argv[2])
# Setup the width and the height (your cam might not support these settings)
width= int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
out= cv2.VideoWriter(sys.argv[4], cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))


# Now load the mask and create its inverse mask as well
mask = cv2.imread(sys.argv[3])
mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
mask_inv = cv2.bitwise_not(mask)

while True:
    # Capture the frames
    ret, frame1 = cap1.read()

    if ret == False:
        break

    #######match image dimensions
    #(this step is for testing; the dimensions of the 2 videos and the mask should match without resizing)
    dim = (frame1.shape[1], frame1.shape[0])
    frame2 = cv2.resize(frame2, dim, interpolation=cv2.INTER_AREA)
    mask = cv2.resize(mask, dim, interpolation=cv2.INTER_AREA)
    mask_inv = cv2.resize(mask_inv, dim, interpolation=cv2.INTER_AREA)
    #######

    # Now black-out the area to be replaced in frame1
    img1_bg = cv2.bitwise_and(frame1,frame1,mask=mask_inv)

    # Take only region of the area to be replaced from frame2.
    img2_fg = cv2.bitwise_and(frame2,frame2,mask=mask)

    # merge
    frame1 = cv2.add(img1_bg,img2_fg)
    out.write(frame1)
      
  
    #cv2.imshow('res',frame1)
    # If q is pressed terminate
    if cv2.waitKey(1) == ord('q'):
        break

# Release and destroy all windows
cap1.release()
#cap2.release()
out.release()
cv2.destroyAllWindows()


print(time.time()-start_time)