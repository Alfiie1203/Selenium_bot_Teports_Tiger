from ToolBook import tiger_tool
from ToolBook.Navegadores.Edge import edge
from datetime import datetime
from selenium.webdriver.edge.options import Options
import logging

# Configuring the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(URL,USER,PASS,download_dir,new_Name):
    driver = None
    try:
        # Initialising the WebDriver with the settings
        driver = edge.initialize_driver(download_dir=download_dir)
        driver.get(URL)

        try:
            tiger_tool.login(driver,USER,PASS)
            tiger_tool.close_cookie_banner(driver)
        except Exception:
            logger.info("Login failed, trying to continue without authentication...")
            
        # Get current date
        curren_date = datetime.now()
        # Format the date in the desired format
        format_date = curren_date.strftime('%Y-%b-%d')
        
        tiger_tool.download_get_my_data(driver, URL, "MI", download_dir,"mydata-"+format_date.lower()+".xlsx",new_Name)
        
    finally:
        if driver:
            logger.info("Closing WebDriver...")
            driver.quit()
            logger.info("WebDriver closed.")
            