DROP DATABASE IF EXISTS `OmniDatabase`;
CREATE DATABASE `OmniDatabase`;
USE `OmniDatabase`;


DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
   gameID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   name VARCHAR(50) NOT NULL,
);


DROP TABLE IF EXISTS `profiles`;
CREATE TABLE `profiles` (
   profileID INT PRIMARY KEY AUTO_INCREMENT,
   username VARCHAR(20) NOT NULL,
   isAdmin BOOLEAN,
   isPublic BOOLEAN,
   isPremium BOOLEAN,
   password VARCHAR(20) NOT NULL
);


DROP TABLE IF EXISTS `gamesProfiles`;
CREATE TABLE `gamesProfiles` (
   gameInstanceID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameID INT NOT NULL,
   profileID INT NOT NULL,
   gameUsername VARCHAR(30),
   showOnDashboard BOOLEAN,
   FOREIGN KEY (gameID) REFERENCES games(gameID),
   FOREIGN KEY (profileID) REFERENCES profiles(profileID)
);


DROP TABLE IF EXISTS `playerStats`;
CREATE TABLE `playerStats` (
   statTableID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameInstanceID INT NOT NULL,
   kills INT NOT NULL,
   deaths INT NOT NULL,
   assists INT NOT NULL,
   totalDamage INT NOT NULL,
   totalHeadshots INT NOT NULL,
   totalShotsHit INT NOT NULL,
   totalWins INT NOT NULL,
   FOREIGN KEY (gameInstanceID) REFERENCES gamesProfiles(gameInstanceID)
);


DROP TABLE IF EXISTS `weapons`;
CREATE TABLE `weapons` (
   weaponID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameID INT NOT NULL,
   weaponType VARCHAR(50),
   name VARCHAR(50),
   FOREIGN KEY (gameID) REFERENCES games(gameID)
);


DROP TABLE IF EXISTS `map`;
CREATE TABLE `map` (
   mapID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameID INT NOT NULL,
   POIs VARCHAR(50),
   Name VARCHAR(50),
   FOREIGN KEY (gameID) REFERENCES games(gameID)
);


DROP TABLE IF EXISTS `weaponStats`;
CREATE TABLE `weaponStats` (
   statTableID INT NOT NULL,
   weaponID INT NOT NULL,
   totalUsageTime DOUBLE(4, 3) NOT NULL,
   kills INT NOT NULL,
   accuracy DOUBLE(4,3),
   amountBought INT,
   FOREIGN KEY (statTableID) REFERENCES playerStats(statTableID),
   FOREIGN KEY (weaponID) REFERENCES weapons(weaponID)
);


DROP TABLE IF EXISTS `mapStats`;
CREATE TABLE `mapStats` (
   statTableID INT NOT NULL,
   gameID INT NOT NULL,
   weaponType VARCHAR(50),
   name VARCHAR(50) NOT NULL,
   FOREIGN KEY (statTableID) REFERENCES playerStats(statTableID),
   FOREIGN KEY (gameID) REFERENCES games(gameID)
);


DROP TABLE IF EXISTS `matches`;
CREATE TABLE `matches` (
   matchID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameID INT NOT NULL,
   mapID INT NOT NULL,
   matchDate DATETIME NOT NULL,
   matchType VARCHAR(20),
   lobbyRank VARCHAR(15),
   FOREIGN KEY (gameID) REFERENCES games(gameID),
   FOREIGN KEY (mapID) REFERENCES map(mapID)
);


DROP TABLE IF EXISTS `matchStats`;
CREATE TABLE `matchStats` (
   matchStatsID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   matchID INT NOT NULL,
   gameInstanceID INT NOT NULL,
   kills INT,
   deaths INT,
   assists INT,
   Headshots INT,
   TotalShots INT,
   shotsHit INT,
   matchDuration INT,
   rounds INT,
   win BOOLEAN,
   damageDealt INT,
   firstBloods INT,
   FOREIGN KEY (matchID) REFERENCES matches(matchID),
   FOREIGN KEY (gameInstanceID) REFERENCES gamesProfiles(gameInstanceID)
);


DROP TABLE IF EXISTS `goals`;
CREATE TABLE `goals` (
   goalsID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
   gameID INT NOT NULL,
   dateCreated DATETIME NOT NULL,
   dateAchieved DATETIME,
   description VARCHAR(100),
   FOREIGN KEY (gameID) REFERENCES games(`gameID`)
);


DROP TABLE IF EXISTS `milestones`;
CREATE TABLE `milestones`
(
   milestoneID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
   profileID   INT NOT NULL,
   goalID      INT NOT NULL,
   FOREIGN KEY (profileID) REFERENCES profiles (profileID),
   FOREIGN KEY (goalID) REFERENCES goals (goalsID)
);
