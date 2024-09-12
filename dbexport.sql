-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 12, 2024 at 02:11 PM
-- Server version: 8.0.32
-- PHP Version: 8.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cafeteria`
--
CREATE DATABASE IF NOT EXISTS `cafeteria` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `cafeteria`;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `custCode` int NOT NULL,
  `name` varchar(25) DEFAULT NULL,
  `custType` varchar(7) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL
) ;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`custCode`, `name`, `custType`, `status`) VALUES
(1, 'Ms. Deivanai', 'Staff', 'A'),
(2, 'Ms. Shanthi', 'Staff', 'A'),
(3, 'Mr. Rethina Kumar', 'Staff', 'A'),
(4, 'Ms. Vijayalakshmi', 'Staff', 'A'),
(5, 'Amuthavanan', 'Student', 'A'),
(6, 'Darshan', 'Student', 'A'),
(7, 'Dhaniel Paresh', 'Student', 'A'),
(8, 'Elango', 'Student', 'A'),
(9, 'Gladson', 'Student', 'A'),
(10, 'Harish Kumar', 'Student', 'A'),
(11, 'Imesh Karthick', 'Student', 'A'),
(12, 'Jitendar Dhariwal', 'Student', 'A'),
(13, 'Kanishkumar', 'Student', 'A'),
(14, 'Md. Fardeen Shariff', 'Student', 'A'),
(15, 'Monish', 'Student', 'A'),
(16, 'Nishanth', 'Student', 'A'),
(17, 'Sai Srikar', 'Student', 'A'),
(18, 'Sakthi Saran', 'Student', 'A'),
(19, 'Sanjay', 'Student', 'A'),
(20, 'Srimanikandan', 'Student', 'A'),
(21, 'Visweshwaran', 'Student', 'A'),
(22, 'Akshaya Nivasini', 'Student', 'A'),
(23, 'Darsha', 'Student', 'A'),
(24, 'Harini', 'Student', 'A'),
(25, 'Harshitha P R', 'Student', 'A'),
(26, 'Harshitha S', 'Student', 'A'),
(27, 'Jacintha', 'Student', 'A'),
(28, 'Joshitha', 'Student', 'A'),
(29, 'Jude Inika', 'Student', 'A'),
(30, 'Keerthana', 'Student', 'A'),
(31, 'Nivethaasree', 'Student', 'A'),
(32, 'Pavithra', 'Student', 'A'),
(33, 'Pratiksha', 'Student', 'A'),
(34, 'Shashannthika', 'Student', 'A'),
(35, 'Vaishnavi', 'Student', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `dailystock`
--

CREATE TABLE `dailystock` (
  `itemCode` int NOT NULL,
  `receiptDate` date NOT NULL,
  `quantity` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `itemCode` int NOT NULL,
  `itemName` varchar(50) DEFAULT NULL,
  `rate` decimal(7,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`itemCode`, `itemName`, `rate`) VALUES
(1, 'Coffee', 15.00),
(2, 'Tea', 10.00),
(3, 'Mineral Water', 10.00),
(4, 'Buttermilk', 20.00),
(5, 'Grape juice', 20.00),
(6, 'Veg pulao', 50.00),
(7, 'Veg briyani', 50.00),
(8, 'Meals', 40.00),
(9, 'Sarbath', 20.00),
(10, 'Veg puffs', 20.00),
(11, 'Egg puffs', 30.00),
(12, 'Veg Sandwich', 35.00),
(13, 'Vadai', 15.00),
(14, 'Mini samosa', 20.00),
(15, 'Veg roll', 15.00),
(16, 'Chicken roll', 20.00),
(17, 'Veg Burger', 50.00),
(18, 'Donut', 35.00),
(19, 'Bread omelette', 55.00),
(20, 'Sambar rice', 50.00),
(21, 'Corn puffs', 20.00),
(22, 'Cream bun', 20.00),
(23, 'Chips', 20.00),
(24, 'Milkshake', 35.00),
(25, 'Skittles', 10.00),
(26, 'Kitkat', 25.00),
(27, 'Munch (large)', 20.00);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `tokenId` int DEFAULT NULL,
  `tDate` date DEFAULT NULL,
  `custCode` int DEFAULT NULL,
  `itemCode` int DEFAULT NULL,
  `qty` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int NOT NULL,
  `name` varchar(25) DEFAULT NULL,
  `userId` varchar(20) DEFAULT NULL,
  `passwd` varchar(64) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL
) ;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `name`, `userId`, `passwd`, `status`) VALUES
(1, 'Administrator', 'admin', 'admin@p$wd', 'A');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`custCode`);

--
-- Indexes for table `dailystock`
--
ALTER TABLE `dailystock`
  ADD PRIMARY KEY (`itemCode`,`receiptDate`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`itemCode`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD KEY `custCode` (`custCode`),
  ADD KEY `itemCode` (`itemCode`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dailystock`
--
ALTER TABLE `dailystock`
  ADD CONSTRAINT `dailystock_ibfk_1` FOREIGN KEY (`itemCode`) REFERENCES `items` (`itemCode`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`custCode`) REFERENCES `customer` (`custCode`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`itemCode`) REFERENCES `items` (`itemCode`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
