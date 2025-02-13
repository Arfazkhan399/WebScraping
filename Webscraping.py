import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Chrome WebDriver with headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser
# options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
# options.add_argument("--disable-ssl-errors")  # Disable SSL errors
# options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")  # Spoof user agent
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List of stock symbols to scrape
stocks = ["AAPL", "TSLA", "AMZN", "GOOGL", "MSFT"]

# Yahoo Finance URL template
base_url = "https://finance.yahoo.com/quote/"

# List to store stock data
stock_data = []

# Loop through each stock and scrape data
for stock in stocks:
    url = f"{base_url}{stock}"
    driver.get(url)
    # input("Press Enter to close the browser...")
    try:
        # Wait for stock price to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'fin-streamer[data-field="regularMarketPrice"]'))
        )

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract stock price
        price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        price = price_tag.text if price_tag else "N/A"

        # Extract market change
        change_tag = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"})
        change = change_tag.text if change_tag else "N/A"

        # Store data in list
        stock_data.append({"Stock": stock, "Price ($)": price, "Change (%)": change})

        print(f"Scraped {stock}: ${price} ({change})")

    except Exception as e:
        print(f"Error scraping {stock}: {e}")

# Close the browser
driver.quit()

# Save data to CSV
df = pd.DataFrame(stock_data)
df.to_csv("stock_prices.csv", index=False)

print("\n✅ Stock data saved to stock_prices.csv")
