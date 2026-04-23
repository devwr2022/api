from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# 🔌 Conexión segura
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tu_base"
    )

# 🚀 Inicializar si está vacío
def inicializar_datos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            cursor.execute("""
                INSERT INTO usuarios 
                (nombre, apellido, dni, telefono, direccion_postal, dias_licencia)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ("Default", "User", "00000000", "0000000000", "Sin direccion", 0))

            conn.commit()

    except Exception as e:
        print("Error inicializando:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 📄 Obtener todos
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios")
        resultados = cursor.fetchall()

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 🔍 Obtener por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(usuario)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ➕ Crear usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json or {}

    nombre = data.get('nombre', 'Sin nombre')
    apellido = data.get('apellido', 'Sin apellido')
    dni = data.get('dni', '0')
    telefono = data.get('telefono', 'No informado')
    direccion = data.get('direccion_postal', 'No informada')
    dias = data.get('dias_licencia', 0)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuarios (nombre, apellido, dni, telefono, direccion_postal, dias_licencia)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, apellido, dni, telefono, direccion, dias))
        conn.commit()

        return jsonify({
            "id": cursor.lastrowid,
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "telefono": telefono,
            "direccion_postal": direccion,
            "dias_licencia": dias
        }), 201

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ✏️ Actualizar
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.json or {}

    nombre = data.get('nombre', 'Sin nombre')
    apellido = data.get('apellido', 'Sin apellido')
    dni = data.get('dni', '0')
    telefono = data.get('telefono', 'No informado')
    direccion = data.get('direccion_postal', 'No informada')
    dias = data.get('dias_licencia', 0)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE usuarios 
        SET nombre=%s, apellido=%s, dni=%s, telefono=%s, direccion_postal=%s, dias_licencia=%s
        WHERE id=%s
        """

        cursor.execute(sql, (nombre, apellido, dni, telefono, direccion, dias, id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"mensaje": "Usuario actualizado"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ❌ Eliminar
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"mensaje": "Usuario eliminado"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ▶️ Ejecutar
if __name__ == '__main__':
    inicializar_datos()
    app.run(debug=True)