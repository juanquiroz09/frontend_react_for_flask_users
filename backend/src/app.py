"""app"""

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonreactdb'
mongo = PyMongo(app)

CORS(app)
#CORS(app, resources={r"/users": {"origins": "http://localhost:5173"}})

users_collection = mongo.db.users

@app.route('/users/<id>', methods=['GET'])
def get_user(id): # pylint: disable=redefined-builtin
    """Obtiene un usuario por su ID"""
    try:
        user = users_collection.find_one({'_id': ObjectId(id)})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        user_data = {
            '_id': str(user['_id']),
            'name': user.get('name', 'No name'),
            'email': user.get('email', 'No email'),
            'password': user.get('password', 'No password')
        }
        return jsonify(user_data), 200
    except ValueError as e:
        print(f"Error: {e}")
        return jsonify({"error": "ID no válido"}), 400

@app.route("/users", methods=["GET"])
def get_users():
    """GET'S"""
    users = []
    for doc in users_collection.find():
        users.append({
            '_id': str(doc['_id']),
            'name': doc.get('name', 'No name'),
            'email': doc.get('email', 'No email'),
            'password': doc.get('password', 'No password')
        })
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    """CREATE"""
    data = request.json
    user = users_collection.insert_one({
        "name": data["name"], 
        "email": data["email"],
        'password': data["password"]
    }).inserted_id
    return jsonify({"id": str(user), "message": "Usuario creado"}), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id): # pylint: disable=redefined-builtin
    """Actualiza un usuario por su ID"""
    try:
        # Verificar si el ID es válido
        user_id = ObjectId(id)
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        # Realizar la actualización
        result = users_collection.update_one(
            {'_id': user_id},  # Filtro: Buscar el usuario por ID
            {'$set': {
                "name": data.get("name", ""),  # Actualiza 'name', si existe
                "email": data.get("email", ""),  # Actualiza 'email', si existe
                "password": data.get("password", "")  # Actualiza 'password', si existe
            }}
        )
        # Verificar si se encontró y actualizó un documento
        if result.matched_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200

    except ValueError as e:
        print(f"Error: {e}")
        return jsonify({"error": "ID no válido o error en la solicitud"}), 400

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id): # pylint: disable=redefined-builtin
    """Elimina un usuario por su ID"""
    try:
        # Convertir el ID a ObjectId
        user_id = ObjectId(id)
        # Eliminar el usuario con el ID proporcionado
        result = users_collection.delete_one({'_id': user_id})
        # Verificar si el usuario fue encontrado y eliminado
        if result.deleted_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200

    except ValueError as e:
        print(f"Error: {e}")
        return jsonify({"error": "ID no válido o error en la solicitud"}), 400


if __name__ == "__main__":
    app.run(debug=True)
