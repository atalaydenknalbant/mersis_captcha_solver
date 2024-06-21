from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    UnexpectedAlertPresentException, ElementNotInteractableException, ElementClickInterceptedException, \
    NoSuchWindowException, JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import os
import undetected_chromedriver as uc
from MathCaptchaSolver import CaptchaSolver
import time
from io import BytesIO
from PIL import Image
import numpy as np

dir = os.getcwd()

for _ in range(50):
    driver = webdriver.Chrome(service=Service())
    driver.implicitly_wait(12)
    driver.get('https://mersis.ticaret.gov.tr/Portal/Home/Index')
    driver.maximize_window()
                

    while True:
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "small-badge1")))[-1]
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "small-badge1")))
        try:
            driver.find_elements(By.CLASS_NAME, "small-badge1")[-1].click()
        except ElementClickInterceptedException:
            driver.refresh()
            continue
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'captchaImage')))
        
        captcha_element = driver.find_element(By.ID, 'captchaImage')
        captcha_screenshot = captcha_element.screenshot_as_png
        captcha_image = Image.open(BytesIO(captcha_screenshot))
        captcha_image_np = np.array(captcha_image)

        solver = CaptchaSolver(captcha_image_np)
        result = solver.solve_captcha()



        try:
            WebDriverWait(driver, 6).until(ec.visibility_of_element_located((By.CLASS_NAME, 'form-control'))).send_keys(result)
        except TypeError or TimeoutException:
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#modalDialog > div > div.modal-header > button'))).click()  
            continue
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR,'#divDogrula > div > input'))).click()
        time.sleep(3)
        try:
            WebDriverWait(driver, 4).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#divResult > span'))).text == 'Bu belge kodu ile ilişkili bir kayıt bulunamamıştır.'
            break
        except TimeoutException:
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#modalDialog > div > div.modal-header > button'))).click()  
    driver.quit()