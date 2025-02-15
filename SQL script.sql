-- Creating Master (Parent) Tables First
CREATE TABLE User (
  User_ID INT,
  Username VARCHAR(50),
  Password VARCHAR(50),
  Email VARCHAR(100),
  Phone VARCHAR(15),
  Payment_cardno VARCHAR(20),
  PRIMARY KEY (User_ID)
);

CREATE TABLE Laundry_Machine (
  Machine_ID INT,
  Status VARCHAR(20),
  Remaining_Time INT,  -- Assuming time is represented in minutes or a similar unit
  PRIMARY KEY (Machine_ID)
);

-- Creating Subordinate (Child) Tables
CREATE TABLE Reservation (
  Reservation_ID INT,
  User_ID INT,
  Date DATE,
  Machine_ID INT,
  PRIMARY KEY (Reservation_ID),
  FOREIGN KEY (User_ID) REFERENCES User(User_ID),
  FOREIGN KEY (Machine_ID) REFERENCES Laundry_Machine(Machine_ID)
);

CREATE TABLE Laundry_Timeslot (
  ReservationItem_ID INT PRIMARY KEY,
  Starting_time TIME,
  Ending_time TIME,
  Reservation_ID INT,
  Penalty_amount DECIMAL(10, 2),
  FOREIGN KEY (Reservation_ID) REFERENCES Reservation(Reservation_ID)
);

CREATE TABLE Payment (
  Payment_ID INT,
  Amount DECIMAL(10, 2),
  Payment_Method VARCHAR(20),
  Reservation_ID INT,
  PRIMARY KEY (Payment_ID),
  FOREIGN KEY (Reservation_ID) REFERENCES Reservation(Reservation_ID)
);

-- Inserting  Records into User Table
INSERT INTO User (User_ID, Username, Password, Email, Phone, Payment_cardno) VALUES
(1, 'john_doe', 'password123', 'john@gmail.com', '1234567890', '1234567812345678'),
(2, 'jane_doe', 'securepass', 'jane@gmail.com', '0987654321', '8765432187654321'),
(3, 'alice_smith', 'alicepwd', 'alice@gmail.com', '1122334455', '1122334411223344'),
(4, 'bob_jones', 'bobby123', 'bob@gmail.com', '2233445566', '2233445522334455'),
(5, 'charlie_wade', 'charliepwd', 'charlie@gmail.com', '3344556677', '3344556633445566'),
(6, 'dave_white', 'davepwd', 'dave@gmail.com', '4455667788', '4455667744556677'),
(7, 'eve_brown', 'evepass', 'eve@gmail.com', '5566778899', '5566778855667788'),
(8, 'frank_black', 'frank123', 'frank@gmail.com', '6677889900', '6677889966778899'),
(9, 'grace_green', 'gracepwd', 'grace@gmail.com', '7788990011', '7788990077889900'),
(10, 'henry_kane', 'henrypwd', 'henry@gmail.com', '8899001122', '8899001188990011');
INSERT INTO User (User_ID, Username, Password, Email, Phone, Payment_cardno) VALUES
(11, 'Steve_jobs','stevepwd', 'steve@gmail.com','7896784568','1254536567456578'),
(12, 'Jennel_harris', 'jennel143','jennel@gmail.com','2728463838','3846294748373837'),
(13, 'Trumph_doe','trumphpwd', 'trumph@gmail.com','4738363837','38575857937959489'),
(14, 'Morgan_jobs','morganpwd', 'morgan@gmail.com','74836438529','1731737283604950'),
(15, 'Andrea_lisa','andrea268', 'andrea@gmail.com','6484820280','6283927458082747'),
(16, 'Desire_harris','desire987', 'desire@gmail.com','9264827482','7494793748294373'),
(17, 'Lindsey_roy','lindseypwd', 'lindsey@gmail.com','6473838457','6438937484936578'),
(18, 'Ashley_wade','ashley78', 'ashely@gmail.com','5473839292','4682924659294746'),
(19, 'Laura_caldwell','laurapwd', 'laura@gmail.com','5482846483','64826492746382192'),
(20, 'Jacob_king','jacob345', 'jacob@gmail.com','3464790975','2836484916474638'),
(21, 'Warren_leon','warrenpwd', 'warren@gmail.com','6484930322','9173849273939474'),
(22, 'Kristin_colman','kristi546', 'kristin@gmail.com','3578565757','4678997759768950'),
(23, 'Brandi_Wingate','brandipwd', 'brandi@gmail.com','4564758995','4767935658690654'),
(24, 'Sri_lekha','sripwd', 'lekha@gmail.com','6484226474','9173849273988444'),
(25, 'Vinay_kotagiri','vinay78', 'vinay@gmail.com','5473836565','4682924659209876'),
(26, 'Sri_ram','rampwd', 'ramreddy@gmail.com','74836430945','1231737283604990'),
(27, 'Vamshi_krishna','vamshipwd', 'krishna@gmail.com','6473838467','6438937484456778'),
(28, 'Maaz_leon','mazz268', 'mazz@gmail.com','6484821234','6283927458078906'),
(29, 'Vidhut_mandu','vidhupwd', 'vidhut@gmail.com','5482840989','64826492746365748'),
(30, 'Moua_yegi','mona345', 'mona@gmail.com','3464799089','2836484916472354');

