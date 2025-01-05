from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time

#made by https://github.com/milliyin

def autofiller3(id,password,option,msg,cmsg,teachers):

    # Selenium setup
    service = Service(executable_path="chromedriver.exe")  # Replace with your chromedriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    # Define the URLs
    login_url = "https://portals.au.edu.pk/qec/login.aspx"
    form_url = "https://portals.au.edu.pk/qec/p10.aspx"



    # Function to execute script on the page
    def execute_script(option, instructor_message, course_message):
        script = f"""
        function TeacherEvaluation() {{
            let option = {option}; // Rating option passed from Python
            let InstructorMessage = "{instructor_message}"; // Instructor feedback passed from Python
            let CourseMessage = "{course_message}"; // Course feedback passed from Python

            let teacher = document.querySelector("#ctl00_ContentPlaceHolder2_ddlTeacher");
            let course = document.querySelector("#ctl00_ContentPlaceHolder2_ddlCourse");
            
            if (teacher && teacher.length === 0) {{
                console.log("Completed. Returning to home..");
                let backButton = document.querySelector("#ctl00_ContentPlaceHolder2_linkBack");
                if (backButton) {{
                    backButton.click();
                }}
                return; // Exit the function after navigating
            }}
            
            if (teacher && teacher.options.length > 1) {{
                teacher.options[1].selected = true; // Selecting the first teacher
                setTimeout(() => __doPostBack('ctl00$ContentPlaceHolder2$ddlTeacher', ''), 0); // Trigger PostBack for teacher selection
            }}

            try {{
                if (course && course.options.length <= 1) {{
                    course.options[0].selected = true; // Selecting the only available course
                }}
            }} catch (error) {{
                console.log("Course dropdown exception: ", error);
            }}

            let selector = "#ctl00_ContentPlaceHolder2_q{{VAR}}_{{OPTION}}";
            for (let i = 1; i <= 16; i++) {{
                let curr = selector.replace("{{VAR}}", i).replace("{{OPTION}}", option);
                let element = document.querySelector(curr);
                if (element) {{
                    element.click(); // Ensure the element exists before clicking
                }}
            }}

            // Set feedback messages
            let instructorBox = document.querySelector("#ctl00_ContentPlaceHolder2_q20");
            if (instructorBox) {{
                instructorBox.value = InstructorMessage;
            }}
            let courseBox = document.querySelector("#ctl00_ContentPlaceHolder2_q21");
            if (courseBox) {{
                courseBox.value = CourseMessage;
            }}

            // Save the evaluation
            let saveButton = document.querySelector("#ctl00_ContentPlaceHolder2_btnSave");
            if (saveButton) {{
                saveButton.click(); // Ensure the save button exists before clicking
            }}
        }}

        // Execute the function
        TeacherEvaluation();
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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_txt_regid"))).send_keys(id)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_txt_password").send_keys(password)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_btnAccountlogin").click()

        # Navigate to form page and execute script multiple times
        for _ in range(teachers):  # Adjust the range for the desired number of executions
            driver.get(form_url)
            execute_script(option, msg,cmsg)
            handle_alert()  # Handle any alert that may appear
            time.sleep(5)  # Add a delay between executions to prevent issues

    finally:
        driver.quit()
