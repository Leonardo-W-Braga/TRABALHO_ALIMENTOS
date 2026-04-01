CREATE DATABASE IF NOT EXISTS db_alimentos;
USE db_alimentos;

CREATE TABLE IF NOT EXISTS frutas (
    id INT NOT NULL AUTO_INCREMENT,
    sec CHAR(4),
    grupo_id CHAR(1) NOT NULL,
    fruta VARCHAR(100) NOT NULL,
    pais CHAR(2) NOT NULL DEFAULT 'BR',
    codigo_completo VARCHAR(20) AS (CONCAT(pais, sec, grupo_id)) STORED,
    PRIMARY KEY (id)
);

DELIMITER $$

CREATE TRIGGER trg_sec_auto
BEFORE INSERT ON frutas
FOR EACH ROW
BEGIN
    DECLARE proximo INT;

    SELECT COALESCE(MAX(CAST(sec AS UNSIGNED)),0) + 1
    INTO proximo
    FROM frutas
    WHERE grupo_id = NEW.grupo_id
      AND fruta = NEW.fruta;

    SET NEW.sec = LPAD(proximo, 4, '0');
END$$

DELIMITER ;

-- 🔥 DADOS INICIAIS PARA O GITHUB ACTIONS NÃO FICAR VAZIO
-- Esses inserts são ESSENCIAIS para testar o TRIGGER

INSERT INTO frutas (grupo_id, fruta) VALUES
('A','Banana'),

('A','Maçã'),
('A','Maçã'),
('A','Maçã'),

('B','Laranja'),
('C','Abacaxi');