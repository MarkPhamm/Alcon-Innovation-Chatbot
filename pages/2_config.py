import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SCRAPER_API_URL = os.getenv('SCRAPER_API_URL')

# Predefined URLs
URL_OPTIONS = {
    "JnJ": "https://www.jnj.com/media-center/press-releases/johnson-johnson-rolls-out-new-tecnis-odyssey-next-generation-intraocular-lens-offering-cataract-patients-precise-vision-at-every-distance-in-any-lighting",
    "RXSight": "https://www.centerforeyes.com/rxsight/",  # Example link
    "Zeiss IOLs": "https://www.zeiss.com/meditec-ag/en/media-news/press-releases/2024/zeiss-at-aao.html"  # Example link
}

# Function to save content as markdown
def save_as_markdown(content, filename):
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    # Save the content to a markdown file
    with open(os.path.join('data', filename), 'w', encoding='utf-8') as f:
        f.write(content)

# Function to scrape website
def scrape_website(url):
    payload = {'api_key': API_KEY, 'url': url}
    response = requests.get(SCRAPER_API_URL, params=payload)
    
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to scrape the website. Status code: {response.status_code}")
        return ""
    
if SCRAPER_API_URL:  # Check if the SCRAPER_API_URL is valid
    print(scrape_website(URL_OPTIONS["JnJ"]))
else:
    st.error("SCRAPER_API_URL is not set. Please check your environment variables.")

# # Streamlit UI
# st.title("Innov8 AI Platform")

# # Multi-select dropdown to choose websites
# selected_sites = st.multiselect("Select Websites to Scrape", options=list(URL_OPTIONS.keys()))

# # Step 1: Scrape the Website(s)
# if st.button("Scrape Selected Websites"):
#     if selected_sites:
#         st.write("Scraping the selected websites...")
        
#         scraped_content = ""
#         # Loop through selected sites and scrape each
#         for site in selected_sites:
#             url = URL_OPTIONS[site]
#             site_content = scrape_website(url)
#             if site_content:
#                 cleaned_content = clean_body_content(site_content)
#                 scraped_content += f"\n\n--- Content from {site} ---\n\n" + cleaned_content
        
#         # Store the cleaned content in Streamlit session state
#         if scraped_content:
#             st.session_state.scraped_content = scraped_content
            
#             # Save the scraped content as markdown
#             save_as_markdown(scraped_content, 'scraped_content.md')
            
#             # Display the cleaned content in an expandable text box
#             with st.expander("View Cleaned Content"):
#                 st.text_area("Cleaned Content", scraped_content, height=300)
