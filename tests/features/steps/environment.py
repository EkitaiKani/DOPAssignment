import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Constants
WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def setup_chrome_options():
    """Configure Chrome options for headless mode, no GPU, etc."""
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    return chrome_options

def setup_chrome_driver():
    """Initialize Chrome WebDriver with options."""
    try:
        chrome_options = setup_chrome_options()
        # ChromeDriver is already in PATH thanks to setup-chromedriver action
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome driver: {str(e)}")
        logger.error("Please ensure ChromeDriver is properly installed and in PATH")
        raise

def before_all(context):
    """Initial setup for the test run."""
    context.config.setup_logging()
    logger.info("Setting up environment before all scenarios")

def before_scenario(context, scenario):
    """Initialize browser before each scenario."""
    try:
        if not hasattr(context, 'driver'):
            logger.info(f"Initializing WebDriver for scenario: {scenario.name}")
            context.driver = setup_chrome_driver()
            context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)
            logger.info(f"WebDriver initialized for scenario: {scenario.name}")
        else:
            logger.warning("Driver already initialized. Skipping initialization.")
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver for scenario: {scenario.name}, error: {str(e)}")
        raise

def after_scenario(context, scenario):
    """Clean up after each scenario."""
    try:
        if hasattr(context, 'driver'):
            context.driver.quit()
            delattr(context, 'driver')
            logger.info(f"WebDriver cleaned up for scenario: {scenario.name}")
    except Exception as e:
        logger.error(f"Error during WebDriver cleanup for scenario {scenario.name}: {str(e)}")

def after_all(context):
    """Final cleanup after all scenarios."""
    logger.info("Test execution completed.")