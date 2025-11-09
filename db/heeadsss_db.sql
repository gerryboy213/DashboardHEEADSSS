-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2025 at 06:49 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `form_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `position` varchar(100) NOT NULL,
  `center_name` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `province` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `full_name`, `username`, `password`, `position`, `center_name`, `region`, `province`, `city`, `email`, `phone`, `address`, `profile_image`) VALUES
(15, 'Lorem Ipsum BHS', 'admin-BHS-Union', 'pbkdf2:sha256:600000$p0WnhaQfhj5hNGRL$75d2d9567e86479fcf42ae1bf74a08e81674477a4975e45792d88ceb98b70c43', 'Barangay Health Worker', 'BHS Union AFHF', '08', '0837', '083735', 'admin@gmail.com', 'None', 'None', '/static/uploads/5b0c0ec9838649ea83d48b773a6584ba_friend-04.png'),
(22, 'Dr. Lorem Ipsum', 'rhumayorga', 'pbkdf2:sha256:600000$0IKg8oF22v7Qk9vb$78a66b6225499bec09f2ce8e15341c7b1a7fba914aef7cea3ed3001d041e4da1', 'Doctor', 'RHU Mayorga', '08', '0837', '083735', 'ruth.copino07@gmail.com', '09354320561', NULL, NULL),
(23, 'Dr. Lorem Ipsum2', 'rhugandara', 'pbkdf2:sha256:600000$Yb7XEXqBkn995rFy$016c292504c285dec27e072942ae167b0ffbd024bec2eca2705a7269762beae0', 'Nurse', 'RHU Gandara', '08', '0860', '086007', 'rhugandara@gmail.com', '09094112295', NULL, NULL),
(25, 'Dr. Lorem Ipsum3', 'abuyogdh', 'pbkdf2:sha256:600000$tKXgvi3LZWwTEpyA$9228e1b1fba50f75b0501f1602fb7b73b18b379761afd71c30e15b0065a7486a', 'Doctor', 'Abuyog DH AFHF', '08', '0837', '083701', 'abuyogdh@gmail.com', '09354320561', NULL, NULL),
(26, 'Admin-Name Gandara', 'gandara', 'pbkdf2:sha256:600000$rp4VCl9Qa20aby14$4f8ef9fcf267aeb6be185a2a83cbda50d4fe132cfa0111389fe4c3f034097718', 'Health Officer', 'Gandara AFHF', '08', '0860', '086007', 'gandara@gmail.com', '09097390983', NULL, NULL),
(27, 'Aljon L. Aa', 'aall', 'pbkdf2:sha256:600000$vugVPL2pdgRPsExL$42e22d8a7e1eff201769393ba1a695c5b5720c1ef990690a6845fc5738a349a2', 'IT', 'RHU Pagsanghan', '08', '0837', '083717', 'aljon.abines@evsu.edu.ph', '09169088561', NULL, NULL),
(28, 'Ruth Copino', 'ruth9', 'pbkdf2:sha256:600000$DXCYnEGk5IbX5IPe$f6d17ec97f036fc496c0ebb57dc938d737bd9fdfcd2b6c3e7ed8301f80a8c1ca', 'Health Officer', 'Gandara DH AFHF', '08', '0860', '086007', 'ruth.copino07@gmail.com', '09354320561', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `assessment`
--

CREATE TABLE `assessment` (
  `id` int(11) NOT NULL,
  `assessment_text` text NOT NULL,
  `translation_text` text NOT NULL,
  `category` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `assessment`
--

INSERT INTO `assessment` (`id`, `assessment_text`, `translation_text`, `category`) VALUES
(1, 'Are there any problems within your family that directly or indirectly concerns you? ', '(Meron bang problema sa inyong pamilya kung saan ikaw ay maaring naaapektuhan?)', 'Home'),
(2, 'Do your parents/guardian listen to you and take your feelings seriously? ', '(Pinapakinggan ka ba ng iyong magulang/guardian?)', 'Home'),
(3, 'Have you ever seriously thought of running away from home? ', '(May pagkakataon bang naisip mong maglayas?)', 'Home'),
(4, 'In the past year, have there been any major family changes?', '(Sa nakaraang taon, meron bang pagbabagong naganap sa inyong pamilya?)', 'Home'),
(5, 'Are you studying?', '(Nag-aaral ka ba?)', 'Education'),
(6, 'Are you working?', '(Ikaw ba ay nagtratrabaho?)', 'Education'),
(7, 'Are you having problems in school/work?', '(May problema ka ba sa iskwela o sa trabaho mo?)', 'Education'),
(8, 'Have you experienced bullying in school or at any other occasion)', '(Nakaranas ka na ba ng pangbu-bully o pang-aapi sa iskwela o saan man okasyon?)', 'Education'),
(9, 'Are you satisfied with the way you look / your weight?', '(Kuntento ka ba sa iyong itsura/anyo o sa iyong timbang?)', 'Eating Habits'),
(10, 'Have you tried to lose weight or maintain weight by vomiting, taking diet pills, laxatives, or straving yourself?', '(Sinubukan mo na bang magbawas ng timbang sa pamamagitan ng pagsuka ng kinain, uminom ng diet pills o pampadumi, o kaya ang di pagkain?)', 'Eating Habits'),
(11, 'Has somebody pointed out that you have gained weight or lost weight?', '(May nagpuna na ba na ikaw ay tumataba o pumapayat?)', 'Eating Habits'),
(12, 'Do you participate in any sports or activities in school? At work? At home?', '(Mayroon ka bang sinasalihang sports/actibidad sa iskwela, trabaho, o bahay?)', 'Activities'),
(13, 'Do you exercise regularly?', '(Regular ka bang mag-ehersisyo?)', 'Activities'),
(14, 'Do you use internet/computer?', '(Gumagamit ka ba ng internet / computer?)', 'Activities'),
(15, 'Tobacco ', '(Paninigarilyo)', 'Drugs'),
(16, 'Alcohol', '(Uminom ng alak)\r\n', 'Drugs'),
(17, 'Street drugs/prohibited drugs ', '(Gumamit ng bawal na gamot?)', 'Drugs'),
(18, 'Do you have any concerns regarding your health / your body changes?', '(Nababahala ka ba sa iyong kalusugan o mga pagbabago ng iyong pangangatawan?', 'Sexuality'),
(19, 'Have you ever had sex?', '(Ikaw ba ay may karanasan na sa sex?)', 'Sexuality'),
(20, 'If yes, how many partners have you had in the previous year?', 'Kung OO, naka-ilang partner ka na sa mga nakaraang taon?)', 'Sexuality'),
(21, 'Do you think you may be gay, lesbian, or bisexual?', '(Sa tingin mo ba ikaw ay bakla, tomboy, o silahis?)', 'Sexuality'),
(22, 'Have you ever been pregnant or gotten someone pregnant?', '(Ikaw ba ay nakaranas ng magbuntis or nakabuntis?)', 'Sexuality'),
(23, 'Have you had a sexually transmitted infection?', '(Ikaw ba ay nagkaroon na ng nakakahawang sakit dulot ng pakikipagtalik?)', 'Sexuality'),
(24, 'Do you use any form of protection when you have sex?', '(May ginagamit ka bang pangproteksyon kapag ikaw ay nakikipagtalik?)', 'Sexuality'),
(25, 'Have you ever been touched/hit/slap/kicked/pushed/ or shoved in any way by any person?', '(Ikaw ba ay nakaranas mahipuan/masuntok/masampal/matulak ng kahit sino?)', 'Safety/Weapons/Violence'),
(26, 'Are you currently in a relationship where you are physically hurt, threatened, or made to feel afraid?', '(Nakaranas ka na bang masaktan o takutin ng iyong karelasyon sa ngayon?', 'Safety/Weapons/Violence'),
(27, 'Do you wear a seatbelt when riding a car? A helmet when riding a motorbike?', '(Gumagamit ka ba ng sinturong pangkaligtasan, o gumagamit ng helmet kapag sumasakay ng motorbike?)', 'Safety/Weapons/Violence'),
(28, 'Do you or anyone you live with have a gun, rifle, or firearm?', '(May kasama ka bang nagmamay-ari ng baril o rifle sa inyong bahay?)', 'Safety/Weapons/Violence'),
(29, 'Are you anxious, sad, or depressed in any way?', '(Ikaw ba ay balisa o malungkot?)', 'Suicide/Depression'),
(30, 'Have you thought of hurting yourself or ending your life in any way?', '(Naisip mo na bang saktan ang sarili mo o tapusin ang buhay mo?)', 'Suicide/Depression'),
(31, 'Is there any member of the family with a history of suicide, depression, or anxiety?', '(May miyembro ba sa inyong pamilya na nagtangkang magpakamatay, matinding kalungkutan o laging balisa?', 'Suicide/Depression');

-- --------------------------------------------------------

--
-- Table structure for table `assessment_response`
--

CREATE TABLE `assessment_response` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `assessment_number` int(11) NOT NULL,
  `response` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `assessment_response`
--

INSERT INTO `assessment_response` (`id`, `user_id`, `assessment_number`, `response`) VALUES
(1, 29, 1, 'Yes'),
(2, 29, 2, 'No'),
(3, 29, 3, 'Yes'),
(4, 29, 4, 'No'),
(5, 29, 5, 'Yes'),
(6, 29, 6, 'No'),
(7, 29, 7, 'Yes'),
(8, 29, 8, 'Yes'),
(9, 29, 9, 'No'),
(10, 29, 10, 'No'),
(11, 29, 11, 'No'),
(12, 29, 12, 'No'),
(13, 29, 1, 'Yes'),
(14, 29, 2, 'No'),
(15, 29, 3, 'Yes'),
(16, 29, 4, 'Yes'),
(17, 29, 5, 'Yes'),
(18, 29, 6, 'Yes'),
(19, 29, 7, 'Yes'),
(20, 29, 8, 'Yes'),
(21, 29, 9, 'Yes'),
(22, 29, 10, 'Yes'),
(23, 29, 11, 'Yes'),
(24, 29, 12, 'Yes'),
(25, 29, 13, 'Yes'),
(26, 29, 14, 'Yes'),
(27, 29, 15, 'No'),
(28, 29, 16, 'No'),
(29, 29, 17, 'No'),
(30, 29, 18, 'Yes'),
(31, 29, 19, 'No'),
(32, 29, 20, 'No'),
(33, 29, 21, 'No'),
(34, 29, 22, 'No'),
(35, 29, 23, 'No'),
(36, 29, 24, 'No'),
(37, 29, 25, 'Yes'),
(38, 29, 26, 'No'),
(39, 29, 27, 'No'),
(40, 29, 28, 'No'),
(41, 29, 29, 'Yes'),
(42, 29, 30, 'Yes'),
(43, 29, 31, 'Yes'),
(44, 38, 1, 'Yes'),
(45, 41, 1, 'Yes'),
(46, 41, 2, 'Yes'),
(47, 41, 3, 'Yes'),
(48, 41, 4, 'Yes'),
(49, 41, 5, 'Yes'),
(50, 41, 6, 'Yes'),
(51, 41, 7, 'Yes'),
(52, 41, 8, 'Yes'),
(53, 41, 9, 'Yes'),
(54, 41, 10, 'Yes'),
(55, 41, 11, 'Yes'),
(56, 41, 12, 'Yes'),
(57, 41, 13, 'Yes'),
(58, 41, 14, 'Yes'),
(59, 41, 15, 'Yes'),
(60, 41, 16, 'Yes'),
(61, 41, 17, 'Yes'),
(62, 41, 18, 'Yes'),
(63, 41, 19, 'Yes'),
(64, 41, 20, 'Yes'),
(65, 41, 21, 'Yes'),
(66, 41, 22, 'Yes'),
(67, 41, 23, 'Yes'),
(68, 41, 24, 'Yes'),
(69, 41, 25, 'Yes'),
(70, 41, 26, 'Yes'),
(71, 41, 27, 'Yes'),
(72, 41, 28, 'Yes'),
(73, 41, 29, 'Yes'),
(74, 41, 30, 'Yes'),
(75, 41, 31, 'Yes'),
(76, 45, 1, 'No'),
(77, 45, 2, 'Yes'),
(78, 45, 3, 'No'),
(79, 45, 4, 'No'),
(80, 45, 5, 'No'),
(81, 45, 6, 'Yes'),
(82, 45, 7, 'No'),
(83, 45, 8, 'No'),
(84, 45, 9, 'Yes'),
(85, 45, 10, 'Yes'),
(86, 45, 11, 'Yes'),
(87, 45, 12, 'Yes'),
(88, 45, 13, 'No'),
(89, 45, 14, 'Yes'),
(90, 45, 15, 'No'),
(91, 45, 16, 'No'),
(92, 45, 17, 'Yes'),
(93, 45, 18, 'Yes'),
(94, 45, 19, 'Yes'),
(95, 45, 20, 'Yes'),
(96, 45, 21, 'Yes'),
(97, 45, 22, 'No'),
(98, 45, 23, 'Yes'),
(99, 45, 24, 'No'),
(100, 45, 25, 'No'),
(101, 45, 26, 'No'),
(102, 45, 27, 'Yes'),
(103, 45, 28, 'Yes'),
(104, 45, 29, 'Yes'),
(105, 45, 30, 'Yes'),
(106, 45, 31, 'Yes'),
(107, 49, 1, 'Yes'),
(108, 49, 2, 'Yes'),
(109, 49, 3, 'No'),
(110, 49, 4, 'Yes'),
(111, 49, 5, 'No'),
(112, 49, 6, 'No'),
(113, 49, 7, 'No'),
(114, 49, 8, 'No'),
(115, 49, 9, 'No'),
(116, 49, 10, 'No'),
(117, 49, 11, 'No'),
(118, 49, 12, 'No'),
(119, 49, 13, 'No'),
(120, 49, 14, 'No'),
(121, 49, 15, 'No'),
(122, 49, 16, 'No'),
(123, 49, 17, 'No'),
(124, 49, 18, 'No'),
(125, 49, 19, 'No'),
(126, 49, 20, 'No'),
(127, 49, 21, 'No'),
(128, 49, 22, 'No'),
(129, 49, 23, 'Yes'),
(130, 49, 24, 'Yes'),
(131, 49, 25, 'Yes'),
(132, 49, 26, 'Yes'),
(133, 49, 27, 'Yes'),
(134, 49, 28, 'Yes'),
(135, 49, 29, 'Yes'),
(136, 49, 30, 'Yes'),
(137, 49, 31, 'Yes'),
(138, 49, 31, 'Yes'),
(139, 49, 31, 'Yes'),
(140, 49, 31, 'Yes'),
(141, 50, 1, 'Yes'),
(142, 50, 2, 'Yes'),
(143, 50, 3, 'No'),
(144, 50, 4, 'Yes'),
(145, 50, 5, 'Yes'),
(146, 50, 6, 'Yes'),
(147, 50, 7, 'Yes'),
(148, 50, 8, 'Yes'),
(149, 50, 9, 'Yes'),
(150, 50, 10, 'Yes'),
(151, 50, 11, 'No'),
(152, 50, 12, 'No'),
(153, 50, 13, 'No'),
(154, 50, 14, 'No'),
(155, 50, 15, 'No'),
(156, 50, 16, 'No'),
(157, 50, 17, 'No'),
(158, 50, 18, 'No'),
(159, 50, 19, 'No'),
(160, 50, 20, 'No'),
(161, 50, 21, 'No'),
(162, 50, 22, 'No'),
(163, 50, 23, 'No'),
(164, 50, 24, 'No'),
(165, 50, 25, 'No'),
(166, 50, 26, 'No'),
(167, 50, 27, 'No'),
(168, 50, 28, 'No'),
(169, 50, 29, 'No'),
(170, 50, 30, 'No'),
(171, 50, 31, 'No'),
(172, 50, 31, 'No'),
(173, 50, 31, 'No'),
(174, 50, 31, 'No'),
(175, 51, 31, 'No'),
(176, 52, 1, 'Yes'),
(177, 52, 2, 'No'),
(178, 52, 3, 'Yes'),
(179, 52, 4, 'Yes'),
(180, 52, 5, 'Yes'),
(181, 52, 6, 'Yes'),
(182, 52, 7, 'Yes'),
(183, 52, 8, 'Yes'),
(184, 52, 9, 'Yes'),
(185, 52, 10, 'Yes'),
(186, 52, 11, 'Yes'),
(187, 52, 12, 'Yes'),
(188, 52, 13, 'Yes'),
(189, 52, 14, 'Yes'),
(190, 52, 15, 'Yes'),
(191, 52, 16, 'Yes'),
(192, 52, 17, 'Yes'),
(193, 52, 18, 'Yes'),
(194, 52, 19, 'No'),
(195, 52, 20, 'No'),
(196, 52, 21, 'No'),
(197, 52, 22, 'No'),
(198, 52, 23, 'No'),
(199, 52, 24, 'No'),
(200, 52, 25, 'No'),
(201, 52, 26, 'No'),
(202, 52, 27, 'No'),
(203, 52, 28, 'No'),
(204, 52, 29, 'No'),
(205, 52, 30, 'No'),
(206, 52, 31, 'Yes'),
(207, 53, 1, 'No'),
(208, 53, 2, 'No'),
(209, 53, 3, 'No'),
(210, 53, 4, 'No'),
(211, 53, 5, 'No'),
(212, 53, 6, 'No'),
(213, 53, 7, 'No'),
(214, 53, 8, 'No'),
(215, 53, 9, 'No'),
(216, 53, 10, 'No'),
(217, 53, 11, 'No'),
(218, 53, 12, 'No'),
(219, 53, 13, 'No'),
(220, 53, 14, 'No'),
(221, 53, 15, 'No'),
(222, 53, 16, 'No'),
(223, 53, 17, 'No'),
(224, 53, 18, 'No'),
(225, 53, 19, 'No'),
(226, 53, 20, 'No'),
(227, 53, 21, 'No'),
(228, 53, 22, 'No'),
(229, 53, 23, 'No'),
(230, 53, 24, 'No'),
(231, 53, 25, 'No'),
(232, 53, 26, 'No'),
(233, 53, 27, 'No'),
(234, 53, 28, 'No'),
(235, 53, 29, 'No'),
(236, 53, 30, 'No'),
(237, 53, 31, 'Yes'),
(238, 60, 1, 'Yes'),
(239, 60, 2, 'Yes'),
(240, 60, 3, 'Yes'),
(241, 60, 4, 'Yes'),
(242, 60, 5, 'Yes'),
(243, 60, 6, 'Yes'),
(244, 60, 7, 'Yes'),
(245, 60, 8, 'No'),
(246, 60, 9, 'Yes'),
(247, 60, 10, 'No'),
(248, 60, 11, 'Yes'),
(249, 60, 12, 'Yes'),
(250, 60, 13, 'Yes'),
(251, 60, 14, 'Yes'),
(252, 60, 15, 'Yes'),
(253, 60, 16, 'Yes'),
(254, 60, 17, 'Yes'),
(255, 60, 18, 'Yes'),
(256, 60, 19, 'No'),
(257, 60, 20, 'Yes'),
(258, 60, 21, 'No'),
(259, 60, 22, 'Yes'),
(260, 60, 23, 'Yes'),
(261, 60, 24, 'Yes'),
(262, 60, 25, 'Yes'),
(263, 60, 26, 'Yes'),
(264, 60, 27, 'Yes'),
(265, 60, 28, 'Yes'),
(266, 60, 29, 'Yes'),
(267, 60, 30, 'Yes'),
(268, 60, 31, 'Yes'),
(269, 44, 1, 'Yes'),
(270, 44, 2, 'Yes'),
(271, 44, 3, 'No'),
(272, 44, 4, 'No'),
(273, 44, 5, 'No'),
(274, 44, 6, 'No'),
(275, 44, 7, 'No'),
(276, 44, 8, 'No'),
(277, 44, 9, 'No'),
(278, 44, 10, 'No'),
(279, 44, 11, 'No'),
(280, 44, 12, 'No'),
(281, 44, 13, 'No'),
(282, 44, 14, 'No'),
(283, 44, 15, 'No'),
(284, 44, 16, 'No'),
(285, 44, 17, 'No'),
(286, 44, 18, 'No'),
(287, 44, 19, 'No'),
(288, 44, 20, 'No'),
(289, 44, 21, 'No'),
(290, 44, 22, 'No'),
(291, 44, 23, 'No'),
(292, 44, 24, 'No'),
(293, 44, 25, 'No'),
(294, 44, 26, 'No'),
(295, 44, 27, 'No'),
(296, 44, 28, 'No'),
(297, 44, 29, 'No'),
(298, 44, 30, 'No'),
(299, 44, 31, 'No'),
(300, 42, 1, 'Yes'),
(301, 42, 2, 'Yes'),
(302, 42, 3, 'No'),
(303, 42, 4, 'No'),
(304, 42, 5, 'No'),
(305, 42, 6, 'No'),
(306, 42, 7, 'No'),
(307, 42, 8, 'No'),
(308, 42, 9, 'No'),
(309, 42, 10, 'No'),
(310, 42, 11, 'No'),
(311, 42, 12, 'No'),
(312, 42, 13, 'No'),
(313, 42, 14, 'No'),
(314, 42, 15, 'No'),
(315, 42, 16, 'No'),
(316, 42, 17, 'No'),
(317, 42, 18, 'No'),
(318, 42, 19, 'No'),
(319, 42, 20, 'No'),
(320, 42, 21, 'No'),
(321, 42, 22, 'No'),
(322, 42, 23, 'No'),
(323, 42, 24, 'No'),
(324, 42, 25, 'No'),
(325, 42, 26, 'No'),
(326, 42, 27, 'No'),
(327, 42, 28, 'No'),
(328, 42, 29, 'No'),
(329, 42, 30, 'No'),
(330, 42, 31, 'No'),
(331, 114, 1, 'Yes'),
(332, 114, 2, 'Yes'),
(333, 114, 3, 'Yes'),
(334, 114, 4, 'Yes'),
(335, 114, 5, 'Yes'),
(336, 114, 6, 'Yes'),
(337, 114, 7, 'Yes'),
(338, 114, 8, 'Yes'),
(339, 114, 9, 'No'),
(340, 114, 10, 'No'),
(341, 114, 11, 'No'),
(342, 114, 12, 'No'),
(343, 114, 13, 'No'),
(344, 114, 14, 'No'),
(345, 114, 15, 'No'),
(346, 114, 16, 'No'),
(347, 114, 17, 'No'),
(348, 114, 18, 'No'),
(349, 114, 19, 'No'),
(350, 114, 20, 'No'),
(351, 114, 21, 'No'),
(352, 114, 22, 'No'),
(353, 114, 23, 'No'),
(354, 114, 24, 'No'),
(355, 114, 25, 'No'),
(356, 114, 26, 'No'),
(357, 114, 27, 'No'),
(358, 114, 28, 'No'),
(359, 114, 29, 'No'),
(360, 114, 30, 'No'),
(361, 114, 31, 'No'),
(362, 47, 1, 'Yes'),
(363, 147, 1, 'No'),
(364, 147, 2, 'No'),
(365, 147, 3, 'No'),
(366, 147, 4, 'No'),
(367, 147, 5, 'No'),
(368, 147, 6, 'No'),
(369, 147, 7, 'No'),
(370, 147, 8, 'No'),
(371, 147, 9, 'No'),
(372, 147, 10, 'No'),
(373, 147, 11, 'No'),
(374, 147, 12, 'No'),
(375, 147, 13, 'No'),
(376, 147, 14, 'No'),
(377, 147, 15, 'No'),
(378, 147, 16, 'No'),
(379, 147, 17, 'No'),
(380, 147, 18, 'No'),
(381, 147, 19, 'No'),
(382, 147, 20, '0'),
(383, 147, 21, 'No'),
(384, 147, 22, 'No'),
(385, 147, 23, 'No'),
(386, 147, 24, 'No'),
(387, 147, 25, 'No'),
(388, 147, 26, 'No'),
(389, 147, 27, 'No'),
(390, 147, 28, 'No'),
(391, 147, 29, 'No'),
(392, 147, 30, 'No'),
(393, 147, 31, 'No'),
(394, 148, 1, 'Yes'),
(395, 148, 2, 'No'),
(396, 148, 2, 'No'),
(397, 148, 3, 'Yes'),
(398, 148, 4, 'No'),
(399, 148, 5, 'Yes'),
(400, 148, 6, 'No'),
(401, 148, 7, 'No'),
(402, 148, 8, 'No'),
(403, 148, 9, 'No'),
(404, 148, 10, 'No'),
(405, 148, 11, 'No'),
(406, 148, 12, 'No'),
(407, 148, 13, 'No'),
(408, 148, 14, 'No'),
(409, 148, 15, 'No'),
(410, 148, 16, 'No'),
(411, 148, 17, 'No'),
(412, 148, 18, 'No'),
(413, 148, 19, 'No'),
(414, 148, 20, 'No'),
(415, 148, 21, 'No'),
(416, 148, 22, 'No'),
(417, 148, 23, 'No'),
(418, 148, 24, 'No'),
(419, 148, 25, 'No'),
(420, 148, 26, 'No'),
(421, 148, 27, 'No'),
(422, 148, 28, 'No'),
(423, 148, 29, 'No'),
(424, 148, 30, 'No'),
(425, 148, 31, 'No'),
(426, 148, 1, 'No'),
(427, 148, 2, 'No'),
(428, 148, 3, 'No'),
(429, 148, 4, 'No'),
(430, 148, 5, 'No'),
(431, 148, 6, 'No'),
(432, 148, 7, 'No'),
(433, 148, 8, 'No'),
(434, 148, 9, 'No'),
(435, 148, 10, 'No'),
(436, 148, 11, 'No'),
(437, 148, 12, 'No'),
(438, 148, 13, 'No'),
(439, 148, 14, 'No'),
(440, 148, 15, 'No'),
(441, 148, 16, 'No'),
(442, 148, 17, 'No'),
(443, 148, 18, 'No'),
(444, 148, 19, 'No'),
(445, 148, 20, 'No'),
(446, 148, 21, 'No'),
(447, 148, 22, 'No'),
(448, 148, 23, 'No'),
(449, 148, 24, 'No'),
(450, 148, 25, 'No'),
(451, 148, 26, 'No'),
(452, 148, 27, 'No'),
(453, 148, 28, 'No'),
(454, 148, 29, 'No'),
(455, 148, 30, 'No'),
(456, 148, 31, 'No'),
(457, 148, 31, 'No'),
(458, 144, 1, 'Yes'),
(459, 144, 2, 'Yes'),
(460, 144, 3, 'Yes'),
(461, 144, 4, 'Yes'),
(462, 144, 5, 'Yes'),
(463, 144, 6, 'Yes'),
(464, 144, 7, 'Yes'),
(465, 144, 8, 'Yes'),
(466, 144, 9, 'Yes'),
(467, 144, 10, 'No'),
(468, 144, 11, 'No'),
(469, 144, 12, 'No'),
(470, 144, 13, 'No'),
(471, 144, 14, 'No'),
(472, 144, 15, 'No'),
(473, 144, 16, 'No'),
(474, 144, 17, 'No'),
(475, 144, 18, 'No'),
(476, 144, 19, 'No'),
(477, 144, 20, 'No'),
(478, 144, 21, 'No'),
(479, 144, 22, 'No'),
(480, 144, 23, 'No'),
(481, 144, 24, 'No'),
(482, 144, 25, 'No'),
(483, 144, 26, 'No'),
(484, 144, 27, 'No'),
(485, 144, 28, 'No'),
(486, 144, 29, 'No'),
(487, 144, 30, 'No'),
(488, 144, 31, 'No'),
(489, 144, 31, 'No'),
(490, 144, 31, 'No'),
(491, 144, 31, 'No'),
(492, 144, 31, 'No'),
(493, 144, 31, 'No'),
(494, 155, 1, 'No'),
(495, 155, 2, 'No'),
(496, 155, 3, 'No'),
(497, 155, 4, 'No'),
(498, 155, 5, 'No'),
(499, 155, 6, 'No'),
(500, 155, 7, 'No'),
(501, 155, 8, 'No'),
(502, 155, 9, 'No'),
(503, 155, 10, 'No'),
(504, 155, 11, 'No'),
(505, 155, 12, 'No'),
(506, 155, 13, 'No'),
(507, 155, 14, 'No'),
(508, 155, 15, 'No'),
(509, 155, 16, 'No'),
(510, 155, 17, 'No'),
(511, 155, 18, 'No'),
(512, 155, 19, 'No'),
(513, 155, 20, 'No'),
(514, 155, 21, 'No'),
(515, 155, 22, 'No'),
(516, 155, 23, 'No'),
(517, 155, 24, 'No'),
(518, 155, 25, 'No'),
(519, 155, 26, 'No'),
(520, 155, 27, 'No'),
(521, 155, 28, 'No'),
(522, 155, 29, 'No'),
(523, 155, 30, 'No'),
(524, 155, 31, 'No'),
(525, 109, 1, 'No'),
(526, 109, 2, 'No'),
(527, 109, 3, 'No'),
(528, 109, 4, 'No'),
(529, 109, 5, 'No'),
(530, 109, 6, 'No'),
(531, 109, 7, 'No'),
(532, 109, 8, 'No'),
(533, 109, 9, 'No'),
(534, 109, 10, 'No'),
(535, 109, 11, 'No'),
(536, 109, 12, 'No'),
(537, 109, 13, 'No'),
(538, 109, 14, 'No'),
(539, 109, 15, 'No'),
(540, 109, 16, 'No'),
(541, 109, 17, 'No'),
(542, 109, 18, 'No'),
(543, 109, 19, 'No'),
(544, 109, 20, 'No'),
(545, 109, 21, 'No'),
(546, 109, 22, 'No'),
(547, 109, 23, 'No'),
(548, 109, 24, 'No'),
(549, 109, 25, 'No'),
(550, 109, 26, 'No'),
(551, 109, 27, 'No'),
(552, 109, 28, 'No'),
(553, 109, 29, 'No'),
(554, 109, 30, 'No'),
(555, 109, 31, 'No'),
(556, 166, 1, 'Yes'),
(557, 166, 2, 'No'),
(558, 166, 3, 'No'),
(559, 166, 4, 'Yes'),
(560, 166, 5, 'No'),
(561, 166, 6, 'Yes'),
(562, 166, 7, 'No'),
(563, 166, 8, 'Yes'),
(564, 166, 9, 'No'),
(565, 166, 10, 'Yes'),
(566, 166, 11, 'Yes'),
(567, 166, 12, 'Yes'),
(568, 166, 13, 'Yes'),
(569, 166, 14, 'Yes'),
(570, 166, 15, 'Yes'),
(571, 166, 16, 'Yes'),
(572, 166, 17, 'Yes'),
(573, 166, 18, 'Yes'),
(574, 166, 19, 'Yes'),
(575, 166, 20, 'Yes'),
(576, 166, 21, 'Yes'),
(577, 166, 22, 'Yes'),
(578, 166, 23, 'Yes'),
(579, 166, 24, 'Yes'),
(580, 166, 25, 'Yes'),
(581, 166, 26, 'Yes'),
(582, 166, 27, 'Yes'),
(583, 166, 28, 'Yes'),
(584, 166, 29, 'Yes'),
(585, 166, 30, 'Yes'),
(586, 166, 31, 'Yes'),
(587, 166, 1, 'No'),
(588, 166, 2, 'No'),
(589, 166, 3, 'No'),
(590, 166, 4, 'No'),
(591, 166, 5, 'No'),
(592, 166, 6, 'No'),
(593, 166, 7, 'No'),
(594, 166, 8, 'No'),
(595, 166, 9, 'No'),
(596, 166, 10, 'No'),
(597, 166, 11, 'No'),
(598, 166, 12, 'No'),
(599, 166, 13, 'No'),
(600, 166, 14, 'No'),
(601, 166, 15, 'No'),
(602, 166, 16, 'No'),
(603, 166, 17, 'No'),
(604, 166, 18, 'No'),
(605, 166, 19, 'No'),
(606, 166, 20, 'No'),
(607, 166, 21, 'No'),
(608, 166, 22, 'No'),
(609, 166, 23, 'No'),
(610, 166, 24, 'No'),
(611, 166, 25, 'No'),
(612, 166, 26, 'No'),
(613, 166, 27, 'No'),
(614, 166, 28, 'No'),
(615, 166, 29, 'No'),
(616, 166, 30, 'No'),
(617, 166, 31, 'No');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `center_name` varchar(100) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `urgency` varchar(10) DEFAULT NULL,
  `unread` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`id`, `user_id`, `center_name`, `message`, `urgency`, `unread`, `timestamp`) VALUES
(1, 96, 'RHU Mayorga', 'Client 0837-01-00001 forwarded to your center.', 'medium', 1, '2025-05-23 01:18:32'),
(3, 105, 'Abuyog DH AFHF', 'Client 0837-01-00007 forwarded to your center.', 'medium', 1, '2025-05-23 05:48:04'),
(4, 111, 'Gandara DH AFHF', 'Client 0860-04-00001 forwarded to your center.', 'medium', 1, '2025-05-23 06:33:25'),
(5, 113, 'RHU Mayorga', 'Client 0837-01-00009 forwarded to your center.', 'medium', 1, '2025-05-23 07:45:18'),
(6, 116, 'RHU Mayorga', 'Client 0837-01-00012 forwarded to your center.', 'medium', 1, '2025-05-27 02:27:04'),
(7, 121, 'RHU Mayorga', 'Client 0837-01-00017 forwarded to your center.', 'medium', 1, '2025-05-27 05:40:13'),
(8, 122, 'RHU Mayorga', 'Client 0837-01-00018 forwarded to your center.', 'medium', 1, '2025-05-27 06:16:24'),
(9, 118, 'RHU Mayorga', 'Client 0837-01-00014 forwarded to your center.', 'medium', 1, '2025-05-27 06:21:53'),
(10, 119, 'RHU Mayorga', 'Client 0837-01-00015 forwarded to your center.', 'medium', 1, '2025-05-27 06:24:04'),
(11, 134, 'RHU Mayorga', 'Client 0837-01-00019 forwarded to your center.', 'medium', 1, '2025-05-27 07:23:18'),
(12, 119, 'Abuyog DH AFHF', 'Client 0837-01-00015 forwarded to your center.', 'medium', 1, '2025-05-28 00:05:53'),
(13, 134, 'Abuyog DH AFHF', 'Client 0837-01-00019 forwarded to your center.', 'medium', 1, '2025-05-28 05:50:01'),
(14, 110, 'Abuyog DH AFHF', 'Client 0837-02-00002 forwarded to your center.', 'medium', 1, '2025-05-28 05:50:45'),
(15, 116, 'Abuyog DH AFHF', 'Client 0837-01-00012 forwarded to your center.', 'medium', 1, '2025-05-28 05:51:38'),
(16, 114, 'RHU Mayorga', 'Client 0837-01-00010 forwarded to your center.', 'medium', 1, '2025-05-28 05:54:18');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `question_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question_text`) VALUES
(1, '1. Ikaw ba ay nakakaranas ng pananakit o pananakot sa iyong tahanan/bahay?'),
(2, '2. May mga pagkakataon ba na pinag-isipan mong maglayas o umalis na ng inyong bahay?'),
(3, '3. Nakaranas ka ba ng bullying na pisikal o cyber bullying sa paaralan o sa trabaho?'),
(4, '4. May pagkakataon ba na seryoso mong naiisip na wakasan ang iyong buhay?'),
(5, '5. Naninigarilyo ka ba?'),
(6, '6. Umiinom ka ba ng alak?'),
(7, '7. Nakakita ka na ba ng mga ipinagbabawal na \"gamot\" o drugs?'),
(8, '8. Ikaw ba ay nakaranas ng magkarelasyon (boyfriend/girlfriend)?'),
(9, '9. Ikaw ba ay nakaranas ng makipag sex o makipagtalik?'),
(10, '10. Nakaranas ka ba na ikaw ay pinilit makipag sex?'),
(11, '11. Ikaw ba ay nakaranas nang mabuntis, o makabuntis?'),
(12, '12. Gusto mo bang mag pa counsel o komunsulta para matulungan ka?');

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `id` int(11) NOT NULL,
  `recommendation_text` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `recommendation_saved` tinyint(1) NOT NULL,
  `source` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `recommendations`
--

INSERT INTO `recommendations` (`id`, `recommendation_text`, `timestamp`, `user_id`, `recommendation_saved`, `source`) VALUES
(1, 'Refer to RHU', '2025-05-23 01:18:30', 96, 1, 'brgy'),
(2, 'Refer to RHU', '2025-05-23 01:43:53', 98, 1, 'brgy'),
(3, 'Follow-up at 2025-05-26T01:00', '2025-05-23 01:43:53', 98, 1, 'brgy'),
(4, 'Refer to DSWD', '2025-05-23 03:15:10', 100, 1, 'hospital'),
(5, 'Preventive Counseling', '2025-05-23 03:15:10', 100, 1, 'hospital'),
(6, 'Refer to DSWD', '2025-05-23 03:15:15', 100, 1, 'hospital'),
(7, 'Preventive Counseling', '2025-05-23 03:15:15', 100, 1, 'hospital'),
(8, 'Refer to DSWD', '2025-05-23 03:19:53', 100, 1, 'hospital'),
(9, 'Preventive Counseling', '2025-05-23 03:19:53', 100, 1, 'hospital'),
(10, 'Refer to DSWD', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(11, 'Preventive Counseling', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(12, 'Refer to DSWD', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(13, 'Preventive Counseling', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(14, 'Refer to DSWD', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(15, 'Preventive Counseling', '2025-05-23 03:19:55', 100, 1, 'hospital'),
(16, 'Refer to DSWD', '2025-05-23 03:20:31', 100, 1, 'hospital'),
(17, 'Preventive Counseling', '2025-05-23 03:20:31', 100, 1, 'hospital'),
(18, 'Refer to DSWD', '2025-05-23 03:20:32', 100, 1, 'hospital'),
(19, 'Preventive Counseling', '2025-05-23 03:20:32', 100, 1, 'hospital'),
(20, 'Refer to DSWD', '2025-05-23 03:23:29', 102, 1, 'rhu'),
(21, 'Refer to DSWD', '2025-05-23 04:46:30', 104, 1, 'brgy'),
(31, 'Refer to RHU', '2025-05-23 06:31:28', 111, 1, 'rhu'),
(32, 'Refer to Hospital', '2025-05-23 07:37:18', 113, 1, 'brgy'),
(33, 'Refer to DSWD', '2025-05-23 07:37:18', 113, 1, 'brgy'),
(34, 'Parental Notification', '2025-05-23 07:37:18', 113, 1, 'brgy'),
(37, 'Refer to DSWD', '2025-05-23 07:43:52', 114, 1, 'brgy'),
(38, 'Refer to RHU', '2025-05-25 13:14:43', 105, 1, 'brgy'),
(39, 'Refer to DSWD', '2025-05-25 13:14:43', 105, 1, 'brgy'),
(40, 'Preventive Counseling', '2025-05-25 13:14:43', 105, 1, 'brgy'),
(41, 'Schedule Follow-up', '2025-05-25 13:14:43', 105, 1, 'brgy'),
(42, 'Follow-up at 2025-05-24T13:48', '2025-05-25 13:14:43', 105, 1, 'brgy'),
(43, 'Refer to RHU', '2025-05-27 02:04:51', 116, 1, 'brgy'),
(44, 'Refer to RHU', '2025-05-27 02:26:52', 115, 1, 'brgy'),
(45, 'Refer to RHU', '2025-05-27 05:39:50', 121, 1, 'brgy'),
(47, 'Refer to RHU', '2025-05-27 06:21:51', 118, 1, 'brgy'),
(48, 'Refer to RHU', '2025-05-27 06:23:56', 119, 1, 'brgy'),
(49, 'Refer to RHU', '2025-05-27 06:40:37', 127, 1, 'brgy'),
(50, 'Refer to DSWD', '2025-05-27 06:40:37', 127, 1, 'brgy'),
(51, 'Refer to RHU', '2025-05-27 06:43:51', 128, 1, 'brgy'),
(52, 'Refer to DSWD', '2025-05-27 06:43:51', 128, 1, 'brgy'),
(53, 'Refer to RHU', '2025-05-27 07:22:57', 122, 1, 'brgy'),
(54, 'Refer to Hospital', '2025-05-27 07:22:57', 122, 1, 'brgy'),
(69, 'Refer to RHU', '2025-05-28 00:04:08', 134, 1, 'brgy'),
(70, 'Refer to Hospital', '2025-05-28 00:04:08', 134, 1, 'brgy'),
(71, 'Preventive Counseling', '2025-05-28 00:04:08', 134, 1, 'brgy'),
(72, 'Schedule Follow-up', '2025-05-28 00:04:08', 134, 1, 'brgy'),
(73, 'Follow-up at 2025-05-28T07:55', '2025-05-28 00:04:08', 134, 1, 'brgy'),
(74, 'Refer to RHU', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(75, 'Refer to Hospital', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(76, 'Refer to DSWD', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(77, 'Preventive Counseling', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(78, 'Schedule Follow-up', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(79, 'Follow-up at 2025-05-28T07:55', '2025-05-28 00:04:25', 134, 1, 'rhu'),
(80, 'Refer to RHU', '2025-05-28 00:04:43', 119, 1, 'rhu'),
(81, 'Refer to Hospital', '2025-05-28 00:04:43', 119, 1, 'rhu'),
(82, 'Refer to RHU', '2025-05-28 00:08:30', 119, 1, 'unknown'),
(83, 'Refer to Hospital', '2025-05-28 00:08:31', 119, 1, 'unknown'),
(84, 'Refer to DSWD', '2025-05-28 00:08:31', 119, 1, 'unknown'),
(85, 'Refer to RHU', '2025-05-28 00:14:30', 119, 1, 'hospital'),
(86, 'Refer to Hospital', '2025-05-28 00:14:30', 119, 1, 'hospital'),
(87, 'Refer to DSWD', '2025-05-28 00:14:30', 119, 1, 'hospital'),
(88, 'Parental Notification', '2025-05-28 00:14:30', 119, 1, 'hospital');

-- --------------------------------------------------------

--
-- Table structure for table `referral_history`
--

CREATE TABLE `referral_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `from_center` varchar(100) NOT NULL,
  `to_center` varchar(100) NOT NULL,
  `forwarded_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `service_name` varchar(255) NOT NULL,
  `service_detail` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `services_saved` tinyint(1) DEFAULT NULL,
  `source` varchar(50) NOT NULL,
  `follow_up` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `service_name`, `service_detail`, `timestamp`, `user_id`, `services_saved`, `source`, `follow_up`) VALUES
(1, 'Assessed using HEEADSSS', '', '2025-05-23 01:18:30', 96, 1, 'brgy', NULL),
(2, 'Referred to RHU', '', '2025-05-23 01:43:53', 98, 1, 'brgy', NULL),
(3, 'Assessed using HEEADSSS', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(4, 'Reached by HYO', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(5, 'Referred to RHU', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(6, 'Referred to Hospital', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(7, 'Referred to DSWD', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(8, 'Parental Notification', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(9, 'Preventive Counseling', '', '2025-05-23 03:15:10', 100, 1, 'hospital', NULL),
(10, 'Assessed using HEEADSSS', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(11, 'Reached by HYO', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(12, 'Referred to RHU', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(13, 'Referred to Hospital', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(14, 'Referred to DSWD', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(15, 'Parental Notification', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(16, 'Preventive Counseling', '', '2025-05-23 03:15:15', 100, 1, 'hospital', NULL),
(17, 'Assessed using HEEADSSS', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(18, 'Reached by HYO', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(19, 'Referred to RHU', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(20, 'Referred to Hospital', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(21, 'Referred to DSWD', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(22, 'Parental Notification', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(23, 'Preventive Counseling', '', '2025-05-23 03:19:53', 100, 1, 'hospital', NULL),
(24, 'Assessed using HEEADSSS', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(25, 'Reached by HYO', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(26, 'Referred to RHU', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(27, 'Referred to Hospital', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(28, 'Referred to DSWD', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(29, 'Parental Notification', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(30, 'Preventive Counseling', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(31, 'Assessed using HEEADSSS', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(32, 'Reached by HYO', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(33, 'Referred to RHU', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(34, 'Referred to Hospital', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(35, 'Referred to DSWD', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(36, 'Parental Notification', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(37, 'Preventive Counseling', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(38, 'Assessed using HEEADSSS', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(39, 'Reached by HYO', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(40, 'Referred to RHU', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(41, 'Referred to Hospital', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(42, 'Referred to DSWD', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(43, 'Parental Notification', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(44, 'Preventive Counseling', '', '2025-05-23 03:19:55', 100, 1, 'hospital', NULL),
(45, 'Assessed using HEEADSSS', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(46, 'Reached by HYO', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(47, 'Referred to RHU', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(48, 'Referred to Hospital', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(49, 'Referred to DSWD', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(50, 'Parental Notification', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(51, 'Preventive Counseling', '', '2025-05-23 03:20:31', 100, 1, 'hospital', NULL),
(52, 'Assessed using HEEADSSS', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(53, 'Reached by HYO', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(54, 'Referred to RHU', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(55, 'Referred to Hospital', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(56, 'Referred to DSWD', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(57, 'Parental Notification', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(58, 'Preventive Counseling', '', '2025-05-23 03:20:32', 100, 1, 'hospital', NULL),
(59, 'Referred to Hospital', '', '2025-05-23 03:23:29', 102, 1, 'rhu', NULL),
(60, 'Referred to DSWD', '', '2025-05-23 03:23:29', 102, 1, 'rhu', NULL),
(61, 'Referred to RHU', '', '2025-05-23 03:26:18', 103, 1, 'brgy', NULL),
(62, 'Referred to Hospital', '', '2025-05-23 03:26:18', 103, 1, 'brgy', NULL),
(63, 'Referred to RHU', '', '2025-05-23 03:26:30', 103, 1, 'brgy', NULL),
(64, 'Referred to Hospital', '', '2025-05-23 03:26:30', 103, 1, 'brgy', NULL),
(65, 'Referred to Hospital', '', '2025-05-23 04:46:30', 104, 1, 'brgy', NULL),
(66, 'Assessed using HEEADSSS', '', '2025-05-23 05:40:00', 110, 1, 'rhu', NULL),
(69, 'Assessed using HEEADSSS', '', '2025-05-23 05:41:12', 110, 1, 'rhu', NULL),
(70, 'Assessed using HEEADSSS', '', '2025-05-23 05:41:51', 110, 1, 'rhu', NULL),
(72, 'Assessed using HEEADSSS', '', '2025-05-23 06:31:28', 111, 1, 'rhu', NULL),
(73, 'Assessed using HEEADSSS', '', '2025-05-23 07:37:18', 113, 1, 'brgy', NULL),
(74, 'Referred to RHU', '', '2025-05-23 07:37:18', 113, 1, 'brgy', NULL),
(75, 'Parental Notification', '', '2025-05-23 07:37:18', 113, 1, 'brgy', NULL),
(76, 'Preventive Counseling', '', '2025-05-23 07:37:18', 113, 1, 'brgy', NULL),
(92, 'Assessed using HEEADSSS', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(93, 'Reached by HYO', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(94, 'Referred to RHU', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(95, 'Refer to Hospital', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(96, 'Parental Notification', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(97, 'Preventive Counseling', '', '2025-05-23 07:43:52', 114, 1, 'brgy', NULL),
(98, 'Assessed using HEEADSSS', '', '2025-05-25 13:14:43', 105, 1, 'brgy', NULL),
(99, 'Assessed using HEEADSSS', '', '2025-05-27 02:04:51', 116, 1, 'brgy', NULL),
(100, 'Parental Notification', '', '2025-05-27 02:04:51', 116, 1, 'brgy', NULL),
(101, 'Assessed using HEEADSSS', '', '2025-05-27 02:26:52', 115, 1, 'brgy', NULL),
(102, 'Assessed using HEEADSSS', '', '2025-05-27 05:39:50', 121, 1, 'brgy', NULL),
(104, 'Assessed using HEEADSSS', '', '2025-05-27 06:21:51', 118, 1, 'brgy', NULL),
(105, 'Assessed using HEEADSSS', '', '2025-05-27 06:23:56', 119, 1, 'brgy', NULL),
(106, 'Assessed using HEEADSSS', '', '2025-05-27 06:40:37', 127, 1, 'brgy', NULL),
(107, 'Assessed using HEEADSSS', '', '2025-05-27 06:43:51', 128, 1, 'brgy', NULL),
(108, 'Parental Notification', '', '2025-05-27 06:43:51', 128, 1, 'brgy', NULL),
(109, 'Assessed using HEEADSSS', '', '2025-05-27 07:22:57', 122, 1, 'brgy', NULL),
(110, 'Parental Notification', '', '2025-05-27 07:22:57', 122, 1, 'brgy', NULL),
(122, 'Assessed using HEEADSSS', '', '2025-05-28 00:04:08', 134, 1, 'brgy', NULL),
(123, 'Reached by HYO', '', '2025-05-28 00:04:08', 134, 1, 'brgy', NULL),
(124, 'Preventive Counseling', '', '2025-05-28 00:04:08', 134, 1, 'brgy', NULL),
(125, 'Assessed using HEEADSSS', '', '2025-05-28 00:04:25', 134, 1, 'rhu', NULL),
(126, 'Reached by HYO', '', '2025-05-28 00:04:25', 134, 1, 'rhu', NULL),
(127, 'Preventive Counseling', '', '2025-05-28 00:04:25', 134, 1, 'rhu', NULL),
(128, 'Assessed using HEEADSSS', '', '2025-05-28 00:04:43', 119, 1, 'rhu', NULL),
(129, 'Parental Notification', '', '2025-05-28 00:04:43', 119, 1, 'rhu', NULL),
(130, 'Assessed using HEEADSSS', '', '2025-05-28 00:08:31', 119, 1, 'unknown', NULL),
(131, 'Reached by HYO', '', '2025-05-28 00:08:31', 119, 1, 'unknown', NULL),
(132, 'Parental Notification', '', '2025-05-28 00:08:31', 119, 1, 'unknown', NULL),
(133, 'Assessed using HEEADSSS', '', '2025-05-28 00:14:30', 119, 1, 'hospital', NULL),
(134, 'Reached by HYO', '', '2025-05-28 00:14:30', 119, 1, 'hospital', NULL),
(135, 'Parental Notification', '', '2025-05-28 00:14:30', 119, 1, 'hospital', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `signature`
--

CREATE TABLE `signature` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `signature`
--

INSERT INTO `signature` (`id`, `admin_id`, `user_id`, `filename`, `timestamp`) VALUES
(1, NULL, 98, '20250523014351470789_signature.png', '2025-05-23 01:43:51'),
(2, NULL, 100, '20250523031432104587_signature.png', '2025-05-23 03:14:32'),
(11, NULL, 105, '20250523053944445838_signature.png', '2025-05-23 05:39:44'),
(12, NULL, 105, '20250523053951507745_signature.png', '2025-05-23 05:39:51'),
(13, NULL, 110, '20250523054109180305_signature.png', '2025-05-23 05:41:09'),
(14, NULL, 111, '20250523063127345695_signature.png', '2025-05-23 06:31:27'),
(15, NULL, 113, '20250523073715814668_signature.png', '2025-05-23 07:37:15'),
(16, NULL, 114, '20250523074210245862_signature.png', '2025-05-23 07:42:10'),
(17, NULL, 115, '20250527020018553657_signature.png', '2025-05-27 02:00:18'),
(18, NULL, 116, '20250527020450649414_signature.png', '2025-05-27 02:04:50'),
(19, NULL, 121, '20250527053949016768_signature.png', '2025-05-27 05:39:49');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `control_num` varchar(255) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_initial` varchar(5) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `age` int(11) NOT NULL,
  `contact` varchar(13) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `region` varchar(30) NOT NULL,
  `province` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `barangay` varchar(30) NOT NULL,
  `street` varchar(50) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `location` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `assigned_center` varchar(100) NOT NULL,
  `referral_history` text NOT NULL,
  `reason` varchar(255) NOT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `visible_to_brgy` tinyint(1) NOT NULL,
  `visible_to_rhu` tinyint(1) NOT NULL,
  `visible_to_hospital` tinyint(1) NOT NULL,
  `last_forwarded_by` varchar(150) NOT NULL,
  `last_forwarded_by_position` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `control_num`, `first_name`, `middle_initial`, `last_name`, `dob`, `age`, `contact`, `sex`, `region`, `province`, `city`, `barangay`, `street`, `is_deleted`, `location`, `date`, `assigned_center`, `referral_history`, `reason`, `submitted_at`, `visible_to_brgy`, `visible_to_rhu`, `visible_to_hospital`, `last_forwarded_by`, `last_forwarded_by_position`) VALUES
