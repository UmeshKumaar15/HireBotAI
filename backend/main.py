from app import app, socketio
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cheating_surveillance.main import start_video_proctoring


if __name__ == '__main__':
    socketio.run(app, debug=True)
    start_video_proctoring()