from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

driver=webdriver.Chrome()
driver.set_page_load_timeout(20)
driver.get('https://www.youtube.com/playlist?list=PLJicmE8fK0Eh88ix1co6RG4pDcRjpaPj4')
driver.maximize_window()
sleep(5)

user_data = driver.find_elements(By.XPATH,"""//*[@id="video-title"]""")
links = []
for i in user_data:
            links.append(i.get_attribute('href'))

df = pd.DataFrame(columns = ['link', 'title', 'views', 'posted_time', 'thumbnails', 'comments'])
wait = WebDriverWait(driver, 10)
counter = 0
actions = ActionChains(driver)
list = []

for index, x in enumerate(links):
    if counter == 3:
        break
    driver.get(x)
    v_id = x.strip('https://www.youtube.com/watch?v=')

    v_title_xpath = f'(//*[@id="video-title"])[{index+1}]'
    try:
        v_title = wait.until(EC.visibility_of_element_located((By.XPATH, v_title_xpath))).text
        v_views = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="info"]/span[1]'))).text
        v_posted_time = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="info"]/span[3]'))).text

        for _ in range(3): 
            actions.send_keys(Keys.PAGE_DOWN).perform()
            sleep(1)

        v_thumbnail_selector = 'img[src^="https://i.ytimg.com/vi/"]'
        v_thumbnail = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, v_thumbnail_selector)))
        v_thumbnail_url = v_thumbnail.get_attribute('src')
        
        v_comments_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]/span')
        for comment_element in v_comments_elements:
            comment_text = comment_element.text
            df = df.append({'link': v_id, 'title': v_title, 'views': v_views, 'posted_time': v_posted_time, 'thumbnails': v_thumbnail_url, 'comment': comment_text}, ignore_index=True)

    except Exception as e:
        print("Error occurred:", e)
        print("Unable to extract data for video:", v_id)
    finally:
        counter += 1

df.to_csv("comment_1.csv", index=False)
driver.close()