CREATE DATABASE IF NOT EXISTS pricelens CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pricelens;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS grocery_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(80) NOT NULL,
    brand VARCHAR(120) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_grocery_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS clothing_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(80) NOT NULL,
    brand VARCHAR(120) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_clothing_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS gadgets_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(80) NOT NULL,
    brand VARCHAR(120) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_gadgets_name (name)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(80) NOT NULL,
    product_id INT NOT NULL,
    platform VARCHAR(80) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_prices_category (category),
    INDEX idx_prices_product (product_id),
    INDEX idx_prices_platform (platform),
    INDEX idx_prices_last_updated (last_updated)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS user_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(80) NOT NULL,
    product_id INT NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_history_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_history_user (user_id),
    INDEX idx_user_history_category (category),
    INDEX idx_user_history_product (product_id),
    INDEX idx_user_history_viewed_at (viewed_at)
) ENGINE=InnoDB;