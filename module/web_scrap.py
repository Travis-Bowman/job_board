import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

def scrape_job_posting():
    urls = [
        "https://www.gd.com/careers/job-search?state=eyJhZGRyZXNzIjpbXSwiZmFjZXRzIjpbXSwicGFnZSI6MCwid2hhdCI6InNvZnR3YXJlIiwicGFnZVNpemUiOjEwfQ%3D%3D"
    ]

    job_listings = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        postings = soup.find_all(class_="job-posting")

        for post in postings:
            job_title = post.find(class_="job-title").get_text(strip=True)
            job_location = post.find(class_="job-location").get_text(strip=True)
            date_posted = post.find(class_="date_posted").get_text(strip=True)

            job_listings.append({
                "job_title": job_title,
                "job_location": job_location,
                "date_posted": date_posted,
                "url": url
            })

    # Save to CSV
    df = pd.DataFrame(job_listings)
    df.to_csv("job_postings.csv", index=False)
    print("Scraping complete. Data saved to job_postings.csv")

# Schedule the job to run at a specific interval (optional)
# schedule.every(1).hour.do(scrape_job_posting)

# Run the job immediately for testing
scrape_job_posting()

# Uncomment the following lines if you want to schedule the job to run periodically
# while True:
#     schedule.run_pending()
#     time.sleep(1)
