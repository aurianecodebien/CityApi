CREATE TABLE city (
    id INT PRIMARY KEY,
    department_code VARCHAR(10) NOT NULL,
    insee_code VARCHAR(20),
    zip_code VARCHAR(20),
    name VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL
);