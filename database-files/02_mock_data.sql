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
(statTableID, mapID, kills, wins, losses)
VALUES
(1, 1, 23, 3, 5),
(1, 2, 21, 4, 3);

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
('KaiGhost', FALSE, TRUE, TRUE, 'pass123')

INSERT IGNORE INTO gamesProfiles ( gameID, profileID, gameUsername, showOnDashboard) VALUES
(1, 9, 'KaiGhost', TRUE);

INSERT IGNORE INTO map (gameID, POIs, Name) VALUES
  (1, 'A Site, B Site,Mid', 'Ascent');

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
(statTableID, mapID, kills, wins, losses)
VALUES
(1, 1, 30,  3, 2),
(1, 2, 10, 1, 3);

INSERT IGNORE INTO goals
(gameID, dateCreated, dateAchieved, description)
VALUES
(1, NOW(), NULL, 'Maintain 60% HS over next 10 scrims');

INSERT IGNORE INTO milestones
(profileID, goalID)
VALUES
(111, 2);

-- DATA FOR JORDAN LEE/PERSONA 4
-- ===================================
-- Mock Data Inserts for Jordan Lee User Stories
-- ===================================

-- ====== BASE TABLES ======
-- PROFILES (role management via isAdmin/isPremium/isPublic)
INSERT INTO profiles (profileID, username, isAdmin, isPublic, isPremium, password) VALUES
  (10, 'jordan_lee', 1, 1, 1, 'hashed_pw_jordan'), -- admin, public, premium
  (11, 'mod_kim',     1, 1, 0, 'hashed_pw_kim'), -- admin, public
  (12, 'analyst_ryu', 0, 1, 0, 'hashed_pw_ryu'), -- public
  (13, 'viewer_amy',  0, 1, 0, 'hashed_pw_amy'); -- public

-- GAMES 
INSERT IGNORE INTO games (gameID, name) VALUES
(3, 'Fortnite'),
(4, 'Half Life'),
(5, 'Cyberpunk 2077'),
(6, 'Apex Reckoning'),
(7, 'Elden Ring'),
(8, 'The Witcher 3: Wild Hunt'),
(9, 'Stardew Valley'),
(10, 'Among Us'),
(11, 'Genshin Impact'),
(12, 'Quantum Strike'),
(13, 'Celeste'),
(14, 'Dead Cells'),
(15, 'Hades'),
(16, 'Phantom Vanguard'),
(17, 'Bulletstorm Royale'),
(18, 'Final Fantasy XIV'),
(19, 'Grand Theft Auto V'),
(20, 'Fall Guys'),
(21, 'Lethal Company'),
(22, 'Galactic Frontline'),
(23, 'Sea of Thieves'),
(24, 'No Man''s Sky'),
(25, 'Destiny 2'),
(26, 'Echo Combat'),
(27, 'Iron Vanguard'),
(28, 'Monster Hunter: World'),
(29, 'Crimson Point'),
(30, 'Neon Blitz'),
(31, 'Shadowfall'),
(32, 'Diablo III'),
(33, 'Apex Legends'),
(34, 'Rainbow Six Siege');

-- MAPS
INSERT IGNORE INTO map (mapID, gameID, Name) VALUES
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
  (3000, 32, 1, 'JordanXR', 1); -- Extraciton Royale, jordan_lee account, on leaderboard

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


INSERT INTO profiles (profileID, username, isAdmin, isPublic, isPremium, password) VALUES
(13, 'AlexTurner', FALSE, TRUE, TRUE, 'pass123'),
(14, 'MiaCruz', FALSE, TRUE, FALSE, 'pass123'),
(15, 'TheNightFury', TRUE, TRUE, TRUE, 'pass123'),
(16, 'Liam_W', FALSE, TRUE, TRUE, 'pass123'),
(17, 'EpicGamer22', FALSE, TRUE, FALSE, 'pass123'),
(18, 'ZoeChen', TRUE, TRUE, FALSE, 'pass123'),
(19, 'CyberGhost', FALSE, TRUE, TRUE, 'pass123'),
(20, 'OliverStone', FALSE, TRUE, FALSE, 'pass123'),
(21, 'Luna_Blaze', FALSE, TRUE, TRUE, 'pass123'),
(22, 'FinnDavis', FALSE, TRUE, FALSE, 'pass123'),
(23, 'NinjaShark', TRUE, TRUE, TRUE, 'pass123'),
(24, 'ChloePrice', FALSE, TRUE, FALSE, 'pass123'),
(25, 'PixelKnight', FALSE, TRUE, TRUE, 'pass123'),
(26, 'Sam_Rivera', FALSE, TRUE, FALSE, 'pass123'),
(27, 'CosmicEcho', FALSE, TRUE, TRUE, 'pass123'),
(28, 'AvaJones', TRUE, TRUE, FALSE, 'pass123'),
(29, 'Silent_Sniper', FALSE, TRUE, FALSE, 'pass123'),
(30, 'EthanBaker', FALSE, TRUE, TRUE, 'pass123'),
(31, 'VortexViper', FALSE, TRUE, FALSE, 'pass123'),
(32, 'IslaGray', TRUE, TRUE, TRUE, 'pass123'),
(33, 'DragonSlayer99', FALSE, TRUE, TRUE, 'pass123'),
(34, 'NoahFoster', FALSE, TRUE, FALSE, 'pass123'),
(35, 'ShadowStalker', FALSE, TRUE, TRUE, 'pass123'),
(36, 'LilyAdams', FALSE, TRUE, FALSE, 'pass123'),
(37, 'RogueOne', TRUE, TRUE, TRUE, 'pass123'),
(38, 'JackHarper', FALSE, TRUE, TRUE, 'pass123'),
(39, 'SolarFlare', FALSE, TRUE, FALSE, 'pass123'),
(40, 'GraceLee', FALSE, TRUE, TRUE, 'pass123'),
(41, 'Nightshade_Op', TRUE, TRUE, FALSE, 'pass123'),
(42, 'RyanMurphy', FALSE, TRUE, TRUE, 'pass123');

