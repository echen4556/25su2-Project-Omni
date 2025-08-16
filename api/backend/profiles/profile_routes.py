from flask import Blueprint, jsonify, current_app
from backend.db_connection import db
import pymysql.cursors

profiles = Blueprint('profiles', __name__)

# GET all profiles
@profiles.route('/profiles', methods=['GET'])
def get_profiles():
    current_app.logger.info('GET /profiles')
    cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT profileID, username, isAdmin, isPublic, isPremium FROM profiles ORDER BY profileID')
    rows = cursor.fetchall()
    return jsonify(rows), 200

# GET single profile
@profiles.route('/profiles/<int:profileID>', methods=['GET'])
def get_profile(profileID):
    current_app.logger.info(f'GET /profiles/{profileID}')
    cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT profileID, username, isAdmin, isPublic, isPremium FROM profiles WHERE profileID=%s', (profileID,))
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'profile not found'}), 404
    return jsonify(row), 200

# -------------------------------
# GET games for a profile
# -------------------------------
@profiles.route('/profiles/<int:profileID>/games', methods=['GET'])
def get_user_games_route(profileID):
    current_app.logger.info(f'GET /profiles/{profileID}/games')
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT t2.gameID, t2.name FROM gamesProfiles t1 JOIN games t2 ON t1.gameID = t2.gameID WHERE t1.profileID = %s',
        (profileID,)
    )
    rows = cursor.fetchall()
    columns = ['gameID', 'name']
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data), 200
