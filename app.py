from flask import Flask, render_template, request
import hashlib  # Esta libreria permite encriptar una contrasena
import controlador # importamos el archivo con la logica para acceder a la BBDD
from datetime import datetime # Libreria de fecha y hora para crear
import envioemail # importamos archivo con la logica de envio de correo

app = Flask(__name__)
origen="" # aqui almacenaremos el correo de origen

@app.route("/")
def inicio():
    return render_template("login.html")

# Esta ruta recibe ambos metodos del formulario desde donde validadmos la info
@app.route("/verificarUsuario",methods=["GET","POST"]) # usamos el mismo nombre de la ruta en la funcion para evitar confuciones
def verificarUsuario():
    if request.method=="POST":
        correo=request.form["txtusuario"]
        correo=correo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")
        password=request.form["txtpass"]
        password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

        password2=password.encode() # codificamos para luego encriptar
        password2=hashlib.sha384(password2).hexdigest() # una vez codificado lo encriptamos y alamacenamos nuevamente en la misma variable

        global origen # dentro de la funcion indicamos que esta variable es global
        # Enviamos los dos parametros del formulario a controlador.py se conecta a la BBDD, recibe las cabeceras, crea una consulta SQL, la ejecuta y devuelve el resultado
        respuesta=controlador.consultar_usuario(correo, password2)

        if len(respuesta)==0: # evaluamos la respuesta de la BBDD. Si es vacia
            origen=""
            mensajes= "Error de autenticacion, veririfique su usuario y contraseña."
            return render_template("informacion.html",data=mensajes)

        else: # Si existe lo llevara a principal.html
            origen=correo
            resp2=controlador.lista_destinatarios(correo)
            return render_template("principal.html",listaD=resp2,usuario=respuesta)

@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"] # requerimos la informacion del id txtnombre y la almacenamos en una variable
        nombre=nombre.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

        correo=request.form["txtusuarioregistro"]
        correo=correo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

        password=request.form["txtpassregistro"]
        password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

        password2=password.encode()
        password2=hashlib.sha384(password2).hexdigest()

        codigo=datetime.now() # la funcion now trae la fecha actual
        codigo2=str(codigo) # lo convertimos a string para poder manipularlo
        codigo2=codigo2.replace("-","") # remplazamos los simbolos
        codigo2=codigo2.replace(":","") # quedandonos solo con los numeros
        codigo2=codigo2.replace(".","") # para crear un codigo de activacion unico
        codigo2=codigo2.replace(" ","") # y lo alamecenamos en la misma variable

        resp_re=controlador.regisUsuario(nombre,correo,password2,codigo2) # agregamos el codigo2 al controlador

        if resp_re=="1":
            asunto="Codigo de activacion"
            mensaje="Sr "+nombre+" su codigo de activacion es "+codigo2+" recuerde copiarlo y pegarlo para validar usuario";
            resp_correo=envioemail.enviar(correo,asunto,mensaje)
            if(resp_correo=="1"):
                mensajes= "Usuario registrado satisfactoriamente 😎"
            else:
                mensajes="Usuario Registrado con Exito, Email no enviado, servicio no disponible, utiliza el siguiente codigo de activacion="+codigo2
        else:
            mensajes="ERROR, no es posible realizar el registro, el Usuario y/o Correo ya existe."

        return render_template("informacion.html",data=mensajes)

@app.route("/ActivarUsuario",methods=["GET","POST"])
def ActivarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

        respuesta=controlador.activarUsuario(codigo) # procedimiento de activacion
        if len(respuesta)==0: #  Evaluamos el codigo de activacion
            mensajes= "El codigo es incorrecto"
            return render_template("informacion.html",data=mensajes)
        else:
            mensajes= "Usuario Activado Satisfactoriamente"
            return render_template("informacion.html",data=mensajes)

@app.route("/enviarEE",methods=["GET","POST"])
def enviarEE():

    asunto=request.form["asunto"]
    asunto=asunto.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

    mensaje=request.form["mensaje"]
    mensaje=mensaje.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

    destino=request.form["destino"]
    destino=destino.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

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
    return render_template("historial2.html",listaCorreos=respuesta)

@app.route("/actualizarPa",methods=["GET","POST"])
def actualizarPa():
    password=request.form["password"]
    password=password.replace("''","=====89988====73828ssss==").replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("DROP","").replace("select","").replace("insert","").replace("update","").replace("delete","").replace("drop","")

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    controlador.actualziarPassW(password2,origen)

    return "La contraseña se ha actualizado correctamente"
