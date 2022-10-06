import sqlite3

def consultar_usuario(correo, password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    return cursor.fetchall()

def lista_destinatarios(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where  estado='1' and correo<>'"+correo+"'"
    cursor.execute(consulta)
    return cursor.fetchall()


def enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreusuario  from mensajeria m, usuarios u where m.origen='"+correo+"' and m.destino=u.correo"
    cursor.execute(consulta)
    return cursor.fetchall()

def recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreusuario  from mensajeria m, usuarios u where m.destino='"+correo+"' and m.origen=u.correo"
    cursor.execute(consulta)
    return cursor.fetchall()


def regisUsuario(nombe,correo, password,codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios (nombreusuario,correo,password,estado,codigoactivacion) values ('"+nombe+"','"+correo+"','"+password+"','0','"+codigo+"')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def actualziarPassW(pwd, correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set password='"+pwd+"' where correo='"+correo+"' "
    cursor.execute(consulta)
    db.commit()
    return "1"

def registroEMail(asunto,mensaje,origen,destino):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,origen,destino,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"


def activarU(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()

    consulta="select *from usuarios where codigoactivacion='"+codigo+"' and estado='1'"
    cursor.execute(consulta)
    return cursor.fetchall()

