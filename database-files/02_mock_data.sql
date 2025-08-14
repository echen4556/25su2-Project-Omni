USE OmniDatabase;

-- GAMES
INSERT IGNORE INTO games (gameID, name) VALUES
(1, 'Valorant'),
(2, 'CS2');

-- DATA FOR EMMA SMITH/PERSONA 1 (VALORANT)
-- ===================================
-- Mock Data Inserts for Emma Smith User Stories
-- ===================================

INSERT IGNORE INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('EmmaSmith', FALSE, TRUE, FALSE, 'password');

INSERT IGNORE INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) 
VALUES
(1, 1, 'EmmaSmith', 1);

INSERT INTO playerStats
(gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins)
VALUES
(1, 45, 63, 25, 25330, 34, 132, 7);

INSERT IGNORE INTO matches (gameID, mapID, matchDate, matchType, lobbyRank)
VALUES
(1, 1, '2025-08-21 16:45:00','Unrated', 'Silver 2');

INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt,firstBloods)
VALUES
(999, 1, 14, 23, 7, 2, 343, 94, 2100, 16, 0, 9340, 1); 

INSERT IGNORE INTO weaponStats
(statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought)
VALUES
(2, 1, 2.000, 131, 0.310, 81),
(2, 2, 1.000,  42, 0.430,  32);

INSERT IGNORE INTO mapStats
(statTableID, gameID, weaponType, name)
VALUES
(1, 1, 'Rifle',  'Ascent'),
(1, 1, 'Sniper', 'Bind');

INSERT IGNORE INTO goals
(gameID, dateCreated, dateAchieved, description)
VALUES
(1, NOW(), NULL, 'Reach 1000 kills');

INSERT IGNORE INTO milestones
(profileID, goalID)
VALUES
(1, 2);


-- DATA FOR MATTHEW BONES/PERSONA 2 (VALORANT)
-- ===================================
-- Mock Data Inserts for Matthew Bones User Stories
-- ===================================

-- PROFILES (players)
INSERT INTO profiles (username, isAdmin, isPublic, isPremium, password) 
VALUES
('MatthewBones', FALSE, TRUE, TRUE, 'pass123'),
('Jamppi', FALSE, TRUE, TRUE, 'pass123'),
('Nivera', FALSE, TRUE, TRUE, 'pass123'),
('Soulcas', FALSE, TRUE, TRUE, 'pass123'),
('ScreaM', FALSE, TRUE, TRUE, 'pass123'),
('OpponentAce', FALSE, TRUE, FALSE, 'pass123'),
('OpponentShadow', FALSE, TRUE, FALSE, 'pass123');

-- GAME PROFILES (linking players to Valorant)
INSERT INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) 
VALUES
(1, 2, 'MattBones', TRUE),
(1, 3, 'JamppiTL', TRUE),
(1, 4, 'NiveraTL', TRUE),
(1, 5, 'SoulcasTL', TRUE),
(1, 6, 'ScreaMTL', TRUE),
(1, 7, 'AceRival', TRUE),
(1, 8, 'ShadowRival', TRUE);

-- PLAYER STATS
INSERT INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, 
totalHeadshots, totalShotsHit, totalWins) 
VALUES
(2, 180, 150, 40, 34500, 80, 520, 12),  -- MatthewBones
(3, 250, 140, 60, 40000, 120, 680, 15), -- Jamppi
(4, 220, 160, 55, 37000, 110, 640, 14), -- Nivera
(5, 190, 170, 70, 35500, 90, 600, 13),  -- Soulcas
(6, 300, 130, 50, 45000, 150, 720, 16), -- ScreaM
(7, 200, 180, 45, 34000, 85, 580, 10),  -- OpponentAce
(8, 210, 175, 48, 35000, 95, 590, 11);  -- OpponentShadow

-- WEAPONS
INSERT INTO weapons (gameID, weaponType, name) VALUES
(1, 'Rifle', 'Vandal'),
(1, 'Rifle', 'Phantom'),
(1, 'SMG', 'Spectre'),
(1, 'Sniper', 'Operator'),
(1, 'Pistol', 'Ghost'),
(1, 'Shotgun', 'Judge');

