# Environment setup
Go to [this website](http://interactivebrokers.github.io/) and download the latest
version of the TWS API (it was call IB API) in earlier versions.
Once downloaded, navigate to /twsapi_macunix.976.01/IBJts/source/pythonclient (your version number
might be different), and 
run `python3 setup.py install` to install the package. Note that if you are working with venv,
you must activate the venv before running the install, otherwise the package will be installed
to the base interpreter.

# Client port
Download the trader client, I prefer to use [TWS](https://www.interactivebrokers.com/en/index.php?f=16042)
Once logged in, go to Edit/Files – Global Configuration – API – Settings

Socket port is 7496.