INSERT IGNORE INTO gamesProfiles (gameInstanceID, gameID, profileID, gameUsername, showOnDashboard) VALUES
(3001, 23, 37, 'RogueOne_GP_3001', 1),
(3002, 19, 14, 'MiaCruz_GP_3002', 1),
(3003, 31, 29, 'Silent_Sniper_GP_3003', 0),
(3004, 2, 23, 'NinjaShark_GP_3004', 1),
(3005, 34, 18, 'ZoeChen_GP_3005', 0),
(3006, 11, 41, 'Nightshade_Op_GP_3006', 1),
(3007, 26, 3, 'Jamppi_GP_3007', 1),
(3008, 16, 26, 'Sam_Rivera_GP_3008', 0),
(3009, 32, 20, 'OliverStone_GP_3009', 1),
(3010, 1, 33, 'DragonSlayer99_GP_3010', 0),
(3011, 28, 13, 'AlexTurner_GP_3011', 1),
(3012, 15, 30, 'EthanBaker_GP_3012', 1),
(3013, 22, 16, 'Liam_W_GP_3013', 0),
(3014, 8, 38, 'JackHarper_GP_3014', 1),
(3015, 29, 21, 'Luna_Blaze_GP_3015', 1),
(3016, 4, 34, 'NoahFoster_GP_3016', 0),
(3017, 18, 2, 'MatthewBones_GP_3017', 1),
(3018, 3, 24, 'ChloePrice_GP_3018', 1),
(3019, 13, 31, 'VortexViper_GP_3019', 0),
(3020, 25, 17, 'EpicGamer22_GP_3020', 1),
(3021, 6, 40, 'GraceLee_GP_3021', 1),
(3022, 33, 22, 'FinnDavis_GP_3022', 0),
(3023, 10, 35, 'ShadowStalker_GP_3023', 1),
(3024, 7, 19, 'CyberGhost_GP_3024', 1),
(3025, 20, 32, 'IslaGray_GP_3025', 0),
(3026, 5, 25, 'PixelKnight_GP_3026', 1),
(3027, 27, 36, 'LilyAdams_GP_3027', 1),
(3028, 9, 28, 'AvaJones_GP_3028', 0),
(3029, 24, 42, 'RyanMurphy_GP_3029', 1),
(3030, 30, 15, 'TheNightFury_GP_3030', 1),
(3031, 14, 39, 'SolarFlare_GP_3031', 0),
(3032, 17, 4, 'Nivera_GP_3032', 1),
(3033, 2, 27, 'CosmicEcho_GP_3033', 1),
(3034, 34, 1, 'EmmaSmith_GP_3034', 0),
(3035, 11, 23, 'NinjaShark_GP_3035', 1),
(3036, 26, 18, 'ZoeChen_GP_3036', 1),
(3037, 16, 41, 'Nightshade_Op_GP_3037', 0),
(3038, 32, 3, 'Jamppi_GP_3038', 1),
(3039, 1, 26, 'Sam_Rivera_GP_3039', 1),
(3040, 28, 20, 'OliverStone_GP_3040', 0),
(3041, 15, 33, 'DragonSlayer99_GP_3041', 1),
(3042, 22, 13, 'AlexTurner_GP_3042', 1),
(3043, 8, 30, 'EthanBaker_GP_3043', 0),
(3044, 29, 16, 'Liam_W_GP_3044', 1),
(3045, 4, 38, 'JackHarper_GP_3045', 1),
(3046, 18, 21, 'Luna_Blaze_GP_3046', 0),
(3047, 3, 34, 'NoahFoster_GP_3047', 1),
(3048, 13, 2, 'MatthewBones_GP_3048', 1),
(3049, 25, 24, 'ChloePrice_GP_3049', 0),
(3050, 6, 31, 'VortexViper_GP_3050', 1),
(3051, 33, 17, 'EpicGamer22_GP_3051', 1),
(3052, 10, 40, 'GraceLee_GP_3052', 0),
(3053, 7, 22, 'FinnDavis_GP_3053', 1),
(3054, 20, 35, 'ShadowStalker_GP_3054', 1),
(3055, 5, 19, 'CyberGhost_GP_3055', 0),
(3056, 27, 32, 'IslaGray_GP_3056', 1),
(3057, 9, 25, 'PixelKnight_GP_3057', 1),
(3058, 24, 36, 'LilyAdams_GP_3058', 0),
(3059, 30, 28, 'AvaJones_GP_3059', 1),
(3060, 14, 42, 'RyanMurphy_GP_3060', 1),
(3061, 17, 15, 'TheNightFury_GP_3061', 0),
(3062, 2, 39, 'SolarFlare_GP_3062', 1),
(3063, 34, 4, 'Nivera_GP_3063', 1),
(3064, 11, 27, 'CosmicEcho_GP_3064', 0),
(3065, 26, 1, 'EmmaSmith_GP_3065', 1),
(3066, 16, 23, 'NinjaShark_GP_3066', 1),
(3067, 32, 18, 'ZoeChen_GP_3067', 0),
(3068, 1, 41, 'Nightshade_Op_GP_3068', 1),
(3069, 28, 3, 'Jamppi_GP_3069', 1),
(3070, 15, 26, 'Sam_Rivera_GP_3070', 0),
(3071, 22, 20, 'OliverStone_GP_3071', 1),
(3072, 8, 33, 'DragonSlayer99_GP_3072', 1),
(3073, 29, 13, 'AlexTurner_GP_3073', 0),
(3074, 4, 30, 'EthanBaker_GP_3074', 1),
(3075, 18, 16, 'Liam_W_GP_3075', 1),
(3076, 3, 38, 'JackHarper_GP_3076', 0),
(3077, 13, 21, 'Luna_Blaze_GP_3077', 1),
(3078, 25, 34, 'NoahFoster_GP_3078', 1),
(3079, 6, 2, 'MatthewBones_GP_3079', 0),
(3080, 33, 24, 'ChloePrice_GP_3080', 1),
(3081, 10, 31, 'VortexViper_GP_3081', 1),
(3082, 7, 17, 'EpicGamer22_GP_3082', 0),
(3083, 20, 40, 'GraceLee_GP_3083', 1),
(3084, 5, 22, 'FinnDavis_GP_3084', 1),
(3085, 27, 35, 'ShadowStalker_GP_3085', 0),
(3086, 9, 19, 'CyberGhost_GP_3086', 1),
(3087, 24, 32, 'IslaGray_GP_3087', 1),
(3088, 30, 25, 'PixelKnight_GP_3088', 0),
(3089, 14, 36, 'LilyAdams_GP_3089', 1),
(3090, 17, 28, 'AvaJones_GP_3090', 1),
(3091, 2, 42, 'RyanMurphy_GP_3091', 0),
(3092, 34, 15, 'TheNightFury_GP_3092', 1),
(3093, 11, 39, 'SolarFlare_GP_3093', 1),
(3094, 26, 4, 'Nivera_GP_3094', 0),
(3095, 16, 27, 'CosmicEcho_GP_3095', 1),
(3096, 32, 1, 'EmmaSmith_GP_3096', 1),
(3097, 1, 23, 'NinjaShark_GP_3097', 0),
(3098, 28, 18, 'ZoeChen_GP_3098', 1),
(3099, 15, 41, 'Nightshade_Op_GP_3099', 1),
(3100, 22, 3, 'Jamppi_GP_3100', 0),
(3101, 8, 26, 'Sam_Rivera_GP_3101', 1),
(3102, 29, 20, 'OliverStone_GP_3102', 1),
(3103, 4, 33, 'DragonSlayer99_GP_3103', 0),
(3104, 18, 13, 'AlexTurner_GP_3104', 1),
(3105, 3, 30, 'EthanBaker_GP_3105', 1),
(3106, 13, 16, 'Liam_W_GP_3106', 0),
(3107, 25, 38, 'JackHarper_GP_3107', 1),
(3108, 6, 21, 'Luna_Blaze_GP_3108', 1),
(3109, 33, 34, 'NoahFoster_GP_3109', 0),
(3110, 10, 2, 'MatthewBones_GP_3110', 1),
(3111, 7, 24, 'ChloePrice_GP_3111', 1),
(3112, 20, 31, 'VortexViper_GP_3112', 0),
(3113, 5, 17, 'EpicGamer22_GP_3113', 1),
(3114, 27, 40, 'GraceLee_GP_3114', 1),
(3115, 9, 22, 'FinnDavis_GP_3115', 0);

