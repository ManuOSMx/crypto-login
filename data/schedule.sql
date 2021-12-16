create database NombreBD;

use NombreBD;

create table users(
	id SERIAL primary key not null,
	email varchar (255) not null,
	pass varchar (255) not null,
	pass_ext varchar (255) not null
);

-- Verificar que funcione la base de datos funcione
INSERT INTO users (email,pass,pass_ext) VALUES ('correo@ejemplo.com','12345678','12345678');
SELECT * FROM users;