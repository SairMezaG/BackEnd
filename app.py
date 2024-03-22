from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename #Esto es para darle seguridad a las imagenes(Debo consultar a fondo cuando y como se usa)
from flask import session  #Esto es para el inicio y cierre de sesiones(investigar al respecto)
from functools import wraps #Esto es para impedir que se vaya a las rutas desde la barra de busqueda


app = Flask(__name__)
app.secret_key = 'Mi_clave_secreta_LexIsa2211'

#Esta es la parte del codigo para hacer la conexion a MongoDB
mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client['GESTIONPRODUCTOS']
usuarios = db['usuarios']
productos = db['productos']
categoria = db['categoria']


#Esta es la ruta principal de la aplicacion
@app.route('/')
def index():
    return render_template("loginIngreso.html") #Renderizamos al login de ingreso


def login_required(f): #Esta funcion es para que no se pueda acceder desde la barra de búsqueda(Debo investigar sobre esto)
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta protegida que requiere inicio de sesión
@app.route('/agregarProducto', methods=['GET', 'POST'])
@login_required
def agregarProducto():
    if request.method == 'POST':
        # Lógica para agregar producto
        return redirect(url_for('agregarProducto'))  # Redirigir a la misma página después de agregar el producto
    else:
        # Obtener los productos de la base de datos
        productos = db['productos'].find()
        return render_template('agregarProducto.html', productos=productos)
    
    

    

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        user = usuarios.find_one({'usuario': usuario, 'contrasenia': contrasenia})
        if user:
            session['usuario'] = usuario  # Iniciar sesión para el usuario
            return redirect(url_for('agregarProducto'))  # Redirigir a la página de agregar producto después del inicio de sesión
        else:
            mensajeDeError = "Usuario o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('loginIngreso.html', mensajeDeError=mensajeDeError)
    return render_template('loginIngreso.html')

@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    # Redirigir al formulario de inicio de sesión
    return redirect(url_for('login'))

#Esta es la ruta para el login
""" @app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        user = usuarios.find_one({'usuario': usuario, 'contrasenia': contrasenia})
        if user:
            return redirect(url_for('agregarProducto')) # Renderizamos a la funcion agregarProducto
        else:
            # Si los datos son incorrectos, renderiza el formulario de inicio de sesión nuevamente
            mensajeDeError = "Usuario o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('loginIngreso.html' , mensajeDeError = mensajeDeError)
    # Si la solicitud es GET, simplemente renderiza el formulario de inicio de sesión
    return render_template('loginIngreso.html')
 """




""" @app.route('/agregarProducto', methods=['GET', 'POST']) #Esta es la parte de Crear (CREATE) del CRUD
def agregarProducto():
    if request.method == 'POST':
       
        return redirect(url_for('agregarProducto'))
    else:
        # Obtener los productos de la base de datos
        productos = db['productos'].find()  # Aquí obtenemos todos los productos
        # Renderizar la plantilla y pasar los productos como contexto
        return render_template('agregarProducto.html', productos=productos)
 
 
         """
  #Este codigo era para cuando no se había hecho la verificacion de si un producto ya existe      
""" @app.route('/guardarProducto', methods=['POST'])
def guardarProducto():
    if request.method == 'POST':
        
        # Obtenemos los datos del formulario
        id_producto = request.form['id'] #Estos son los name del formulario
        nombre = request.form['nombre']  #"                                "
        precio = request.form['precio']  #"                                "
        categoria = request.form['categoria'] #"                                "

        foto = request.files['foto'] #"                                "
        if foto:
            ruta_archivo = '/static/imagenes/' + secure_filename(foto.filename)
        else:
            ruta_archivo = None  

        # Guardar los datos en la base de datos
        productos = db['productos']
        productos.insert_one({
            'id': id_producto,
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria,
            'foto': ruta_archivo  
        })

       
        return redirect(url_for('agregarProducto')) #Para que siga en el formulario para agregar mas productos
         """
         
        
