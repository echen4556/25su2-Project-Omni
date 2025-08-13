from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint 
weapons = Blueprint('weapons', __name__)

#------------------------------------------------------------
# Get names of all weapons in a specific game
@weapons.route('/weapons/<gameID>/', methods=['GET'])
def get_weapons_by_game(gameID):
    current_app.logger.info(f'GET /weapons/{gameID} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT weaponID, name FROM weapons WHERE gameID = %s', (gameID,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Get information about a specific weapon in a specific game
@weapons.route('/weapons/<gameID>/<weaponID>', methods=['GET'])
def get_weapon(gameID, weaponID):
    current_app.logger.info(f'GET /weapons/{gameID}/{weaponID} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT weaponID, name, type FROM weapons WHERE gameID = %s AND weaponID = %s', (gameID, weaponID))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new weapon in a specific game
@weapons.route('/weapons/<gameID>/<weaponID>', methods=['POST'])
def create_weapon(gameID, weaponID):
    current_app.logger.info(f'POST /weapons/{gameID}/{weaponID} route')
    weapon_info = request.json
    name = weapon_info['name']
    w_type = weapon_info['type']
    query = 'INSERT INTO weapons (weaponID, gameID, name, type) VALUES (%s, %s, %s, %s)'
    data = (weaponID, gameID, name, w_type)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'Weapon created!', 201

#------------------------------------------------------------
# Modify the name or type of a specific weapon
@weapons.route('/weapons/<gameID>/<weaponID>', methods=['PUT'])
def update_weapon(gameID, weaponID):
    current_app.logger.info(f'PUT /weapons/{gameID}/{weaponID} route')
    weapon_info = request.json
    name = weapon_info.get('name')
    w_type = weapon_info.get('type')
    query = 'UPDATE weapons SET name = %s, type = %s WHERE gameID = %s AND weaponID = %s'
    data = (name, w_type, gameID, weaponID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'Weapon updated!'

#------------------------------------------------------------
# Remove a weapon in a specific game
@weapons.route('/weapons/<gameID>/<weaponID>', methods=['DELETE'])
def delete_weapon(gameID, weaponID):
    current_app.logger.info(f'DELETE /weapons/{gameID}/{weaponID} route')
    query = 'DELETE FROM weapons WHERE gameID = %s AND weaponID = %s'
    data = (gameID, weaponID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'Weapon deleted!'