INSERT IGNORE INTO playerStats (statTableID, gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins) VALUES
(100, 3001, 25, 20, 10, 5000, 45, 150, 1),
(101, 3002, 18, 15, 8, 3500, 30, 110, 0),
(102, 3003, 35, 25, 15, 7500, 60, 200, 1),
(103, 3004, 22, 18, 5, 4200, 25, 105, 1),
(104, 3005, 30, 10, 3, 6000, 55, 85, 1),
(105, 3006, 28, 22, 12, 6500, 50, 220, 0),
(106, 3007, 26, 21, 11, 5500, 40, 180, 1),
(107, 3008, 20, 16, 9, 4800, 35, 140, 0),
(108, 3009, 15, 12, 7, 3000, 20, 125, 1),
(109, 3010, 10, 8, 4, 2500, 10, 60, 0),
(110, 3011, 30, 24, 13, 6200, 50, 180, 1),
(111, 3012, 20, 17, 9, 3800, 32, 120, 1),
(112, 3013, 40, 30, 18, 8500, 70, 215, 1),
(113, 3014, 25, 20, 6, 4800, 28, 115, 0),
(114, 3015, 32, 11, 4, 6500, 60, 90, 1),
(115, 3016, 30, 25, 14, 7000, 55, 230, 1),
(116, 3017, 28, 23, 12, 6000, 45, 195, 0),
(117, 3018, 22, 18, 10, 5000, 38, 150, 1),
(118, 3019, 18, 14, 8, 3500, 22, 130, 0),
(119, 3020, 12, 10, 5, 2800, 12, 65, 1),
(120, 3021, 27, 22, 11, 5800, 48, 165, 1),
(121, 3022, 19, 16, 8, 3600, 31, 118, 0),
(122, 3023, 38, 28, 16, 8000, 65, 205, 1),
(123, 3024, 23, 19, 6, 4500, 26, 110, 0),
(124, 3025, 31, 12, 3, 6200, 58, 88, 1),
(125, 3026, 29, 24, 13, 6800, 52, 225, 1),
(126, 3027, 27, 22, 11, 5700, 43, 190, 0),
(127, 3028, 21, 17, 9, 4900, 36, 145, 1),
(128, 3029, 16, 13, 7, 3200, 21, 128, 0),
(129, 3030, 11, 9, 4, 2600, 11, 62, 1),
(130, 3031, 26, 21, 10, 5500, 45, 160, 0),
(131, 3032, 17, 14, 7, 3400, 28, 115, 1),
(132, 3033, 36, 27, 15, 7800, 62, 210, 1),
(133, 3034, 24, 20, 7, 4700, 27, 120, 1),
(134, 3035, 33, 13, 4, 6800, 61, 95, 0),
(135, 3036, 31, 26, 15, 7500, 58, 240, 1),
(136, 3037, 29, 24, 13, 6200, 48, 200, 1),
(137, 3038, 23, 19, 11, 5100, 40, 155, 0),
(138, 3039, 19, 15, 8, 3800, 24, 135, 1),
(139, 3040, 13, 11, 5, 3000, 13, 70, 0),
(140, 3041, 28, 23, 12, 6000, 50, 170, 1),
(141, 3042, 21, 18, 9, 4000, 34, 125, 0),
(142, 3043, 42, 32, 19, 9000, 75, 220, 1),
(143, 3044, 26, 21, 8, 5000, 30, 125, 1),
(144, 3045, 34, 14, 5, 7000, 65, 100, 1),
(145, 3046, 32, 27, 16, 8000, 60, 250, 0),
(146, 3047, 30, 25, 14, 6500, 50, 205, 1),
(147, 3048, 24, 20, 12, 5300, 42, 160, 0),
(148, 3049, 20, 16, 9, 4000, 26, 140, 1),
(149, 3050, 14, 12, 6, 3200, 14, 75, 0),
(150, 3051, 29, 24, 13, 6300, 52, 175, 1),
(151, 3052, 22, 19, 10, 4200, 36, 130, 1),
(152, 3053, 45, 35, 20, 9500, 80, 225, 1),
(153, 3054, 27, 22, 9, 5200, 32, 130, 0),
(154, 3055, 35, 15, 6, 7200, 68, 105, 1),
(155, 3056, 34, 29, 17, 8500, 62, 260, 0),
(156, 3057, 31, 26, 15, 6800, 52, 210, 1),
(157, 3058, 25, 21, 13, 5500, 44, 165, 1),
(158, 3059, 21, 17, 10, 4200, 28, 145, 0),
(159, 3060, 15, 13, 7, 3400, 15, 80, 1),
(160, 3061, 30, 25, 14, 6500, 55, 185, 1),
(161, 3062, 23, 20, 11, 4400, 38, 135, 0),
(162, 3063, 48, 38, 22, 10000, 85, 230, 1),
(163, 3064, 28, 23, 10, 5400, 34, 135, 1),
(164, 3065, 36, 16, 7, 7500, 70, 110, 1),
(165, 3066, 36, 30, 18, 9000, 65, 270, 0),
(166, 3067, 32, 27, 16, 7000, 55, 215, 1),
(167, 3068, 26, 22, 14, 5700, 46, 170, 0),
(168, 3069, 22, 18, 11, 4400, 30, 150, 1),
(169, 3070, 16, 14, 8, 3600, 16, 85, 0),
(170, 3071, 31, 26, 15, 6700, 58, 190, 1),
(171, 3072, 24, 21, 12, 4600, 40, 140, 1),
(172, 3073, 50, 40, 24, 10500, 90, 235, 1),
(173, 3074, 29, 24, 11, 5600, 36, 140, 0),
(174, 3075, 37, 17, 8, 7800, 72, 115, 1),
(175, 3076, 38, 32, 19, 9500, 68, 280, 1),
(176, 3077, 33, 28, 17, 7200, 58, 220, 0),
(177, 3078, 27, 23, 15, 5900, 48, 175, 1),
(178, 3079, 23, 19, 12, 4600, 32, 155, 0),
(179, 3080, 17, 15, 9, 3800, 17, 90, 1),
(180, 3081, 32, 27, 16, 6900, 60, 195, 1),
(181, 3082, 25, 22, 13, 4800, 42, 145, 0),
(182, 3083, 52, 42, 25, 11000, 95, 240, 1),
(183, 3084, 30, 25, 12, 5800, 38, 145, 1),
(184, 3085, 38, 18, 9, 8000, 75, 120, 1),
(185, 3086, 40, 34, 20, 10000, 70, 290, 0),
(186, 3087, 34, 29, 18, 7500, 60, 225, 1),
(187, 3088, 28, 24, 16, 6100, 50, 180, 0),
(188, 3089, 24, 20, 13, 4800, 34, 160, 1),
(189, 3090, 18, 16, 10, 4000, 18, 95, 0),
(190, 3091, 33, 28, 17, 7100, 62, 200, 1),
(191, 3092, 26, 23, 14, 5000, 44, 150, 1),
(192, 3093, 54, 44, 26, 11500, 100, 245, 1),
(193, 3094, 31, 26, 13, 6000, 40, 150, 0),
(194, 3095, 39, 19, 10, 8200, 78, 125, 1),
(195, 3096, 42, 36, 21, 10500, 72, 300, 1),
(196, 3097, 35, 30, 19, 7800, 62, 230, 0),
(197, 3098, 29, 25, 17, 6300, 52, 185, 1),
(198, 3099, 25, 21, 14, 5000, 36, 165, 0),
(199, 3100, 19, 17, 11, 4200, 19, 100, 1),
(200, 3101, 34, 29, 18, 7300, 64, 205, 1),
(201, 3102, 27, 24, 15, 5200, 46, 155, 0),
(202, 3103, 56, 46, 27, 12000, 105, 250, 1),
(203, 3104, 32, 27, 14, 6200, 42, 155, 1),
(204, 3105, 40, 20, 11, 8500, 80, 130, 1),
(205, 3106, 44, 38, 22, 11000, 74, 310, 0),
(206, 3107, 36, 31, 20, 8000, 64, 235, 1),
(207, 3108, 30, 26, 18, 6500, 54, 190, 0),
(208, 3109, 26, 22, 15, 5200, 38, 170, 1),
(209, 3110, 20, 18, 12, 4400, 20, 105, 0),
(210, 3111, 35, 30, 19, 7500, 66, 210, 1),