-- Inserting Records into Laundry_Machine Table
INSERT INTO Laundry_Machine (Machine_ID, Status, Remaining_Time) VALUES
(1, 'Available', 0),
(2, 'In Use', 25),
(3, 'Available', 0),
(4, 'In Use', 15),
(5, 'Available', 0),
(6, 'Available', 0),
(7, 'In Use', 25),
(8, 'Available', 0),
(9, 'In Use', 15),
(10, 'Available', 0);
INSERT INTO Laundry_Machine (Machine_ID, Status, Remaining_Time) VALUES
(32, 'Available', 0),
(12, 'In Use', 25),
(13, 'Available', 0),
(14, 'In Use', 15),
(15, 'Available', 0),
(16, 'Available', 0),
(17, 'In Use', 25),
(18, 'Available', 0),
(19, 'In Use', 15),
(20, 'Available', 0),
(21, 'Available', 0),
(22, 'In Use', 25),
(23, 'Available', 0),
(24, 'In Use', 15),
(25, 'Available', 0),
(26, 'Available', 0),
(27, 'In Use', 25),
(28, 'Available', 0),
(29, 'In Use', 15),
(30, 'Available', 0);

-- Inserting Records into Reservation Table
INSERT INTO Reservation (Reservation_ID, User_ID, Date, Machine_ID) VALUES
(1, 1, '2024-11-04', 1),
(2, 2, '2024-11-04', 2),
(3, 3, '2024-11-04', 3),
(4, 4, '2024-11-05', 4),
(5, 5, '2024-11-05', 5),
(6, 6, '2024-11-05', 6),
(7, 7, '2024-11-06', 7),
(8, 8, '2024-11-06', 8),
(9, 9, '2024-11-06', 9),
(10, 10, '2024-11-07', 10);
INSERT INTO Reservation (Reservation_ID, User_ID, Date, Machine_ID) VALUES
(11, 11, '2024-11-04', 11),
(12, 12, '2024-11-04', 12),
(13, 13, '2024-11-04', 13),
(14, 14, '2024-11-05', 14),
(15, 15, '2024-11-05', 15),
(16, 16, '2024-11-05', 16),
(17, 17, '2024-11-06', 17),
(18, 18, '2024-11-06', 18),
(19, 19, '2024-11-06', 19),
(20, 20, '2024-11-07', 20),
(21, 21, '2024-11-04', 21),
(22, 22, '2024-11-04', 22),
(23, 23, '2024-11-04', 23),
(24, 24, '2024-11-05', 24),
(25, 25, '2024-11-05', 25),
(26, 26, '2024-11-05', 26),
(27, 27, '2024-11-06', 27),
(28, 28, '2024-11-06', 28),
(29, 29, '2024-11-06', 29),
(30, 30, '2024-11-07', 30);

