from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

milestones = Blueprint('milestones', __name__)

# GET all milestones for a specific profile
@milestones.route('/milestones/profile/<int:profileID>', methods=['GET'])
def get_all_milestones(profileID):
    current_app.logger.info(f'GET /milestones/profile/{profileID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM milestones
                      WHERE profileID = %s''', (profileID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

@milestones.route('/milestones/<int:profileID>', methods=['POST'])
def create_milestone(profileID):
    current_app.logger.info(f'POST /milestones/{profileID}')
    milestone_info = request.json
    milestone_name = milestone_info.get('milestoneName')
    description = milestone_info.get('description')
    due_date = milestone_info.get('dueDate', None)

    if not milestone_name:
        return jsonify({"error": "Milestone name is required"}), 400

    query = '''INSERT INTO milestones (profileID, milestoneName, description, dueDate)
               VALUES (%s, %s, %s, %s)'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (profileID, milestone_name, description, due_date))
    db.get_db().commit()
    return jsonify({"message": "Milestone created!"}), 201

# GET details for a specific milestone
@milestones.route('/milestones/<int:profileID>/<int:milestoneID>', methods=['GET'])
def get_milestone_details(profileID, milestoneID):
    current_app.logger.info(f'GET /milestones/{profileID}/{milestoneID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM milestones
                      WHERE profileID = %s AND milestoneID = %s''',
                   (profileID, milestoneID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# PUT update details for a specific milestone
@milestones.route('/milestones/<int:profileID>/<int:milestoneID>', methods=['PUT'])
def update_milestone(profileID, milestoneID):
    current_app.logger.info(f'PUT /milestones/{profileID}/{milestoneID}')
    milestone_info = request.json
    milestone_name = milestone_info.get('milestoneName')
    description = milestone_info.get('description')
    due_date = milestone_info.get('dueDate')
    query = '''UPDATE milestones
               SET milestoneName = %s, description = %s, dueDate = %s
               WHERE profileID = %s AND milestoneID = %s'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (milestone_name, description, due_date, profileID, milestoneID))
    db.get_db().commit()
    return 'Milestone updated!', 200

# DELETE a specific milestone
@milestones.route('/milestones/<int:profileID>/<int:milestoneID>', methods=['DELETE'])
def delete_milestone(profileID, milestoneID):
    current_app.logger.info(f'DELETE /milestones/{profileID}/{milestoneID}')
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM milestones
                      WHERE profileID = %s AND milestoneID = %s''',
                   (profileID, milestoneID))
    db.get_db().commit()
    return 'Milestone deleted!', 200
