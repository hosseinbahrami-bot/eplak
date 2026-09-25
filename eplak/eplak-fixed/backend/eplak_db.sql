/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100411 (10.4.11-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : eplak_db

 Target Server Type    : MySQL
 Target Server Version : 100411 (10.4.11-MariaDB)
 File Encoding         : 65001

 Date: 20/08/2026 14:49:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin_users
-- ----------------------------
DROP TABLE IF EXISTS `admin_users`;
CREATE TABLE `admin_users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL DEFAULT 'admin',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_users
-- ----------------------------
INSERT INTO `admin_users` VALUES (1, 'admin', '$2y$10$pKyqVTfWPksLZVEsyAfIVuXMuDjF0J7aPt55ymNERRi5wzj/ebx1.', 'super_admin', '2026-08-10 19:11:40');

-- ----------------------------
-- Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `address` varchar(500) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of customers
-- ----------------------------

-- ----------------------------
-- Table structure for departments
-- ----------------------------
DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL COMMENT 'نام واحد',
  `slug` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NULL DEFAULT NULL COMMENT 'نام یکتا برای URL',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NULL DEFAULT NULL COMMENT 'کد اختصاری واحد',
  `parent_id` int UNSIGNED NULL DEFAULT NULL COMMENT 'واحد والد',
  `sort_order` int UNSIGNED NOT NULL DEFAULT 0 COMMENT 'ترتیب نمایش',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'وضعیت فعال/غیرفعال',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NULL COMMENT 'توضیحات واحد',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NULL DEFAULT NULL COMMENT 'آیکون واحد (FontAwesome)',
  `color` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NULL DEFAULT '#0f766e' COMMENT 'رنگ واحد (هگزادسیمال)',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uq_departments_slug`(`slug` ASC) USING BTREE,
  UNIQUE INDEX `uq_departments_code`(`code` ASC) USING BTREE,
  UNIQUE INDEX `uq_departments_name_parent`(`name` ASC, `parent_id` ASC) USING BTREE,
  INDEX `idx_departments_parent`(`parent_id` ASC) USING BTREE,
  INDEX `idx_departments_sort`(`parent_id` ASC, `sort_order` ASC) USING BTREE,
  INDEX `idx_departments_active`(`is_active` ASC) USING BTREE,
  CONSTRAINT `fk_departments_parent` FOREIGN KEY (`parent_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 66 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_persian_ci COMMENT = 'جدول واحدهای سازمانی' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of departments
-- ----------------------------
INSERT INTO `departments` VALUES (1, 'حوزه شهردار', 'hoveze-shahrdar', 'HS', NULL, 1, 1, NULL, 'fa-user-tie', '#1e293b', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (2, 'دفتر شهردار ورامین', 'daftar-shahrdar', 'DS', 1, 1, 1, NULL, 'fa-building', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:46:30');
INSERT INTO `departments` VALUES (3, 'روابط عمومی و امور بین‌الملل', 'rabeteh-amoozi', 'RA', 1, 2, 1, NULL, 'fa-handshake', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (4, 'بازرسی و ارزیابی عملکرد', 'bazresi-arzeshyabi', 'BEA', 1, 3, 1, NULL, 'fa-search', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (5, 'حراست شهرداری', 'harasat', 'HRS', 1, 4, 1, NULL, 'fa-shield-alt', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:47:18');
INSERT INTO `departments` VALUES (6, 'امور حقوقی', 'amoor-hoghooghi', 'HOG', 1, 5, 1, NULL, 'fa-gavel', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (7, 'شورای مشاوران', 'shora-ye-moshaveran', 'SMS', 1, 6, 1, NULL, 'fa-users-cog', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (8, 'معاونت اداری و مالی', 'moavenat-edari-va-mali', 'MEM', NULL, 2, 1, NULL, 'fa-coins', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (9, 'منابع انسانی', 'manabe-ensani', 'MAE', 8, 1, 1, NULL, 'fa-users', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (10, 'امور اداری', 'amoor-edari', 'AED', 8, 2, 1, NULL, 'fa-file-alt', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (11, 'امور مالی و حسابداری', 'amoor-mali-va-hesabdari', 'AMH', 8, 3, 1, NULL, 'fa-calculator', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (12, 'بودجه و برنامه‌ریزی', 'budjeh-va-barnameh-rizi', 'BBR', 8, 4, 1, NULL, 'fa-chart-line', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (13, 'تدارکات و پشتیبانی', 'tadakkat-va-poshtibani', 'TAP', 8, 5, 1, NULL, 'fa-truck', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (14, 'فناوری اطلاعات (IT)', 'fanaori-atlaat-it', 'FIT', 8, 6, 1, NULL, 'fa-laptop-code', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (15, 'معاونت فنی و عمرانی', 'moavenat-fanni-va-omrani', 'MFO', NULL, 3, 1, NULL, 'fa-hard-hat', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (16, 'طراحی و اجرای پروژه‌های عمرانی', 'tarh-va-ejra-projeh-ha', 'TEP', 15, 1, 1, NULL, 'fa-drafting-compass', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (17, 'ساخت و نگهداری معابر', 'sakht-va-negahdari-maaber', 'SNM', 15, 2, 1, NULL, 'fa-road', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (18, 'پل‌ها و تونل‌ها', 'pol-ha-va-tonel-ha', 'PTH', 15, 3, 1, NULL, 'fa-bridge', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (19, 'ساختمان‌های عمومی', 'sakhteman-ha-ye-omoomi', 'SHO', 15, 4, 1, NULL, 'fa-building', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (20, 'تأسیسات شهری', 'tasisat-shahri', 'TSS', 15, 5, 1, NULL, 'fa-faucet', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (21, 'معاونت شهرسازی و معماری', 'moavenat-shahr-sazi-va-memar', 'MSS', NULL, 4, 1, NULL, 'fa-city', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (22, 'صدور پروانه ساختمانی', 'sodor-parvaneh-sakhtemani', 'SPSA', 21, 1, 1, NULL, 'fa-file-signature', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (23, 'پایان کار ساختمان', 'payan-kar-sakhteman', 'PKS', 21, 2, 1, NULL, 'fa-check-double', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (24, 'کنترل و نظارت ساختمانی', 'kontrol-va-nazarat-sakhtemani', 'KNS', 21, 3, 1, NULL, 'fa-clipboard-check', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (25, 'طرح‌های توسعه شهری', 'tarh-ha-ye-tosea-shahri', 'TTS', 21, 4, 1, NULL, 'fa-draw-polygon', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (26, 'کمیسیون‌های شهرسازی', 'komision-ha-ye-shahr-sazi', 'KSS', 21, 5, 1, NULL, 'fa-people-arrows', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (27, 'معاونت خدمات شهری', 'moavenat-khadamat-shahri', 'MKS', NULL, 5, 1, NULL, 'fa-broom', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (28, 'نظافت شهری', 'nazafat-shahri', 'NSH', 27, 1, 1, NULL, 'fa-trash-alt', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (29, 'مدیریت پسماند', 'modiriat-pasmand', 'MPS', 27, 2, 1, NULL, 'fa-recycle', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (30, 'فضای سبز', 'fazaye-sabz', 'FAS', 27, 3, 1, NULL, 'fa-tree', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (31, 'زیباسازی شهر', 'zibasazi-shahr', 'ZIS', 27, 4, 1, NULL, 'fa-paint-brush', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (32, 'آرامستان‌ها', 'aramestan-ha', 'ARM', 27, 5, 1, NULL, 'fa-cross', '#64748b', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (33, 'کنترل حیوانات شهری', 'kontrol-hayvanat-shahri', 'KHS', 27, 6, 1, NULL, 'fa-dog', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (34, 'معاونت حمل‌ونقل و ترافیک', 'moavenat-haml-veh-naghleh-va-trafik', 'MHT', NULL, 6, 1, NULL, 'fa-bus', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (35, 'مدیریت ترافیک', 'modiriat-trafik', 'MTR', 34, 1, 1, NULL, 'fa-traffic-light', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (36, 'پارکینگ‌ها', 'parking-ha', 'PKH', 34, 2, 1, NULL, 'fa-parking', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (37, 'حمل‌ونقل عمومی', 'haml-o-naghl-omoomi', 'HNO', 34, 3, 1, NULL, 'fa-bus-alt', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (38, 'پایانه‌ها', 'payaneh-ha', 'PYH', 34, 4, 1, NULL, 'fa-warehouse', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (39, 'ایمنی و علائم راهنمایی', 'aymani-va-alam-ha-rahnamayi', 'AAR', 34, 5, 1, NULL, 'fa-exclamation-triangle', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (40, 'معاونت فرهنگی و اجتماعی', 'moavenat-farhangi-va-ijtimaei', 'MFS', NULL, 7, 1, NULL, 'fa-music', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (41, 'فرهنگسراها', 'farhangsara-ha', 'FHS', 40, 1, 1, NULL, 'fa-landmark', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (42, 'کتابخانه‌ها', 'ketabkhaneh-ha', 'KTH', 40, 2, 1, NULL, 'fa-book-open', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (43, 'امور جوانان', 'amoor-javanan', 'AJV', 40, 3, 1, NULL, 'fa-user-graduate', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (44, 'امور بانوان', 'amoor-banan', 'ABN', 40, 4, 1, NULL, 'fa-female', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (45, 'مشارکت‌های مردمی', 'mosharekat-ha-ye-mardomi', 'MMD', 40, 5, 1, NULL, 'fa-hands-helping', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (46, 'ورزش همگانی', 'varzeshe-hamgani', 'VSH', 40, 6, 1, NULL, 'fa-running', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (47, 'معاونت برنامه‌ریزی و توسعه', 'moavenat-barnameh-rizi-va-tosea', 'MBT', NULL, 8, 1, NULL, 'fa-chart-pie', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (48, 'آمار و اطلاعات', 'amaar-va-etelaat', 'AEI', 47, 1, 1, NULL, 'fa-database', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (49, 'پژوهش و نوآوری', 'pajoohesh-va-noavari', 'PNO', 47, 2, 1, NULL, 'fa-flask', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (50, 'مدیریت پروژه', 'modiriat-proje', 'MPR', 47, 3, 1, NULL, 'fa-tasks', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (51, 'هوشمندسازی شهر', 'hooshmand-sazi-shahr', 'HSS', 47, 4, 1, NULL, 'fa-microchip', '#0891b2', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (52, 'سازمان‌ها و شرکت‌های وابسته', 'sazman-ha-va-sherkat-ha-ye-vabasteh', 'SSV', NULL, 9, 1, NULL, 'fa-building-columns', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (53, 'سازمان مدیریت پسماند', 'sazman-modiriat-pasmand', 'SMP', 52, 1, 1, NULL, 'fa-recycle', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (54, 'سازمان آتش‌نشانی و خدمات ایمنی', 'sazman-atesh-neshani', 'SAN', 52, 2, 1, NULL, 'fa-fire-extinguisher', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (55, 'سازمان پارک‌ها و فضای سبز', 'sazman-park-ha-va-faza-ye-sabz', 'SPF', 52, 3, 1, NULL, 'fa-tree', '#16a34a', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (56, 'سازمان زیباسازی', 'sazman-zibasazi', 'SZS', 52, 4, 1, NULL, 'fa-paint-roller', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (57, 'سازمان حمل‌ونقل بار و مسافر', 'sazman-haml-o-naghl-bar-va-mosafir', 'SHB', 52, 5, 1, NULL, 'fa-truck-fast', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (58, 'سازمان میادین و بازارها', 'sazman-miadan-va-bazaar-ha', 'SMB', 52, 6, 1, NULL, 'fa-store', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (59, 'سازمان آرامستان‌ها', 'sazman-aramestan-ha', 'SAR', 52, 7, 1, NULL, 'fa-cross', '#64748b', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (60, 'سازمان فناوری اطلاعات و ارتباطات', 'sazman-fanavari-atlaat-va-ertebatat', 'SFI', 52, 8, 1, NULL, 'fa-laptop', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (61, 'سازمان فرهنگی، اجتماعی و ورزشی', 'sazman-farhangi-ijtimaei-va-varzeshi', 'SFV', 52, 9, 1, NULL, 'fa-people-group', '#7c3aed', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (62, 'سازمان سرمایه‌گذاری و مشارکت‌های مردمی', 'sazman-sarmayeh-gozari', 'SSG', 52, 10, 1, NULL, 'fa-hand-holding-usd', '#0f766e', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (63, 'شرکت بهره‌برداری مترو', 'sherkat-bahre-bardari-metro', 'SBM', 52, 11, 1, NULL, 'fa-subway', '#2563eb', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (64, 'شرکت واحد اتوبوسرانی', 'sherkat-vahdat-autobusrani', 'SVA', 52, 12, 1, NULL, 'fa-bus', '#dc2626', '2026-08-20 14:37:27', '2026-08-20 14:37:27');
INSERT INTO `departments` VALUES (65, 'شرکت نوسازی و بهسازی شهری', 'sherkat-nosazi-va-behsazi-shahri', 'SNB', 52, 13, 1, NULL, 'fa-helmet-safety', '#d97706', '2026-08-20 14:37:27', '2026-08-20 14:37:27');

-- ----------------------------
-- Table structure for favorites
-- ----------------------------
DROP TABLE IF EXISTS `favorites`;
CREATE TABLE `favorites`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `item_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_phone`(`user_phone` ASC) USING BTREE,
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_phone`) REFERENCES `users` (`phone`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of favorites
-- ----------------------------

-- ----------------------------
-- Table structure for notifications
-- ----------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `body` text CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `send_id` int NULL,
  `read_flag` tinyint(1) NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_phone`(`user_phone` ASC) USING BTREE,
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_phone`) REFERENCES `users` (`phone`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notifications
-- ----------------------------


-- ----------------------------
-- Table structure for notification_sends
-- ----------------------------
DROP TABLE IF EXISTS `notification_sends`;
CREATE TABLE `notification_sends` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `target_type` varchar(50) NOT NULL DEFAULT 'all',
  `recipients_count` int NOT NULL DEFAULT 0,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;

-- ----------------------------
-- Table structure for push_subscriptions
-- ----------------------------
DROP TABLE IF EXISTS `push_subscriptions`;
CREATE TABLE `push_subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) NOT NULL,
  `endpoint` text NOT NULL,
  `endpoint_hash` char(64) NOT NULL,
  `p256dh` varchar(255) NOT NULL,
  `auth` varchar(255) NOT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_push_endpoint_hash` (`endpoint_hash`),
  KEY `idx_push_user_phone` (`user_phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL DEFAULT 'news',
  `title` varchar(255) NOT NULL,
  `summary` varchar(500) DEFAULT NULL,
  `body` text NOT NULL,
  `icon` varchar(32) DEFAULT NULL,
  `image_url` varchar(1000) DEFAULT NULL,
  `published` tinyint(1) NOT NULL DEFAULT 1,
  `sort_order` int NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_news_type_published` (`type`,`published`),
  KEY `idx_news_sort` (`sort_order`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;

INSERT INTO `news` (`type`,`title`,`summary`,`body`,`icon`,`image_url`,`published`,`sort_order`) VALUES
('news','افتتاح پارک جدید در منطقه شمالی ورامین','پارک جدید شهر با امکانات ورزشی و فضای سبز گسترده افتتاح شد.','پارک جدید شهرداری ورامین با مساحت بیش از ۵ هکتار و امکاناتی شامل زمین‌های ورزشی، مسیر پیاده‌روی، فضای بازی کودکان و فضای سبز گسترده، آماده بهره‌برداری شهروندان عزیز شده است. این پروژه با مشارکت شهروندان و در راستای ارتقای کیفیت زندگی شهری اجرا شده است.','🌳',NULL,1,10),
('news','اطلاعیه نوبت‌دهی پرداخت عوارض نوسازی','مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید شد.','به اطلاع شهروندان محترم می‌رساند مهلت پرداخت عوارض نوسازی سال جاری تا پایان خرداد ماه تمدید گردیده است. شهروندان می‌توانند از طریق بخش «پرداخت عوارض» همین برنامه نسبت به پرداخت بدهی خود اقدام نمایند.','📋',NULL,1,20),
('news','برگزاری جشنواره فرهنگی شهر ورامین','جشنواره فرهنگی و هنری شهر با حضور هنرمندان محلی برگزار می‌شود.','شهرداری ورامین با همکاری اداره فرهنگ و ارشاد اسلامی، جشنواره فرهنگی و هنری شهر را با حضور هنرمندان محلی و برنامه‌های متنوع برای خانواده‌ها برگزار می‌کند. زمان و مکان دقیق برگزاری متعاقباً اعلام خواهد شد.','🎉',NULL,1,30),
('news','آغاز طرح بازآفرینی بافت فرسوده مرکز شهر','طرح نوسازی و بازآفرینی بافت فرسوده مرکز شهر آغاز شد.','با هدف ارتقای کیفیت بصری و کالبدی مرکز شهر، طرح بازآفرینی بافت فرسوده با همکاری شهرداری و سازمان نوسازی شهری آغاز شده و طی فازهای مختلف تا پایان سال ادامه خواهد داشت.','🏗️',NULL,1,40),
('tip','مسجد جامع ورامین','تنها نمونه کامل مساجد چهارایوانی ایران؛ شاهکاری از معماری دوران ایلخانی.','مسجد جامع ورامین، معروف به مسجد جمعه ورامین، یکی از کهن‌ترین و باشکوه‌ترین بناهای برجامانده از دوره ایلخانی در ایران است. ساخت آن در روزگار سلطان محمد خدابنده (الجایتو) آغاز شد و در دوران فرزند و جانشین او، ابوسعید بهادرخان، در سال ۷۲۲ هجری قمری به پایان رسید. این مسجد با نقشه‌ای مستطیلی به ابعاد تقریبی ۶۶ در ۴۳ متر، تنها نمونه کامل و یکپارچه مساجد چهارایوانی در ایران است؛ سبکی که از سلجوقیان آغاز شده و در این بنا به اوج پختگی خود رسیده است. گنبدخانه مسجد با گذر از فیل‌پوش‌ها از مربع به هشت‌ضلعی و سپس شانزده‌ضلعی، به گنبدی باشکوه ختم می‌شود. سردر بلند و کشیده ورودی، کاشی‌کاری‌های معرق فیروزه‌ای و لاجوردی، گچ‌بری‌های ظریف گرداگرد محراب و کتیبه‌های تاریخی به خط ثلث و کوفی، این بنا را به یکی از مهم‌ترین آثار هنری و معماری دوران اسلامی ایران بدل کرده‌اند. در دوران معاصر، استاد محمدکریم پیرنیا، پدر معماری سنتی ایران، مرمت این اثر گران‌بها را بر عهده داشت.','🏛️','assets/img/varamin-mosque.jpg',1,10),
('tip','برج علاءالدوله ورامین','برج آرامگاهی استوانه‌ای با گنبدی مخروطی بلند، یادگار دوره ایلخانی.','برج علاءالدوله، که با نام برج علاءالدین نیز شناخته می‌شود، یکی از قدیمی‌ترین برج‌های آرامگاهی به‌جامانده از ایران است. این بنا در سال ۶۸۸ هجری قمری، در اواخر سده هفتم هجری، به دستور فخرالدین بر فراز آرامگاه پدرش، حسن علاءالدوله، حاکم وقت شهر ری، ساخته شد. برج از بدنه‌ای استوانه‌ای آجری با چین‌خوردگی‌های عمودی شکل گرفته که در ارتفاعی نزدیک به ۱۷ متر به گنبدی مخروطی و بلند ختم می‌شود؛ ترکیبی که سیمای منحصربه‌فرد و شناخته‌شده این بنا را در میدان مرکزی ورامین رقم زده است. در محل اتصال بخش استوانه‌ای به مخروطی، کتیبه‌ای آجری با خطوط کوفی برگ‌دار حک شده که نام بانی، تاریخ بنا و دعایی برای آرامش روح علاءالدوله را در خود دارد. نمای بیرونی برج با شمسه‌های آجری و کاشی‌های فیروزه‌ای و لاجوردی تزئین شده است. این اثر در ۱۵ دی ماه ۱۳۱۰ با شماره ثبت ۱۷۷ در فهرست آثار ملی ایران به ثبت رسید و امروزه یکی از نمادهای شناخته‌شده شهر ورامین و مقصد علاقه‌مندان به تاریخ و معماری ایرانی است.','🕌','assets/img/varamin-tower.jpg',1,20);

-- ----------------------------
-- Table structure for eplak_settings
-- ----------------------------
DROP TABLE IF EXISTS `eplak_settings`;
CREATE TABLE `eplak_settings` (
  `setting_key` varchar(100) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`setting_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;
INSERT INTO `eplak_settings` VALUES ('news_defaults_seeded_v1','1',CURRENT_TIMESTAMP);

-- ----------------------------
-- Table structure for payments
-- ----------------------------
DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `code` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `due_date` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `amount` decimal(12, 2) NOT NULL,
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_phone`(`user_phone` ASC) USING BTREE,
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`user_phone`) REFERENCES `users` (`phone`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of payments
-- ----------------------------

-- ----------------------------
-- Table structure for reports
-- ----------------------------
DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `category` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `reply` text CHARACTER SET utf8 COLLATE utf8_persian_ci NULL,
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `sub_department` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `location` varchar(500) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_phone`(`user_phone` ASC) USING BTREE,
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_phone`) REFERENCES `users` (`phone`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reports
-- ----------------------------
INSERT INTO `reports` VALUES (1, '09306060331', 'تست فناوری دیتابیس', 'تست فناوری دیتابیس', 'طراحی و اجرای پروژه‌های عمرانی', '', '', '', 'pending', '2026-08-10 20:48:44', NULL);
INSERT INTO `reports` VALUES (3, '09359307540', '0935 سوا جدید', '0935 سوا جدید', 'دفتر شهردار', '', '', '', 'done', '2026-08-10 20:57:13', 'تست پاسخ به گزارش کاربر');
INSERT INTO `reports` VALUES (4, '09123947714', 'پیام به دفتر شهر دار', 'پیام به دفتر شهر دار', 'دفتر شهردار', '', '', '', 'pending', '2026-08-10 21:16:15', NULL);
INSERT INTO `reports` VALUES (5, '09104927131', 'حرااست خرابه', 'حرااست خرابه', 'حراست', 'حوزه شهردار', 'حراست', 'تهران میدان شوش', 'done', '2026-08-18 23:36:21', 'تست پاسخ 1');
INSERT INTO `reports` VALUES (6, '09104927131', 'حرااست خرابه بابا چرا درست ن', 'حرااست خرابه بابا چرا درست نمیکنید', 'دفتر شهرداری ورامین', 'حوزه شهردار', 'دفتر شهرداری ورامین', 'تهران میدان شوشتری', 'pending', '2026-08-19 01:33:45', NULL);
INSERT INTO `reports` VALUES (7, '09104927131', 'حرااست خرابه بابا چرا درست ن', 'حرااست خرابه بابا چرا درست نمیکنید اخه چرا', 'دفتر شهرداری ورامین', 'حوزه شهردار', 'دفتر شهرداری ورامین', 'تهران میدان شوشتری خیابان عباس علی رشیدی', 'done', '2026-08-19 01:42:50', 'اوکی شد');
INSERT INTO `reports` VALUES (8, '09104927131', 'تست گزارش', 'تست گزارش', 'نظافت شهری', 'معاونت خدمات شهری', 'نظافت شهری', 'تست ادرس', 'pending', '2026-08-19 02:05:06', NULL);
INSERT INTO `reports` VALUES (9, '09123456789', 'تست گزارش', 'توضیحات تست', 'نظافت', 'معاونت خدمات شهری', 'نظافت شهری', 'ورامین', 'pending', '2026-08-19 02:13:29', 'jsj');

-- ----------------------------
-- Table structure for report_media
-- ----------------------------
DROP TABLE IF EXISTS `report_media`;
CREATE TABLE `report_media`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_id` int NOT NULL,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `media_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `file_path` varchar(500) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `original_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `mime_type` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `file_size` int UNSIGNED NOT NULL DEFAULT 0,
  `duration_seconds` decimal(6, 3) NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_report_media_report`(`report_id` ASC) USING BTREE,
  INDEX `idx_report_media_phone`(`user_phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tickets
-- ----------------------------
DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `status` varchar(50) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT 'pending',
  `reply` text CHARACTER SET utf8 COLLATE utf8_persian_ci NULL,
  `category` varchar(100) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT '',
  `priority` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT 'medium',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_phone`(`user_phone` ASC) USING BTREE,
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`user_phone`) REFERENCES `users` (`phone`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tickets
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_persian_ci NOT NULL,
  `address` varchar(500) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT NULL,
  `nid` varchar(20) CHARACTER SET utf8 COLLATE utf8_persian_ci NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_persian_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '09306060331', 'شهروند', 'ورامین میدان رازی', '0421088273', '2026-08-10 20:39:25');
INSERT INTO `users` VALUES (2, '09104927131', 'مرتضی بهنامی', 'ورامین', '0421088273', '2026-08-10 20:40:08');
INSERT INTO `users` VALUES (7, '09359307540', 'مرتضی بهنامی', 'ادرس میدان امام خامنه ای', '0421088273', '2026-08-10 20:56:35');
INSERT INTO `users` VALUES (10, '09123947714', 'محمود بهنامی', 'تهران میدان ارژانتین', '04210101010', '2026-08-10 21:13:45');
INSERT INTO `users` VALUES (19, '09123456789', 'Test User', 'ورامین', '1234567890', '2026-08-19 02:13:29');

SET FOREIGN_KEY_CHECKS = 1;
