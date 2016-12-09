#User Guide

###Linux Users *(may work on Macs too)*

1.  First cd into the Stock Prediction directory.
2.  Run `install.sh` with `bash install.sh`
3.  Run `run.sh` with `bash run.sh`. At this point, a browser should open. If it does
    not, you will need to:
    1.  Run `server.py` with `python server.py`.
    2.  Manually open `harambeinvestments1.html`.

###Other Operating Systems

1. You will need to manually install a few python libraries: `yahoo-finance`,
    `scipy`, `requests`. To install these, run:  
    `sudo pip install yahoo-finance`  
    `sudo pip install scipy`  
    `sudo pip install requests`  
2. Run `server.py` with `python server.py`
3. Open `harambeinvestments1.html` in a browser.

###Things to Consider
Over time, the accuracy of the model may decrease. If this is the case, run our
training script with `python trainParams.py`. This can take several hours to run
since it needs to load data on over a thousand stocks. The accuracy score is printed
every few thousand training iterations. When you are satisfied with the score (a
score of 600 represents 100% accuracy - this is impossible so don't wait around for
this to happen), you can press `ctrl+C` to end training.

You can run the `predictionAccuracy.py` script (with `python predictionAccuracy.py`
to get a sense of how accurate the model currently is.
