import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def driver():
    """Setup du driver Firefox (GeckoDriver)."""
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)


    driver.implicitly_wait(10)
    
    yield driver

    driver.quit()

def test_full_scenario(driver):

    unique_user = f"user_{int(time.time())}"

    driver.get(f"{BASE_URL}/register")
    

    driver.find_element(By.NAME, "username").send_keys(unique_user)
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.NAME, "confirm").send_keys("pass")
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    time.sleep(1) 
    
    driver.find_element(By.NAME, "username").send_keys(unique_user)
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    driver.get(f"{BASE_URL}/tasks/new")
    
    driver.find_element(By.NAME, "title").send_keys("Tache Firefox E2E")
    driver.find_element(By.NAME, "description").send_keys("Test sur Firefox")
    driver.find_element(By.NAME, "due_date").send_keys("2025-12-31")
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    time.sleep(1)
    assert "Tache Firefox E2E" in driver.page_source
    assert "Test sur Firefox" in driver.page_source
