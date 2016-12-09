#User Guide

First, download and unzip this repository.

###Linux Users *(may work on Macs too)*

1.  `cd` into the Stock Prediction directory.
2.  Run `chmod +x install.sh run.sh` to ensure both scripts are executable.
3.  Run `bash install.sh`.
4.  Run `bash run.sh`. At this point, a browser should open. If it does not,
    you will need to:
    1.  Run `server.py` with `python server.py`.
    2.  Manually open `harambeinvestments1.html`.
5. You can use `ctrl+C` to kill the server.

###Other Operating Systems

1. You will need to manually install a few python libraries: `yahoo-finance`,
    `scipy`, `requests`, `numpy`. To install these, run:  
    `sudo pip install yahoo-finance`  
    `sudo pip install scipy`  
    `sudo pip install requests`
    `sudo pip install numpy`  
2. After you `cd` into the Stock Prediction directory, run `server.py` with
    `python server.py`
3. Open `harambeinvestments1.html` in a browser.

###Things to Consider

Over time, the accuracy of the model may decrease. If this is the case, run our
training script with `python trainParams.py`. This can take several hours to run
since it needs to load data on over a thousand stocks. For best results, run this
script after the market closes (4PM EST).

The accuracy score is printed every few thousand training iterations. When you
are satisfied with the (square-root-scaled) score (where a score of `numStocks / 2` -
105 for the default script - represents 100% accuracy - this is practically
impossible so don't wait around for this to happen), you can press `ctrl+C` to
end training.

You can run the `predictionAccuracy.py` script (with `python predictionAccuracy.py`
to get a sense of how accurate the model currently is. This script provides a percentage
accuracy. 

Due to API limitations, the app can take a few seconds to load stock data and output
a prediction. Also, we can only make a limited number of calls to the Google Trends
API in a given time frame. So after a few requests, the app will not be able to
display data for a few minutes.

Finally, due to socket limitations, once you exit stop `server.py`,
you will not be able open the app again for a few minutes.
