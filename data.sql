-- Data to populate the cafeteria database
-- Written by M.V.Harish Kumar - Grade 12 'A'

USE cafeteria;

INSERT INTO staff VALUES
(1, 'Administrator', 'admin', 'admin@p$wd', 'A'),
(2, 'Harish', 'harish', 'harish@p$wd', 'A'),
(3, 'Ravi', 'ravi', 'ravi@p$wd', 'A');

INSERT INTO items VALUES
(1, 'Coffee', 15.00),
(2, 'Tea', 14.00),
(3, 'Milkshake', 60.00),
(4, 'Cake', 80.50);

INSERT INTO customer VALUES
(1, 'Harish', 'Student', 'A'),
(2, 'Raam', 'Student', 'A'),
(3, 'Shanthi', 'Staff', 'A');
