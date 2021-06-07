-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 06, 2021 at 07:10 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iitb`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add register', 7, 'add_register'),
(26, 'Can change register', 7, 'change_register'),
(27, 'Can delete register', 7, 'delete_register'),
(28, 'Can view register', 7, 'view_register'),
(29, 'Can add city', 8, 'add_city'),
(30, 'Can change city', 8, 'change_city'),
(31, 'Can delete city', 8, 'delete_city'),
(32, 'Can view city', 8, 'view_city'),
(33, 'Can add education', 9, 'add_education'),
(34, 'Can change education', 9, 'change_education'),
(35, 'Can delete education', 9, 'delete_education'),
(36, 'Can view education', 9, 'view_education'),
(37, 'Can add family type', 10, 'add_familytype'),
(38, 'Can change family type', 10, 'change_familytype'),
(39, 'Can delete family type', 10, 'delete_familytype'),
(40, 'Can view family type', 10, 'view_familytype'),
(41, 'Can add occupation', 11, 'add_occupation'),
(42, 'Can change occupation', 11, 'change_occupation'),
(43, 'Can delete occupation', 11, 'delete_occupation'),
(44, 'Can view occupation', 11, 'view_occupation'),
(45, 'Can add parents info', 12, 'add_parentsinfo'),
(46, 'Can change parents info', 12, 'change_parentsinfo'),
(47, 'Can delete parents info', 12, 'delete_parentsinfo'),
(48, 'Can view parents info', 12, 'view_parentsinfo'),
(49, 'Can add religious belief', 13, 'add_religiousbelief'),
(50, 'Can change religious belief', 13, 'change_religiousbelief'),
(51, 'Can delete religious belief', 13, 'delete_religiousbelief'),
(52, 'Can view religious belief', 13, 'view_religiousbelief'),
(53, 'Can add state', 14, 'add_state'),
(54, 'Can change state', 14, 'change_state'),
(55, 'Can delete state', 14, 'delete_state'),
(56, 'Can view state', 14, 'view_state'),
(57, 'Can add school', 15, 'add_school'),
(58, 'Can change school', 15, 'change_school'),
(59, 'Can delete school', 15, 'delete_school'),
(60, 'Can view school', 15, 'view_school'),
(61, 'Can add students info', 16, 'add_studentsinfo'),
(62, 'Can change students info', 16, 'change_studentsinfo'),
(63, 'Can delete students info', 16, 'delete_studentsinfo'),
(64, 'Can view students info', 16, 'view_studentsinfo');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$216000$ENhIZVt9Btk6$k3Dtd/gFMOhgM8aWrJ54STCYE1sVbquyCAY0fO/UhXM=', '2021-06-05 06:22:17.782317', 1, 'ishaa', '', '', '', 1, 1, '2021-06-05 06:21:57.042910'),
(2, 'pbkdf2_sha256$216000$lUuEUtsU1UPc$JNe37G2UsctMwGSIOTv4SAJCQ/HbVbSHOdi7gYbLU+4=', NULL, 0, 'ishajoglekar', '', '', '', 0, 1, '2021-06-05 06:31:14.492443'),
(3, 'pbkdf2_sha256$216000$uS1nPVylTlvm$9vkBw5cscaUKfYquaT+Awyj4gvf/y0dA6+FJmyZWaVk=', NULL, 0, 'khushilshah', '', '', '', 0, 1, '2021-06-05 07:23:19.974857'),
(4, 'pbkdf2_sha256$216000$TyLw1oy4UvPg$qEXwKQlRDOvx1zyqHfvkE7lj0pYhGaQO32zPMSpM3tc=', NULL, 0, 'chintan', '', '', '', 0, 1, '2021-06-05 09:49:51.293266'),
(5, 'pbkdf2_sha256$216000$ZdgMylTQ4eHh$oyUFzguqCghtb5HOgpgo38oPQ28N4OE+P5nYeL13r/M=', NULL, 0, 'johndoe', '', '', '', 0, 1, '2021-06-05 09:51:38.186151'),
(6, 'pbkdf2_sha256$216000$zicrAD1Z2ehp$Rye3XJU/hAHwIsCfftgmCv9M4q13r64LF8LonyjjRwk=', NULL, 0, 'sheldon', '', '', '', 0, 1, '2021-06-05 10:19:42.294244');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(8, 'registration', 'city'),
(9, 'registration', 'education'),
(10, 'registration', 'familytype'),
(11, 'registration', 'occupation'),
(12, 'registration', 'parentsinfo'),
(7, 'registration', 'register'),
(13, 'registration', 'religiousbelief'),
(15, 'registration', 'school'),
(14, 'registration', 'state'),
(16, 'registration', 'studentsinfo'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-05-04 22:30:37.386271'),
(2, 'auth', '0001_initial', '2021-05-04 22:30:37.784098'),
(3, 'admin', '0001_initial', '2021-05-04 22:30:38.680681'),
(4, 'admin', '0002_logentry_remove_auto_add', '2021-05-04 22:30:38.887275'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2021-05-04 22:30:38.921925'),
(6, 'contenttypes', '0002_remove_content_type_name', '2021-05-04 22:30:39.061117'),
(7, 'auth', '0002_alter_permission_name_max_length', '2021-05-04 22:30:39.175154'),
(8, 'auth', '0003_alter_user_email_max_length', '2021-05-04 22:30:39.228247'),
(9, 'auth', '0004_alter_user_username_opts', '2021-05-04 22:30:39.268622'),
(10, 'auth', '0005_alter_user_last_login_null', '2021-05-04 22:30:39.356109'),
(11, 'auth', '0006_require_contenttypes_0002', '2021-05-04 22:30:39.368382'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2021-05-04 22:30:39.399695'),
(13, 'auth', '0008_alter_user_username_max_length', '2021-05-04 22:30:39.447162'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2021-05-04 22:30:39.523750'),
(15, 'auth', '0010_alter_group_name_max_length', '2021-05-04 22:30:39.577407'),
(16, 'auth', '0011_update_proxy_permissions', '2021-05-04 22:30:39.609058'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2021-05-04 22:30:39.659330'),
(18, 'registration', '0001_initial', '2021-05-04 22:30:39.751893'),
(19, 'registration', '0002_auto_20210504_2101', '2021-05-04 22:30:39.898568'),
(20, 'registration', '0003_auto_20210504_2118', '2021-05-04 22:30:40.077935'),
(21, 'sessions', '0001_initial', '2021-05-04 22:30:40.136964'),
(22, 'registration', '0004_auto_20210507_1518', '2021-06-05 05:13:36.250501'),
(23, 'registration', '0005_auto_20210517_1253', '2021-06-05 05:13:36.306553'),
(24, 'registration', '0006_auto_20210605_1042', '2021-06-05 05:13:37.152716'),
(25, 'registration', '0007_auto_20210605_1047', '2021-06-05 05:17:42.284598'),
(26, 'registration', '0008_auto_20210605_1049', '2021-06-05 05:19:29.418106'),
(27, 'registration', '0009_auto_20210605_1109', '2021-06-05 05:39:39.730513'),
(28, 'registration', '0010_school_studentsinfo', '2021-06-05 06:36:29.415025'),
(29, 'registration', '0011_studentsinfo_user', '2021-06-05 07:16:46.518815'),
(30, 'registration', '0012_remove_studentsinfo_age', '2021-06-05 07:20:00.318055');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('vbo62kter4l73v5caxp3nnfqc1jl0snq', '.eJxVjEEOwiAUBe_C2hCgIB-X7j1D8-GhVA0kpV0Z765NutDtm5n3EiOvSxnXnudxgjgJLQ6_W-T0yHUDuHO9NZlaXeYpyk2RO-3y0pCf5939Oyjcy7c2ykXlACbvNCylxAMxYyB4shyyMuqIZA1UJLpqbwgWpIMLmY1X4v0B4xU3oA:1lpPhJ:UmD-4YjPtu15rXB2uvshz3gxJTh4a5oyq2eWNl9TaeI', '2021-06-19 06:22:17.788684');

-- --------------------------------------------------------

--
-- Table structure for table `registration_city`
--

CREATE TABLE `registration_city` (
  `id` int(11) NOT NULL,
  `city` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_city`
