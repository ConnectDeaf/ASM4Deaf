-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: dbserver.in.cs.ucy.ac.cy
-- Generation Time: Oct 18, 2022 at 12:39 PM
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
-- Table structure for table `photos`
--

CREATE TABLE `photos` (
  `id` int(11) NOT NULL,
  `username` bigint(20) NOT NULL,
  `name` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `target_file` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `download_file` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `face` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `photos`
--

INSERT INTO `photos` (`id`, `username`, `name`, `category`, `target_file`, `download_file`, `face`) VALUES
(5, 1, '', 'diversity,sustainability,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/University_of_Cyprus_en.jpg', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/University_of_Cyprus_en.jpg', ''),
(4, 1, '', 'diversity,sustainability,', '/sys-data/WebData/projects/asm4deaf/wp-content/plugins/interface/uploads/University_of_Cyprus_en.jpg', 'http://asm4deaf.eu/wp-content/plugins/interface/uploads/University_of_Cyprus_en.jpg', 'happy'),
(3, 1, '', 'sustainability,', 'test.txt', 'test.txt', 'happy');

INSERT INTO `photos` (`id`, `username`, `name`, `category`, `target_file`, `download_file`, `face`) VALUES
(1, 1, '', 'diversity,sustainability,', 'University_of_Cyprus_en.jpg', 'University_of_Cyprus_en.jpg', '');
--
-- Indexes for dumped tables
--

--
-- Indexes for table `photos`
--
ALTER TABLE `photos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `photos`
--
ALTER TABLE `photos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
