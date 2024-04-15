import logging

from src.front_end.MeowTrade import MeowTrade


# setup the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# create the app
app = MeowTrade()
app.connect("127.0.0.1", 7496, clientId=123)  # Ensure the host and port are correct
app.run()

'''
#Uncomment this section if unable to connect
#and to prevent errors on a reconnect
import time
time.sleep(2)
app.disconnect()
'''