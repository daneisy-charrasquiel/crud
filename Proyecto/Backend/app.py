from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql 
import bcrypt
from flasgger import Swagger 


app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
#Conexión a la base de datos 
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql .connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset= "utf8mb4" )
    return conn

# Ruta para la consulta general 
@app.route("/", methods= ["GET"])
def consulta_general():
    """
    consulta general del baúl de contraseña 
    ---
    responses:
        200:
            description: Lista de resgistro 
    """
    try: 
        conn = conectar("localhost", "root", "1234", "gestor_contrasena")
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            dato = { "id_baul": row [0], "Plataforma": row[1], "Usuario": row[2]}
            data.append(dato)
            cur.close()
            conn.close()
            return jsonify({"baul": data, "mensaje": "Baúl de contraseñas"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": "Error"})

#Ruta para consulta individual 
@app.route("/consulta_individual/<codigo>", methods=["GET"])
def consulta_individual(codigo):
    """
    Consulta individual por ID
    ---
    paramenters:
        - name:codigo
        in: path
        required: true 
        type: integer 
    responses:
        200:
            description: Registro encontrado
    """
    try:
        conn = conectar("localhost", "root", "1234","gestor_contrasena")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM baul WHERE id_baul = {codigo}") # SI algo faltan otras comillas 
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {"id_baul": datos[0], "Plataforma": datos[1], "Usuario": datos[2], "clave": datos[3]}
            return jsonify({"baul": dato, "mensaje": "Registro no encontrado"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": "Error"})


#Ruta para registro
@app.route("/registro/", methods=["POST"])
def registro():
    """
    Registrar nueva contraseña
    ---
    parameters:
        - name: body
        in: body
        requerid: true
        schema: 
            type: object 
            properties:
                plataforma:
                    type: string 
                usuario: 
                    type: string
                clave:
                    type: string
    responses:
        200:
          description: Registro agregado

    """
     # schane: lenguaje estructurado de datos que define entidades, acciones y relaciones en Internet
    try:
        data = request.get_json()
        plataforma = data["plataforma"]
        usuario = data["usuario"]
        clave = bcrypt.hashpw(data["clave"].encode("utf-8"), bcrypt.gensalt()) .decode("utf-8")
        
        conn = conectar("localhost", "root", "1234", "gestor_contrasena")
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s,%s,%s)",
                    (plataforma, usuario, clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Registro agregado"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": "Error"})


#Ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods=["DELETE"])
def eliminar(codigo):
    """
    Eliminar registro por ID
    ---
    parameters:
        - name: codigo
        in: path
        required: true
        type: integer
    resposes:
        200:
            descption: Registro eliminado 
    """
    try:
        conn = conectar("localhost","root", "1234", "gestor_contrasena")
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s",(codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Eliminado"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": "Error"})


#Ruta para actualizar registro 
@app.route("/actualizar/<codigo>", methods=["PUT"])
def actualizar(codigo):
    """
    Actualizar regidtro de ID 
    ---
    parameters:
        - name: codigo 
            in: path 
            required: true 
            schema:
            type: object 
                properties:
                    plataforma:
                        type: string
                    usuario:
                        type: string
                    clave: 
                        type: string 
    responses:
        200:
            description: Registro actualizado
    """
    try: 
        data = request.get_json()
        plataforma = data["plataforma"]
        usuario = data["usuario"]
        clave= bcrypt.hashpw(data["clave"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        conn = conectar("localhost", "root", "1234", "gestor_contrasena")
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id baul = %s", (plataforma, usuario, clave, codigo))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensaje": "Registro actualizado"})
    except Exception as ex:
        print(ex)
        return jsonify({"mensaje": "Error"})

if __name__== "__main__":
    app.run(debug=True)