INSERT IGNORE INTO weapons (weaponID, gameID, weaponType, name) VALUES
(1001, 1, 'Assault Rifle', 'M4 Carbine'),
(1002, 2, 'Sniper Rifle', 'AWP'),
(1003, 3, 'Submachine Gun', 'MP5'),
(1004, 4, 'Pistol', 'Desert Eagle'),
(1005, 5, 'Shotgun', 'Pump-Action Shotgun'),
(1006, 6, 'Assault Rifle', 'AK-47'),
(1007, 7, 'Sniper Rifle', 'Barrett .50 cal'),
(1008, 8, 'Submachine Gun', 'P90'),
(1009, 9, 'Pistol', 'Glock-18'),
(1010, 10, 'Shotgun', 'Spas-12'),
(1011, 11, 'Assault Rifle', 'SCAR-H'),
(1012, 12, 'Sniper Rifle', 'M24'),
(1013, 13, 'Submachine Gun', 'Vector'),
(1014, 14, 'Pistol', 'USP'),
(1015, 15, 'Shotgun', 'Mossberg 500'),
(1016, 16, 'Assault Rifle', 'G36C'),
(1017, 17, 'Sniper Rifle', 'Kar98k'),
(1018, 18, 'Submachine Gun', 'UMP45'),
(1019, 19, 'Pistol', 'M1911'),
(1020, 20, 'Shotgun', 'Benelli M4'),
(1021, 21, 'Assault Rifle', 'FAMAS'),
(1022, 22, 'Sniper Rifle', 'SVD'),
(1023, 23, 'Submachine Gun', 'Kriss Vector'),
(1024, 24, 'Pistol', 'P226'),
(1025, 25, 'Shotgun', 'S12K'),
(1026, 26, 'Assault Rifle', 'Aug A3'),
(1027, 27, 'Sniper Rifle', 'CheyTac M200'),
(1028, 28, 'Submachine Gun', 'Tommy Gun'),
(1029, 29, 'Pistol', 'Beretta 92'),
(1030, 30, 'Shotgun', 'Double Barrel'),
(1031, 31, 'Assault Rifle', 'Galil AR'),
(1032, 32, 'Sniper Rifle', 'AWM'),
(1033, 33, 'Submachine Gun', 'Bizon'),
(1034, 34, 'Pistol', 'FN Five-seveN'),
(1035, 35, 'Shotgun', 'Saiga-12'),
(1036, 1, 'Assault Rifle', 'HK416'),
(1037, 2, 'Sniper Rifle', 'Remington 700'),
(1038, 3, 'Submachine Gun', 'MAC-10'),
(1039, 4, 'Pistol', 'CZ75'),
(1040, 5, 'Shotgun', 'Supernova'),
(1041, 6, 'Assault Rifle', 'M16A4'),
(1042, 7, 'Sniper Rifle', 'Dragunov'),
(1043, 8, 'Submachine Gun', 'MP7'),
(1044, 9, 'Pistol', 'Walther P99'),
(1045, 10, 'Shotgun', 'KSG'),
(1046, 11, 'Assault Rifle', 'F2000'),
(1047, 12, 'Sniper Rifle', 'VSS Vintorez'),
(1048, 13, 'Submachine Gun', 'PP-19 Bizon'),
(1049, 14, 'Pistol', 'Hi-Power'),
(1050, 15, 'Shotgun', 'DP-12'),
(1051, 16, 'Assault Rifle', 'Type 95'),
(1052, 17, 'Sniper Rifle', 'TRG-22'),
(1053, 18, 'Submachine Gun', 'G3SG1'),
(1054, 19, 'Pistol', 'Revolver R8'),
(1055, 20, 'Shotgun', 'AA-12'),
(1056, 21, 'Assault Rifle', 'ACR'),
(1057, 22, 'Sniper Rifle', 'SKS'),
(1058, 23, 'Submachine Gun', 'Thompson'),
(1059, 24, 'Pistol', 'USP-S'),
(1060, 25, 'Shotgun', 'Nova'),
(1061, 26, 'Assault Rifle', 'Groza'),
(1062, 27, 'Sniper Rifle', 'SV-98'),
(1063, 28, 'Submachine Gun', 'MP9'),
(1064, 29, 'Pistol', 'Tec-9'),
(1065, 30, 'Shotgun', 'M3 Super 90'),
(1066, 31, 'Assault Rifle', 'L85A2'),
(1067, 32, 'Sniper Rifle', 'Arctic Warfare'),
(1068, 33, 'Submachine Gun', 'MP5-SD'),
(1069, 34, 'Pistol', 'Five-seveN'),
(1070, 35, 'Shotgun', 'Mag-7'),
(1071, 1, 'Assault Rifle', 'FAL'),
(1072, 2, 'Sniper Rifle', 'Mosin-Nagant'),
(1073, 3, 'Submachine Gun', 'MPX'),
(1074, 4, 'Pistol', 'CZ P-09'),
(1075, 5, 'Shotgun', 'Striker'),
(1076, 6, 'Assault Rifle', 'Tavor X95'),
(1077, 7, 'Sniper Rifle', 'Intervention'),
(1078, 8, 'Submachine Gun', 'Honey Badger'),
(1079, 9, 'Pistol', 'P250'),
(1080, 10, 'Shotgun', 'Sawed-Off'),
(1081, 11, 'Assault Rifle', 'Oden'),
(1082, 12, 'Sniper Rifle', 'AX-50'),
(1083, 13, 'Submachine Gun', 'Fennec'),
(1084, 14, 'Pistol', 'X16'),
(1085, 15, 'Shotgun', 'Model 680'),
(1086, 16, 'Assault Rifle', 'Kilo 141'),
(1087, 17, 'Sniper Rifle', 'HDR'),
(1088, 18, 'Submachine Gun', 'MP7'),
(1089, 19, 'Pistol', 'Renetti'),
(1090, 20, 'Shotgun', 'R9-0'),
(1091, 21, 'Assault Rifle', 'M13'),
(1092, 22, 'Sniper Rifle', 'ZRG 20mm'),
(1093, 23, 'Submachine Gun', 'AUG'),
(1094, 24, 'Pistol', '1911'),
(1095, 25, 'Shotgun', '725'),
(1096, 26, 'Assault Rifle', 'AS VAL'),
(1097, 27, 'Sniper Rifle', 'LW3-Tundra'),
(1098, 28, 'Submachine Gun', 'AK-74u'),
(1099, 29, 'Pistol', 'Magnum'),
(1100, 30, 'Shotgun', 'Hauer 77'),
(1101, 31, 'Melee', 'Combat Knife'),
(1102, 32, 'Melee', 'Katana'),
(1103, 33, 'Melee', 'Axe'),
(1104, 34, 'Melee', 'Baseball Bat'),
(1105, 35, 'Melee', 'Sledgehammer'),
(1106, 1, 'Launcher', 'RPG-7'),
(1107, 2, 'Launcher', 'MGL-140'),
(1108, 3, 'Launcher', 'Grenade Launcher'),
(1109, 4, 'Launcher', 'Javelin'),
(1110, 5, 'Launcher', 'Stinger'),
(1111, 6, 'Light Machine Gun', 'M249'),
(1112, 7, 'Light Machine Gun', 'MG36'),
(1113, 8, 'Light Machine Gun', 'PKM'),
(1114, 9, 'Light Machine Gun', 'M60'),
(1115, 10, 'Light Machine Gun', 'Browning M2'),
(1116, 11, 'Light Machine Gun', 'L86 LSW'),
(1117, 12, 'Light Machine Gun', 'RPD'),
(1118, 13, 'Light Machine Gun', 'UL736'),
(1119, 14, 'Light Machine Gun', 'Holger-26'),
(1120, 15, 'Light Machine Gun', 'Chopper'),
(1121, 16, 'Assault Rifle', 'Volk'),
(1122, 17, 'Sniper Rifle', 'Gorenko Anti-Tank Rifle'),
(1123, 18, 'Submachine Gun', 'Sten'),
(1124, 19, 'Pistol', 'Welgun'),
(1125, 20, 'Shotgun', 'Combat Shotgun');