-- Inserting  Records into Laundry_Timeslot Table
INSERT INTO Laundry_Timeslot (ReservationItem_ID, Starting_time, Ending_time, Reservation_ID, Penalty_amount) VALUES
(1, '08:00:00', '09:00:00', 1, 5.00),
(2, '09:00:00', '10:00:00', 2, 0.00),
(3, '10:00:00', '11:00:00', 3, 5.00),
(4, '11:00:00', '12:00:00', 4, 0.00),
(5, '12:00:00', '13:00:00', 5, 2.50),
(6, '13:00:00', '14:00:00', 6, 0.00),
(7, '14:00:00', '15:00:00', 7, 7.50),
(8, '15:00:00', '16:00:00', 8, 0.00),
(9, '16:00:00', '17:00:00', 9, 3.00),
(10, '17:00:00', '18:00:00', 10, 0.00);
INSERT INTO Laundry_Timeslot (ReservationItem_ID, Starting_time, Ending_time, Reservation_ID, Penalty_amount) VALUES
(11, '08:00:00', '09:00:00', 11, 5.00),
(12, '09:00:00', '10:00:00', 12, 0.00),
(13, '10:00:00', '11:00:00', 13, 5.00),
(14, '11:00:00', '12:00:00', 14, 0.00),
(15, '12:00:00', '13:00:00', 15, 2.50),
(16, '13:00:00', '14:00:00', 16, 0.00),
(17, '14:00:00', '15:00:00', 17, 7.50),
(18, '15:00:00', '16:00:00', 18, 0.00),
(19, '16:00:00', '17:00:00', 19, 3.00),
(20, '17:00:00', '18:00:00', 20, 0.00),
(21, '08:00:00', '09:00:00', 21, 5.00),
(22, '09:00:00', '10:00:00', 22, 0.00),
(23, '10:00:00', '11:00:00', 23, 5.00),
(24, '11:00:00', '12:00:00', 24, 0.00),
(25, '12:00:00', '13:00:00', 25, 2.50),
(26, '13:00:00', '14:00:00', 26, 0.00),
(27, '14:00:00', '15:00:00', 27, 7.50),
(28, '15:00:00', '16:00:00', 28, 0.00),
(29, '16:00:00', '17:00:00', 29, 3.00),
(30, '17:00:00', '18:00:00', 30, 0.00);

-- Inserting Records into Payment Table
INSERT INTO Payment (Payment_ID, Amount, Payment_Method, Reservation_ID) VALUES
(1, 15.00, 'Credit Card', 1),
(2, 10.00, 'Debit Card', 2),
(3, 12.50, 'Cash', 3),
(4, 20.00, 'Credit Card', 4),
(5, 18.75, 'Debit Card', 5),
(6, 11.25, 'Cash', 6),
(7, 22.50, 'Credit Card', 7),
(8, 16.00, 'Debit Card', 8),
(9, 9.75, 'Cash', 9),
(10, 14.25, 'Credit Card', 10);
INSERT INTO Payment (Payment_ID, Amount, Payment_Method, Reservation_ID) VALUES
(11, 15.00, 'Credit Card', 11),
(12, 10.00, 'Debit Card', 12),
(13, 12.50, 'Cash', 13),
(14, 20.00, 'Credit Card', 14),
(15, 18.75, 'Debit Card', 15),
(16, 11.25, 'Cash', 16),
(17, 22.50, 'Credit Card', 17),
(18, 16.00, 'Debit Card', 18),
(19, 9.75, 'Cash', 19),
(20, 14.25, 'Credit Card', 20),
(21, 15.00, 'Credit Card', 21),
(22, 10.00, 'Debit Card', 22),
(23, 12.50, 'Cash', 23),
(24, 20.00, 'Credit Card', 24),
(25, 18.75, 'Debit Card', 25),
(26, 11.25, 'Cash', 26),
(27, 22.50, 'Credit Card', 27),
(28, 16.00, 'Debit Card', 28),
(29, 9.75, 'Cash', 29),
(30, 14.25, 'Credit Card', 30);

SELECT *FROM Laundry_Machine;