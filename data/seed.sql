-- seed.sql (run when Product table is empty)

INSERT INTO Product
(Name, Type, ProduceYear, Price, Total, Model, Cpu, Gpu, Motherboard, Ram, Description)
VALUES
('ThinkPad X1 Carbon', 'Laptop', 2023, 1499, 10, 'X1C Gen11', 'Intel i7', 'Intel Iris', 'Lenovo Board', '16GB', 'Lightweight business laptop'),
('MacBook Air M2', 'Laptop', 2022, 1299, 12, 'Air M2', 'Apple M2', 'Integrated', 'Apple Board', '16GB', 'Ultra portable'),
('Dell XPS 13', 'Laptop', 2023, 1399, 8, 'XPS 9315', 'Intel i5', 'Intel Iris', 'Dell Board', '16GB', 'Premium ultrabook'),
('HP Pavilion 15', 'Laptop', 2023, 899, 15, 'Pavilion 15-eg', 'AMD Ryzen 5', 'AMD Radeon', 'HP Board', '8GB', 'Everyday value laptop'),
('Asus Zenbook 14', 'Laptop', 2023, 1199, 6, 'UX3404', 'Intel i5', 'Intel Iris', 'Asus Board', '16GB', 'Sleek and powerful'),
('Lenovo IdeaPad 5', 'Laptop', 2022, 749, 20, 'IdeaPad 5 15', 'AMD Ryzen 5', 'Integrated', 'Lenovo Board', '8GB', 'Great for students'),
('Acer Swift 3', 'Laptop', 2023, 699, 14, 'SF314-512', 'Intel i5', 'Intel Iris', 'Acer Board', '8GB', 'Thin and light'),
('MSI Modern 14', 'Laptop', 2023, 949, 9, 'B14', 'Intel i5', 'Intel Iris', 'MSI Board', '16GB', 'Professional style'),
('Razer Blade 14', 'Laptop', 2023, 1899, 5, 'RZ09-0482', 'AMD Ryzen 9', 'NVIDIA RTX 4060', 'Razer Board', '16GB', 'Gaming performance'),
('LG Gram 17', 'Laptop', 2023, 1599, 7, '17Z90Q', 'Intel i7', 'Intel Iris', 'LG Board', '16GB', 'Large lightweight display'),
('Surface Laptop 5', 'Laptop', 2023, 1299, 11, 'Surface Laptop 5', 'Intel i5', 'Intel Iris', 'Microsoft Board', '8GB', 'Premium Windows experience'),
('Framework Laptop 13', 'Laptop', 2023, 1099, 8, 'Framework 13', 'Intel i5', 'Intel Iris', 'Framework Board', '8GB', 'Repairable and upgradeable'),
('HP EliteBook 840', 'Laptop', 2023, 1349, 10, 'EliteBook 840 G10', 'Intel i5', 'Intel Iris', 'HP Board', '16GB', 'Enterprise reliability'),
('Dell Inspiron 15', 'Laptop', 2022, 599, 18, 'Inspiron 3520', 'Intel i3', 'Intel UHD', 'Dell Board', '8GB', 'Affordable everyday use'),
('Lenovo Slim 7', 'Laptop', 2023, 1149, 8, 'Slim 7 14', 'AMD Ryzen 7', 'AMD Radeon', 'Lenovo Board', '16GB', 'Balanced performance'),
('Asus VivoBook 15', 'Laptop', 2022, 549, 22, 'X1504', 'Intel i3', 'Intel UHD', 'Asus Board', '8GB', 'Entry-level value'),
('MacBook Pro 14', 'Laptop', 2023, 1999, 6, 'Pro 14 M3', 'Apple M3', 'Integrated', 'Apple Board', '18GB', 'Pro power and portability');

INSERT INTO ProductImages (ProductID, ImageURL, AltText)
VALUES
(1, '/static/img/x1.jpg', 'ThinkPad X1 Image'),
(2, '/static/img/airm2.jpg', 'MacBook Air Image'),
(3, '/static/img/xps13.jpg', 'Dell XPS Image'),
(4, '/static/img/laptop-02.jpg', 'HP Pavilion Image'),
(5, '/static/img/laptop-03.jpg', 'Asus Zenbook Image'),
(6, '/static/img/laptop-04.jpg', 'Lenovo IdeaPad Image'),
(7, '/static/img/laptop-05.jpg', 'Acer Swift Image'),
(8, '/static/img/laptop-06.jpg', 'MSI Modern Image'),
(9, '/static/img/laptop-07.jpg', 'Razer Blade Image'),
(10, '/static/img/x1.jpg', 'LG Gram Image'),
(11, '/static/img/airm2.jpg', 'Surface Laptop Image'),
(12, '/static/img/xps13.jpg', 'Framework Laptop Image'),
(13, '/static/img/laptop-02.jpg', 'HP EliteBook Image'),
(14, '/static/img/laptop-03.jpg', 'Dell Inspiron Image'),
(15, '/static/img/laptop-04.jpg', 'Lenovo Slim Image'),
(16, '/static/img/laptop-05.jpg', 'Asus VivoBook Image'),
(17, '/static/img/laptop-06.jpg', 'MacBook Pro Image');
