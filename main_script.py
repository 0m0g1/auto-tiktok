from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import re
import requests
from anticaptchaofficial.imagecaptcha import *


def close_new_tab(driver):
    try:
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
    except:
        pass


def keep_first_word(text):
    words = text.split()
    return words[0] if words else ""


def extract_text_from_image(driver, image_filename):
    try:
        # Open the image file
            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key("014a048cb9d6b3ba949dd6c76e2ce51b")
            solver.set_soft_id(0)

            extracted_text = solver.solve_and_return_solution(image_filename)
            if extracted_text != 0:
                print ("captcha extracted_text: "+extracted_text)
                return keep_first_word(extracted_text)
            else:
                print ("task error "+solver.error_code)
                time.sleep(1)
                extract_text_from_image(driver, image_filename)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_wait_time_sleep(driver):
    wait = WebDriverWait(driver, 10)
    countdown_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".countdown-circles")))

    data_time_value = countdown_element.get_attribute("data-time")
    print(f"data-time value: {data_time_value}")

    wait_time = int(data_time_value)
    print(f"Waiting for {wait_time} seconds...")
    time.sleep(wait_time)
    print("Wait completed.")
    time.sleep(2)


def click_use_button(driver):
    try:
        wait = WebDriverWait(driver, 10)
        use_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Use')]")))

        use_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")


def dashboard(driver, video_link,username_input):
   driver.get("https://homedecoratione.com")
   time.sleep(5)
   close_new_tab(driver)
   try:
        click_use_button(driver)
        try:
            try:
                get_wait_time_sleep(driver)
                try:
                    # Wait for the modal to appear and close button to be clickable
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-header .close"))
                    )   
                    # Find the close button and click it
                    close_button = driver.find_element(By.CSS_SELECTOR, ".modal-header .close")
                    close_button.click()    
                    print("Popup closed successfully.")
                except:
                    pass
                    
                click_use_button(driver)
            except:
                pass
            

            try:
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter URL']")
            except:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.modal-dialog.modal-dialog-centered'))
                )
                close_button = driver.find_element(By.CSS_SELECTOR, '.modal-dialog .modal-header .close')
                close_button.click()
                print("Modal closed successfully.")
                get_wait_time_sleep(driver)
                click_use_button(driver)


        except:
            pass 
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter URL']")))
        url_to_search = video_link
        input_field.clear()
        input_field.send_keys(url_to_search)
        time.sleep(1)

        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()

        print("URL entered and search button clicked successfully.")
        time.sleep(2)
        try:
            # original_tab = driver.current_window_handle
            wait = WebDriverWait(driver, 10)
            com_op_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-type='com_op']")))

            com_op_button.click()
            time.sleep(3)
        except:
            current_url=driver.current_url
            if current_url=="https://homedecoratione.com/" or current_url=="https://homedecoratione.com":
               wait = WebDriverWait(driver, 10)
               com_op_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-type='com_op']")))
               com_op_button.click()
            else:
                 # Wait for the new tab to open
                 wait.until(EC.number_of_windows_to_be(2))

                #  # Get the handle of the new tab
                #  new_tab = [window for window in driver.window_handles if window != original_tab][0]

                #  # Switch to the new tab
                #  driver.switch_to.window(new_tab)

                #  # Close the new tab
                #  driver.close()

                #  # Switch back to the original tab
                #  driver.switch_to.window(original_tab)
                

        print("Button with data-type='com_op' ")
        time.sleep(1)
        
        show_comments_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show comments')]"))
        )

        # Click the "Show comments" button
        show_comments_button.click()
        time.sleep(3)
        
        try:

            div_present = EC.presence_of_element_located((By.ID, 'lljxmhy'))
            WebDriverWait(driver, 10).until(div_present)

            # Find the div element
            div_element = driver.find_element(By.ID, 'lljxmhy')

            # Within the div element, find the 'a' element
            a_element = div_element.find_element(By.ID, 'lkarb')

            # Remember the current window handle
            original_window = driver.current_window_handle

            # Click the 'a' element (this will open a new tab)
            a_element.click()

            # Wait for the new tab to open
            WebDriverWait(driver, 10).until(EC.new_window_is_opened([original_window]))

            # Get all window handles
            windows = driver.window_handles

            # Switch to the new tab (which is not the original tab)
            for window in windows:
                if window != original_window:
                    driver.switch_to.window(window)
                    break

            # Do whatever you need to do in the new tab
            # ...

            # Close the new tab
            driver.close()

            # Switch back to the original tab
            driver.switch_to.window(original_window)
        except:
            pass

    
        while True:
            usernameToMatch = username_input
            WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".input-group.mb-1"))
            )
            comments = driver.find_elements(By.CSS_SELECTOR, ".input-group.mb-1")
            for comment in comments:
                username = comment.find_element(By.CSS_SELECTOR, "strong").text.strip()
                if username == usernameToMatch:
                    heartButton = comment.find_element(By.CSS_SELECTOR, ".btn.btn-info.btn-sm")
                    if heartButton:
                        try:
                          heartButton.click()
                        except:
                            heartButton.click()
                        get_wait_time_sleep(driver)  
                        print("50+  successfully")
                        return

            data_elem = driver.find_element(By.CSS_SELECTOR, 'div#ContactM')
            pagination_elem = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li[title="next"]')
            if pagination_elem:
                pagination_elem.click()
                time.sleep(5)
            else:
                if data_elem:
                    break
                else:
                    driver.refresh()
   except:
       dashboard(video_link,username_input)



def main(video_link, username_input, repeat_number):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.media_stream_mic": 2,
    })

    #chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("start-maximized")
    #chrome_options.add_argument("--disable-extensions")
    ###chrome_options.add_extension("AdBlock.zip")
    #chrome_options.add_argument("Permissions-Policy=interest-cohort=()")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://whoer.com/")
    time.sleep(5)
    close_new_tab(driver)
    driver.get("https://homedecoratione.com/")
    time.sleep(5)

    while True:
        time.sleep(5)
        close_new_tab(driver)
        try:
          img_element = driver.find_element(By.CSS_SELECTOR, ".card.border-info.mb-3 img")

          # Get the URL of the CAPTCHA image
          image_url = img_element.get_attribute("src")
    
          # Download the CAPTCHA image and save it locally
          image_path = "downloaded_image.png"
          with open(image_path, "wb") as image_file:
              image_file.write(img_element.screenshot_as_png)


          time.sleep(1)
  
  
          text=extract_text_from_image(driver, image_path)
          try:
              captcha_input = driver.find_element(By.CSS_SELECTOR, "form#cat input[name='captcha']")
              captcha_input.send_keys(text)
              submit_button = driver.find_element(By.CSS_SELECTOR, "form#cat button[type='submit']")
              submit_button.click()
              time.sleep(3)
              try:
                 driver.find_element(By.CSS_SELECTOR, ".card.border-info.mb-3 img")
                 continue
              except:
                  pass
          except:
              time.sleep(2)
              continue
        except:
            pass


        for i in range(repeat_number):
            dashboard(driver, video_link, username_input)
            
        return True
    
def run_all_items(items):
    for item in items:
        main(item["url"], item["username"], item["repeat"])
    return True