INSERT IGNORE INTO map (mapID, gameID, POIs, Name) VALUES
(1001, 1, 'Market, Tunnels, Courtyard', 'Dust II'),
(1002, 2, 'Mid, A-Long, B-Short', 'Mirage'),
(1003, 3, 'Water, Boiler, Catwalk', 'Inferno'),
(1004, 4, 'B-Ramp, Truck, Heaven', 'Cache'),
(1005, 5, 'Connector, A-Main, B-Main', 'Overpass'),
(1006, 6, 'A-Site, B-Site, Mid', 'Bind'),
(1007, 7, 'Tower, A-Main, Hookah', 'Haven'),
(1008, 8, 'A-Lobby, B-Lobby, Garden', 'Split'),
(1009, 9, 'A-Site, B-Site, Mid', 'Ascent'),
(1010, 10, 'A-Main, B-Main, C-Main', 'Icebox'),
(1011, 11, 'Market, Bank, T-Main', 'Fracture'),
(1012, 12, 'B-Site, Mid, A-Main', 'Pearl'),
(1013, 13, 'Upper, Lower, Mid', 'The Pit'),
(1014, 14, 'Train Yard, A-Site, B-Site', 'Crossfire'),
(1015, 15, 'Catacombs, Docks, Fortress', 'Uplink'),
(1016, 16, 'Library, Green, Blue', 'Terminal'),
(1017, 17, 'A-Lobby, B-Lobby, Bridge', 'Highrise'),
(1018, 18, 'Underpass, Tunnel, Bridge', 'Firing Range'),
(1019, 19, 'B-Site, Bridge, A-Site', 'Summit'),
(1020, 20, 'Tower, B-Main, A-Main', 'Nuketown'),
(1021, 21, 'Main Street, Building, Rooftop', 'Rust'),
(1022, 22, 'C-Site, B-Site, A-Site', 'Crash'),
(1023, 23, 'S-12, E-5, N-2', 'Verdansk'),
(1024, 24, 'Stadium, Airport, Downtown', 'Rebirth Island'),
(1025, 25, 'Train Station, Prison, Port', 'Caldera'),
(1026, 26, 'Capital, Docks, Bridge', 'Ashika Island'),
(1027, 27, 'A-Site, B-Site, C-Site', 'Shipment'),
(1028, 28, 'A-Site, B-Site, Mid', 'Vanguard'),
(1029, 29, 'Pillbox, Tunnel, Office', 'House'),
(1030, 30, 'Café, Library, Kitchen', 'Consulate'),
(1031, 31, 'Dorms, Bar, Garage', 'Oregon'),
(1032, 32, 'Throne Room, Bedroom, Kitchen', 'Kafe Dostoyevsky'),
(1033, 33, 'Engine Room, Cargo Bay, Control', 'Skyscraper'),
(1034, 34, 'Main, Mid, T-Side', 'Bank'),
(1035, 35, 'Mid, Side, Back', 'Chalet'),
(1036, 1, 'Market, Tunnels, Courtyard', 'Dust II 2'),
(1037, 2, 'Mid, A-Long, B-Short', 'Mirage 2'),
(1038, 3, 'Water, Boiler, Catwalk', 'Inferno 2'),
(1039, 4, 'B-Ramp, Truck, Heaven', 'Cache 2'),
(1040, 5, 'Connector, A-Main, B-Main', 'Overpass 2'),
(1041, 6, 'A-Site, B-Site, Mid', 'Bind 2'),
(1042, 7, 'Tower, A-Main, Hookah', 'Haven 2'),
(1043, 8, 'A-Lobby, B-Lobby, Garden', 'Split 2'),
(1044, 9, 'A-Site, B-Site, Mid', 'Ascent 2'),
(1045, 10, 'A-Main, B-Main, C-Main', 'Icebox 2'),
(1046, 11, 'Market, Bank, T-Main', 'Fracture 2'),
(1047, 12, 'B-Site, Mid, A-Main', 'Pearl 2'),
(1048, 13, 'Upper, Lower, Mid', 'The Pit 2'),
(1049, 14, 'Train Yard, A-Site, B-Site', 'Crossfire 2'),
(1050, 15, 'Catacombs, Docks, Fortress', 'Uplink 2'),
(1051, 16, 'Library, Green, Blue', 'Terminal 2'),
(1052, 17, 'A-Lobby, B-Lobby, Bridge', 'Highrise 2'),
(1053, 18, 'Underpass, Tunnel, Bridge', 'Firing Range 2'),
(1054, 19, 'B-Site, Bridge, A-Site', 'Summit 2'),
(1055, 20, 'Tower, B-Main, A-Main', 'Nuketown 2'),
(1056, 21, 'Main Street, Building, Rooftop', 'Rust 2'),
(1057, 22, 'C-Site, B-Site, A-Site', 'Crash 2'),
(1058, 23, 'S-12, E-5, N-2', 'Verdansk 2'),
(1059, 24, 'Stadium, Airport, Downtown', 'Rebirth Island 2'),
(1060, 25, 'Train Station, Prison, Port', 'Caldera 2'),
(1061, 26, 'Capital, Docks, Bridge', 'Ashika Island 2'),
(1062, 27, 'A-Site, B-Site, C-Site', 'Shipment 2'),
(1063, 28, 'A-Site, B-Site, Mid', 'Vanguard 2'),
(1064, 29, 'Pillbox, Tunnel, Office', 'House 2'),
(1065, 30, 'Café, Library, Kitchen', 'Consulate 2'),
(1066, 31, 'Dorms, Bar, Garage', 'Oregon 2'),
(1067, 32, 'Throne Room, Bedroom, Kitchen', 'Kafe Dostoyevsky 2'),
(1068, 33, 'Engine Room, Cargo Bay, Control', 'Skyscraper 2'),
(1069, 34, 'Main, Mid, T-Side', 'Bank 2'),
(1070, 35, 'Mid, Side, Back', 'Chalet 2');

