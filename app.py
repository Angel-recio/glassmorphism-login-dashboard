from flask import Flask , jsonify , request , render_template,redirect,url_for
from pymongo import MongoClient
from flask import session



app = Flask(__name__)

app.secret_key = 'huemac123'


# Conexión a la base de datos y colección
def conectar_mongodb(coleccion_nombre):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['prueba']
    coleccion = db[coleccion_nombre]
    return coleccion

# Conectar antes de iniciar la aplicación Flask
coleccion_login = conectar_mongodb('login')
coleccion_registro = conectar_mongodb('registro')



@app.route('/')
def index():
    if 'usuario' in session:
        return render_template('principal.html')
    else:
        return render_template('index.html')

@app.route('/registro')
def registrar():
    return render_template('registro.html')

@app.route('/principal')
def principal1():
    return render_template('principal.html')

@app.route('/registrar' , methods=['POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        contra = request.form['contra']
        

        usuario_nuevo = {
            "usuario": usuario,
            "correo": correo,
            "contra": contra
        }
        coleccion_registro.insert_one(usuario_nuevo)

    
        return redirect(url_for('index'))
    else:
        return  redirect(url_for('registrar'))
    
@app.route('/iniciar_sesion', methods=['GET' , 'POST'])
def iniciar_sesion1():
    if request.method =='POST' :
        usuario = request.form['usuario']
        contra = request.form['contra']

        usuario_query = coleccion_registro.find_one({"usuario": usuario , "contra":contra})
        if usuario_query:
            session['usuario'] = usuario
            return redirect(url_for('principal1'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
    


if __name__ == "__main__":
    app.run(debug=True,port=4231)