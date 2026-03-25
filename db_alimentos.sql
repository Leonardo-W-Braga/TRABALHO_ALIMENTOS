create database estoque_frutas;

CREATE TABLE frutas (
    id INT NOT NULL AUTO_INCREMENT,
    sec VARCHAR(10) NOT NULL,
    grupo_id CHAR(1) NOT NULL,
    fruta VARCHAR(100) NOT NULL,
    pais CHAR(2) NOT NULL DEFAULT 'BR',
    codigo_completo VARCHAR(20) AS (CONCAT(pais, sec, grupo_id)) STORED,
    PRIMARY KEY (id),
    UNIQUE KEY idx_codigo_unico (codigo_completo),
    UNIQUE KEY idx_fruta_grupo_unico (fruta, grupo_id)
)

select * from frutas;