-- WEAPON STATS
INSERT INTO weaponStats (statTableID, weaponID, totalUsageTime, 
kills, accuracy, amountBought) 
VALUES
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
INSERT INTO map (gameID, POIs, Name) 
VALUES
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
(2, 2, 20, 15, 5, 10, 75, 50, 35, 24, TRUE, 3800, 3), -- MatthewBones
(2, 3, 25, 12, 7, 15, 80, 55, 35, 24, TRUE, 4200, 4), -- Jamppi
(2, 7, 18, 16, 4, 8, 70, 45, 35, 24, FALSE, 3400, 2), -- OpponentAce
(2, 8, 15, 18, 6, 7, 65, 42, 35, 24, FALSE, 3200, 1); -- OpponentShadow

-- Match 2 (Bind)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots,
 TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
 VALUES
(3, 4, 22, 14, 6, 11, 78, 52, 34, 24, TRUE, 4000, 3), -- Nivera
(3, 5, 18, 17, 8, 9, 70, 48, 34, 24, TRUE, 3600, 2), -- Soulcas
(3, 7, 20, 15, 5, 10, 75, 50, 34, 24, FALSE, 3800, 3), -- OpponentAce
(3, 8, 16, 18, 7, 8, 68, 46, 34, 24, FALSE, 3500, 2); -- OpponentShadow

-- Match 3 (Haven)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists,
 Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
 VALUES
(4, 6, 30, 10, 4, 16, 85, 60, 33, 24, TRUE, 5000, 5), -- ScreaM
(4, 2, 18, 16, 5, 9, 72, 48, 33, 24, TRUE, 3500, 2), -- MatthewBones
(4, 7, 22, 14, 6, 12, 80, 54, 33, 24, FALSE, 4100, 4), -- OpponentAce
(4, 8, 19, 15, 5, 10, 75, 50, 33, 24, FALSE, 3800, 3); -- OpponentShadow

-- DATA FOR KAI NGUYEN/PERSONA 3 (VALORANT)
-- ===================================
-- Mock Data Inserts for Kai Nguyen User Stories
-- ===================================

INSERT IGNORE INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('KaiGhost', 0, 1, 1, 'test123');

INSERT IGNORE INTO gamesProfiles ( gameID, profileID, gameUsername, showOnDashboard) VALUES
(1, 9, 'KaiGhost', 1);

INSERT IGNORE INTO map (gameID, POIs, Name) VALUES
  (1, 'A Site,B Site,Mid', 'Ascent');

INSERT IGNORE INTO weapons (gameID, weaponType, name) VALUES
 (1, 'Rifle',  'Vandal');

INSERT IGNORE INTO matches (gameID, mapID, matchDate, matchType, lobbyRank)
VALUES
(1, 1, '2025-08-01 18:30:00','Ranked', 'Immortal');

INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots,shotsHit, matchDuration, rounds, win, damageDealt,firstBloods)
VALUES
(5, 8, 22, 15, 5, 12, 300, 129, 2100, 16, 1, 10370, 2); 

INSERT INTO playerStats
(gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins)
VALUES
(9, 258, 191, 72, 33850, 132, 1082, 34);

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
(111, 2);

-- CSGO

-- ===================================
-- Mock Data Inserts for CSGO (First 5 Players)
-- ===================================

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
(6, 8, 23, 16, 6, 11, 80, 54, 38, 30, TRUE, 4200, 3), -- MatthewBonesCS
(6, 9, 28, 14, 8, 15, 88, 60, 38, 30, TRUE, 4700, 4), -- JamppiCS
(6, 10, 20, 18, 7, 10, 78, 52, 38, 30, FALSE, 4000, 3),-- NiveraCS
(6, 11, 18, 20, 5, 9, 72, 48, 38, 30, FALSE, 3700, 2), -- SoulcasCS
(6, 12, 30, 12, 4, 17, 92, 65, 38, 30, TRUE, 5200, 5); -- ScreaMCS

