-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               8.0.37 - MySQL Community Server - GPL
-- Операционная система:         Win64
-- HeidiSQL Версия:              12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Дамп структуры базы данных v2_tasks_db
CREATE DATABASE IF NOT EXISTS `v2_tasks_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `v2_tasks_db`;

-- Дамп структуры для таблица v2_tasks_db.tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `detail` text,
  `creation_date` date NOT NULL,
  `execution_date` date NOT NULL,
  `execution_mark` text NOT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Дамп данных таблицы v2_tasks_db.tasks: ~14 rows (приблизительно)
INSERT INTO `tasks` (`id`, `title`, `detail`, `creation_date`, `execution_date`, `execution_mark`) VALUES
	(23, 'Сделать пост', 'нет', '2024-10-02', '2024-10-02', 'Готово'),
	(24, 'Make web-service for our company', 'string', '2024-10-05', '2024-10-07', 'Готово'),
	(25, 'сделать так, чтобы даты начала и завершения задачи в редакторе брались из уже существующих данных задачи (например, из task.creation_date и task.execution_date)', 'нет', '2024-10-06', '2024-10-06', 'Готово'),
	(26, 'протестировать веб сервис', '', '2024-10-08', '2024-10-10', 'В работе'),
	(29, 'Проверить работу pdf файла, то как он работает с длинным текстом и несколькими пользователями в задаче, которая продемонстрирует все это', '', '2024-11-16', '2024-11-17', 'В работе'),
	(31, 'отладить вывод информации в pdf файле, то  как передаются данные без разрыва', '', '2024-11-16', '2024-11-18', 'В работе'),
	(33, 'сделать', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(34, 'ущкашукошуакошощукащшоакущшуакощшоуак', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(35, 'кщшоауаокуошакошкуащшоукашощуакщшокуащшоуакщшоуакщшоукащшо', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(36, 'cjkskefksefnsefseffe', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(37, 'uudfusfiuf fewjiofewjoefwiewfoijf ', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(38, 'ка оыушыуашо  ыущоуаыщ шщуыау', 'нет', '2024-11-21', '2024-11-22', 'В очереди'),
	(45, 'ощзулаузщлуалзщазлщау', 'нет', '2024-11-21', '2024-11-21', 'В очереди'),
	(49, 'лдулкькдлуьлкьпльукп', 'нет', '2024-11-21', '2024-11-21', 'В работе');

-- Дамп структуры для таблица v2_tasks_db.task_users
CREATE TABLE IF NOT EXISTS `task_users` (
  `task_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`task_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `task_users_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `task_users_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Дамп данных таблицы v2_tasks_db.task_users: ~24 rows (приблизительно)
INSERT INTO `task_users` (`task_id`, `user_id`) VALUES
	(49, 2),
	(38, 4),
	(33, 5),
	(23, 6),
	(24, 6),
	(26, 6),
	(29, 6),
	(31, 6),
	(33, 6),
	(37, 6),
	(23, 7),
	(24, 7),
	(25, 7),
	(26, 7),
	(31, 7),
	(34, 7),
	(35, 7),
	(36, 7),
	(37, 7),
	(45, 7),
	(24, 8),
	(26, 8),
	(31, 8),
	(31, 12),
	(31, 13);

-- Дамп структуры для таблица v2_tasks_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Дамп данных таблицы v2_tasks_db.users: ~13 rows (приблизительно)
INSERT INTO `users` (`id`, `username`) VALUES
	(1, 'Сыктывкаров Валерий Богданович'),
	(2, 'Шувалов Алексей Маратович'),
	(4, 'Миронова Ольга Владимировна'),
	(5, 'Муллагалиев Ильшат Фаритович'),
	(6, 'Баренцев Артур Михайлович'),
	(7, 'Ахметзянов Инсаф Ильгизович'),
	(8, 'Хайруллин Булат Айдарович'),
	(12, 'Рамзиль'),
	(13, 'Данис'),
	(14, 'Усман'),
	(15, 'Динар'),
	(16, 'Айнур');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
