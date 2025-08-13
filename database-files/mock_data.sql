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


-- DATA FOR MATTHEW BONES/PERSONA 2 (VALORANT)
-- ===================================
-- Mock Data Inserts for Matthew Bones User Stories
-- ===================================

-- GAMES
INSERT INTO games (name) VALUES
('Valorant');

-- PROFILES (players)
INSERT INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('MatthewBones', FALSE, TRUE, TRUE, 'pass123'),
('Jamppi', FALSE, TRUE, TRUE, 'pass123'),
('Nivera', FALSE, TRUE, TRUE, 'pass123'),
('Soulcas', FALSE, TRUE, TRUE, 'pass123'),
('ScreaM', FALSE, TRUE, TRUE, 'pass123'),
('OpponentAce', FALSE, TRUE, FALSE, 'pass123'),
('OpponentShadow', FALSE, TRUE, FALSE, 'pass123');

-- GAME PROFILES (linking players to Valorant)
INSERT INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) VALUES
(1, 1, 'MattBones', TRUE),
(1, 2, 'JamppiTL', TRUE),
(1, 3, 'NiveraTL', TRUE),
(1, 4, 'SoulcasTL', TRUE),
(1, 5, 'ScreaMTL', TRUE),
(1, 6, 'AceRival', TRUE),
(1, 7, 'ShadowRival', TRUE);

-- PLAYER STATS
INSERT INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins) VALUES
(1, 180, 150, 40, 34500, 80, 520, 12),  -- MatthewBones
(2, 250, 140, 60, 40000, 120, 680, 15), -- Jamppi
(3, 220, 160, 55, 37000, 110, 640, 14), -- Nivera
(4, 190, 170, 70, 35500, 90, 600, 13),  -- Soulcas
(5, 300, 130, 50, 45000, 150, 720, 16), -- ScreaM
(6, 200, 180, 45, 34000, 85, 580, 10),  -- OpponentAce
(7, 210, 175, 48, 35000, 95, 590, 11);  -- OpponentShadow

-- WEAPONS
INSERT INTO weapons (gameID, weaponType, name) VALUES
(1, 'Rifle', 'Vandal'),
(1, 'Rifle', 'Phantom'),
(1, 'SMG', 'Spectre'),
(1, 'Sniper', 'Operator'),
(1, 'Pistol', 'Ghost'),
(1, 'Shotgun', 'Judge');

-- WEAPON STATS
INSERT INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought) VALUES
-- MatthewBones
(1, 1, 12.5, 90, 0.27, 50),
(1, 2, 8.0, 60, 0.25, 35),
(1, 5, 3.5, 20, 0.32, 25),
-- Jamppi
(2, 1, 15.0, 120, 0.28, 60),
(2, 4, 10.5, 80, 0.35, 40),
(2, 3, 5.0, 50, 0.30, 30),
-- Nivera
(3, 2, 13.0, 100, 0.26, 55),
(3, 3, 6.0, 60, 0.31, 28),
-- Soulcas
(4, 1, 10.0, 80, 0.25, 40),
(4, 2, 9.0, 70, 0.24, 38),
-- ScreaM
(5, 1, 18.0, 150, 0.29, 70),
(5, 4, 7.5, 80, 0.34, 35);

-- MAPS
INSERT INTO map (gameID, POIs, Name) VALUES
(1, 'A Site, B Site, Mid', 'Ascent'),
(1, 'A Site, B Site, Hookah', 'Bind'),
(1, 'A Site, B Site, C Site', 'Haven');

-- MATCHES
INSERT INTO matches (gameID, mapID, matchDate, matchType, lobbyRank)
 VALUES
(1, 1, '2025-08-01 20:00:00', 'Ranked', 'Immortal'),
(1, 2, '2025-08-02 21:00:00', 'Ranked', 'Immortal'),
(1, 3, '2025-08-03 19:00:00', 'Ranked', 'Immortal');

-- MATCH STATS
-- Match 1 (Ascent)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists,
Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods)
 VALUES
(1, 1, 20, 15, 5, 10, 75, 50, 35, 24, TRUE, 3800, 3), -- MatthewBones
(1, 2, 25, 12, 7, 15, 80, 55, 35, 24, TRUE, 4200, 4), -- Jamppi
(1, 6, 18, 16, 4, 8, 70, 45, 35, 24, FALSE, 3400, 2), -- OpponentAce
(1, 7, 15, 18, 6, 7, 65, 42, 35, 24, FALSE, 3200, 1); -- OpponentShadow

-- Match 2 (Bind)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots,
 TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
 VALUES
(2, 3, 22, 14, 6, 11, 78, 52, 34, 24, TRUE, 4000, 3), -- Nivera
(2, 4, 18, 17, 8, 9, 70, 48, 34, 24, TRUE, 3600, 2), -- Soulcas
(2, 6, 20, 15, 5, 10, 75, 50, 34, 24, FALSE, 3800, 3), -- OpponentAce
(2, 7, 16, 18, 7, 8, 68, 46, 34, 24, FALSE, 3500, 2); -- OpponentShadow

-- Match 3 (Haven)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists,
 Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
 VALUES
(3, 5, 30, 10, 4, 16, 85, 60, 33, 24, TRUE, 5000, 5), -- ScreaM
(3, 1, 18, 16, 5, 9, 72, 48, 33, 24, TRUE, 3500, 2), -- MatthewBones
(3, 6, 22, 14, 6, 12, 80, 54, 33, 24, FALSE, 4100, 4), -- OpponentAce
(3, 7, 19, 15, 5, 10, 75, 50, 33, 24, FALSE, 3800, 3); -- OpponentShadow

