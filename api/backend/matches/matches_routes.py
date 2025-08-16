from flask import Blueprint, jsonify, make_response, current_app
from backend.db_connection import db
# Import the dictionary cursor
from pymysql.cursors import DictCursor

# Create a new blueprint for match-related routes
matches_bp = Blueprint('matches_bp', __name__)

# This route gets all match history for a SPECIFIC USER across all games
@matches_bp.route('/profile/<int:profileID>', methods=['GET'])
def get_all_match_history_for_user(profileID):
    current_app.logger.info(f'GET /matches/profile/{profileID}')
    cursor = db.get_db().cursor(cursor=DictCursor)

    # This query joins all necessary tables to gather full match details for one user
    query = '''
        SELECT
            m.matchID,
            m.matchDate,
            m.matchType,
            m.lobbyRank,
            g.name AS gameName,
            `map`.Name AS mapName,
            ms.kills,
            ms.deaths,
            ms.assists,
            ms.Headshots AS headshots,
            ms.damageDealt AS damage,
            ms.rounds,
            ms.matchDuration,
            ms.win
        FROM matchStats ms
        JOIN gamesProfiles gp ON ms.gameInstanceID = gp.gameInstanceID
        JOIN matches m ON ms.matchID = m.matchID
        JOIN `map` ON m.mapID = `map`.mapID
        JOIN games g ON m.gameID = g.gameID
        WHERE
            gp.profileID = %s
        ORDER BY
            m.matchDate DESC;
    '''

    try:
        cursor.execute(query, (profileID,))
        data = cursor.fetchall()
        return make_response(jsonify(data), 200)
    except Exception as e:
        current_app.logger.error(f"Error fetching user match history: {e}")
        return make_response(jsonify({"error": "Failed to fetch user match history"}), 500)
