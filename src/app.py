import mysql.connector

def conectar():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",   # Actions usa IP, não localhost
            user="root",
            password="root",
            database="db_alimentos"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None


def obter_proximo_sec(cursor, grupo_id):
    """FUNÇÃO MANTIDA para os testes antigos"""
    if not grupo_id:
        raise ValueError("Grupo inválido")

    query = "SELECT MAX(CAST(sec AS UNSIGNED)) FROM frutas WHERE grupo_id = %s"
    cursor.execute(query, (grupo_id,))
    resultado = cursor.fetchone()[0]

    novo_numero = (resultado + 1) if resultado else 1
    return str(novo_numero).zfill(4)


def cadastrar_fruta():
    db = conectar()
    if not db:
        return

    cursor = db.cursor()

    print("\n--- NOVO CADASTRO ---")
    fruta_nome = input("Digite o nome da fruta: ").strip().capitalize()
    grupo_letra = input("Digite a letra do Grupo ID: ").strip().upper()

    if not fruta_nome or not grupo_letra:
        print("Erro: Nome da fruta e Grupo são obrigatórios.")
        db.close()
        return

    try:
        # Trigger gera o SEC automaticamente
        sql_insert = "INSERT INTO frutas (grupo_id, fruta) VALUES (%s, %s)"
        cursor.execute(sql_insert, (grupo_letra, fruta_nome))
        db.commit()

        print("Fruta cadastrada com sucesso!")

        cursor.execute(
            "SELECT codigo_completo FROM frutas ORDER BY id DESC LIMIT 1")
        codigo = cursor.fetchone()[0]
        print(f"Código gerado: {codigo}")

    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar: {err}")
    finally:
        cursor.close()
        db.close()