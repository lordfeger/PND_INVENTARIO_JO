from flask import Flask , render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy 


app=Flask(__name__) # para que funcione Flask en @app

#seccion y conexxion 
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///db_inventory.sqlite"
db=SQLAlchemy(app)

# App para  Flask y funcion de home y el decorador de ruta 
@app.route("/")
def home():
    inventario= Invetory.query.all()
    return render_template("home.html", inventario_html = inventario )


# creando columnas para base de datos 
class Invetory(db.Model):
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    codigo=db.Column(db.String(100))
    nombre=db.Column(db.String(100))
    stock=db.Column(db.Integer)
    status=db.Column(db.Boolean)

# creacion de base de datos 
with app.app_context():
    db.create_all()
    


# para insertar  variables a la base de datos 
@app.route("/add", methods=['POST'])
def add():
    codigo_txt = request.form.get('codigo_txt')
    nom_producto_txt = request.form.get('nom_producto_txt')
    stock_txt = request.form.get('stock_txt')
    ingreso=Invetory(codigo=codigo_txt, nombre=nom_producto_txt, stock=stock_txt, status=False)
    db.session.add(ingreso)
    db.session.commit()
    return redirect(url_for('home'))


#Elimiar -una buena practica es crear una columna y cambiar el estado de la fila -
@app.route("/eliminar/<int:selecion_id>")
def eliminar(selecion_id):
    selecion = Invetory.query.filter_by(id=selecion_id).first()
    selecion.status = not selecion.status
    db.session.commit()
    return redirect(url_for("home"))



#actualizar -dentro de db en codigo y nombre 
@app.route("/actualizar/<int:selecion_id>", methods=['POST'])
def actualizar(selecion_id):
    selecion = Invetory.query.filter_by(id=selecion_id).first()
    selecion.nombre = request.form.get('new_nom_producto_txt')
    selecion.codigo = request.form.get('new_codigo_txt')
    db.session.commit()
    return redirect(url_for("home"))



#mas 
@app.route("/mas/<int:selecion_id>")
def mas(selecion_id):
    selecion = Invetory.query.filter_by(id=selecion_id).first()
    selecion.stock = selecion.stock + 1
    
    db.session.commit()
    return redirect(url_for("home"))


#menos 
@app.route("/menos/<int:selecion_id>")
def menos(selecion_id):
    selecion = Invetory.query.filter_by(id=selecion_id).first()
    selecion.stock = selecion.stock - 1
    db.session.commit()
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)
    