--

INSERT INTO `registration_city` (`id`, `city`) VALUES
(1, 'Mumbai'),
(2, 'Surat');

-- --------------------------------------------------------

--
-- Table structure for table `registration_education`
--

CREATE TABLE `registration_education` (
  `id` int(11) NOT NULL,
  `education` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_education`
--

INSERT INTO `registration_education` (`id`, `education`) VALUES
(1, 'BTech'),
(2, 'BA');

-- --------------------------------------------------------

--
-- Table structure for table `registration_familytype`
--

CREATE TABLE `registration_familytype` (
  `id` int(11) NOT NULL,
  `family` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_familytype`
--

INSERT INTO `registration_familytype` (`id`, `family`) VALUES
(1, 'Joint Family'),
(2, 'Nuclear');

-- --------------------------------------------------------

--
-- Table structure for table `registration_occupation`
--

CREATE TABLE `registration_occupation` (
  `id` int(11) NOT NULL,
  `occupation` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_occupation`
--

INSERT INTO `registration_occupation` (`id`, `occupation`) VALUES
(1, 'Engineer'),
(2, 'Doctor');

-- --------------------------------------------------------

--
-- Table structure for table `registration_parentsinfo`
--

CREATE TABLE `registration_parentsinfo` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `consent` tinyint(1) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `address` varchar(255) NOT NULL,
  `pincode` int(11) NOT NULL,
  `no_of_family_members` int(11) NOT NULL,
  `children_count` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `edu_id` int(11) NOT NULL,
  `occupation_id` int(11) NOT NULL,
  `religion_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  `type_of_family_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_parentsinfo`
--

INSERT INTO `registration_parentsinfo` (`id`, `email`, `consent`, `name`, `gender`, `age`, `address`, `pincode`, `no_of_family_members`, `children_count`, `city_id`, `edu_id`, `occupation_id`, `religion_id`, `state_id`, `type_of_family_id`, `user_id`) VALUES
(1, 'isha.joglekar@somaiya.edu', 1, 'Ishaa', 'Female', 19, '202 Ramanand Society Savarkar Road', 421201, 3, 1, 1, 1, 1, 1, 1, 2, 2),
(2, 'chintan@gmail.com', 1, 'Chintan Jagad', 'Male', 20, 'Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero', 421201, 5, 4, 1, 1, 1, 1, 1, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `registration_religiousbelief`
--

CREATE TABLE `registration_religiousbelief` (
  `id` int(11) NOT NULL,
  `religion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_religiousbelief`
--

INSERT INTO `registration_religiousbelief` (`id`, `religion`) VALUES
(1, 'Hindu'),
(2, 'Islam'),
(3, 'Jain');

-- --------------------------------------------------------

--
-- Table structure for table `registration_school`
--

CREATE TABLE `registration_school` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `pincode` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_school`
--

INSERT INTO `registration_school` (`id`, `name`, `address`, `pincode`, `city_id`, `state_id`) VALUES
(1, 'KJ Somaiya School', 'Vidyavihar', 400001, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `registration_state`
--

CREATE TABLE `registration_state` (
  `id` int(11) NOT NULL,
  `state` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_state`
--

INSERT INTO `registration_state` (`id`, `state`) VALUES
(1, 'Maharashtra'),
(2, 'Gujarat');

-- --------------------------------------------------------

--
-- Table structure for table `registration_studentsinfo`
--

CREATE TABLE `registration_studentsinfo` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `address` varchar(255) NOT NULL,
  `rollno` int(11) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `dob` date NOT NULL,
  `school_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `registration_studentsinfo`
--

INSERT INTO `registration_studentsinfo` (`id`, `name`, `address`, `rollno`, `gender`, `dob`, `school_id`, `user_id`) VALUES
(1, 'Khushil Shah', 'Fusce vulputate eleifend sapien. Ut leo.', 1234, 'Male', '2001-04-13', 1, 3),
(2, 'John Doe', 'Sed cursus turpis vitae tortor. Donec sodales sagittis magna.', 1234567, 'Male', '2001-04-13', 1, 5),
(3, 'Sheldon', 'Duis vel nibh at velit scelerisque suscipit.', 4566, 'Male', '2021-06-05', 1, 6);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `registration_city`
--
ALTER TABLE `registration_city`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_education`
--
ALTER TABLE `registration_education`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_familytype`
--
ALTER TABLE `registration_familytype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_occupation`
--
ALTER TABLE `registration_occupation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_parentsinfo`
--
ALTER TABLE `registration_parentsinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `registration_parents_type_of_family_id_581a2072_fk_registrat` (`type_of_family_id`),
  ADD KEY `registration_parents_city_id_acbd0e86_fk_registrat` (`city_id`),
  ADD KEY `registration_parents_edu_id_86556239_fk_registrat` (`edu_id`),
  ADD KEY `registration_parents_occupation_id_3ae90877_fk_registrat` (`occupation_id`),
  ADD KEY `registration_parents_state_id_32cacd4e_fk_registrat` (`state_id`),
  ADD KEY `registration_parents_religion_id_4eac561d_fk_registrat` (`religion_id`);

--
-- Indexes for table `registration_religiousbelief`
--
ALTER TABLE `registration_religiousbelief`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_school`
--
ALTER TABLE `registration_school`
  ADD PRIMARY KEY (`id`),
  ADD KEY `registration_school_city_id_5cf5c0a9_fk_registration_city_id` (`city_id`),
  ADD KEY `registration_school_state_id_e924f13d_fk_registration_state_id` (`state_id`);

--
-- Indexes for table `registration_state`
--
ALTER TABLE `registration_state`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration_studentsinfo`
--
ALTER TABLE `registration_studentsinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `registration_student_school_id_3de74945_fk_registrat` (`school_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `registration_city`
--
ALTER TABLE `registration_city`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_education`
--
ALTER TABLE `registration_education`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_familytype`
--
ALTER TABLE `registration_familytype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_occupation`
--
ALTER TABLE `registration_occupation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_parentsinfo`
--
ALTER TABLE `registration_parentsinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_religiousbelief`
--
ALTER TABLE `registration_religiousbelief`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `registration_school`
--
ALTER TABLE `registration_school`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `registration_state`
--
ALTER TABLE `registration_state`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `registration_studentsinfo`
--
ALTER TABLE `registration_studentsinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `registration_parentsinfo`
--
ALTER TABLE `registration_parentsinfo`
  ADD CONSTRAINT `registration_parents_city_id_acbd0e86_fk_registrat` FOREIGN KEY (`city_id`) REFERENCES `registration_city` (`id`),
  ADD CONSTRAINT `registration_parents_edu_id_86556239_fk_registrat` FOREIGN KEY (`edu_id`) REFERENCES `registration_education` (`id`),
  ADD CONSTRAINT `registration_parents_occupation_id_3ae90877_fk_registrat` FOREIGN KEY (`occupation_id`) REFERENCES `registration_occupation` (`id`),
  ADD CONSTRAINT `registration_parents_religion_id_4eac561d_fk_registrat` FOREIGN KEY (`religion_id`) REFERENCES `registration_religiousbelief` (`id`),
  ADD CONSTRAINT `registration_parents_state_id_32cacd4e_fk_registrat` FOREIGN KEY (`state_id`) REFERENCES `registration_state` (`id`),
  ADD CONSTRAINT `registration_parents_type_of_family_id_581a2072_fk_registrat` FOREIGN KEY (`type_of_family_id`) REFERENCES `registration_familytype` (`id`),
  ADD CONSTRAINT `registration_parentsinfo_user_id_7e287518_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `registration_school`
--
ALTER TABLE `registration_school`
  ADD CONSTRAINT `registration_school_city_id_5cf5c0a9_fk_registration_city_id` FOREIGN KEY (`city_id`) REFERENCES `registration_city` (`id`),
  ADD CONSTRAINT `registration_school_state_id_e924f13d_fk_registration_state_id` FOREIGN KEY (`state_id`) REFERENCES `registration_state` (`id`);

--
-- Constraints for table `registration_studentsinfo`
--
ALTER TABLE `registration_studentsinfo`
  ADD CONSTRAINT `registration_student_school_id_3de74945_fk_registrat` FOREIGN KEY (`school_id`) REFERENCES `registration_school` (`id`),
  ADD CONSTRAINT `registration_studentsinfo_user_id_a7efb689_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
