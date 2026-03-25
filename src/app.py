import mysql.connector
#ola

def conectar():
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="estoque_frutas"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None


def obter_proximo_sec(cursor, grupo_id):

    if not grupo_id:
        raise ValueError("Grupo inválido")

    query = "SELECT MAX(CAST(sec AS UNSIGNED)) FROM frutas WHERE grupo_id = %s"
    cursor.execute(query, (grupo_id,))
    resultado = cursor.fetchone()[0]

    novo_numero = (resultado + 1) if resultado else 1
    return str(novo_numero).zfill(4)


def cadastrar_fruta():
    """Lógica principal de validação e inserção de dados."""
    db = conectar()
    if not db:
        return

    cursor = db.cursor()

    print("\n--- NOVO CADASTRO ---")
    fruta_nome = input("Digite o nome da fruta: ").strip().capitalize()
    grupo_letra = input("Digite a letra do Grupo ID: ").strip().upper()

    # Validação básica de campos vazios
    if not fruta_nome or not grupo_letra:
        print("Erro: Nome da fruta e Grupo são obrigatórios.")
        db.close()
        return

    try:
        #Verificar se a fruta já existe nesse grupo específico
        query_busca = "SELECT codigo_completo FROM frutas WHERE fruta = %s AND grupo_id = %s"
        cursor.execute(query_busca, (fruta_nome, grupo_letra))
        registro = cursor.fetchone()

        if registro:
            print(
                f"BLOQUEADO: A fruta '{fruta_nome}' já está cadastrada no Grupo '{grupo_letra}' (Código: {registro[0]}).")
            print("Não é possível repetir o mesmo item no mesmo grupo.")
        else:
            sec_final = obter_proximo_sec(cursor, grupo_letra)

            sql_insert = "INSERT INTO frutas (sec, grupo_id, fruta) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (sec_final, grupo_letra, fruta_nome))
            db.commit()
            print(f"Sucesso! Item cadastrado com o código: BR{sec_final}{grupo_letra}")

    except mysql.connector.Error as err:
        if err.errno == 1062:
            print("Erro: Este registro já existe no banco de dados.")
        else:
            print(f"Erro inesperado: {err}")
    finally:
        cursor.close()
        db.close()


# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
if __name__ == "__main__":
    print("========================================")
    print("   SISTEMA DE GESTÃO DE FRUTAS (BR)     ")
    print("========================================")

    while True:
        cadastrar_fruta()

        # Pergunta se o usuário quer continuar ou sair
        opcao = input("\nDeseja cadastrar outra fruta? (S/N): ").strip().upper()
        if opcao != 'S':
            print("\nEncerrando sistema... Cadastro finalizado!")
            break