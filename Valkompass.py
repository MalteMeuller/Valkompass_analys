
def restart():
    print("argv: ", sys.argv)
    print("sys.executable: ", sys.executable)
    print("Restart now!")
    os.execv(sys.executable, ['python'] + sys.argv)

#-------------------------------------------------------------
#här ska datan matas in
try:
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    import random
    import time
    import pandas as pd
    import numpy as np
    from tabulate import tabulate
    import sys
    import os
    import mysql.connector

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Ask me at malte.meuller@gmail.com",
        database="valkompasser"
    )

    my_cursor = db.cursor()

    df = pd.DataFrame(columns=['V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD'])

    def funk(f):
        # ladda sidan och ta bort adds.
        print('iterations', f)
        driver = webdriver.Chrome()
        driver.get('https://valkompass.com/#google_vignette')
        driver.maximize_window()
        driver.find_element(By.CSS_SELECTOR, '.tocompass').click()
        time.sleep(0.2)

        #--------------------------------------------------------------------------------
        def fråga(i):
            #hittar alla svarsalternativ, skapar lista.
            print('i:',i)
            code = driver.find_element(By.XPATH, '//*[@id="content"]/form/div['+ str(i)+']').get_attribute('outerHTML')
            lenght = int(code.count('"radio"') / 2)
            print('lenght:', lenght)
            new_list = [j for j in range(1,lenght+1)]
            print('list:', new_list)
            #slumpmässigt väljer ut en siffra, dvs ett svarsalternativ
            rand = random.choice(new_list)
            print('rand:', rand)
            time.sleep(0.2)
            #skrollar ner, funkade då
            driver.execute_script("window.scrollTo(0, 700)")
            time.sleep(0.2)
            #trycker på alternativet. Se div och label.
            driver.find_element(By.XPATH, '//*[@id="content"]/form/div['+ str(i)+']/label['+ str(rand)+']/strong').click()
            #skrollar ner och trycker på nästa.
            time.sleep(0.2)
            driver.execute_script("window.scrollTo(0, 900)")
            time.sleep(0.2)
            driver.find_element(By.XPATH, '//*[@id="content"]/form/div['+ str(i)+']/div[1]/button[2]').click()
            time.sleep(0.2)
        #------------------------------------------------------------------------------------------------
        antal = [i for i in range (1, 18)]
        for i in antal:
            fråga(i)

        #----------------------------------------------------------------------------
        #sista frågan, skapa nytt slumpsystem (inte helt slump dock)

        time.sleep(0.2)
        A='//*[@id="content"]/form/div[18]/label[1]'
        B='//*[@id="content"]/form/div[18]/label[2]'
        CE='//*[@id="content"]/form/div[18]/label[3]'
        D='//*[@id="content"]/form/div[18]/label[4]'
        E='//*[@id="content"]/form/div[18]/label[5]'
        F='//*[@id="content"]/form/div[18]/label[6]'
        G='//*[@id="content"]/form/div[18]/label[7]'

        last= [A,B,CE,D,E,F,G]
        rand_last = random.choices(last, k=3)
        time.sleep(0.2)
        driver.find_element(By.XPATH, rand_last[0]).click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, rand_last[1]).click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, rand_last[2]).click()
        time.sleep(0.2)

        driver.execute_script("window.scrollTo(0, 900)")
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="content"]/form/div[18]/div[1]/button[2]').click()
        time.sleep(1)

        #plockasiffror.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        numbers = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]').text
        test_list=numbers.split("%",8)
        print(test_list)

        V=int(test_list[0])
        S=int(test_list[1])
        MP=int(test_list[2])
        C=int(test_list[3])
        L=int(test_list[4])
        M=int(test_list[5])
        KD=int(test_list[6])
        SD=int(test_list[7])

        insert = "INSERT INTO valkompassen (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (V, S, MP, C, L, M, KD, SD)
        my_cursor.execute(insert, values)
        db.commit()

        driver.close()

    #slut på scriptet
    #-----------------------------------------------------

    iterations = [f for f in range (1, 1000)]
    for f in iterations:
        funk(f)
except:
    restart()