-- Match 2 (Mirage)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, 
TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
VALUES
(7, 8, 25, 15, 6, 12, 82, 56, 36, 30, TRUE, 4300, 3),
(7, 9, 26, 14, 9, 14, 85, 58, 36, 30, TRUE, 4500, 4),
(7, 10, 22, 17, 5, 11, 80, 54, 36, 30, FALSE, 4100, 3),
(7, 11, 17, 19, 8, 8, 70, 46, 36, 30, FALSE, 3600, 2),
(7, 12, 32, 11, 3, 18, 95, 68, 36, 30, TRUE, 5400, 5);

-- Match 3 (Inferno)
INSERT INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, 
Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) 
VALUES
(8, 8, 19, 17, 7, 9, 75, 50, 37, 30, FALSE, 3800, 2),
(8, 9, 24, 13, 10, 13, 83, 57, 37, 30, TRUE, 4400, 4),
(8, 10, 21, 16, 6, 10, 79, 53, 37, 30, FALSE, 3950, 3),
(8, 11, 16, 21, 9, 7, 68, 44, 37, 30, FALSE, 3500, 1),
(8, 12, 28, 12, 4, 15, 90, 62, 37, 30, TRUE, 5000, 4);


-- Valorant

-- ===================================
-- Mock Data Inserts for Valorant (First 5 Players)
-- ===================================

-- PROFILES (five new Valorant players)
INSERT IGNORE INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('TenZ',    FALSE, TRUE, TRUE, 'pass123'),   -- profileID 10
('Derke',   FALSE, TRUE, TRUE, 'pass123'),   -- profileID 11
('aspas',   FALSE, TRUE, TRUE, 'pass123'),   -- profileID 12
('Boaster', FALSE, TRUE, TRUE, 'pass123'),   -- profileID 13
('Leaf',    FALSE, TRUE, TRUE, 'pass123');   -- profileID 14

-- GAME PROFILES (link to Valorant)
INSERT IGNORE INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) VALUES
(1, 10, 'TenZ', 1),    -- gameInstanceID 13
(1, 11, 'Derke', 1),   -- gameInstanceID 14
(1, 12, 'aspas', 1),   -- gameInstanceID 15
(1, 13, 'Boaster', 1), -- gameInstanceID 16
(1, 14, 'Leaf', 1);    -- gameInstanceID 17

-- PLAYER STATS (one row per Valorant player)
INSERT IGNORE INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins) VALUES
(13, 320, 210, 70, 54000, 165, 820, 18),  -- TenZ
(14, 290, 200, 85, 50500, 150, 790, 17),  -- Derke
(15, 340, 190, 60, 56000, 175, 840, 19),  -- aspas
(16, 260, 230, 95, 48000, 130, 760, 15),  -- Boaster
(17, 300, 210, 80, 52000, 155, 800, 16);  -- Leaf

-- WEAPON STATS (use existing Valorant weaponIDs)
INSERT IGNORE INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought) VALUES
-- TenZ
(14, 1, 15.0, 150, 0.29, 70),  -- Vandal
(14, 2, 10.0,  90, 0.28, 45),  -- Phantom
-- Derke
(15, 1, 14.5, 140, 0.28, 65),  -- Vandal
(15, 4,  9.0,  80, 0.35, 40),  -- Operator
-- aspas
(16, 1, 16.0, 160, 0.30, 75),  -- Vandal
(16, 3,  8.5,  70, 0.31, 38),  -- Spectre
-- Boaster
(17, 2, 13.0, 120, 0.27, 60),  -- Phantom
(17, 5,  5.0,  40, 0.33, 25),  -- Ghost
-- Leaf
(18, 1, 15.5, 145, 0.29, 68),  -- Vandal
(18, 4,  7.5,  65, 0.34, 32);  -- Operator

-- MATCHES (three Valorant matches after your CSGO set)
INSERT IGNORE INTO matches (gameID, mapID, matchDate, matchType, lobbyRank) VALUES
(1, 1, '2025-08-10 20:00:00', 'Ranked', 'Radiant'), 
(1, 2, '2025-08-11 21:00:00', 'Ranked', 'Radiant'), 
(1, 3, '2025-08-12 19:00:00', 'Ranked', 'Radiant'); 

