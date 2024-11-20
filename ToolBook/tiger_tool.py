from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import os
import shutil
import time

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def close_cookie_banner(driver: webdriver)-> None:
    """
    The function `close_cookie_banner` attempts to close a cookie banner on a webpage using Selenium in
    Python.
    
    :param driver: The `driver` parameter in the `close_cookie_banner` function is typically an instance of a
    WebDriver, which is used to automate interactions with a web browser. It allows you to navigate web
    pages, interact with elements on the page, and perform various actions like clicking buttons or
    entering text into input fields
    """
    try:
        cookie_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_button.click()
        logger.info("Closed cookie banner.")
    except Exception as e:
        logger.info("The cookie banner was not found or could not be closed.")

def login(driver: webdriver, USER: str, PASS: str) -> None:
    """
    The function `login` automates the login process by entering user credentials and verifying them on
    a web page using Selenium WebDriver in Python.
    
    :param driver: The `driver` parameter in the `login` function is typically an instance of a
    WebDriver, which is used to automate interactions with a web browser. It allows you to navigate web
    pages, interact with elements on the page, and perform various actions like clicking buttons or
    entering text into input fields
    :param USER: The `USER` parameter in the `login` function is used to pass the username or user
    identifier for authentication. It is the username that the user enters to log in to the system or
    application
    :param PASS: The `PASS` parameter in the `login` function represents the password that the user
    needs to enter during the authentication process. This password is typically used to verify the
    identity of the user and grant access to the system or application. It is a sensitive piece of
    information that should be kept confidential and not
    """
    try:
        # We try to find and click on the continue button
        continuar_button = driver.find_element(By.NAME, "action")
        continuar_button.click()

        # We wait until the user field is present
        user_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        logger.info("Authentication page detected. Entering credentials...")

        # Clear and enter user name
        user_input.clear()
        user_input.send_keys(USER)

        # Click on continue
        continuar_button = driver.find_element(By.NAME, "action")
        continuar_button.click()

        # We are waiting for the password field
        pass_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input28")))

        # Clear and enter password
        pass_input.clear()
        pass_input.send_keys(USER)

        # Click on the "Next" button
        next_button = driver.find_element(By.XPATH, "//input[@value='Next']")
        next_button.click()

        # Here we try to wait for the second password field
        try:
            pass_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input29")))
        except TimeoutException:
            pass_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input62")))

        # Clear and enter the real password
        pass_input.clear()
        pass_input.send_keys(PASS)

        # Click on "Verify".
        next_button = driver.find_element(By.XPATH, "//input[@value='Verify']")
        next_button.click()

        # We wait for the URL to change (indicating a successful login).
        WebDriverWait(driver, 15).until(EC.url_contains("dashboard"))
        logger.info("Login exitoso.")
        
    except Exception as e:
        # Si ocurre un error en cualquier parte del proceso de login
        logger.error(f"Error durante el proceso de autenticación")

def wait_for_file(download_dir, file_name, timeout=10):
    """
    Wait for the downloaded file to appear in the download directory. 
    
    The function periodically checks if the file specified by `file_name` is present in the `download_dir` download directory.
    The wait will continue until the file is found or until the timeout specified by `timeout` times out.

    :param download_dir: Directory where the downloaded file is expected to appear. 
    :param file_name: Name of the file expected to be found in the directory. 
    :param timeout: Maximum timeout time in seconds (default 10 seconds). If the file is not found before the timeout, the function returns `False`.

    :return: `True` if the file was found within the timeout, otherwise `False`. 
    :raises: None.
    """
    end_time = time.time() + timeout  # Calculate the time limit for waiting
    while time.time() < end_time:
        files = os.listdir(download_dir)  # Gets the list of files in the directory
        if any(file_name in file for file in files):  # Check if the desired file is present
            return True
        time.sleep(1)  # Wait 1 second before checking again

    # If the file is not found after the timeout, it returns False.
    return False

def save_standard_report(download_dir, original_name, new_name):
    """
    Saves the downloaded report by renaming it and moving it to the destination directory. 
    
    The function waits for the file specified by `original_name` to become available in the download directory `download_dir`. 
    Once downloaded, the file is renamed to `new_name` and saved in the same directory. If a file with the new name already exists, 
    it is deleted before proceeding with the renaming.

    :param download_dir: Directory where the downloaded file is located. 
    :param original_name: Original name of the downloaded file. 
    :param new_name: New name to be assigned to the downloaded file.

    :return: None
    :raises: Exception if an error occurs when renaming or moving the file.
    """
    try:
        # Wait for the downloaded file to become available
        if wait_for_file(download_dir, original_name):
            original_file_path = os.path.join(download_dir, original_name)  # Full path to the original file
            new_file_path = os.path.join(download_dir, new_name)  # Full path to the file with the new name
            
            # Check if the file with the new name already exists and delete it.
            if os.path.exists(new_file_path):
                logger.info(f"The file {new_file_path} already exists. Removing to replace...")
                os.remove(new_file_path)

            # Rename the file
            os.rename(original_file_path, new_file_path)
            logger.info(f"Report saved and renamed to {new_name} successfully.")
        else:
            logger.info(f"File {original_name} not found in the download directory.")
            
    except Exception as e:
        logger.error(f"An error occurred while saving the report")
        raise  # Throws exception to be handled by caller function

