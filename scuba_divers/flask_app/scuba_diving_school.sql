-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema scuba_diving_school
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema scuba_diving_school
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `scuba_diving_school` DEFAULT CHARACTER SET utf8mb3 ;
USE `scuba_diving_school` ;

-- -----------------------------------------------------
-- Table `scuba_diving_school`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scuba_diving_school`.`courses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scuba_diving_school`.`divers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scuba_diving_school`.`divers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `course_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_divers_courses_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_divers_courses`
    FOREIGN KEY (`course_id`)
    REFERENCES `scuba_diving_school`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
