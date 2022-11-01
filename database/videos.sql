-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: dbserver.in.cs.ucy.ac.cy
-- Generation Time: Oct 18, 2022 at 11:20 AM
-- Server version: 10.5.10-MariaDB
-- PHP Version: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
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
-- Table structure for table `videos`
--

CREATE TABLE `videos` (
  `id` int(11) NOT NULL,
  `username` bigint(20) NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `keywords` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `target_file` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `download_file` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtitles` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `race` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `hand` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `videos`
--

INSERT INTO `videos` (`id`, `username`, `title`, `keywords`, `target_file`, `download_file`, `subtitles`, `country`, `race`, `gender`, `hand`) VALUES
(48, 1, 'testing', 'ICT,participation,sustainability,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', '', '', '', '', 'american'),
(49, 1, 'testing', 'diversity,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', '', '', '', '', ''),
(50, 1, 'Testr', 'participation,sustainability,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', 'yes', '', '', '', ''),
(51, 1, 'afrteat', 'sustainability,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', 'no', 'Bahamas', '', '', ''),
(52, 1, 'new test', 'creative,participation,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', 'yes', 'Dominica', 'american_india', '', ''),
(53, 1, 'et', 'inclusive,social,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', 'yes', 'Iraq', 'black', 'male', ''),
(54, 1, 'refsgh', 'participation,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/tes.mp4', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/tes.mp4', 'yes', 'Cyprus', 'white', 'female', 'left');

INSERT INTO `videos` (`id`, `username`, `title`, `keywords`, `target_file`, `download_file`, `subtitles`, `country`, `race`, `gender`, `hand`) VALUES
(55, 1, 'new_test', 'sustainability', 'video_1665401083.mp4', 'video_1665401083.mp4', '', '', '', '', 'american');
-- Indexes for dumped tables
--

--
-- Indexes for table `videos`
--
ALTER TABLE `videos` ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