INSERT IGNORE INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought) VALUES
(100, 1, 120.5, 55, 0.450, 10),
(100, 2, 85.3, 30, 0.325, 5),
(100, 3, 210.0, 98, 0.512, 12),
(100, 4, 95.7, 45, 0.298, 8),
(100, 5, 150.1, 75, 0.485, 15),
(100, 6, 60.4, 25, 0.301, 7),
(100, 7, 180.2, 88, 0.499, 11),
(100, 8, 105.6, 52, 0.387, 9),
(100, 9, 220.8, 110, 0.550, 14),
(100, 10, 75.9, 40, 0.355, 6),
(100, 11, 195.0, 95, 0.505, 13),
(100, 12, 115.3, 60, 0.410, 10),
(100, 13, 240.7, 125, 0.601, 16),
(100, 14, 88.2, 42, 0.315, 8),
(100, 15, 165.4, 80, 0.477, 11),
(100, 16, 72.1, 38, 0.345, 7),
(100, 17, 205.9, 105, 0.530, 14),
(100, 18, 130.6, 65, 0.425, 10),
(100, 19, 255.3, 130, 0.615, 18),
(100, 20, 90.0, 48, 0.360, 9),
(100, 21, 175.8, 85, 0.490, 12),
(100, 22, 68.9, 35, 0.333, 6),
(100, 23, 235.5, 120, 0.580, 15),
(100, 24, 112.4, 58, 0.405, 11),
(100, 25, 260.1, 140, 0.650, 20),
(100, 26, 80.5, 41, 0.305, 7),
(100, 27, 188.7, 92, 0.502, 13),
(100, 28, 77.2, 39, 0.310, 8),
(100, 29, 215.6, 115, 0.565, 16),
(100, 30, 108.9, 56, 0.395, 9),
(100, 31, 245.0, 135, 0.620, 17),
(100, 32, 65.8, 32, 0.295, 6),
(100, 33, 199.3, 100, 0.520, 14),
(100, 34, 145.5, 70, 0.440, 10),
(100, 35, 225.0, 128, 0.590, 18),
(101, 1, 122.5, 57, 0.455, 11),
(101, 2, 86.3, 31, 0.330, 6),
(101, 3, 212.0, 100, 0.515, 13),
(101, 4, 96.7, 47, 0.300, 9),
(101, 5, 152.1, 78, 0.490, 16),
(101, 6, 61.4, 26, 0.305, 8),
(101, 7, 182.2, 90, 0.504, 12),
(101, 8, 106.6, 54, 0.390, 10),
(101, 9, 222.8, 112, 0.555, 15),
(101, 10, 76.9, 41, 0.360, 7),
(101, 11, 197.0, 97, 0.510, 14),
(101, 12, 116.3, 62, 0.415, 11),
(101, 13, 242.7, 127, 0.605, 17),
(101, 14, 89.2, 43, 0.320, 9),
(101, 15, 167.4, 82, 0.482, 12),
(101, 16, 73.1, 39, 0.350, 8),
(101, 17, 207.9, 107, 0.535, 15),
(101, 18, 131.6, 67, 0.430, 11),
(101, 19, 257.3, 132, 0.620, 19),
(101, 20, 91.0, 49, 0.365, 10),
(101, 21, 177.8, 87, 0.495, 13),
(101, 22, 69.9, 36, 0.338, 7),
(101, 23, 237.5, 122, 0.585, 16),
(101, 24, 113.4, 60, 0.410, 12),
(101, 25, 262.1, 142, 0.655, 21),
(101, 26, 81.5, 42, 0.310, 8),
(101, 27, 189.7, 94, 0.507, 14),
(101, 28, 78.2, 40, 0.315, 9),
(101, 29, 217.6, 117, 0.570, 17),
(101, 30, 109.9, 58, 0.400, 10),
(101, 31, 247.0, 137, 0.625, 18),
(101, 32, 66.8, 33, 0.300, 7),
(101, 33, 201.3, 102, 0.525, 15),
(101, 34, 146.5, 72, 0.445, 11),
(101, 35, 227.0, 130, 0.595, 19),
(102, 1, 124.5, 59, 0.460, 12),
(102, 2, 87.3, 32, 0.335, 7),
(102, 3, 214.0, 102, 0.520, 14),
(102, 4, 97.7, 49, 0.305, 10),
(102, 5, 154.1, 80, 0.495, 17),
(102, 6, 62.4, 27, 0.310, 9),
(102, 7, 184.2, 92, 0.509, 13),
(102, 8, 107.6, 56, 0.395, 11),
(102, 9, 224.8, 114, 0.560, 16),
(102, 10, 77.9, 42, 0.365, 8),
(102, 11, 199.0, 99, 0.515, 15),
(102, 12, 117.3, 64, 0.420, 12),
(102, 13, 244.7, 129, 0.610, 18),
(102, 14, 90.2, 44, 0.325, 10),
(102, 15, 169.4, 84, 0.487, 13),
(102, 16, 74.1, 40, 0.355, 9),
(102, 17, 209.9, 109, 0.540, 16),
(102, 18, 132.6, 69, 0.435, 12),
(102, 19, 259.3, 134, 0.625, 20),
(102, 20, 92.0, 50, 0.370, 11),
(102, 21, 179.8, 89, 0.500, 14),
(102, 22, 70.9, 37, 0.343, 8),
(102, 23, 239.5, 124, 0.590, 17),
(102, 24, 114.4, 62, 0.415, 13),
(102, 25, 264.1, 144, 0.660, 22),
(102, 26, 82.5, 43, 0.315, 9),
(102, 27, 190.7, 96, 0.512, 15),
(102, 28, 79.2, 41, 0.320, 10),
(102, 29, 219.6, 119, 0.575, 18),
(102, 30, 110.9, 60, 0.405, 11),
(102, 31, 249.0, 139, 0.630, 19),
(102, 32, 67.8, 34, 0.305, 8),
(102, 33, 203.3, 104, 0.530, 16),
(102, 34, 147.5, 74, 0.450, 12),
(102, 35, 229.0, 132, 0.600, 20);

