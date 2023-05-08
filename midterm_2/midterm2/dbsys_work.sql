-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023-05-08 14:04:16
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `dbsys_work`
--
CREATE DATABASE IF NOT EXISTS `dbsys_work` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `dbsys_work`;

-- --------------------------------------------------------

--
-- 資料表結構 `course`
--

CREATE TABLE `course` (
  `CourseID` int(4) NOT NULL,
  `CourseName` char(15) NOT NULL,
  `DepartmentID` int(4) NOT NULL,
  `Grade` int(1) NOT NULL,
  `CourseType` int(1) NOT NULL,
  `MNOS` int(3) NOT NULL,
  `CNOS` int(3) NOT NULL,
  `CS` int(3) NOT NULL,
  `CourseCredit` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `course`
--

INSERT INTO `course` (`CourseID`, `CourseName`, `DepartmentID`, `Grade`, `CourseType`, `MNOS`, `CNOS`, `CS`, `CourseCredit`) VALUES
(1, '資料庫系統', 1, 2, 0, 60, 55, 103, 3),
(2, '資料結構', 1, 2, 0, 60, 55, 106, 3),
(4, '電子學', 2, 2, 0, 60, 44, 402, 3),
(5, '密碼學', 1, 2, 1, 60, 46, 302, 3),
(7, '組合數學', 1, 2, 1, 60, 60, 503, 2),
(6, '編譯器', 1, 3, 1, 60, 53, 302, 3),
(8, '計算機概論', 2, 1, 0, 60, 57, 507, 3),
(9, '機率與統計', 1, 2, 0, 60, 46, 108, 3),
(10, '軟體測試', 1, 3, 1, 60, 47, 203, 3),
(11, '數位信號處理', 2, 3, 1, 60, 35, 207, 3),
(12, '電磁波', 2, 3, 1, 60, 30, 306, 3),
(3, '計算機概論', 1, 1, 0, 60, 56, 107, 3),
(13, '系統安全', 1, 3, 1, 60, 35, 108, 3),
(14, '寬頻網路', 1, 3, 1, 60, 57, 502, 3),
(15, '程式語言', 1, 3, 1, 60, 48, 307, 3),
(16, 'web程式設計', 1, 2, 1, 60, -915, 208, 3);

-- --------------------------------------------------------

--
-- 資料表結構 `department`
--

CREATE TABLE `department` (
  `DepartmentID` int(4) NOT NULL,
  `DepartmentName` char(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `department`
--

INSERT INTO `department` (`DepartmentID`, `DepartmentName`) VALUES
(1, '資訊工程學系'),
(2, '通訊工程學系');

-- --------------------------------------------------------

--
-- 資料表結構 `enrollment`
--

CREATE TABLE `enrollment` (
  `CourseID` int(4) NOT NULL,
  `StudentID` char(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `enrollment`
--

INSERT INTO `enrollment` (`CourseID`, `StudentID`) VALUES
(1, 'D0123456'),
(2, 'D0123456'),
(9, 'D0123456'),
(4, 'D7891011'),
(8, 'D7891011'),
(8, 'D1099985'),
(4, 'D1099985');

-- --------------------------------------------------------

--
-- 資料表結構 `student`
--

CREATE TABLE `student` (
  `StudentName` char(20) NOT NULL,
  `StudentID` char(8) NOT NULL,
  `DepartmentID` int(11) NOT NULL,
  `Grade` int(1) NOT NULL,
  `StudentCredit` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `student`
--

INSERT INTO `student` (`StudentName`, `StudentID`, `DepartmentID`, `Grade`, `StudentCredit`) VALUES
('王大明', 'D0123456', 1, 2, 3),
('劉小明', 'D7891011', 1, 3, 0),
('張三', 'D1099985', 1, 2, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
