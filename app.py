import sqlite3
import xml.etree.ElementTree as ElementTree

# Classe que cria, conecta e manipula o banco de dados SQLite.
class Manipulador:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def criar_tabela(self, table_name, columns):
        self.cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

    def confirmar(self):
        self.conn.commit()
        self.conn.close()

# Classe que insere dados nas tabelas
class Insersor:
    def __init__(self, db_handler, root):
        self.db_handler = db_handler
        self.root = root

    def inserir_dados(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f':{col}' for col in data.keys()])
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self.db_handler.cursor.execute(query, data)

def main():
    # Nome do arquivo XML
    nome_arquivo = 'Alarms.xml'

    # Parse do arquivo XML
    tree = ElementTree.parse(nome_arquivo)
    root = tree.getroot()

    # Criar instância do manipulador de banco de dados
    db_handler = Manipulador('alarms.db')

    # --- TABELA TRIGGERS ---

    # Definir colunas para a tabela 'triggers'
    triggers_columns = '''
        id TEXT PRIMARY KEY,
        type TEXT,
        exp TEXT,
        label TEXT
    '''

    # Criar tabela 'triggers'
    db_handler.criar_tabela('triggers', triggers_columns)

    # Criar instância do insersor de dados
    data_inserter_triggers = Insersor(db_handler, root)

    # Inserir dados na tabela 'triggers'
    for trigger in root.findall(".//trigger"):
        trigger_data = {
            'id': trigger.get('id'),
            'type': trigger.get('type'),
            'exp': trigger.get('exp'),
            'label': trigger.get('label')
        }
        data_inserter_triggers.inserir_dados('triggers', trigger_data)


    # --- TABELA MESSAGES ---

    # Definir colunas para a tabela 'messages'
    messages_columns = '''
        id TEXT PRIMARY KEY,
        trigger_value TEXT,
        identifier TEXT,
        trigger TEXT,
        text TEXT
    '''

    # Criar tabela 'messages'
    db_handler.criar_tabela('messages', messages_columns)

    # Criar instância do inseridor de dados
    data_inserter_messages = Insersor(db_handler, root)

    # Inserir dados na tabela 'messages'
    for message in root.findall(".//message"):
        message_data = {
            'id': message.get('id'),
            'trigger_value': message.get('trigger-value'),
            'identifier': message.get('identifier'),
            'trigger': message.get('trigger'),
            'text': message.get('text')
        }
        data_inserter_messages.inserir_dados('messages', message_data)

    # Confirmar e fechar a conexão
    db_handler.confirmar()


if __name__ == "__main__":
    main()