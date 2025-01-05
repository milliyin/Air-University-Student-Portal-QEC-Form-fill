from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time

#made by https://github.com/milliyin

def autofiller2(txt_regid,txt_password,option,InstructorMessage,courses):
    # Selenium setup
    service = Service(executable_path="chromedriver.exe")  # Replace with your chromedriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    # Define the URLs
    login_url = "https://portals.au.edu.pk/qec/login.aspx"
    form_url = "https://portals.au.edu.pk/qec/p1.aspx"



    # Function to execute script on the page
    def execute_script(option, instructor_message):
        script = f"""
        function CourseEvaluation() {{
            let option = {option}; // A = 1, B = 2, C = 3, D = 4
            let baseOpts = document.querySelector("#ctl00_ContentPlaceHolder2_cmb_courses");
            
            if (baseOpts && baseOpts.length === 1) {{ // Check if baseOpts exists and has only one option
                console.log("Completed. Returning to home..");
                let backButton = document.querySelector("#ctl00_ContentPlaceHolder2_linkBack");
                if (backButton) {{
                    backButton.click();
                }}
                return; // Exit the function after navigating
            }}
            
            if (baseOpts && baseOpts.options.length > 1) {{
                baseOpts.options[1].selected = true; // Selecting the first available value
            }}
            
            let selector = "#ctl00_ContentPlaceHolder2_q{{VAR}}_{{OPTION}}";
            for (let i = 1; i <= 12; i++) {{
                let curr = selector.replace("{{VAR}}", i).replace("{{OPTION}}", option);
                let element = document.querySelector(curr);
                if (element) {{
                    element.click(); // Ensure the element exists before clicking
                }}
            }}
            
            let saveButton = document.querySelector("#ctl00_ContentPlaceHolder2_btnSave");
            if (saveButton) {{
                saveButton.click(); // Ensure the save button exists before clicking
            }}
        }}
        
        // Execute the function
        CourseEvaluation();
        """
        driver.execute_script(script)
        print("Script executed successfully.")


    # Function to handle alerts
    def handle_alert():
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"Alert detected: {alert.text}")
            alert.accept()  # Accept the alert
            print("Alert handled.")
        except NoAlertPresentException:
            print("No alert present.")

    # Start Selenium browser
    try:
        # Open login page
        driver.get(login_url)

        # Fill in login details
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_txt_regid"))).send_keys(txt_regid)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_txt_password").send_keys(txt_password)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_btnAccountlogin").click()

        # Navigate to form page and execute script multiple times
        for _ in range(courses):  # Adjust the range for the desired number of executions
            driver.get(form_url)
            execute_script(option, InstructorMessage)
            handle_alert()  # Handle any alert that may appear
            time.sleep(5)  # Add a delay between executions to prevent issues

    finally:
        driver.quit()