-- MATCH STATS
-- Match 1 (Ascent)
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(9, 14, 25, 15, 6, 12, 82, 56, 36, 24, TRUE,  4300, 3), -- TenZ
(9, 15, 28, 14, 9, 15, 88, 60, 36, 24, TRUE,  4700, 4), -- Derke
(9, 16, 20, 18, 7, 10, 78, 52, 36, 24, FALSE, 4000, 3), -- aspas
(9, 17, 18, 20, 5,  9, 72, 48, 36, 24, FALSE, 3700, 2), -- Boaster
(9, 18, 30, 12, 4, 17, 92, 65, 36, 24, TRUE,  5200, 5); -- Leaf

-- Match 2 (Bind)
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(10, 14, 27, 13, 8, 14, 85, 58, 36, 24, TRUE,  4500, 4),
(10, 15, 26, 14, 9, 14, 85, 58, 36, 24, TRUE,  4500, 4),
(10, 16, 22, 17, 5, 11, 80, 54, 36, 24, FALSE, 4100, 3),
(10, 17, 17, 19, 8,  8, 70, 46, 36, 24, FALSE, 3600, 2),
(10, 18, 32, 11, 3, 18, 95, 68, 36, 24, TRUE,  5400, 5);

-- Match 3 (Haven)
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(11, 14, 19, 17, 7,  9, 75, 50, 37, 24, FALSE, 3800, 2),
(11, 15, 24, 13,10, 13, 83, 57, 37, 24, TRUE,  4400, 4),
(11, 16, 21, 16, 6, 10, 79, 53, 37, 24, FALSE, 3950, 3),
(11, 17, 16, 21, 9,  7, 68, 44, 37, 24, FALSE, 3500, 1),
(11, 18, 28, 12, 4, 15, 90, 62, 37, 24, TRUE,  5000, 4);

-- CS2

-- ===================================
-- Mock Data Inserts for CS2 (First 5 Players)
-- ===================================

-- PROFILES (new CS2 players)  -- expected profileIDs: 15..19
INSERT IGNORE INTO profiles (username, isAdmin, isPublic, isPremium, password) VALUES
('s1mpleCS2', FALSE, TRUE, TRUE, 'pass123'),
('ZywOoCS2',  FALSE, TRUE, TRUE, 'pass123'),
('NiKoCS2',   FALSE, TRUE, TRUE, 'pass123'),
('m0NESY',    FALSE, TRUE, TRUE, 'pass123'),
('ropzCS2',   FALSE, TRUE, TRUE, 'pass123');

-- BRIDGE: gamesProfiles (profile <-> CS2)  -- expected gameInstanceIDs: 19..23
INSERT IGNORE INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard) VALUES
(2, 6, 's1mple', TRUE),
(2, 7, 'ZywOo',  TRUE),
(2, 8, 'NiKo',   TRUE),
(2, 9, 'm0NESY', TRUE),
(2, 10, 'ropz',   TRUE);

-- PLAYER STATS (one per gameInstanceID 19..23)
INSERT IGNORE INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins) VALUES
(19, 320, 200, 60, 52000, 150, 780, 18),  -- s1mple
(20, 310, 190, 75, 51000, 145, 770, 17),  -- ZywOo
(21, 300, 210, 65, 50500, 140, 760, 16),  -- NiKo
(22, 290, 220, 70, 49500, 135, 740, 15),  -- m0NESY
(23, 305, 205, 68, 50800, 142, 750, 16);  -- ropz

-- CS2 WEAPONS (use new IDs so we don't collide with CSGO's gameID=2 weapons)
-- expected weaponIDs 13..18
INSERT IGNORE INTO weapons (gameID, weaponType, name) VALUES
(3, 'Rifle',  'AK-47'),
(3, 'Rifle',  'M4A1-S'),
(3, 'Sniper', 'AWP'),
(3, 'SMG',    'MP9'),
(3, 'Pistol', 'Desert Eagle'),
(3, 'Shotgun','Nova');

