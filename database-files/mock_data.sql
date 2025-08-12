USE OmniDatabase;
INSERT IGNORE INTO games (gameID, name) VALUES
(1, 'Valorant'),
(2, 'CS2');

INSERT IGNORE INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('KaiGhost', 0, 1, 1, 'test123');

INSERT IGNORE INTO gamesProfiles ( gameID, profileID, gameUsername, showOnDashboard) VALUES
(1, 1, 'KaiGhost', 1);

INSERT IGNORE INTO map (gameID, POIs, Name) VALUES
  (1, 'A Site,B Site,Mid', 'Ascent');

INSERT IGNORE INTO weapons (gameID, weaponType, name) VALUES
 (1, 'Rifle',  'Vandal');