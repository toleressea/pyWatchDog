import datetime
import os
import zipfile
import cv2

def takeScreenshot(dir, frame):
    if not os.path.isdir(dir):
        os.mkdir(dir)

    sFilename = os.path.join(dir, datetime.datetime.now().strftime("%y%m%d_%H-%M-%S-%f") + '.png')
    cv2.imwrite(sFilename, frame)

# def zipScreenshots(screenShots, count):
#     with zipfile.ZipFile('screenshots_{0}.zip'.format(str(count)), 'w') as myzip:
#         for screenshot in screenShots:
#             myzip.write(screenshot)
#             os.remove(screenshot)