-- WEAPON STATS (2 per player, minimal but realistic)
INSERT IGNORE INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought) VALUES
-- s1mple
(19, 13, 15.0, 150, 0.28, 70),
(19, 15,  9.0,  85, 0.34, 40),
-- ZywOo
(20, 13, 14.5, 140, 0.27, 68),
(20, 15, 10.0,  90, 0.35, 42),
-- NiKo
(21, 14, 13.0, 130, 0.26, 60),
(21, 13, 12.0, 125, 0.27, 58),
-- m0NESY
(22, 15, 12.0, 110, 0.33, 38),
(22, 13, 11.5, 120, 0.28, 55),
-- ropz
(23, 14, 12.5, 118, 0.26, 57),
(23, 16,  8.0,  60, 0.30, 30);

-- CS2 MAPS 
INSERT IGNORE INTO map (gameID, POIs, Name) VALUES
(3, 'A Site, B Site, Mid', 'Ancient'),
(3, 'A Site, B Site, Yard', 'Nuke'),
(3, 'A Site, B Site, Park', 'Overpass');

-- CS2 MATCHES 
INSERT IGNORE INTO matches (gameID, mapID, matchDate, matchType, lobbyRank) VALUES
(3, 7, '2025-08-13 20:00:00', 'Ranked', 'Global Elite'),
(3, 8, '2025-08-14 21:00:00', 'Ranked', 'Global Elite'),
(3, 9, '2025-08-15 19:00:00', 'Ranked', 'Global Elite');

-- MATCH STATS (5 players across each of the 3 CS2 matches)
-- Match 1 (Ancient) matchID=12
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(12, 19, 27, 14, 6, 13, 86, 58, 36, 30, TRUE,  4600, 4),
(12, 20, 25, 15, 7, 12, 84, 56, 36, 30, TRUE,  4400, 3),
(12, 21, 22, 17, 5, 11, 80, 54, 36, 30, FALSE, 4100, 3),
(12, 22, 18, 20, 8,  9, 72, 48, 36, 30, FALSE, 3600, 2),
(12, 23, 30, 12, 4, 16, 92, 65, 36, 30, TRUE,  5200, 5);

-- Match 2 (Nuke) matchID=13
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(13, 19, 24, 15, 8, 12, 83, 57, 36, 30, TRUE,  4400, 3),
(13, 20, 26, 14, 9, 14, 85, 58, 36, 30, TRUE,  4500, 4),
(13, 21, 21, 16, 6, 10, 79, 53, 36, 30, FALSE, 3950, 3),
(13, 22, 17, 19, 8,  8, 70, 46, 36, 30, FALSE, 3600, 2),
(13, 23, 28, 12, 4, 15, 90, 62, 36, 30, TRUE,  5000, 4);

