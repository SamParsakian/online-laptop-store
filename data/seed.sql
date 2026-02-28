-- seed.sql (run when Product table is empty)

INSERT INTO Product
(Name, Type, ProduceYear, Price, Total, Model, Cpu, Gpu, Motherboard, Ram, Description)
VALUES
('ThinkPad X1 Carbon', 'Laptop', 2023, 1499, 10, 'X1C Gen11', 'Intel i7', 'Intel Iris', 'Lenovo Board', '16GB', 'Lightweight business laptop'),
('MacBook Air M2', 'Laptop', 2022, 1299, 12, 'Air M2', 'Apple M2', 'Integrated', 'Apple Board', '16GB', 'Ultra portable'),
('Dell XPS 13', 'Laptop', 2023, 1399, 8, 'XPS 9315', 'Intel i5', 'Intel Iris', 'Dell Board', '16GB', 'Premium ultrabook'),
('HP Pavilion 15', 'Laptop', 2023, 899, 15, 'Pavilion 15-eg', 'AMD Ryzen 5', 'AMD Radeon', 'HP Board', '8GB', 'Everyday value laptop'),
('Asus Zenbook 14', 'Laptop', 2023, 1199, 6, 'UX3404', 'Intel i5', 'Intel Iris', 'Asus Board', '16GB', 'Sleek and powerful'),
('Lenovo IdeaPad 5', 'Laptop', 2022, 749, 20, 'IdeaPad 5 15', 'AMD Ryzen 5', 'Integrated', 'Lenovo Board', '8GB', 'Great for students');

INSERT INTO ProductImages (ProductID, ImageURL, AltText)
VALUES
(1, '/static/img/x1.jpg', 'ThinkPad X1 Image'),
(2, '/static/img/airm2.jpg', 'MacBook Air Image'),
(3, '/static/img/xps13.jpg', 'Dell XPS Image'),
(4, '/static/img/x1.jpg', 'HP Pavilion Image'),
(5, '/static/img/airm2.jpg', 'Asus Zenbook Image'),
(6, '/static/img/xps13.jpg', 'Lenovo IdeaPad Image');
