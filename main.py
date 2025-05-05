from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Setup options for Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in headless mode (no UI)
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--no-sandbox")  # Bypass OS security model

# Initialize webdriver
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(20)  # Set page load timeout to 20 seconds

# Search for software developer jobs with specific skills in Delhi, Noida, Gurgaon
search_url = "https://www.linkedin.com/jobs/search/?keywords=software%20developer%20(react%20OR%20node%20OR%20python%20OR%20javascript)&location=Delhi%2C%20Noida%2C%20Gurgaon"
driver.get(search_url)
time.sleep(3)  # Reduced wait time

# Scroll to load more results
for _ in range(3):  # Increased scrolls to get more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Reduced wait time

# Extract job listings
job_cards = driver.find_elements(By.CLASS_NAME, "base-card__full-link")
job_urls = []

# First collect all URLs to avoid stale element references
for job in job_cards:
    try:
        job_url = job.get_attribute("href")
        if job_url:
            job_urls.append(job_url)
    except StaleElementReferenceException:
        continue

# Limit the number of jobs to process to save time
max_jobs_to_process = 30  # Increased from 20 to 30
job_urls = job_urls[:max_jobs_to_process]

print(f"Found {len(job_urls)} job listings to process")
job_data = []

# Now process each URL separately
for i, job_url in enumerate(job_urls):
    try:
        print(f"Processing job {i+1}/{len(job_urls)}")
        driver.get(job_url)
        
        # Use shorter wait times with explicit waits
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "top-card-layout__title"))
            )
        except TimeoutException:
            print(f"Timeout waiting for job details at {job_url}, skipping...")
            continue
        
        # Get job title
        title = driver.find_element(By.CLASS_NAME, "top-card-layout__title").text
        
        # Get company name
        company = driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text
        
        # Check for experience requirement in job description
        job_description = driver.find_element(By.CLASS_NAME, "description__text").text.lower()
        
        # Check if job requires 2+ years of experience
        experience_keywords = ["2+ years", "2 years", "two years", "2-3 years", "2-4 years", "2-5 years"]
        has_required_experience = any(keyword in job_description.lower() for keyword in experience_keywords)
        
        # Check for required skills
        skill_keywords = ["react", "node", "python", "javascript"]
        has_required_skills = any(skill in job_description.lower() for skill in skill_keywords)
        
        # Save job if it has either the required experience OR the required skills
        if has_required_experience or has_required_skills:
            # Get applicants count
            try:
                applicants_element = driver.find_element(By.XPATH, "//span[contains(@class, 'num-applicants')]")
                applicants_text = applicants_element.text
                num_applicants = applicants_text.split()[0].replace(",", "")  # Get the number of applicants
            except:
                num_applicants = "Unknown"
            
            # Identify which skills are mentioned in the job description
            matched_skills = []
            for skill in skill_keywords:
                if skill in job_description.lower():
                    matched_skills.append(skill)
            
            # Add job to our list
            job_data.append({
                "Title": title,
                "Company": company,
                "Link": job_url,
                "Applicants": num_applicants,
                "Skills": ", ".join(matched_skills),
                "Experience": "2+ years" if has_required_experience else "Not specified"
            })
            
            print(f"Found matching job: {title} at {company} (Skills: {', '.join(matched_skills)})")
    
    except Exception as e:
        print(f"Error processing job URL {job_url}: {e}")

# Save results to CSV
with open("jobs.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Company", "Link", "Applicants", "Skills", "Experience"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for job in job_data:
        writer.writerow(job)

print(f"Saved {len(job_data)} jobs to jobs.csv")

# Close the driver after execution
driver.quit()
