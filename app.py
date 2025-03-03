from flask import Flask, render_template,jsonify, request,redirect,url_for
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from functools import wraps
import jwt

CLAVE_SECRETA='clavesecreta'
TIEMPO_EXPIRACION=60*60

def cookie_necesaria(f):
    @wraps(f)
    def decorada(*args,**kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            payload= jwt.decode(token,CLAVE_SECRETA,algorithms=['HS256'])
            current_user = payload.get('sub')
            if not current_user:
                return redirect(url_for('login'))
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))
        return f(current_user,*args,**kwargs)
    return decorada


#Inciamos la app de Flask
app= Flask(__name__,template_folder='templates',static_folder='static')

app.config['JWT_SECRET_KEY'] =CLAVE_SECRETA

jwt_obj = JWTManager(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
@cookie_necesaria
def dashboard(current_user):
    return render_template('dashboard.html')


#Autenticacion del usuario
@app.route('/token',methods=['POST'])
def token():
    data=  request.form
    user= data.get('username')
    passw= data.get('password')

    if user!='usuario' or passw!='password':
        return jsonify({'error':'Credenciales invalidas'}) , 401
    
    access_token = create_access_token(identity=user,expires_delta=timedelta(minutes=TIEMPO_EXPIRACION))
    response = jsonify({'message':'Login correcto'})
    response.set_cookie('token',access_token,httponly=True, secure=True)
    return response

@app.route('/logout',methods=['POST'])
def logout():
    response = jsonify({'message':'logout exitoso'})
    response.delete_cookie('token')
    return response

if __name__=='__main__':
    
    app.run(debug=True)
