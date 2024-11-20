import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# API configuration
API_KEY = os.getenv('API_KEY')
SCRAPER_API_URL = os.getenv('SCRAPER_API_URL')

# Predefined URLs
URL_OPTIONS = {
    "JnJ": "https://www.jnj.com/media-center/press-releases/johnson-johnson-rolls-out-new-tecnis-odyssey-next-generation-intraocular-lens-offering-cataract-patients-precise-vision-at-every-distance-in-any-lighting",
    # "RXSight": "https://www.centerforeyes.com/rxsight/",  # Example link
    # "Zeiss IOLs": "https://www.zeiss.com/meditec-ag/en/media-news/press-releases/2024/zeiss-at-aao.html"  # Example link
}

# Function to clean HTML content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    # Remove all blank lines
    cleaned_content = "\n".join(
        line for line in cleaned_content.splitlines() if line
    )

    return cleaned_content

# Function to scrape website
def scrape_website(url):
    payload = {'api_key': API_KEY, 'url': url}
    response = requests.get(SCRAPER_API_URL, params=payload)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to scrape the website. Status code: {response.status_code}")
        return ""

def remove_unwanted_content(content):
    # Define unwanted content patterns
    unwanted_patterns = [
        "Skip to content",
        "Business websites",
        "J&J Innovative Medicine",
        "J&J MedTech",
        "US • English",
        "Choose your country or region",
        "Latest news",
        "Innovation",
        "Caring & giving",
        "Personal stories",
        "Health & wellness",
        "Our Company",
        "Discover J&J",
        "Our Credo",
        "Our Leadership",
        "Code of Business Conduct",
        "Corporate reports",
        "Diversity, Equity & Inclusion",
        "ESG Policies & Positions",
        "Innovation at J&J",
        "Uniting science and technology",
        "Office of the Chief Medical Officer",
        "Veterans, military & military families",
        "Innovative Medicine",
        "MedTech",
        "Our societal impact",
        "Global Health Equity",
        "Global environmental sustainability",
        "Suppliers",
        "Responsible supply base",
        "Supplier-enabled innovation",
        "Supplier resources",
        "Our heritage",
        "Careers",
        "Life at J&J",
        "Diversity, Equity and Inclusion",
        "Career areas of impact",
        "Students",
        "Re-Ignite Program",
        "Contract & freelance partner opportunities",
        "Career stories",
        "Investors",
        "Pharmaceutical pipeline",
        "ESG resources",
        "Investor fact sheet",
        "Media Center",
        "Menu",
        "Search Query",
        "Submit Search",
        "Clear",
        "Dictate search request",
        "Search Results",
        "No Results",
        "Recently Viewed",
        "Listening...",
        "Sorry, I don't understand. Please try again",
        "Show Search",
        "Home",
        "/",
        "JNJ.com",
        "NewPharm.com",
        "China",
        "中国人",
        "France",
        "Français",
        "India",
        "English",
        "Japan",
        "日本",
        "Switzerland",
        "Deutsch",
        "United Kingdom",
        " at J&J",
        "Announcements",
        "Our commitments",
        "Environment, social, governance",
        "Sustainability",
        "Get in touch",
        "Contact us",
        "youtube",
        "facebook",
        "twitter",
        "linkedin",
        "This site is governed solely by applicable U.S. laws and governmental regulations. Please see our",
        "Privacy Policy",
        "Use of this site constitutes your consent to application of such laws and regulations and to our",
        "Legal Notice",
        "Cookie Policy",
        "You should view the",
        "News",
        "section and the most recent SEC Filings in the Investor section in order to receive the most current information made available by Johnson & Johnson Services, Inc.",
        "Contact us",
        "with any questions or search this site for more information.",
        "Do Not Sell or Share My Personal Information",
        "Limit the Use of My Sensitive Personal Information",
        "© 2024 Johnson & Johnson Services, Inc.",
        "Terms of Use",
        "Customize Cookie Settings",
        "Back to top"
    ]
    
    for pattern in unwanted_patterns:
        content = content.replace(pattern, "")
    
    # Remove lines that contain only numbers or sequences of numbers separated by commas
    content = "\n".join(
        line for line in content.splitlines() if not re.match(r'^\d+(,\d+)*$', line) and line.strip()
    )
    
    return content