-- Match 3 (Overpass) matchID=14
INSERT IGNORE INTO matchStats (matchID, gameInstanceID, kills, deaths, assists, Headshots, TotalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
(14, 19, 20, 17, 7,  9, 75, 50, 37, 30, FALSE, 3800, 2),
(14, 20, 24, 13,10, 13, 83, 57, 37, 30, TRUE,  4400, 4),
(14, 21, 23, 16, 6, 11, 81, 55, 37, 30, FALSE, 4000, 3),
(14, 22, 16, 21, 9,  7, 68, 44, 37, 30, FALSE, 3500, 1),
(14, 23, 29, 12, 4, 16, 91, 64, 37, 30, TRUE,  5100, 4);

-- DATA FOR JORDAN LEE/PERSONA 4
-- ===================================
-- Mock Data Inserts for Jordan Lee User Stories
-- ===================================

-- ====== BASE TABLES ======
-- PROFILES (role management via isAdmin/isPremium/isPublic)
INSERT INTO profiles (profileID, username, isAdmin, isPublic, isPremium, password) VALUES
  (91, 'jordan_lee', 1, 1, 1, 'hashed_pw_jordan'), -- admin, public, premium
  (92, 'mod_kim',     1, 1, 0, 'hashed_pw_kim'), -- admin, public
  (93, 'analyst_ryu', 0, 1, 0, 'hashed_pw_ryu'), -- public
  (94, 'viewer_amy',  0, 1, 0, 'hashed_pw_amy'); -- public

-- GAMES 
INSERT INTO games (gameID, name) VALUES
  (10, 'Apex Legends'),
  (11, 'Valorant'),
  (12, 'Overwatch 2'),
  (99, 'Extraction Royale'); -- Games

-- MAPS
INSERT INTO map (mapID, gameID, Name) VALUES
  (100, 10, 'Worlds Edge'), -- Apex Legends map
  (101, 10, 'Olympus'), -- Apex Legends map
  (110, 11, 'Ascent'), -- Valorant map
  (111, 11, 'Bind'), -- Valorant map
  (120, 12, 'New Junk City'), -- Overwatch 2 map
  (190, 99, 'Silo Complex'); -- Extraction Royale map

-- ====== ACCOUNT LINKS / OVERLAY ======
-- gamesProfiles (sync overlay to game playing based on account active)
INSERT INTO gamesProfiles (gameInstanceID, gameID, profileID, gameUsername, showOnDashboard) VALUES
  (1000, 10, 1, 'J0RD4N', 1), -- Apex, jordan_lee account, on leaderboard
  (1001, 11, 1, 'J0RD4N#NA', 1), -- Valorant, jordan_lee account, on leaderboard
  (1002, 12, 1, 'Jord0W2', 0), -- Overwatch 2, jordan_lee account, not on leaderboard
  (2000, 10, 3, 'RyuStats', 1), -- Apex, analyst_ryu account, on leaderboard
  (3000, 99, 1, 'JordanXR', 1); -- Extraciton Royale, jordan_lee account, on leaderboard

-- ====== MATCHES & STATS ======
INSERT INTO matches (matchID, gameID, mapID, matchDate, matchType, lobbyRank) VALUES
  (5001, 10, 100, '2024-10-01 19:05:00', 'ranked', 'Gold'),
  (5002, 10, 101, '2024-11-01 20:12:00', 'ranked', 'Platinum'),
  (5003, 10, 100, '2025-01-10 21:30:00', 'ranked', 'Diamond'),
  (5004, 10, 101, '2025-01-12 21:40:00', 'ranked', 'Diamond');
  -- Will be used to check if player stats are crazy

INSERT INTO matchStats (matchStatsID, matchID, gameInstanceID, kills, deaths, assists, headshots, totalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
  -- normal average game
  (9001, 5001, 1000, 6, 4, 3, 2, 120, 45, 1800, 1, 1, 1150, 0),
  (9002, 5002, 1000, 8, 5, 4, 3, 150, 60, 1900, 1, 1, 1400, 1),
  -- slightly better game
  (9003, 5003, 1000, 12, 6, 5, 5, 210, 98, 2100, 1, 1, 2100, 2), -- 
  -- Game far better then previous stats
  (9004, 5004, 1000, 60, 0, 10, 25, 160, 158, 900, 1, 1, 5200, 5);

-- Overwatch 2 for jordan account not on dashboard
INSERT INTO matches (matchID, gameID, mapID, matchDate, matchType, lobbyRank) VALUES
  (5201, 12, 120, '2024-11-20 13:10:00', 'quickplay', 'Unrated');
INSERT INTO matchStats (matchStatsID, matchID, gameInstanceID, kills, deaths, assists, headshots, totalShots, shotsHit, matchDuration, rounds, win, damageDealt, firstBloods) VALUES
  (9201, 5201, 1002, 30, 20, 18, 0, 500, 250, 1800, 1, 1, 6400, 0);

-- -- ====== COMMUNITY INTEREST PROXY ======
-- -- Use goals as "content ideas" tied to games to infer interest from community.
-- INSERT INTO goals (goalsID, gameID, dateCreated, description) VALUES
--   (7001, 10, '2024-12-01 10:00:00', 'Improve at Apex rotation'),
--   (7002, 11, '2024-12-28 10:00:00', 'Learn Valorant Ascent execute')

-- -- Milestones can reflect content progress or KPIs (view targets)
-- INSERT INTO milestones (milestoneID, profileID, goalID) VALUES
--   (8001, 1, 7001),
--   (8002, 1, 7002)