INSERT IGNORE INTO mapStats (statTableID, mapID, kills, wins, losses) VALUES
(108, 117, 2, 9, 5),
(171, 137, 20, 8, 1),
(174, 169, 23, 10, 0),
(105, 111, 5, 8, 4),
(117, 129, 22, 8, 10),
(139, 163, 25, 2, 9),
(157, 149, 2, 1, 2),
(181, 147, 28, 4, 3),
(131, 101, 16, 5, 5),
(122, 173, 25, 8, 6),
(181, 174, 4, 0, 1),
(144, 130, 24, 4, 2),
(128, 123, 18, 2, 2),
(120, 173, 6, 4, 4),
(134, 148, 6, 2, 2),
(143, 115, 9, 6, 8),
(176, 140, 1, 9, 0),
(107, 151, 12, 6, 10),
(121, 182, 21, 9, 9),
(144, 175, 12, 6, 9),
(123, 151, 27, 0, 4),
(131, 166, 18, 7, 8),
(148, 175, 3, 10, 2),
(109, 137, 1, 8, 0),
(153, 177, 16, 8, 3),
(162, 106, 19, 10, 1),
(159, 144, 19, 4, 2),
(160, 143, 16, 4, 4),
(161, 126, 12, 6, 2),
(137, 116, 29, 3, 3),
(127, 144, 19, 6, 5),
(102, 155, 10, 10, 10),
(167, 169, 19, 1, 3),
(160, 153, 18, 1, 2),
(185, 161, 6, 2, 2),
(155, 130, 12, 6, 9),
(182, 168, 7, 8, 1),
(124, 155, 7, 0, 4),
(158, 175, 14, 0, 2),
(154, 129, 24, 5, 8),
(131, 148, 16, 10, 8),
(127, 185, 8, 9, 3),
(156, 134, 14, 0, 1),
(184, 183, 4, 2, 6),
(140, 173, 29, 5, 6),
(126, 172, 1, 4, 6),
(128, 112, 5, 4, 4),
(178, 103, 4, 7, 6),
(133, 110, 17, 9, 9),
(146, 162, 12, 7, 1),
(145, 185, 21, 4, 9),
(118, 153, 19, 4, 6),
(179, 102, 1, 3, 0),
(125, 175, 7, 8, 6),
(180, 132, 26, 5, 4),
(115, 143, 20, 2, 0),
(165, 167, 5, 6, 4),
(163, 157, 17, 5, 4),
(173, 152, 9, 2, 3),
(172, 164, 10, 1, 0),
(130, 175, 24, 2, 5),
(149, 171, 21, 8, 6),
(145, 124, 17, 9, 4),
(183, 125, 2, 0, 8),
(153, 108, 5, 1, 2),
(166, 140, 9, 9, 1),
(170, 142, 29, 3, 9),
(102, 138, 16, 2, 2),
(135, 121, 20, 0, 0),
(164, 127, 6, 9, 0),
(150, 160, 20, 2, 9),
(138, 146, 0, 7, 1),
(172, 105, 19, 4, 8),
(122, 104, 9, 3, 7),
(159, 182, 29, 4, 7),
(147, 152, 9, 5, 8),
(103, 184, 8, 8, 7),
(138, 103, 19, 0, 7),
(173, 133, 28, 4, 0),
(107, 114, 12, 9, 2),
(105, 116, 15, 8, 4),
(165, 163, 8, 1, 6),
(172, 165, 9, 0, 5),
(183, 104, 0, 1, 9),
(102, 173, 15, 1, 1),
(155, 134, 25, 9, 7),
(128, 156, 16, 8, 9),
(115, 158, 6, 0, 8),
(126, 141, 2, 3, 6),
(145, 172, 13, 3, 6),
(104, 125, 13, 1, 1),
(150, 175, 21, 4, 2),
(153, 142, 21, 6, 8),
(132, 183, 8, 0, 5),
(165, 177, 0, 4, 4),
(118, 136, 16, 2, 5),
(106, 166, 17, 7, 3),
(120, 170, 6, 2, 6),
(157, 181, 16, 6, 8),
(124, 137, 15, 5, 4),
(121, 136, 5, 9, 8),
(166, 135, 1, 4, 4),
(110, 139, 1, 7, 9),
(114, 143, 10, 8, 6),
(101, 149, 8, 8, 3),
(116, 140, 28, 9, 5),
(119, 102, 15, 2, 6),
(148, 178, 8, 1, 8),
(176, 150, 8, 5, 7),
(177, 174, 20, 6, 6),
(163, 129, 28, 0, 8),
(140, 172, 19, 8, 1),
(130, 119, 10, 5, 2),
(109, 171, 18, 2, 6),
(169, 167, 0, 7, 4),
(103, 108, 9, 8, 2),
(178, 124, 0, 0, 4),
(180, 133, 17, 0, 5);
;

