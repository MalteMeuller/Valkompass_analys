
def restart():
    print("argv: ", sys.argv)
    print("sys.executable: ", sys.executable)
    print("Restart now!")
    os.execv(sys.executable, ['python'] + sys.argv)

try:
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    import random
    import time
    import pandas as pd
    import sys
    import os
    import mysql.connector

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Ask me at malte.meuller@gmail.com",
        database="valkompasser",
    )
    my_cursor = db.cursor()

    df = pd.DataFrame(columns=['V', 'S', 'MP', 'C', 'L', 'M', 'KD', 'SD'])

    #--------------------------------------------------
    def funk(f):
        driver = webdriver.Chrome()
        driver.get('https://www.dn.se/valkompass/')
        driver.maximize_window()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()
        time.sleep(1)

        #hjärtefråga
        heart = [a for a in range(1, 26)]  # random number
        randheart = random.choices(heart, k=3)
        print('Random hearts:', randheart)

        def fraga(i):
            #scroll
            time.sleep(0.5)
            target = driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/form/section['+str(i)+']/div/p')
            driver.execute_script("return arguments[0].scrollIntoView();", target)
            time.sleep(0.5)
            #random
            alt = [a for a in range(1,5)] #random number
            rand = random.choice(alt)
            print('Random number:', rand)
            #tryck
            driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/form/section['+str(i)+']/div/div[1]/div[1]/div['+str(rand)+']/label/input').click()
            time.sleep(0.5)
            #hjärtefråga

            if (i in randheart):
                driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/form/section['+str(i)+']/div/div[1]/div[2]/div[2]/div/label').click()

        #-------------------------------------
        antal = [i for i in range (1, 26)]
        for i in antal:
            fraga(i)
        #----------------------------------
        #driver.execute_script("window.scrollTo(0, 500)")
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/form/div[26]/button').click()
        time.sleep(1)
        respos = driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/div[1]/div/section[2]/div/div/div[1]')
        time.sleep(1)
        driver.execute_script("return arguments[0].scrollIntoView();", respos)
        time.sleep(1)
        numbers = driver.find_element(By.XPATH, '//*[@id="site-body"]/article/div/div[2]/div/div[1]/div/section[2]/div/div/div[1]').text
        print(numbers)
        test_list = numbers.split("%", 8)
        print(test_list)

        V = int(test_list[0])
        S = int(test_list[1])
        MP = int(test_list[2])
        C = int(test_list[3])
        L = int(test_list[4])
        M = int(test_list[5])
        KD = int(test_list[6])
        SD = int(test_list[7])

        insert = "INSERT INTO dn (V, S, MP, C, L, M, KD, SD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (V, S, MP, C, L, M, KD, SD)
        my_cursor.execute(insert, values)
        db.commit()

        driver.close()


    #--------------------------------------------------
    iterations = [f for f in range (1, 10000)]
    for f in iterations:
        funk(f)
except:
    restart()
