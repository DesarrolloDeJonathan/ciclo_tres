from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)
origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verifciarUsuario",methods=["GET","POST"])
def verifciarUsuario():

    correo=request.form["txtusuario"]
    password=request.form["txtpass"]

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    global origen

    respuesta=controlador.consultar_usuario(correo, password2)

    if len(respuesta)==0:
       origen=""
       mensajes= "Error de autenticacion, veririfique su usuario y contraseña."
       return render_template("informacion.html",data=mensajes)

    else:
        origen=correo
        resp2=controlador.lista_destinatarios(correo)
        return render_template("principal.html",listaD=resp2,usuario=respuesta)



@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():

    nombre=request.form["txtnombre"]
    correo=request.form["txtusuarioregistro"]
    password=request.form["txtpassregistro"]

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    codigo=datetime.now()
    codigo2=str(codigo)
    codigo2=codigo2.replace("-","")
    codigo2=codigo2.replace(":","")
    codigo2=codigo2.replace(".","")
    codigo2=codigo2.replace(" ","")

    controlador.regisUsuario(nombre,correo,password2,codigo2)

    asunto="Codigo de activacion"
    mensaje="su codigo de activacion es "+codigo2;
    envioemail.enviar(correo,asunto,mensaje)

    mensajes= "Usuario registrado satisfactoriamente..."
    return render_template("informacion.html",data=mensajes)


@app.route("/ActivarUsuario",methods=["GET","POST"])
def ActivarUsuario():

    codigo=request.form["txtcodigo"]

    respuesta=controlador.activarU(codigo)
    if len(respuesta)==0:
        mensajes= "El codigo es incorrecto"
        return render_template("informacion.html",data=mensajes)
    else:
        mensajes= "Usuario Activado con EXITO"
        return render_template("informacion.html",data=mensajes)


@app.route("/enviarEE",methods=["GET","POST"])
def enviarEE():

    asunto=request.form["asunto"]
    mensaje=request.form["mensaje"]
    destino=request.form["destino"]

    controlador.registroEMail(asunto,mensaje,origen,destino)

    asunto2="Nuevo Mensaje"
    mensaje2="Usted recibio un nuevo mensaje por favor ingrese a la plataforma para observarlo."

    envioemail.enviar(destino,asunto2,mensaje2)

    return "Email Enviado Satisfactoriamente"


@app.route("/correosEnviados",methods=["GET","POST"])
def correosEnviados():

    respuesta=controlador.enviados(origen)
    return render_template("historial.html",listaCorreos=respuesta)



@app.route("/correosRecibidos",methods=["GET","POST"])
def correosRecibidos():

    respuesta=controlador.recibidos(origen)
    return render_template("historial.html",listaCorreos=respuesta)


@app.route("/actualizarPa",methods=["GET","POST"])
def actualizarPa():
    password=request.form["password"]

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    controlador.actualziarPassW(password2,origen)

    return "La contraseña se ha actualizado correctamente"
