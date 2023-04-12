from app import create_app
import eventlet
from eventlet import wsgi

app = create_app()

if __name__ == '__main__':
    wsgi.server(eventlet.listen(('', 5000)), app)
    # app.run(debug=True)
