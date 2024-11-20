import requests
from bs4 import BeautifulSoup
import scraper

import os,sys
# Function to scrape a specified number of recent press releases from JnJ
def scrape_jnj_articles(num_articles=1):
    url = "https://www.jnj.com/media-center/press-releases"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to scrape the JnJ press releases. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Update the class name based on the actual HTML structure
    press_releases = soup.find_all("h3", class_="PagePromo-title")[:num_articles]

    if not press_releases:
        print("No press releases found. Please check the class name or the website structure.")
        return None

    scraped_content = []
    seen_lines = set()  # Track seen lines to avoid duplicates
    for release in press_releases:
        release_link = release.find("a")
        release_url = release_link['href']
        if not release_url.startswith("http"):
            release_url = f"https://www.jnj.com{release_url}"
        print(f"Scraping URL: {release_url}")  # Debug: Print each URL being scraped
        
        release_title = release_link.get_text(strip=True)
        release_content = scraper.scrape_website(release_url)
        cleaned_content = scraper.clean_body_content(release_content)
        
        # Remove unwanted content
        cleaned_content = scraper.remove_unwanted_content(cleaned_content)
        
        # Process content to remove duplicates and reduce blank lines
        processed_content = []
        for line in cleaned_content.splitlines():
            if line not in seen_lines:
                seen_lines.add(line)
                if line.strip():  # Only add non-blank lines
                    processed_content.append(line)
                elif processed_content and processed_content[-1]:  # Add a single blank line if the last line was not blank
                    processed_content.append("")

        scraped_content.append(f"\n\n## {release_title}\n\n" + "\n".join(processed_content))

    return "\n".join(scraped_content)

def main():
    jnj_results = scrape_jnj_articles(num_articles=1)

    # Save results to a text file in the data folder
    if jnj_results:
        with open("data/jnj.txt", "w", encoding="utf-8") as file:
            file.write(jnj_results)
            print("Results saved to data/jnj.txt")

if __name__ == "__main__":
    main()