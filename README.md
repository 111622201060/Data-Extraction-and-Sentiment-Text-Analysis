# Blackcoffer Text Analysis Assignment Submission

## 🧠 How I Approached the Solution

I built a robust, end-to-end Python pipeline to fulfill all requirements in `Objective.docx`:

1. **Data Extraction**:
   - Used **Selenium WebDriver** (not `requests`/`BeautifulSoup`) to extract article text from `insights.blackcoffer.com`.
   - Why? The target website blocks automated requests with 403 Forbidden errors and SSL certificate issues. Selenium simulates a real browser, bypassing these protections.
   - Extracted **only article title and body text** by targeting CSS selectors like `.td-post-content`, `article`, and `main`, while removing scripts, styles, ads, and footers.
   - Saved each article as `<URL_ID>.txt` in the `extracted_articles/` folder (e.g., `Netclan20241017.txt`).

2. **Text Analysis**:
   - Loaded **stop words** from `resources/StopWords/` and removed them from analysis.
   - Created **positive/negative word dictionaries** from `resources/MasterDictionary/`, excluding any stop words.
   - Computed **all 13 variables** as defined in `Text Analysis.docx`:
     - **Sentiment**: Positive Score, Negative Score, Polarity Score, Subjectivity Score
     - **Readability**: Avg Sentence Length, Percentage of Complex Words, Fog Index, Avg Words per Sentence
     - **Word Stats**: Complex Word Count, Word Count, Syllable per Word, Personal Pronouns, Avg Word Length
   - Used **NLTK** for sentence and word tokenization (with `punkt_tab` for Python 3.12+ compatibility).
   - Implemented **syllable counting** following spec: ignore 'es', 'ed' endings.
   - Excluded country name **“US”** when counting personal pronouns.

3. **Output**:
   - Saved results in `output/Output Data Structure.xlsx` with all 147 rows and 13 analysis columns in the exact order specified.
   - Handled duplicate URLs gracefully (same article → same analysis → same output values).

---

## ▶️ How to Run the .py File to Generate Output

Follow these steps to reproduce my results:

### 1. Prerequisites
- Python 3.8 or higher
- Google Chrome browser installed (required for Selenium)

### 2. Install Dependencies
Open terminal in the project folder and run:
```bash
pip install selenium webdriver-manager pandas openpyxl nltk