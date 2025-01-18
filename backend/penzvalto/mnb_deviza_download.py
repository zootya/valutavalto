import requests
import pandas as pd
import sqlite3
import datetime
import math


def nmbLetolt():  
    # nmb oldalról letölti a arfolyam.xlsx állományt, ami az aktuális árfolyamokat tartalmazza
    url = "https://www.mnb.hu/Root/ExchangeRate/arfolyam.xlsx"
    filename = "arfolyam.xlsx"
    
    # letölti a MNB weboldalról a(z) arfolyam.xlsx állományt
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully!")
    else:
        print("Failed to download the file.")
    # ------ letöltés vége------------------------------------
    
    
    # beolvassa egy dataframe-be a "filename" állományt
    xls = pd.ExcelFile(filename) 
    sheetX = xls.parse(0)            # az első munkalap
    # beolvasás vége ----------------------------------

    nmbToSqlite(sheetX)

    xls.close()


def nmbToSqlite(dadaFrame):
    # az xls adatait beolvassa egy sqlite tmp táblába, de csak az kerül eltárolásra ami
    # még nem szerepel benne, majd az egész tmp átírja a rendes mnb állományba. 
    # Igy csak egyszer szerepel egy adat
     
    conn = sqlite3.connect('db.sqlite3')

    query = f"CREATE TABLE IF NOT EXISTS mnb_deviza_tmp ( "\
            f"arfolyam TEXT UNIQUE ON CONFLICT IGNORE "\
            f");"

    conn.execute(query)

    fej = dadaFrame.columns
    oszlop = len(fej)
    sor = len(dadaFrame)

    for i in range(sor):
        for j in range(oszlop):
            if i > 0 and j > 0 :
                # az előző 45 napot tölti be
                if dadaFrame[dadaFrame.columns[0]][i] > datetime.datetime.now() - datetime.timedelta(days=45):
                    if not ( math.isnan(dadaFrame[dadaFrame.columns[j]][i]) ):
                        s = f"{dadaFrame[dadaFrame.columns[0]][i].strftime('%Y-%m-%d')}_{fej[j]}_{dadaFrame[dadaFrame.columns[j]][i]}"
                        print(s)
                        query = f"INSERT INTO mnb_deviza_tmp (arfolyam) VALUES ('{s}');"
                        conn.execute(query)

    query = f"DROP TABLE IF EXISTS mnb_deviza;"
    conn.execute(query)

    query = f"CREATE TABLE IF NOT EXISTS penzvalto_mnb_deviza ( "\
            f"id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "\
            f"date DATE NOT NULL, "\
            f"currency VARCHAR (10) NOT NULL, "\
            f"value REAL NOT NULL"\
            f");"
    conn.execute(query)
    
    query = f"INSERT INTO penzvalto_mnb_deviza (date, currency, value) "\
            f"SELECT substr(arfolyam, 1, 10), "\
            f"substr(arfolyam, 12, 3), "\
            f"substr(arfolyam, 16) "\
            f"FROM mnb_deviza_tmp;"
    conn.execute(query)

    conn.commit()
    conn.close()



if __name__ == '__main__':
    nmbLetolt()