(96, '0837-01-00001', 'Ruth', 'C.', 'Copino', '2013-02-08', 12, '09354320561', 'Female', '08', '0837', '083748', '083748041', 'Eramos Street', 0, 'BHS Union AFHF', '2025-05-23', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', '2025-05-23 01:17:17', 1, 0, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(98, '0837-01-00003', 'Kyla', 'S', 'Verona', '2006-05-10', 19, '09786543452', 'Female', '08', '0837', '083748', '083748034', '', 0, 'BHS Union AFHF', '2025-05-23', '', '', '', NULL, 1, 0, 0, '', ''),
(100, '0837-04-00001', 'Aley', 'Dota', 'Ako', '2007-05-04', 18, '09123456789', 'Female', '08', '0837', '083724', '083724001', 'Purok 2', 0, 'Abuyog DH AFHF', '2025-05-23', '', '', '', NULL, 0, 0, 1, '', ''),
(104, '0837-01-00006', 'Ruth', 'M', 'Onpi', '2011-05-23', 14, '09786445362', 'Female', '08', '0837', '083748', '083748041', '', 0, 'BHS Union AFHF', '2025-05-23', '', '', '', NULL, 1, 0, 0, '', ''),
(105, '0837-01-00007', 'Kara', 'O', 'Pascasio', '2013-05-23', 12, '09688531147', 'Female', '08', '0837', '083735', '083735015', 'Purok 1', 0, 'BHS Union AFHF', '2025-05-23', 'Abuyog DH AFHF', 'BHS Union AFHF → RHU Mayorga → Abuyog DH AFHF', '', NULL, 1, 1, 1, 'Dr. Lorem Ipsum', 'Doctor'),
(110, '0837-02-00002', 'LITO', 'COCHE', 'SAÑO', '2010-03-27', 15, '09293223725', 'Male', '08', '0837', '083735', '083735015', 'Zone 2', 0, 'RHU Mayorga', '2025-05-15', 'Abuyog DH AFHF', 'RHU Mayorga → Abuyog DH AFHF', '', NULL, 0, 1, 1, 'Dr. Lorem Ipsum', 'Doctor'),
(111, '0860-04-00001', 'Yyy', 'F', 'Y7y', '2011-05-13', 14, '09995675463', 'Female', '08', '0860', '086010', '086010010', '', 0, 'RHU Pagsanghan', '2025-05-23', 'Gandara DH AFHF', 'RHU Pagsanghan → Gandara DH AFHF', '', NULL, 0, 1, 1, 'Aljon L. Aa', 'IT'),
(113, '0837-01-00009', 'Mel', 'D', 'Marcos', '1991-06-23', 33, '092728323731', 'Male', '08', '0837', '083735', '083735009', '', 0, 'BHS Union AFHF', '2025-05-23', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', NULL, 1, 1, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(114, '0837-01-00010', 'Leo', 'D', 'Erne', '2012-05-23', 12, '0982123456', 'Male', '08', '0837', '083735', '083735001', '', 0, 'BHS Union AFHF', '2025-05-23', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', NULL, 1, 1, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(115, '0837-01-00011', 'Leo', 'S', 'Yepe', '2014-05-14', 11, '09097896532', 'Male', '08', '0837', '083748', '083748041', '', 0, 'BHS Union AFHF', '2025-05-27', '', '', '', NULL, 1, 0, 0, '', ''),
(116, '0837-01-00012', 'Rosie', 'B.', 'Cruz', '2012-05-27', 12, '09368907635', 'Female', '08', '0837', '083748', '083748042', '', 0, 'BHS Union AFHF', '2025-05-27', 'Abuyog DH AFHF', 'BHS Union AFHF → RHU Mayorga → Abuyog DH AFHF', '', NULL, 1, 1, 1, 'Dr. Lorem Ipsum', 'Doctor'),
(118, '0837-01-00014', 'Aa', 'A', 'A', '0000-00-00', 0, '', 'Please Sel', '08', '0837', '083715', '083715011', '', 0, 'BHS Union AFHF', '2025-05-27', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', NULL, 0, 1, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(119, '0837-01-00015', 'C', 'C', 'C', '0000-00-00', 0, '', 'Please Sel', '08', '0837', '083714', '083714011', '', 0, 'BHS Union AFHF', '2025-05-27', 'Abuyog DH AFHF', 'BHS Union AFHF → RHU Mayorga → Abuyog DH AFHF', '', NULL, 1, 1, 1, 'Dr. Lorem Ipsum', 'Doctor'),
(120, '0837-01-00016', 'D', 'D', 'D', '0000-00-00', 0, '', 'Please Sel', '08', '0837', '083717', '083717011', '', 0, 'BHS Union AFHF', '2025-05-27', '', '', '', NULL, 0, 0, 0, '', ''),
(121, '0837-01-00017', 'Bbb', 'Uu', 'Ii', '2017-05-12', 8, '09996666543', 'Male', '08', '0837', '083702', '083702005', '', 0, 'BHS Union AFHF', '2025-05-27', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', NULL, 0, 0, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(122, '0837-01-00018', 'samplw', 'e', 'eew', '2013-06-05', 11, '09099873612', 'Male', '08', '0837', '083717', '083717012', '', 0, 'BHS Union AFHF', '2025-05-27', 'RHU Mayorga', 'BHS Union AFHF → RHU Mayorga', '', '2025-05-27 06:12:22', 1, 0, 0, 'Lorem Ipsum BHS', 'Barangay Health Worker'),
(134, '0837-01-00019', 'Rrt', '', '', '0000-00-00', 0, '', 'Please Sel', '01', '0128', '012802', '012802001', '', 0, 'BHS Union AFHF', '0000-00-00', 'Abuyog DH AFHF', 'BHS Union AFHF → RHU Mayorga → Abuyog DH AFHF', '', NULL, 1, 1, 1, 'Dr. Lorem Ipsum', 'Doctor');

-- --------------------------------------------------------

--
-- Table structure for table `user_response`
--

CREATE TABLE `user_response` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `question_number` int(11) NOT NULL,
  `response` varchar(10) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `submitted_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_response`
--

INSERT INTO `user_response` (`id`, `user_id`, `question_number`, `response`, `is_read`, `submitted_at`) VALUES
(1, 96, 1, 'Yes', 0, '2025-05-23 09:17:23'),
(2, 96, 2, 'No', 0, '2025-05-23 09:17:27'),
(3, 96, 3, 'Yes', 0, '2025-05-23 09:17:29'),
(4, 96, 4, 'No', 0, '2025-05-23 09:17:32'),
(5, 96, 5, 'No', 0, '2025-05-23 09:17:35'),
(6, 96, 6, 'No', 0, '2025-05-23 09:17:39'),
(7, 96, 7, 'No', 0, '2025-05-23 09:17:42'),
(8, 96, 8, 'No', 0, '2025-05-23 09:17:50'),
(9, 96, 9, 'No', 0, '2025-05-23 09:17:54'),
(10, 96, 10, 'No', 0, '2025-05-23 09:17:56'),
(11, 96, 11, 'No', 0, '2025-05-23 09:18:00'),
(12, 96, 12, 'Yes', 0, '2025-05-23 09:18:06'),
(13, 96, 0, 'Completed ', 0, '2025-05-23 09:18:11'),
(27, 98, 1, 'No', 0, '2025-05-23 09:40:34'),
(28, 98, 2, 'No', 0, '2025-05-23 09:40:35'),
(29, 98, 3, 'No', 0, '2025-05-23 09:40:36'),
(30, 98, 4, 'No', 0, '2025-05-23 09:40:37'),
(31, 98, 5, 'No', 0, '2025-05-23 09:40:38'),
(32, 98, 6, 'No', 0, '2025-05-23 09:40:39'),
(33, 98, 7, 'No', 0, '2025-05-23 09:40:41'),
(34, 98, 8, 'No', 0, '2025-05-23 09:40:43'),
(35, 98, 9, 'Yes', 0, '2025-05-23 09:40:53'),
(36, 98, 10, 'Yes', 0, '2025-05-23 09:40:57'),
(37, 98, 11, 'No', 0, '2025-05-23 09:41:04'),
(38, 98, 12, 'Yes', 0, '2025-05-23 09:42:01'),
(39, 98, 0, 'Completed ', 0, '2025-05-23 09:42:01'),
(55, 100, 1, 'Yes', 0, '2025-05-23 11:12:21'),
(56, 100, 2, 'Yes', 0, '2025-05-23 11:12:26'),
(57, 100, 3, 'Yes', 0, '2025-05-23 11:12:32'),
(58, 100, 4, 'Yes', 0, '2025-05-23 11:12:36'),
(60, 100, 5, 'No', 0, '2025-05-23 11:12:38'),
(61, 100, 6, 'No', 0, '2025-05-23 11:12:40'),
(62, 100, 7, 'No', 0, '2025-05-23 11:12:44'),
(63, 100, 8, 'Yes', 0, '2025-05-23 11:12:47'),
(64, 100, 9, 'No', 0, '2025-05-23 11:12:49'),
(65, 100, 10, 'No', 0, '2025-05-23 11:12:53'),
(66, 100, 11, 'No', 0, '2025-05-23 11:12:56'),
(67, 100, 12, 'Yes', 0, '2025-05-23 11:13:02'),
(68, 100, 0, 'Completed ', 0, '2025-05-23 11:13:02'),
(110, 104, 1, 'Yes', 0, '2025-05-23 12:45:31'),
(111, 104, 2, 'No', 0, '2025-05-23 12:45:51'),
(112, 104, 3, 'No', 0, '2025-05-23 12:45:52'),
(113, 104, 4, 'Yes', 0, '2025-05-23 12:45:54'),
(114, 104, 5, 'No', 0, '2025-05-23 12:45:56'),
(115, 104, 6, 'No', 0, '2025-05-23 12:46:01'),
(116, 104, 7, 'No', 0, '2025-05-23 12:46:02'),
(117, 104, 8, 'No', 0, '2025-05-23 12:46:03'),
(118, 104, 9, 'No', 0, '2025-05-23 12:46:05'),
(119, 104, 10, 'Yes', 0, '2025-05-23 12:46:06'),
(120, 104, 11, 'No', 0, '2025-05-23 12:46:11'),
(121, 104, 12, 'Yes', 0, '2025-05-23 12:46:13'),
(122, 104, 0, 'Completed ', 0, '2025-05-23 12:46:13'),
(123, 105, 1, 'Yes', 0, '2025-05-23 13:37:16'),
(124, 105, 2, 'Yes', 0, '2025-05-23 13:37:24'),
(126, 105, 3, 'No', 0, '2025-05-23 13:37:28'),
(127, 105, 4, 'No', 0, '2025-05-23 13:37:32'),
(129, 105, 5, 'Yes', 0, '2025-05-23 13:37:35'),
(130, 105, 6, 'Yes', 0, '2025-05-23 13:37:37'),
(131, 105, 7, 'No', 0, '2025-05-23 13:37:40'),
(133, 105, 8, 'Yes', 0, '2025-05-23 13:37:43'),
(134, 105, 9, 'No', 0, '2025-05-23 13:37:45'),
(135, 105, 10, 'No', 0, '2025-05-23 13:37:48'),
(137, 105, 11, 'No', 0, '2025-05-23 13:37:51'),
(139, 105, 12, 'Yes', 0, '2025-05-23 13:37:53'),
(140, 105, 0, 'Completed ', 0, '2025-05-23 13:37:53'),
(141, 110, 1, 'No', 0, '2025-05-23 13:37:56'),
(145, 110, 2, 'No', 0, '2025-05-23 13:38:03'),
(148, 110, 3, 'No', 0, '2025-05-23 13:38:14'),
(150, 110, 4, 'No', 0, '2025-05-23 13:38:21'),
(152, 110, 5, 'No', 0, '2025-05-23 13:38:26'),
(153, 110, 6, 'Yes', 0, '2025-05-23 13:38:30'),
(155, 110, 7, 'No', 0, '2025-05-23 13:38:36'),
(156, 110, 8, 'Yes', 0, '2025-05-23 13:38:42'),
(157, 110, 9, 'Yes', 0, '2025-05-23 13:38:47'),
(158, 110, 10, 'Yes', 0, '2025-05-23 13:38:56'),
(159, 110, 11, 'Yes', 0, '2025-05-23 13:39:03'),
(160, 110, 12, 'Yes', 0, '2025-05-23 13:39:10'),
(161, 110, 0, 'Completed ', 0, '2025-05-23 13:39:10'),
(162, 111, 1, 'Yes', 0, '2025-05-23 14:30:58'),
(163, 111, 2, 'No', 0, '2025-05-23 14:30:59'),
(164, 111, 3, 'No', 0, '2025-05-23 14:30:59'),
(165, 111, 4, 'No', 0, '2025-05-23 14:31:02'),
(166, 111, 5, 'No', 0, '2025-05-23 14:31:03'),
(167, 111, 6, 'Yes', 0, '2025-05-23 14:31:04'),
(168, 111, 7, 'No', 0, '2025-05-23 14:31:05'),
(169, 111, 8, 'No', 0, '2025-05-23 14:31:06'),
(170, 111, 9, 'No', 0, '2025-05-23 14:31:07'),
(171, 111, 10, 'Yes', 0, '2025-05-23 14:31:10'),
(172, 111, 11, 'No', 0, '2025-05-23 14:31:11'),
(173, 111, 12, 'Yes', 0, '2025-05-23 14:31:12'),
(174, 111, 0, 'Completed ', 0, '2025-05-23 14:31:12'),
(188, 113, 1, 'Yes', 0, '2025-05-23 15:33:49'),
(189, 113, 2, 'Yes', 0, '2025-05-23 15:33:50'),
(190, 113, 3, 'Yes', 0, '2025-05-23 15:33:52'),
(191, 113, 4, 'Yes', 0, '2025-05-23 15:33:53'),
(192, 113, 5, 'Yes', 0, '2025-05-23 15:33:54'),
(193, 113, 6, 'Yes', 0, '2025-05-23 15:33:56'),
(194, 113, 7, 'Yes', 0, '2025-05-23 15:33:57'),
(195, 113, 8, 'Yes', 0, '2025-05-23 15:33:59'),
(196, 113, 9, 'Yes', 0, '2025-05-23 15:34:00'),
(197, 113, 10, 'Yes', 0, '2025-05-23 15:34:01'),
(198, 113, 11, 'Yes', 0, '2025-05-23 15:34:03'),
(199, 113, 12, 'Yes', 0, '2025-05-23 15:34:04'),
(200, 113, 0, 'Completed ', 0, '2025-05-23 15:34:04'),
(201, 114, 1, 'Yes', 0, '2025-05-23 15:41:14'),
(202, 114, 2, 'No', 0, '2025-05-23 15:41:16'),
(203, 114, 3, 'No', 0, '2025-05-23 15:41:18'),
(204, 114, 4, 'No', 0, '2025-05-23 15:41:20'),
(205, 114, 5, 'Yes', 0, '2025-05-23 15:41:23'),
(206, 114, 6, 'No', 0, '2025-05-23 15:41:24'),
(207, 114, 7, 'Yes', 0, '2025-05-23 15:41:26'),
(208, 114, 8, 'No', 0, '2025-05-23 15:41:27'),
(209, 114, 9, 'No', 0, '2025-05-23 15:41:28'),
(210, 114, 10, 'No', 0, '2025-05-23 15:41:30'),
(211, 114, 11, 'No', 0, '2025-05-23 15:41:32'),
(212, 114, 12, 'No', 0, '2025-05-23 15:41:33'),
(213, 114, 0, 'Completed ', 0, '2025-05-23 15:41:33'),
(214, 115, 1, 'Yes', 0, '2025-05-27 09:58:52'),
(215, 115, 2, 'No', 0, '2025-05-27 09:58:53'),
(216, 115, 3, 'No', 0, '2025-05-27 09:58:54'),
(217, 115, 4, 'Yes', 0, '2025-05-27 09:58:55'),
(218, 115, 5, 'No', 0, '2025-05-27 09:58:58'),
(219, 115, 6, 'No', 0, '2025-05-27 09:59:00'),
(220, 115, 7, 'No', 0, '2025-05-27 09:59:02'),
(221, 115, 8, 'No', 0, '2025-05-27 09:59:04'),
(222, 115, 9, 'No', 0, '2025-05-27 09:59:06'),
(223, 115, 10, 'Yes', 0, '2025-05-27 09:59:07'),
(224, 115, 11, 'No', 0, '2025-05-27 09:59:08'),
(225, 115, 12, 'Yes', 0, '2025-05-27 09:59:11'),
(226, 115, 0, 'Completed ', 0, '2025-05-27 09:59:12'),
(227, 116, 1, 'Yes', 0, '2025-05-27 10:04:04'),
(228, 116, 2, 'Yes', 0, '2025-05-27 10:04:07'),
(229, 116, 3, 'Yes', 0, '2025-05-27 10:04:09'),
(230, 116, 4, 'No', 0, '2025-05-27 10:04:10'),
(231, 116, 5, 'No', 0, '2025-05-27 10:04:12'),
(232, 116, 6, 'No', 0, '2025-05-27 10:04:13'),
(233, 116, 7, 'No', 0, '2025-05-27 10:04:14'),
(234, 116, 8, 'No', 0, '2025-05-27 10:04:14'),
(235, 116, 9, 'No', 0, '2025-05-27 10:04:15'),
(236, 116, 10, 'No', 0, '2025-05-27 10:04:16'),
(237, 116, 11, 'No', 0, '2025-05-27 10:04:17'),
(238, 116, 12, 'Yes', 0, '2025-05-27 10:04:18'),
(239, 116, 0, 'Completed ', 0, '2025-05-27 10:04:18'),
(253, 118, 1, 'Yes', 0, '2025-05-27 10:54:41'),
(254, 118, 2, 'No', 0, '2025-05-27 10:54:42'),
(255, 118, 3, 'No', 0, '2025-05-27 10:54:47'),
(256, 118, 4, 'Yes', 0, '2025-05-27 10:54:49'),
(257, 118, 5, 'No', 0, '2025-05-27 10:54:51'),
(258, 118, 6, 'No', 0, '2025-05-27 10:54:52'),
(259, 118, 7, 'No', 0, '2025-05-27 10:54:53'),
(260, 118, 8, 'No', 0, '2025-05-27 10:54:54'),
(261, 118, 9, 'No', 0, '2025-05-27 10:54:56'),
(262, 118, 10, 'Yes', 0, '2025-05-27 10:54:57'),
(263, 118, 11, 'No', 0, '2025-05-27 10:54:59'),
(264, 118, 12, 'Yes', 0, '2025-05-27 10:55:02'),
(265, 118, 0, 'Completed ', 0, '2025-05-27 10:55:02'),
(266, 119, 1, 'Yes', 0, '2025-05-27 11:16:29'),
(267, 119, 2, 'No', 0, '2025-05-27 11:16:31'),
(268, 119, 3, 'No', 0, '2025-05-27 11:16:32'),
(269, 119, 4, 'Yes', 0, '2025-05-27 11:16:34'),
(270, 119, 5, 'No', 0, '2025-05-27 11:16:35'),
(271, 119, 6, 'No', 0, '2025-05-27 11:16:37'),
(272, 119, 7, 'No', 0, '2025-05-27 11:16:38'),
(273, 119, 8, 'No', 0, '2025-05-27 11:16:39'),
(274, 119, 9, 'No', 0, '2025-05-27 11:16:40'),
(275, 119, 10, 'Yes', 0, '2025-05-27 11:16:43'),
(276, 119, 11, 'No', 0, '2025-05-27 11:16:50'),
(277, 119, 12, 'Yes', 0, '2025-05-27 11:16:55'),
(278, 119, 0, 'Completed ', 0, '2025-05-27 11:16:55'),
(279, 120, 1, 'Yes', 0, '2025-05-27 11:26:24'),
(280, 120, 2, 'No', 0, '2025-05-27 11:26:25'),
(281, 120, 3, 'No', 0, '2025-05-27 11:26:26'),
(282, 120, 4, 'Yes', 0, '2025-05-27 11:26:29'),
(283, 120, 5, 'No', 0, '2025-05-27 11:26:32'),
(284, 120, 6, 'No', 0, '2025-05-27 11:26:34'),
(285, 120, 7, 'No', 0, '2025-05-27 11:26:35'),
(286, 120, 8, 'No', 0, '2025-05-27 11:26:37'),
(287, 120, 9, 'No', 0, '2025-05-27 11:26:39'),
(288, 120, 10, 'Yes', 0, '2025-05-27 11:26:41'),
(289, 120, 11, 'No', 0, '2025-05-27 11:26:42'),
(290, 120, 12, 'Yes', 0, '2025-05-27 11:26:43'),
(291, 120, 0, 'Completed ', 0, '2025-05-27 11:26:43'),
(292, 121, 1, 'Yes', 0, '2025-05-27 13:39:20'),
(293, 121, 2, 'No', 0, '2025-05-27 13:39:22'),
(294, 121, 3, 'No', 0, '2025-05-27 13:39:23'),
(295, 121, 4, 'No', 0, '2025-05-27 13:39:25'),
(296, 121, 5, 'No', 0, '2025-05-27 13:39:26'),
(297, 121, 6, 'No', 0, '2025-05-27 13:39:27'),
(298, 121, 7, 'No', 0, '2025-05-27 13:39:27'),
(299, 121, 8, 'No', 0, '2025-05-27 13:39:28'),
(300, 121, 9, 'No', 0, '2025-05-27 13:39:30'),
(301, 121, 10, 'No', 0, '2025-05-27 13:39:31'),
(302, 121, 11, 'No', 0, '2025-05-27 13:39:32'),
(303, 121, 12, 'Yes', 0, '2025-05-27 13:39:34'),
(304, 121, 0, 'Completed ', 0, '2025-05-27 13:39:34'),
(305, 122, 1, 'Yes', 0, '2025-05-27 14:12:25'),
(306, 122, 2, 'No', 0, '2025-05-27 14:12:27'),
(307, 122, 3, 'No', 0, '2025-05-27 14:12:29'),
(308, 122, 4, 'No', 0, '2025-05-27 14:12:33'),
(309, 122, 5, 'Yes', 0, '2025-05-27 14:12:36'),
(310, 122, 6, 'No', 0, '2025-05-27 14:12:38'),
(311, 122, 7, 'No', 0, '2025-05-27 14:12:41'),
(312, 122, 8, 'No', 0, '2025-05-27 14:12:44'),
(313, 122, 9, 'No', 0, '2025-05-27 14:12:47'),
(314, 122, 10, 'No', 0, '2025-05-27 14:12:52'),
(315, 122, 11, 'No', 0, '2025-05-27 14:12:54'),
(316, 122, 12, 'Yes', 0, '2025-05-27 14:12:59'),
(317, 122, 0, 'Completed ', 0, '2025-05-27 14:13:03'),
(318, 122, 0, 'Completed ', 0, '2025-05-27 14:15:34'),
(451, 134, 1, 'No', 0, '2025-05-27 15:21:46'),
(452, 134, 2, 'No', 0, '2025-05-27 15:21:47'),
(453, 134, 3, 'No', 0, '2025-05-27 15:21:48'),
(454, 134, 4, 'No', 0, '2025-05-27 15:21:48'),
(455, 134, 5, 'No', 0, '2025-05-27 15:21:49'),
(456, 134, 6, 'No', 0, '2025-05-27 15:21:50'),
(457, 134, 7, 'No', 0, '2025-05-27 15:21:50'),
(458, 134, 8, 'No', 0, '2025-05-27 15:21:51'),
(459, 134, 9, 'No', 0, '2025-05-27 15:21:51'),
(460, 134, 10, 'No', 0, '2025-05-27 15:21:52'),
(461, 134, 11, 'No', 0, '2025-05-27 15:21:53'),
(462, 134, 12, 'Yes', 0, '2025-05-27 15:21:54'),
(463, 134, 0, 'Completed ', 0, '2025-05-27 15:21:54');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `assessment`
--
ALTER TABLE `assessment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `assessment_response`
--
ALTER TABLE `assessment_response`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `referral_history`
--
ALTER TABLE `referral_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `signature`
--
ALTER TABLE `signature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_response`
--
ALTER TABLE `user_response`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `assessment`
--
ALTER TABLE `assessment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `assessment_response`
--
ALTER TABLE `assessment_response`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=618;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `referral_history`
--
ALTER TABLE `referral_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=136;

--
-- AUTO_INCREMENT for table `signature`
--
ALTER TABLE `signature`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;

--
-- AUTO_INCREMENT for table `user_response`
--
ALTER TABLE `user_response`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=464;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `referral_history`
--
ALTER TABLE `referral_history`
  ADD CONSTRAINT `referral_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `signature`
--
ALTER TABLE `signature`
  ADD CONSTRAINT `signature_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`),
  ADD CONSTRAINT `signature_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `user_response`
--
ALTER TABLE `user_response`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
