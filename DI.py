from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
import sys
import os
import mysql.connector
#------------------------------------------------------------------------
def restart():
    print("argv: ", sys.argv)
    print("sys.executable: ", sys.executable)
    print("Restart now!")
    os.execv(sys.executable, ['python'] + sys.argv)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Ask me at malte.meuller@gmail.com",
        database="valkompasser",
    )
    my_cursor = db.cursor()

    #--------------------------------------------------
    def funk(f):
        driver = webdriver.Chrome()
        driver.get('https://ext.di.se/qs/widgets/pang/Valkompass/index.html?id=1')
        driver.maximize_window()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]').click()

        heart = [a for a in range(1, 29)]  # random number
        randheart = random.choices(heart, k=3)
        print('Random hearts:', randheart)
        time.sleep(1)

        def fraga(i):
            #random heart
            for x in randheart:
                if (i in randheart):
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div[1]').click()
            time.sleep(1)

            A = '//*[@id="button4"]'
            B = '//*[@id="button3"]'
            CE = '//*[@id="button1"]'
            D = '//*[@id="button0"]'

            rand = [A, B, CE, D]
            randquest = random.choice(rand)

            driver.find_element(By.XPATH, randquest).click()

        # -------------------------------------------------------
        antal = [i for i in range(1, 29)]
        for i in antal:
            fraga(i)

        #----------------------------------
        time.sleep(5)

        name_list = []
        value_list = []
        for x in range(1, 9):
            value = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[4]/div[' + str(x) + ']/div[1]/div[1]').text
            value = value.split("%", 1)
            value = int(value[0])
            value_list.append(value)
            name = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[4]/div[' + str(x) + ']/div[2]').text
            name_list.append(name)

        my_dict = dict(zip(name_list, value_list))

        V = my_dict["V"]
        S = my_dict["S"]
        MP = my_dict["MP"]
        C = my_dict["C"]
        L = my_dict["L"]
        M = my_dict["M"]
        KD = my_dict["KD"]
        SD = my_dict["SD"]

        insert = "INSERT INTO di (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (V, S, MP, C, L, M, KD, SD)
        my_cursor.execute(insert, values)
        db.commit()

        time.sleep(2)

        driver.close()

    #--------------------------------------------------
    iterations = [f for f in range (1, 10000)]
    for f in iterations:
        funk(f)
except:
    restart()

