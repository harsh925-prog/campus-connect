from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

class TestCampusConnect:
    def setup_method(self):
        self.driver = webdriver.Chrome()  # Make sure ChromeDriver is installed
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:5000"
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_homepage_load(self):
        """Test that homepage loads correctly"""
        self.driver.get(self.base_url)
        assert "Campus Connect" in self.driver.title
        assert self.driver.find_element(By.TAG_NAME, "h1").text == "Campus Connect"
    
    def test_user_registration(self):
        """Test user registration flow"""
        self.driver.get(f"{self.base_url}/register")
        
        # Fill registration form
        self.driver.find_element(By.NAME, "name").send_keys("Selenium Test User")
        self.driver.find_element(By.NAME, "email").send_keys("selenium@test.com")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.NAME, "major").send_keys("Computer Science")
        self.driver.find_element(By.NAME, "skills").send_keys("Selenium, Testing")
        
        # Submit form
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Check for success message or redirect
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login") or EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
    
    def test_user_login(self):
        """Test user login flow"""
        self.driver.get(f"{self.base_url}/login")
        
        # Fill login form (using pre-registered test user)
        self.driver.find_element(By.NAME, "email").send_keys("test@student.com")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        
        # Submit form
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verify login success - should redirect to dashboard
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        assert "Dashboard" in self.driver.page_source

if __name__ == "__main__":
    # Run Selenium tests
    test_class = TestCampusConnect()
    test_class.setup_method()
    
    try:
        test_class.test_homepage_load()
        print("✓ Homepage test passed")
        
        test_class.test_user_login()
        print("✓ Login test passed")
        
    finally:
        test_class.teardown_method()