INSERT INTO matches (gameID, mapID, matchDate, matchType, lobbyRank) VALUES
(21, 1002, '2024-03-23 20:05:27', 'Casual', 'Immortal'),
(14, 1052, '2024-02-28 18:31:23', 'Scrim', 'Iron'),
(34, 1022, '2024-05-02 16:02:51', 'Ranked', 'Gold'),
(22, 1005, '2024-01-01 20:05:39', 'Custom', 'Iron'),
(33, 1041, '2024-05-01 13:59:45', 'Casual', 'Silver'),
(28, 1049, '2024-06-04 11:03:57', 'Scrim', 'Bronze'),
(16, 1044, '2025-05-08 05:34:44', 'Scrim', 'Diamond'),
(20, 1036, '2024-06-09 08:43:28', 'Custom', 'Ascendant'),
(14, 1009, '2024-09-10 23:24:14', 'Custom', 'Radiant'),
(31, 1035, '2025-02-22 08:12:18', 'Custom', 'Ascendant'),
(14, 1017, '2024-05-06 17:57:05', 'Ranked', 'Ascendant'),
(8, 1022, '2024-08-10 10:34:41', 'Scrim', 'Platinum'),
(15, 1058, '2024-06-25 20:23:38', 'Tournament', 'Radiant'),
(12, 1054, '2025-01-26 01:27:23', 'Casual', 'Ascendant'),
(16, 1033, '2025-04-09 00:18:41', 'Scrim', 'Gold'),
(18, 1055, '2024-06-26 02:15:48', 'Casual', 'Silver'),
(3, 1032, '2025-01-08 10:16:38', 'Tournament', 'Immortal'),
(25, 1017, '2024-12-16 03:04:05', 'Ranked', 'Silver'),
(8, 1049, '2024-05-16 18:41:46', 'Tournament', 'Silver'),
(8, 1008, '2024-03-17 01:16:03', 'Casual', 'Radiant'),
(2, 1003, '2024-06-03 00:39:45', 'Casual', 'Silver'),
(35, 1064, '2024-11-01 05:47:14', 'Tournament', 'Bronze'),
(12, 1060, '2025-08-10 22:24:09', 'Casual', 'Immortal'),
(7, 1064, '2024-11-01 00:55:18', 'Casual', 'Radiant'),
(9, 1020, '2025-03-30 14:53:15', 'Custom', 'Radiant'),
(3, 1011, '2024-04-30 06:18:34', 'Custom', 'Iron'),
(32, 1023, '2024-12-20 16:40:35', 'Scrim', 'Immortal'),
(13, 1025, '2024-09-09 19:43:51', 'Custom', 'Bronze'),
(31, 1042, '2025-02-28 23:15:39', 'Tournament', 'Diamond'),
(19, 1058, '2025-01-28 07:38:32', 'Tournament', 'Silver'),
(19, 1016, '2025-03-12 13:14:08', 'Casual', 'Silver'),
(20, 1006, '2025-04-27 01:44:12', 'Scrim', 'Diamond'),
(26, 1041, '2024-01-21 05:37:26', 'Tournament', 'Ascendant'),
(32, 1027, '2024-11-22 02:46:56', 'Ranked', 'Platinum'),
(1, 1066, '2024-02-03 09:14:16', 'Custom', 'Gold'),
(24, 1011, '2024-10-06 06:10:08', 'Custom', 'Immortal'),
(29, 1028, '2024-07-08 03:19:26', 'Ranked', 'Immortal'),
(26, 1067, '2025-07-07 10:25:33', 'Scrim', 'Ascendant'),
(20, 1068, '2025-07-21 19:04:13', 'Tournament', 'Radiant'),
(31, 1061, '2024-07-20 18:26:59', 'Scrim', 'Silver'),
(18, 1002, '2024-02-14 03:29:53', 'Ranked', 'Silver'),
(9, 1030, '2024-05-29 15:54:31', 'Casual', 'Immortal'),
(21, 1066, '2024-08-19 16:54:06', 'Custom', 'Gold'),
(21, 1065, '2024-01-20 09:27:59', 'Tournament', 'Radiant'),
(7, 1051, '2025-04-15 08:53:19', 'Tournament', 'Radiant'),
(27, 1058, '2025-05-14 23:50:13', 'Casual', 'Immortal'),
(14, 1057, '2025-07-02 17:26:22', 'Tournament', 'Radiant'),
(19, 1047, '2024-11-14 04:18:47', 'Tournament', 'Gold'),
(6, 1036, '2024-06-10 04:02:52', 'Casual', 'Radiant'),
(1, 1066, '2024-07-10 03:37:31', 'Tournament', 'Iron'),
(30, 1070, '2024-10-30 09:00:04', 'Casual', 'Radiant'),
(19, 1006, '2024-08-25 09:17:51', 'Custom', 'Gold'),
(28, 1019, '2024-02-01 01:10:39', 'Tournament', 'Iron'),
(25, 1013, '2024-10-20 11:38:22', 'Custom', 'Iron');


