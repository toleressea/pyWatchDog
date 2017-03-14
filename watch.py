import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("--sound", type=bool, default=True, help="toggle sound on motion")
ap.add_argument("--screenshot", type=bool, default=True, help="toggle screenshot on motion")
ap.add_argument("--tone-frequency", type=int, default=40000, help="set tone frequency")
ap.add_argument("--tone-duration", type=float, default=0.1, help="set tone duration (sec)")
ap.add_argument("--ss-directory", type=str, default="screenshots", help="set screenshots subdir")
args = vars(ap.parse_args())

# default to webcam
camera = cv2.VideoCapture(0)
time.sleep(0.25)

# initialize all the things
firstFrame = None
motionCount = 0

# check arguments and import if needed
playSounds = args["sound"]
if playSounds:
    import sound

takeScreenshots = args["screenshot"]
if takeScreenshots:
    import screenshot

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    motion = False

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour and draw it on the frame
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion = True

    # draw quit instructions
    cv2.putText(frame, "Quit (Q)", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # draw countermeasures toggle state
    cv2.putText(frame, "Play Sounds (S): {0}".format(str(playSounds)), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # draw take screenshots toggle state
    cv2.putText(frame, "Take Screenshots (T): {0}".format(str(takeScreenshots)), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if motion:
        # Protect motion state against false positive by resetting base frame
        # if motion persists more than X iterations
        motionCount += 1

        # Take motion-dependent actions here
        if playSounds:
            sound.playTone(args["tone_frequency"], args["tone_duration"])

        if takeScreenshots:
            screenshot.takeScreenshot(args["ss_directory"], frame)

        if motionCount >= 25:
            firstFrame = gray
            motionCount = 0

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break
    elif key == ord("s"):
        playSounds = not playSounds
    elif key == ord("t"):
        takeScreenshots = not takeScreenshots

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()