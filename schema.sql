-- The Schema for the Cafeteria Project
-- Written by M.V.Harish Kumar - Grade 12 'A'

DROP DATABASE IF EXISTS cafeteria;
CREATE DATABASE cafeteria;
USE cafeteria;

DROP TABLE IF EXISTS Staff;
CREATE TABLE Staff (
	id INT PRIMARY KEY,
	name VARCHAR(25),
	username VARCHAR(20),
	passwd VARCHAR(64),
	status VARCHAR(1) CHECK(status IN ('A', 'I'))
);

DROP TABLE IF EXISTS Items;
CREATE TABLE Items (
	itemCode INT PRIMARY KEY,
	itemName VARCHAR(50),
	rate DECIMAL(7,2)
);

DROP TABLE IF EXISTS DailyStock;
CREATE TABLE DailyStock (
	itemCode INT,
	receiptDate DATE,
	quantity INT,
	PRIMARY KEY(itemCode, reciptDate),
	FOREIGN KEY(itemCode) REFERENCES Items(itemCode)
);

DROP TABLE IF EXISTS Customer;
CREATE TABLE Customer (
	custId INT,
	name VARCHAR(25),
	custType VARCHAR(7) CHECK(custType IN ('Student', 'Staff')),
	status VARCHAR(1) CHECK(status IN ('A', 'I'))
);

DROP TABLE IF EXISTS Sales;
CREATE TABLE Sales (
	tokenId INT,
	tDate DATE,
	custCode INT,
	itemCode INT,
	qty INT
);
