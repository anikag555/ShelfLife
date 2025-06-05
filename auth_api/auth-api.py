from flask import Flask, request, jsonify
import jwt, datetime
from functools import wraps
import logging
from logging.config import dictConfig
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'api_logs.log',
        'formatter': 'default',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
app.logger.info("Logging initialized")

def generate_token(username):
    payload = {
    'username': username,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'],
algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid or expired token!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    try:
        auth = request.get_json()
        if not auth or 'username' not in auth or 'password' not in auth:
            return jsonify({'message': 'Missing or invalid credentials'}), 400

        if auth['username'] == 'admin' and auth['password'] == 'password':
            token = generate_token(auth['username'])
            app.logger.info(f"Login success for user: {auth['username']}")
            return jsonify({'token': token})
        app.logger.warning("Login failed attempt")
        return jsonify({'message': 'Invalid credentials!'}), 403
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({'message': 'Server error'}), 500

@app.route('/secure-api', methods=['GET'])
@token_required
def secure_api():
    app.logger.info("Secure API accessed")
    return jsonify({'message': 'Secure API Access Granted!'})


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Add rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

@app.route('/rate-limited-api', methods=['GET'])
@limiter.limit("10 per minute")
def limited_route():
    return jsonify({'message': 'You are within the rate limit.'})

@app.route('/')
def home():
    return jsonify({'message': 'Auth API is running. Please use /login to get started.'})
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

