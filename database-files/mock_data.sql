USE OmniDatabase;
INSERT IGNORE INTO games (gameID, name) VALUES
(1, 'Valorant'),
(2, 'CS2');

INSERT IGNORE INTO profiles (profileID, username, isAdmin, isPublic, isPremium, password) VALUES
(1, 'KaiGhost', 0, 1, 1, 'test123');