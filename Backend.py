from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

from src.front_end.MeowTrade import MeowTrade

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # HTML file to display the data

def send_market_data(tradetron):
    while True:
        socketio.sleep(1)  # Emit data every second
        if tradetron.market_data:
            socketio.emit('newdata', {'price': tradetron.market_data[1]})

if __name__ == '__main__':
    tt = MeowTrade()
    thread = threading.Thread(target=tt.setup_connection)
    thread.start()
    socketio.run(app, debug=True)
