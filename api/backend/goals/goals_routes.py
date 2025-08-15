from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import db
import pymysql.cursors
from datetime import datetime

goals_bp = Blueprint('goals', __name__)

# ------------------------ GET all goals for a game ------------------------
@goals_bp.route('/goals/game/<int:gameID>', methods=['GET'])
def get_goals(gameID):
    current_app.logger.info(f'GET /goals/game/{gameID}')
    conn = db.get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM goals WHERE gameID = %s ORDER BY goalsID', (gameID,))
    data = cursor.fetchall()
    return jsonify(data), 200

# ------------------------ GET one goal by ID ------------------------
@goals_bp.route('/goals/<int:goalID>', methods=['GET'])
def get_goal(goalID):
    current_app.logger.info(f'GET /goals/{goalID}')
    conn = db.get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM goals WHERE goalsID = %s', (goalID,))
    data = cursor.fetchone()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Goal not found"}), 404

# ------------------------ POST create a new goal ------------------------
@goals_bp.route('/goals', methods=['POST'])
def create_goal():
    current_app.logger.info('POST /goals')
    info = request.json
    description = info.get('description')
    gameID = info.get('gameID')

    if not description or not gameID:
        return jsonify({"error": "Missing description or gameID"}), 400

    dateCreated = datetime.now()
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO goals (gameID, dateCreated, description) VALUES (%s, %s, %s)',
        (gameID, dateCreated, description)
    )
    conn.commit()
    return jsonify({"message": "Goal created!"}), 201

# ------------------------ PUT update a goal ------------------------
@goals_bp.route('/goals/<int:goalID>', methods=['PUT'])
def update_goal(goalID):
    current_app.logger.info(f'PUT /goals/{goalID}')
    info = request.json
    description = info.get('description')
    dateAchieved = info.get('dateAchieved')  # optional

    if not description:
        return jsonify({"error": "Missing description"}), 400

    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE goals SET description = %s, dateAchieved = %s WHERE goalsID = %s',
        (description, dateAchieved, goalID)
    )
    conn.commit()
    return jsonify({"message": "Goal updated!"}), 200

# ------------------------ DELETE a goal ------------------------
@goals_bp.route('/goals/<int:goalID>', methods=['DELETE'])
def delete_goal(goalID):
    current_app.logger.info(f'DELETE /goals/{goalID}')
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM goals WHERE goalsID = %s', (goalID,))
    conn.commit()
    return jsonify({"message": "Goal deleted!"}), 200
