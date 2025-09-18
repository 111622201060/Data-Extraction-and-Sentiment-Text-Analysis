# data_extractor.py
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_text_from_url(url):
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    driver = None
    try:
        print(f"⏳ Launching browser for {url.split('/')[-2]}...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Add random delay before loading
        delay = random.uniform(1, 2)
        time.sleep(delay)

        driver.get(url)

        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Scroll to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Try to find article content
        selectors = [
            '.td-post-content',
            '.tdb_single_content',
            '.entry-content',
            '.post-content',
            'article',
            'main'
        ]

        article_text = ""
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for elem in elements:
                        # Remove unwanted elements
                        for tag in ['script', 'style', '.code-block', '.wp-block-image', 'figcaption', '.td-post-featured-image']:
                            for unwanted in elem.find_elements(By.CSS_SELECTOR, tag):
                                driver.execute_script("arguments[0].remove();", unwanted)
                        text = elem.text.strip()
                        if len(text) > 100:  # Only accept if meaningful content
                            article_text += text + "\n"
                    if article_text:
                        break
            except:
                continue

        # Fallback: get all text from body
        if not article_text.strip():
            body = driver.find_element(By.TAG_NAME, "body")
            article_text = body.text.strip()

        # Final cleanup
        article_text = ' '.join(article_text.split())
        if len(article_text) < 50:
            print(f"⚠️  Very little content extracted from {url}")
            return ""

        # Save to file
        url_id = url.rstrip('/').split('/')[-1]
        filename = f"extracted_articles/{url_id}.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article_text)

        print(f"✅ Successfully extracted {len(article_text)} characters")
        return article_text

    except Exception as e:
        print(f"❌ Browser error for {url}: {str(e)}")
        return ""
    finally:
        if driver:
            driver.quit()