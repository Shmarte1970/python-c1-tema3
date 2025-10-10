-- ventas_comerciales.sql
-- Archivo SQL con datos de ventas comerciales para análisis

-- Crear tabla de regiones
CREATE TABLE regiones (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    pais TEXT NOT NULL
);

-- Insertar datos de regiones
INSERT INTO regiones (id, nombre, pais) VALUES (1, 'Norte', 'España');
INSERT INTO regiones (id, nombre, pais) VALUES (2, 'Sur', 'España');
INSERT INTO regiones (id, nombre, pais) VALUES (3, 'Este', 'España');
INSERT INTO regiones (id, nombre, pais) VALUES (4, 'Oeste', 'España');
INSERT INTO regiones (id, nombre, pais) VALUES (5, 'Centro', 'España');

-- Crear tabla de vendedores
CREATE TABLE vendedores (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    region_id INTEGER,
    fecha_contratacion DATE,
    FOREIGN KEY (region_id) REFERENCES regiones(id)
);

-- Insertar datos de vendedores
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (1, 'María', 'López', 1, '2020-03-15');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (2, 'Juan', 'García', 1, '2019-05-20');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (3, 'Carlos', 'Martínez', 2, '2021-01-10');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (4, 'Laura', 'Rodríguez', 3, '2020-11-05');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (5, 'Ana', 'Sánchez', 4, '2022-02-28');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (6, 'Pablo', 'Fernández', 5, '2021-07-14');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (7, 'Lucía', 'Díaz', 3, '2020-04-22');
INSERT INTO vendedores (id, nombre, apellido, region_id, fecha_contratacion)
VALUES (8, 'Miguel', 'Hernández', 2, '2022-03-01');

-- Crear tabla de productos
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL
);

-- Insertar datos de productos
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (1, 'Laptop Pro', 'Electrónica', 1200.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (2, 'Teléfono Smart', 'Electrónica', 800.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (3, 'Tablet Ultra', 'Electrónica', 500.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (4, 'Monitor 24"', 'Periféricos', 200.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (5, 'Teclado Mecánico', 'Periféricos', 80.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (6, 'Ratón Inalámbrico', 'Periféricos', 30.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (7, 'Software Productividad', 'Software', 150.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (8, 'Antivirus Premium', 'Software', 70.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (9, 'Juego Aventura', 'Software', 60.00);
INSERT INTO productos (id, nombre, categoria, precio_unitario)
VALUES (10, 'Disco Duro Externo', 'Almacenamiento', 120.00);

-- Crear tabla de ventas
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    vendedor_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Insertar datos de ventas (año 2022, primer trimestre)
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-01-05', 1, 1, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-01-10', 2, 3, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-01-15', 3, 2, 4);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-01-20', 4, 5, 5);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-01-25', 5, 4, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-02-03', 6, 6, 10);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-02-08', 7, 7, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-02-14', 8, 8, 7);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-02-19', 1, 9, 5);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-02-24', 2, 10, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-02', 3, 1, 1);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-07', 4, 2, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-12', 5, 3, 4);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-18', 6, 4, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-23', 7, 5, 1);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-03-28', 8, 6, 3);

-- Insertar datos de ventas (año 2022, segundo trimestre)
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-04-04', 1, 7, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-04-09', 2, 8, 1);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-04-15', 3, 9, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-04-21', 4, 10, 4);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-04-26', 5, 1, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-02', 6, 2, 5);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-08', 7, 3, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-13', 8, 4, 1);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-19', 1, 5, 6);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-24', 2, 6, 4);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-05-30', 3, 7, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-06-05', 4, 8, 3);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-06-10', 5, 9, 2);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-06-16', 6, 10, 1);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-06-21', 7, 1, 4);
INSERT INTO ventas (fecha, vendedor_id, producto_id, cantidad) VALUES ('2022-06-27', 8, 2, 3);
