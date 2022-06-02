-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 14, 2022 at 03:18 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `asm4deaf`
--

-- --------------------------------------------------------

--
-- Table structure for table `bodyparts`
--

CREATE TABLE `bodyparts` (
  `BodyPartID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `FileName` varchar(100) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL,
  `PartType` varchar(1) NOT NULL COMMENT '''h'' for head, ''t'' for torso'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Table structure for table `fullbodys`
--

CREATE TABLE `fullbodys` (
  `FullBodyID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `FileName` varchar(100) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL,
  `TorsoID` int(11) NOT NULL,
  `HeadID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `masks`
--

CREATE TABLE `masks` (
  `MaskID` int(11) NOT NULL,
  `FileName` varchar(100) NOT NULL,
  `FullBodyID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `signerraces`
--

CREATE TABLE `signerraces` (
  `RaceID` int(11) NOT NULL,
  `RaceName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `signerraces`
--

INSERT INTO `signerraces` (`RaceID`, `RaceName`) VALUES
(1, 'white'),
(2, 'black / african american'),
(3, 'native hawaiian / pacific islander'),
(4, 'asian'),
(5, 'american indian / alaska native');

-- --------------------------------------------------------

--
-- Table structure for table `signlanguages`
--

CREATE TABLE `signlanguages` (
  `LanguageID` int(11) NOT NULL,
  `LanguageName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `signlanguages`
--

INSERT INTO `signlanguages` (`LanguageID`, `LanguageName`) VALUES
(1, 'american');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `PwdSaltedDigest` tinyblob NOT NULL,
  `IsVerified` int(1) NOT NULL DEFAULT 0 COMMENT '0 for unverified, 1 for verified'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bodyparts`
--
ALTER TABLE `bodyparts`
  ADD PRIMARY KEY (`BodyPartID`),
  ADD KEY `BodyParts_to_signerraces` (`RaceID`),
  ADD KEY `BodyParts_to_signlanguages` (`LanguageID`);

--
-- Indexes for table `fullbodys`
--
ALTER TABLE `fullbodys`
  ADD PRIMARY KEY (`FullBodyID`),
  ADD KEY `TorsoID` (`TorsoID`),
  ADD KEY `HeadID` (`HeadID`),
  ADD KEY `fullbodys_to_signerraces` (`RaceID`),
  ADD KEY `fullbodys_to_signlanguages` (`LanguageID`);

--
-- Indexes for table `masks`
--
ALTER TABLE `masks`
  ADD PRIMARY KEY (`MaskID`),
  ADD KEY `FullBodyID` (`FullBodyID`);

--
-- Indexes for table `signerraces`
--
ALTER TABLE `signerraces`
  ADD PRIMARY KEY (`RaceID`);

--
-- Indexes for table `signlanguages`
--
ALTER TABLE `signlanguages`
  ADD PRIMARY KEY (`LanguageID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bodyparts`
--
ALTER TABLE `bodyparts`
  MODIFY `BodyPartID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `fullbodys`
--
ALTER TABLE `fullbodys`
  MODIFY `FullBodyID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `signerraces`
--
ALTER TABLE `signerraces`
  MODIFY `RaceID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `signlanguages`
--
ALTER TABLE `signlanguages`
  MODIFY `LanguageID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;


--
-- Constraints for dumped tables
--

--
-- Constraints for table `bodyparts`
--
ALTER TABLE `bodyparts`
  ADD CONSTRAINT `BodyParts_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `BodyParts_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `fullbodys`
--
ALTER TABLE `fullbodys`
  ADD CONSTRAINT `fullbodys_ibfk_1` FOREIGN KEY (`TorsoID`) REFERENCES `bodyparts` (`BodyPartID`),
  ADD CONSTRAINT `fullbodys_ibfk_2` FOREIGN KEY (`HeadID`) REFERENCES `bodyparts` (`BodyPartID`),
  ADD CONSTRAINT `fullbodys_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fullbodys_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `masks`
--
ALTER TABLE `masks`
  ADD CONSTRAINT `masks_ibfk_1` FOREIGN KEY (`FullBodyID`) REFERENCES `fullbodys` (`FullBodyID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
