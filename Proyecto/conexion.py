import mysql.connector

conexión =mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "",
    database= ""
)

if conexión.is_connected():
    print(f"conexion exitosa a:{database}")
else:
    print(f"no se pudo conectar")