from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
import jwt 
from functools import wraps
from __init__ import app    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers
        token = auth.get('x-access-token') 

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is missing or invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def create_token(userid):
    token = jwt.encode({'user_id': userid, 'exp': datetime.utcnow() + timedelta(minutes=50) }, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})

def plaintxt(token):
    result = jwt.decode(token, app.config['SECRET_KEY'])
    return result
