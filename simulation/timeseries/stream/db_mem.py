import sqlite3

def initDb():
    c = sqlite3.connect('../outlier.db')
    # Create table
    c.execute("CREATE TABLE if not exists outlier (hash_chave text, ind text, PRIMARY KEY (hash_chave))")
    c.execute("CREATE TABLE if not exists models (hash_chave text, uri text, PRIMARY KEY (hash_chave))")
    c.close()

def gerarOutlier(hash_chave, index):
    c = sqlite3.connect('../outlier.db')
    # Insert a row of data
    c.execute("REPLACE INTO outlier VALUES (?,?)", [hash_chave, index])
    # Save (commit) the changes
    c.commit()
    c.close()

def gerarModel(hash_chave, uri):
    c = sqlite3.connect('../outlier.db')
    # Insert a row of data
    c.execute("REPLACE INTO models VALUES (?,?)", [hash_chave, uri])
    # Save (commit) the changes
    c.commit()
    c.close()

def removerOutlier(hash_chave, index):
    c = sqlite3.connect('../outlier.db')
    # Insert a row of data
    c.execute("DELETE FROM outlier WHERE hash_chave = ? and ind = ?", [hash_chave,index])
    # Save (commit) the changes
    c.commit()
    c.close()

def getOutlier(hash_chave, index):
    c = sqlite3.connect('../outlier.db')
    # Insert a row of data
    tuplaDados = c.execute("SELECT hash_chave FROM outlier WHERE hash_chave = ? and ind = ?", [hash_chave,index]).fetchone()
    if tuplaDados == None:
        return None
    else:
        return tuplaDados[0]
    c.close()