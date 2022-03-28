-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2022 at 03:49 PM
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
-- Table structure for table `fullbodys`
--

CREATE TABLE `fullbodys` (
  `FullBodyID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `VideoURL` varchar(1000) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL,
  `TorsoID` int(11) NOT NULL,
  `HeadID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `heads`
--

CREATE TABLE `heads` (
  `HeadID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `VideoURL` varchar(1000) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `masks`
--

CREATE TABLE `masks` (
  `MaskID` int(11) NOT NULL,
  `MaskURL` varchar(1000) NOT NULL,
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
(1, 'White'),
(2, 'Black / African American'),
(3, 'Native Hawaiian / Pacific Islander'),
(4, 'Asian'),
(5, 'American Indian / Alaska Native');

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
(1, 'American');

-- --------------------------------------------------------

--
-- Table structure for table `torsos`
--

CREATE TABLE `torsos` (
  `TorsoID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `VideoURL` varchar(1000) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

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
-- Indexes for table `heads`
--
ALTER TABLE `heads`
  ADD PRIMARY KEY (`HeadID`),
  ADD KEY `heads_to_signerraces` (`RaceID`),
  ADD KEY `heads_to_signlanguages` (`LanguageID`);

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
-- Indexes for table `torsos`
--
ALTER TABLE `torsos`
  ADD PRIMARY KEY (`TorsoID`),
  ADD KEY `torsos_to_signerraces` (`RaceID`),
  ADD KEY `torsos_to_signlanguages` (`LanguageID`);

--
-- AUTO_INCREMENT for dumped tables
--

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

ALTER TABLE `heads`
  MODIFY `HeadID` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `torsos`
  MODIFY `TorsoID` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `Fullbodys`
  MODIFY `FullBodyID` int(11) NOT NULL AUTO_INCREMENT;


--
-- Constraints for dumped tables
--

--
-- Constraints for table `fullbodys`
--
ALTER TABLE `fullbodys`
  ADD CONSTRAINT `fullbodys_ibfk_1` FOREIGN KEY (`TorsoID`) REFERENCES `torsos` (`TorsoID`),
  ADD CONSTRAINT `fullbodys_ibfk_2` FOREIGN KEY (`HeadID`) REFERENCES `heads` (`HeadID`),
  ADD CONSTRAINT `fullbodys_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fullbodys_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `heads`
--
ALTER TABLE `heads`
  ADD CONSTRAINT `heads_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `heads_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `masks`
--
ALTER TABLE `masks`
  ADD CONSTRAINT `masks_ibfk_1` FOREIGN KEY (`FullBodyID`) REFERENCES `fullbodys` (`FullBodyID`);

--
-- Constraints for table `torsos`
--
ALTER TABLE `torsos`
  ADD CONSTRAINT `torsos_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `torsos_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
