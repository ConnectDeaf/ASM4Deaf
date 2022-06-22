-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2022 at 11:41 AM
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
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `ImageID` int(11) NOT NULL,
  `FileName` varchar(100) NOT NULL
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
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Email`, `PwdSaltedDigest`, `IsVerified`) VALUES
(1, 'stavroullakoumou.a2@gmail.com', 0x378a80fba951acdc9da611bafa72a825482081beadf29545a102934fef6bf2d5b058dd16e75068c067e27283224954e9b112b8c3851717c32929b8127abbccd9, 1);

-- --------------------------------------------------------

--
-- Table structure for table `videos`
--

CREATE TABLE `videos` (
  `VideoID` int(11) NOT NULL,
  `Keywords` varchar(200) NOT NULL,
  `FileName` varchar(100) NOT NULL,
  `RaceID` int(11) DEFAULT NULL,
  `LanguageID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `videos`
--

INSERT INTO `videos` (`VideoID`, `Keywords`, `FileName`, `RaceID`, `LanguageID`) VALUES
(1, 'aaaa', 'gif_1655884180.mp4', 1, 1),
(2, 'aaa', 'video_1655885064.mp4', 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`ImageID`);

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
-- Indexes for table `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`VideoID`),
  ADD KEY `videos_to_signerraces` (`RaceID`),
  ADD KEY `videos_to_signlanguages` (`LanguageID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `ImageID` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `videos`
--
ALTER TABLE `videos`
  MODIFY `VideoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `videos_to_signerraces` FOREIGN KEY (`RaceID`) REFERENCES `signerraces` (`RaceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `videos_to_signlanguages` FOREIGN KEY (`LanguageID`) REFERENCES `signlanguages` (`LanguageID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