-- CSGO

-- ===================================
-- Mock Data Inserts for CSGO (First 5 Players)
-- ===================================

-- GAMES (adding CSGO)
INSERT INTO games (name) 
VALUES
('CSGO');

-- GAME PROFILES for CSGO (gameID = 2)
INSERT INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) 
VALUES
(2, 1, 'MattBones', TRUE),
(2, 2, 'Jamppi', TRUE),
(2, 3, 'Nivera', TRUE),
(2, 4, 'Soulcas', TRUE),
(2, 5, 'ScreaM', TRUE);

-- PLAYER STATS for CSGO
INSERT INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, 
totalHeadshots, totalShotsHit, totalWins) 
VALUES
(8, 210, 160, 50, 42000, 95, 610, 14),  -- MatthewBonesCS
(9, 280, 150, 65, 50000, 140, 750, 17), -- JamppiCS
(10, 240, 170, 58, 46000, 115, 680, 15),-- NiveraCS
(11, 200, 180, 72, 43000, 90, 640, 13), -- SoulcasCS
(12, 320, 140, 55, 54000, 160, 800, 18);-- ScreaMCS

-- WEAPONS for CSGO (gameID = 2)
INSERT INTO weapons (gameID, weaponType, name) 
VALUES
(2, 'Rifle', 'AK-47'),
(2, 'Rifle', 'M4A4'),
(2, 'Sniper', 'AWP'),
(2, 'SMG', 'MP9'),
(2, 'Pistol', 'Desert Eagle'),
(2, 'Shotgun', 'Nova');

-- WEAPON STATS for CSGO
INSERT INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought) 
VALUES
-- MatthewBonesCS
(8, 7, 14.0, 110, 0.26, 55), -- AK-47
(8, 8, 9.0, 70, 0.25, 40),  -- M4A4
(8, 12, 3.0, 15, 0.31, 20), -- Desert Eagle
-- JamppiCS
(9, 7, 16.0, 140, 0.28, 65), -- AK-47
(9, 9, 11.0, 85, 0.34, 45),  -- AWP
(9, 10, 4.5, 25, 0.29, 25),  -- MP9
-- NiveraCS
(10, 8, 13.5, 105, 0.27, 60), -- M4A4
(10, 9, 5.5, 45, 0.33, 28),   -- AWP
-- SoulcasCS
(11, 7, 10.5, 80, 0.24, 45), -- AK-47
(11, 8, 9.5, 72, 0.23, 42),  -- M4A4
-- ScreaMCS
(12, 7, 18.5, 160, 0.29, 75), -- AK-47
(12, 9, 8.0, 78, 0.32, 38);   -- AWP

-- MAPS for CSGO
INSERT INTO map (gameID, POIs, Name) 
VALUES
(2, 'A Site, B Site, Mid', 'Dust II'),
(2, 'A Site, B Site, Palace', 'Mirage'),
(2, 'A Site, B Site, Apartments', 'Inferno');

-- MATCHES for CSGO
INSERT INTO matches (gameID, mapID, matchDate, matchType, lobbyRank) 
VALUES
(2, 4, '2025-08-05 20:00:00', 'Ranked', 'Global Elite'),
(2, 5, '2025-08-06 21:00:00', 'Ranked', 'Global Elite'),
(2, 6, '2025-08-07 19:00:00', 'Ranked', 'Global Elite');

-- MATCH STATS for CSGO
-- Match 1 (Dust II)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, 
Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
VALUES
(4, 8, 23, 16, 6, 11, 80, 54, 38, 30, TRUE, 4200, 3), -- MatthewBonesCS
(4, 9, 28, 14, 8, 15, 88, 60, 38, 30, TRUE, 4700, 4), -- JamppiCS
(4, 10, 20, 18, 7, 10, 78, 52, 38, 30, FALSE, 4000, 3),-- NiveraCS
(4, 11, 18, 20, 5, 9, 72, 48, 38, 30, FALSE, 3700, 2), -- SoulcasCS
(4, 12, 30, 12, 4, 17, 92, 65, 38, 30, TRUE, 5200, 5); -- ScreaMCS

-- Match 2 (Mirage)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, 
TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
VALUES
(5, 8, 25, 15, 6, 12, 82, 56, 36, 30, TRUE, 4300, 3),
(5, 9, 26, 14, 9, 14, 85, 58, 36, 30, TRUE, 4500, 4),
(5, 10, 22, 17, 5, 11, 80, 54, 36, 30, FALSE, 4100, 3),
(5, 11, 17, 19, 8, 8, 70, 46, 36, 30, FALSE, 3600, 2),
(5, 12, 32, 11, 3, 18, 95, 68, 36, 30, TRUE, 5400, 5);

-- Match 3 (Inferno)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, 
Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
VALUES
(6, 8, 19, 17, 7, 9, 75, 50, 37, 30, FALSE, 3800, 2),
(6, 9, 24, 13, 10, 13, 83, 57, 37, 30, TRUE, 4400, 4),
(6, 10, 21, 16, 6, 10, 79, 53, 37, 30, FALSE, 3950, 3),
(6, 11, 16, 21, 9, 7, 68, 44, 37, 30, FALSE, 3500, 1),
(6, 12, 28, 12, 4, 15, 90, 62, 37, 30, TRUE, 5000, 4);


