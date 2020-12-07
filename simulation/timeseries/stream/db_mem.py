import sqlite3

def initDb():
    c = sqlite3.connect('./outlier.db')
    # Create table
    c.execute("CREATE TABLE if not exists outlier (hash_chave text, PRIMARY KEY (hash_chave))")
    c.close()

def gerarOutlier(hash_chave):
    c = sqlite3.connect('./outlier.db')
    # Insert a row of data
    c.execute("REPLACE INTO outlier VALUES (?)", [hash_chave])
    # Save (commit) the changes
    c.commit()
    c.close()

def removerOutlier(hash_chave):
    c = sqlite3.connect('./outlier.db')
    # Insert a row of data
    c.execute("DELETE FROM outlier WHERE hash_chave = ?", [hash_chave])
    # Save (commit) the changes
    c.commit()
    c.close()

def getOutlier(hash_chave):
    c = sqlite3.connect('./outlier.db')
    # Insert a row of data
    tuplaDados = c.execute("SELECT hash_chave FROM outlier WHERE hash_chave = ?", [hash_chave]).fetchone()
    if tuplaDados == None:
        return None
    else:
        return tuplaDados[0]
    c.close()