@app.route('/guardarProducto', methods=['POST'])
@login_required
def guardarProducto():
    if request.method == 'POST': 
        id_producto = request.form['id']       #Esto es del campo "name" de los input
        nombre = request.form['nombre']        #Esto es del campo "name" de los input
        precio = request.form['precio']        #Esto es del campo "name" de los input
        categoria = request.form['categoria']  #Esto es del campo "name" de los input
        
        foto = request.files['foto']           #Esto es del campo "name" de los input
        if foto:
            ruta_archivo = '/static/imagenes/' + secure_filename(foto.filename)
        else:
            ruta_archivo = None  

        # Aquí hacemos la validación de si un producto ya existe por su id
        productos = db['productos']
        producto_existente = productos.find_one({'id': id_producto})

        if producto_existente:
            mensaje_error = f"El producto con el ID {id_producto} ya existe. Por favor, ingresa un ID único."
            # Obtener los productos de la base de datos
            productos = db['productos'].find()
            # Renderizar la plantilla con el mensaje de error como una variable de contexto
            return render_template('agregarProducto.html', productos=productos, mensaje_error=mensaje_error)

        # Guardar los datos en la base de datos
        productos.insert_one({
            'id': id_producto,
            'nombre': nombre,
            'precio': precio,
            'categoria': categoria,
            'foto': ruta_archivo  
        })

    # Si el producto se guardó correctamente o si el formulario no se ha enviado todavía, redirigimos a la página de agregarProducto
    return redirect(url_for('agregarProducto'))




            
@app.route('/actualizarProducto/<id>', methods=['GET', 'POST']) #Esta es la parte de Actualizar (UPDATE) del CRUD
@login_required
def actualizarProducto(id):
    if request.method == 'POST':
        # Procesar los datos enviados desde el formulario de actualización
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        
        # Actualizar los datos del producto en la base de datos
        result = db['productos'].update_one({'id': id}, {'$set': {'nombre': nombre, 'precio': precio, 'categoria': categoria}})
        
        # Verificar si se actualizó correctamente
        if result.modified_count > 0:
            # Con esto nos regidirimos a la página agregarProducto.html después de actualizar el producto
            return redirect(url_for('agregarProducto'))
        else:
            
            return "Producto no encontrado", 404
    
    
    producto = db['productos'].find_one({'id': id})
    return render_template('actualizarProducto.html', producto=producto) 

""" @app.route('/consultarProducto', methods=['POST'])
@login_required
def consultarProducto():
    id_producto = request.form['id_producto']
    producto = db['productos'].find_one({'id': id_producto})
    mensaje = ""
    if producto:
        mensaje = f"El producto con el ID {id_producto} existe en la base de datos."
    else:
        mensaje = f"No se encontró ningún producto con el ID {id_producto}."
    return render_template('agregarProducto.html', mensaje=mensaje) """

@app.route('/consultarProducto', methods=['POST'])
@login_required
def consultarProducto():
    id_producto = request.form['id_producto']
    producto = productos.find_one({'id': id_producto})
    if producto:
        mensaje = f"El producto con el ID {id_producto} existe en la base de datos."
    else:
        mensaje_error = f"No se encontró ningún producto con el ID {id_producto}."
        return redirect(url_for('mostrar_mensaje', mensaje=mensaje_error))
    return redirect(url_for('mostrar_mensaje', mensaje=mensaje))


@app.route('/mensajeConsulta')
@login_required
def mostrar_mensaje():
    mensaje = request.args.get('mensaje')
    return render_template('mensajeConsulta.html', mensaje=mensaje)





@app.route('/eliminarProducto', methods=['POST']) #Esta es la parte de Eliminar (DELETTE) del CRUD
@login_required
def eliminarProducto():
    id_producto = request.form['id']
    # Busca el producto por su ID y lo elimina de la base de datos
    productos.delete_one({'id': id_producto})
    # Redirige de nuevo a la página de agregarProducto
    return redirect(url_for('agregarProducto'))









if __name__ == "__main__":
    app.run(port=3000, debug=True)

