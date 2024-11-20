import os
import json
import glob
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver import Edge
from selenium import webdriver

def get_edge_driver_path():
    """
    Generates the Edge driver path dynamically based on the current project directory.
    Assumes the driver is in a 'Navegadores/Edge/Edge_Driver' folder relative to the project folder.
    C:/Users/FC5010/OneDrive - Vialto/Escritorio/tiger/ToolBook/Navegadores/Edge/Edge_Driver/msedgedriver.exe
    """
    project_dir = os.getcwd()  # Get current working directory (where the script is running)
    edge_driver_path = os.path.join(project_dir,'ToolBook', 'Navegadores', 'Edge', 'Edge_Driver', 'msedgedriver.exe')
    
    # Verifica si la ruta existe
    if not os.path.exists(edge_driver_path):
        raise FileNotFoundError(f"Edge driver not found at {edge_driver_path}")
    
    return edge_driver_path

def initialize_driver(download_dir=None, headless=False, window_size="1920,1080", edge_user_profile=None):
    """
    Initialises the Edge WebDriver with configured options.
    
    :param download_dir: Directory to save downloads (if needed). 
    :param headless: Whether to run in headless mode (default False). 
    :param window_size: Size of the browser window (default "1920,1080"). 
    :param edge_user_profile: Path to Edge user profile (default None). 
    
    :return: WebDriver instance.
    """
    # Get the dynamic Edge driver path
    edge_driver_path = get_edge_driver_path()

    # Initialise Edge options
    edge_options = Options()

    # Configure headless mode if necessary (if provided)
    if headless:
        edge_options.add_argument('--headless')

    # Disable GPU
    edge_options.add_argument('--disable-gpu')

    # Configure window size
    edge_options.add_argument(f'--window-size={window_size}')

    # Configure the download directory if necessary (if provided)
    if download_dir:
        edge_options.add_experimental_option('prefs', {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True,
            'profile.default_content_settings.popups': 0,
        })

    # Configure user profile (if provided)
    if edge_user_profile:
        edge_options.add_argument(f'user-data-dir={edge_user_profile}')

    # Initialise the WebDriver with the configured settings
    print("Initializing WebDriver...")
    service = EdgeService(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    print("WebDriver initialized.")
    
    return driver
