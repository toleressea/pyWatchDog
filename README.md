# pyWatchDog
A simple script for detecting motion, saving proof, and repelling the invader

### Pre-requisites:

* Python 2.7+
* PyAudiere, whose website is defunct but you can get [here](https://web.archive.org/web/20120221041148/http://pyaudiere.org/)

### Usage:

Run the script:

    python watch.py

By default, the script will run with sound playing and screenshotting functionality turned off. The following command contains all optional commandline arguments and their default values:

    python watch.py --min-area=500 --diff-threshold=100
                    --sound --tone-frequency=40000 --tone-duration=0.1
                    --screenshot --ss-directory="screenshots"

There are also three key bindings active when the script is running:

    Q -- Quit script
    S -- Toggle sound playing when motion is detected
    T -- Toggle screenshots when motion is detected
