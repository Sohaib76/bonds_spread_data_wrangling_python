import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()


driver.maximize_window()
driver.get('https://www.investing.com/rates-bonds/')

#Login
email = 'wonderhaven20@gmail.com'
password = 'waspbeastring12'

failedCountryListings = []

login_btn = driver.find_element_by_css_selector('.login')
driver.execute_script('arguments[0].click();', login_btn)

time.sleep(3)

email_input = driver.find_element_by_css_selector('#loginFormUser_email')
email_input.clear()

email_input.send_keys(email)

password_input = driver.find_element_by_css_selector('#loginForm_password')
password_input.clear()

password_input.send_keys(password)

submit_btn = driver.find_elements_by_css_selector('.newButton.orange')[-1]
submit_btn.click()

time.sleep(3)

driver.get('https://www.investing.com/rates-bonds/')

search_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-search-bonds')))
driver.execute_script('arguments[0].click();', search_btn)

country_listing = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.plusIconTd a')))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
country_listings = [elem.get('href') for elem in soup.select('.plusIconTd a')]

print(f'Found {len(country_listings)} country listings')

for i in range(len(country_listings)):
    try:
        print(f'On country listings index => {i}')
        driver.get(f'https://www.investing.com{country_listings[i]}')

        historical_data_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pairSublinksLevel2 a')))
        driver.execute_script('arguments[0].click();', historical_data_btn)
        
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        
        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/1970')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)



        #-------------------Double
            
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        

        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/2010')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)

        #-------------------- Triple
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        

        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/1999')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)
    except:
        print(f'Error downloading | {country_listings[i]}')
        failedCountryListings.append(country_listings[i])
        continue
    
    
        

#---------------------------------------------------------------
print("Downloading Failed Countries")

if len(failedCountryListings) == 0:
    driver.close()
    print("No Failed Countries")
    exit()

for i in range(len(failedCountryListings)):
    try:
        print(f'On failed country listings index => {i}')
        driver.get(f'https://www.investing.com{failedCountryListings[i]}')

        historical_data_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pairSublinksLevel2 a')))
        driver.execute_script('arguments[0].click();', historical_data_btn)
        
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        
        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/1970')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)



        #-------------------Double
            
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        

        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/2010')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)

        #----------------Triple
        date_picker = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#widgetFieldDateRange')))
        driver.execute_script('arguments[0].click();', date_picker)
        

        start_date =  WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#startDate')))
        start_date.clear()
        start_date.send_keys('01/01/1999')
        
        time.sleep(2)
        
        apply_btn = driver.find_element_by_css_selector('#applyBtn')
        driver.execute_script('arguments[0].click();', apply_btn)
        
        time.sleep(3)
        
        download_csv_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.js-download-data')))
        driver.execute_script('arguments[0].click();', download_csv_btn)
    except:
        
  
        continue


driver.close()