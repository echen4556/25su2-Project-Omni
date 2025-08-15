from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import db  

matches_bp = Blueprint('matches', __name__)

# Get ALL matches for a specific profile + gameInstance with optional filters
@matches_bp.route('/profile/<int:profile_id>/games/<int:game_instance_id>/matches', methods=['GET'])
def get_all_matches(profile_id, game_instance_id):
    """
    Returns all matches for a given profile and game instance.
    Supports optional filtering via query params: matchType, rank, startDate, endDate.
    """
    try:
        cursor = db.get_db().cursor(dictionary=True)

        # Base query
        query = """
        SELECT m.matchID, m.matchDate, m.matchType, m.lobbyRank, mp.Name AS mapName
        FROM matches m
        JOIN matchStats ms ON m.matchID = ms.matchID
        JOIN map mp ON m.mapID = mp.mapID
        WHERE ms.gameInstanceID = %s
        """
        params = [game_instance_id]

        # Optional filters
        match_type = request.args.get('matchType')
        rank = request.args.get('rank')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')

        if match_type:
            query += " AND m.matchType = %s"
            params.append(match_type)

        if rank:
            query += " AND m.lobbyRank = %s"
            params.append(rank)

        if start_date:
            query += " AND m.matchDate >= %s"
            params.append(start_date)

        if end_date:
            query += " AND m.matchDate <= %s"
            params.append(end_date)

        query += " ORDER BY m.matchDate DESC"

        cursor.execute(query, tuple(params))
        matches = cursor.fetchall()

        return jsonify(matches), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching matches: {e}")
        return jsonify({"error": str(e)}), 500


# Get DETAILS for a specific match for a profile
@matches_bp.route('/matches/<int:match_id>/<int:profile_id>', methods=['GET'])
def get_match_details(match_id, profile_id):
    """
    Returns detailed stats for a given match for a specific profile.
    """
    try:
        cursor = db.get_db().cursor(dictionary=True)

        query = """
        SELECT ms.kills, ms.deaths, ms.assists, ms.Headshots AS headshots, 
               ms.damageDealt AS damage, ms.TotalShots, ms.shotsHit, 
               ms.matchDuration, ms.rounds, ms.win, ms.firstBloods
        FROM matchStats ms
        JOIN gamesProfiles gp ON ms.gameInstanceID = gp.gameInstanceID
        WHERE ms.matchID = %s AND gp.profileID = %s
        """
        cursor.execute(query, (match_id, profile_id))
        details = cursor.fetchone()

        if details:
            return jsonify(details), 200
        else:
            return jsonify({"message": "No stats found for this match/profile"}), 404

    except Exception as e:
        current_app.logger.error(f"Error fetching match details: {e}")
        return jsonify({"error": str(e)}), 500
