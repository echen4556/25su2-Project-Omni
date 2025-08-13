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

INSERT IGNORE INTO matches (gameID, mapID, matchDate, matchType, lobbyRank)
VALUES
(1, 1, '2025-08-01 18:30:00','Ranked', 'Immortal');

INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots,shotsHit, matchDuration, rounds, win, damageDealt,firstBloods)
VALUES
(1, 1, 22, 15, 5, 12, 300, 129, 2100, 16, 1, 10370, 2); 

INSERT INTO playerStats
(gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins)
VALUES
(1, 258, 191, 72, 33850, 132, 1082, 34);

INSERT IGNORE INTO weaponStats
(statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought)
VALUES
(1, 1, 4.000, 180, 0.520, 150),
(2, 2, 2.000,  78, 0.470,  46);

INSERT IGNORE INTO mapStats
(statTableID, gameID, weaponType, name)
VALUES
(1, 1, 'Rifle',  'Ascent'),
(1, 1, 'Sniper', 'Bind');

INSERT IGNORE INTO goals
(gameID, dateCreated, dateAchieved, description)
VALUES
(1, NOW(), NULL, 'Maintain 60% HS over next 10 scrims');

INSERT IGNORE INTO milestones
(profileID, goalID)
VALUES
(1, 1);