def download_standard_report(driver: webdriver, URL:str, title_Fav_report_tiger:str, download_dir:str, original_name:str, change_name=None):
    """
    Downloads a standard report from the 'TIGER FAVORITOS' web page, based on a specific favourite. 
    
    The function navigates to the URL provided, closes the cookie banner, clicks on a report bookmark, 
    and then initiates the download of the corresponding report. It then waits until the download
    is complete and saves the report with a modified name.

    :param driver: The `driver` parameter in the `download_standard_report` function is typically an instance of a
    WebDriver, which is used to automate interactions with a web browser. It allows you to navigate web
    pages, interact with elements on the page, and perform various actions like clicking buttons or
    entering text into input fields
    :param URL: URL of 'TIGER FAVOURITES' from where the report will be downloaded (FAVOURITES MUST ALREADY BE MAPPED). 
    :param title_Fav_report_tiger: The title of the report in the favourites list, used to identify and click on the appropriate report. 
    :param download_dir: Directory where the downloaded report will be saved. param original_name: Original file name for the report, to be used to create the new file name. 
    :param change_name: In case you want to name the file in a specific way, if you don't enter a value the variable 'title_Fav_report_tiger' will be used to rename the report (not necessary).

    :return: None
    :raises: Exception if an error occurs during the download process or if the report is not downloaded correctly.
    """
    try:
        # Access the URL provided
        driver.get(URL) 

        # Wait until the favourite report is clickable and select it.
        div_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='"+title_Fav_report_tiger+"']"))
        )
        div_element.click()
        time.sleep(3)  # Wait briefly to ensure that the previous action has been completed.

        # Wait until the export report button is clickable and press it.
        button_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='$ctrl.exportReport()']"))
        )
        button_element.click()

        # Wait until the processing message disappears
        WebDriverWait(driver, 300).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@my-success-message-box='' and contains(@class, 'in-progress-message-box')]"))
        )

        # Wait until the success message appears, indicating that the download is complete.
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//div[@my-success-message-box='' and contains(@class, 'success-message-box')]"))
        )

        # Determines new file name based on report title
        if change_name:            
            new_name = f"{change_name}.xlsx"
        else:
            new_name = f"{title_Fav_report_tiger}.xlsx"

        # Calls the function to save the report with the new name
        save_standard_report(download_dir, original_name, new_name)
    
    except Exception as e:
        logger.error(f"An error occurred during report download")
        raise  # Re-throws exception to be handled by caller

def download_get_my_data(driver: webdriver, URL:str, title_Fav_report_tiger:str, download_dir:str, original_name:str, change_name=None):
    """
    Downloads the 'Get My Data' report data from the provided web page, based on a specific bookmark. 
    
    The function navigates to the URL provided, closes the cookie banner, clicks on a report bookmark, and then initiates the download 
    of the corresponding data. It then waits until the download is complete and saves the data under a modified name.

    :param driver: The `driver` parameter in the `download_standard_report` function is typically an instance of a
    WebDriver, which is used to automate interactions with a web browser. It allows you to navigate web
    pages, interact with elements on the page, and perform various actions like clicking buttons or
    entering text into input fields
    :param URL: URL of 'TIGER FAVOURITES' from where the report will be downloaded (FAVOURITES MUST ALREADY BE MAPPED). 
    :param title_Fav_report_tiger: The title of the report in the favourites list, used to identify and click on the appropriate report. 
    :param download_dir: Directory where the downloaded report will be saved. param original_name: Original file name for the report, to be used to create the new file name. 
    :param change_name: In case you want to name the file in a specific way, if you don't enter a value the variable 'title_Fav_report_tiger' will be used to rename the report (not necessary).

    :return: None
    :raises: Exception if an error occurs during the download process or if the report is not downloaded correctly.
    """
    try:
        # Access the URL provided
        driver.get(URL)

        # Wait until the favourite report is clickable and select it.
        div_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='"+title_Fav_report_tiger+"']"))
        )
        div_element.click()
        time.sleep(3)  # Wait briefly to ensure that the previous action has been completed.

        # Wait until the export data button is clickable and press it.
        button_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@ng-click='onExportMyDataClick()']"))
        )
        button_element.click()
        
        button_element_caution = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='proceed()']"))
        )
        button_element_caution.click()

        # Wait until the processing message disappears
        WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@my-success-message-box='' and contains(@class, 'in-progress-message-box')]"))
        )

        # Wait until the success message appears, indicating that the download is complete.
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//div[@my-success-message-box='' and contains(@class, 'success-message-box')]"))
        )
        
        # Determines new file name based on report title
        if change_name:            
            new_name = f"{change_name}.xlsx"
        else:
            new_name = f"{title_Fav_report_tiger}.xlsx"

        # Calls the function to save the data with the new name
        save_standard_report(download_dir, original_name, new_name)
    
    except Exception as e:
        logger.error(f"An error occurred during data download: {str(e)}")
        raise  # Re-throws exception to be handled by caller
