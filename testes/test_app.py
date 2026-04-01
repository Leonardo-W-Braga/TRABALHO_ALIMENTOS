import pytest
from unittest.mock import MagicMock
from src.app import obter_proximo_sec
import mysql.connector
from src.app import conectar

# TESTES ANTIGOS (mantidos)
def test_sec_primeiro_registro():
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (None,)
    assert obter_proximo_sec(cursor_mock, "A") == "0001"

def test_sec_incremento_normal():
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (5,)
    assert obter_proximo_sec(cursor_mock, "A") == "0006"

def test_sec_formatacao_quatro_digitos():
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (9,)
    assert obter_proximo_sec(cursor_mock, "A") == "0010"

# NOVOS TESTES (integração com MySQL)
def conectar_mysql_actions():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="db_alimentos"
    )

def test_conexao_mysql_actions():
    conn = conectar_mysql_actions()
    assert conn.is_connected()
    conn.close()


def test_ver_tabela_actions():
    """Mostra o conteúdo da tabela no GitHub Actions"""

    conn = conectar()
    assert conn is not None, "Falha ao conectar no banco"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM frutas")
    resultados = cursor.fetchall()

    print("\n===== CONTEÚDO DA TABELA FRUTAS =====")
    for linha in resultados:
        print(linha)

    cursor.close()
    conn.close()

    assert len(resultados) > 0

def test_trigger_sec_funcionando():
    conn = conectar_mysql_actions()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sec FROM frutas
        WHERE grupo_id='A' AND fruta='Maçã'
        ORDER BY id
    """)
    macas = [linha[0] for linha in cursor.fetchall()]
    cursor.close()
    conn.close()

    assert macas == ['0001','0002','0003']