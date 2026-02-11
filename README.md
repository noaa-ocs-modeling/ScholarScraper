# ScholarScraper
A Python tool to automatically track, filter, and categorize research publications from Google Scholar for a specific list of authors.


## Project Structure

- **`main.py`**: The entry point. It loads `config.json`, runs the scraper, and saves the final text report.
- **`scraper.py`**: The core logic engine. It handles API requests, filters by year, and categorizes papers based on your keywords.
- **`config.json`**: Your settings file (API keys, Author IDs, and keyword lists).
- **`requirements.txt`**: Contains the necessary Python libraries for the project.

---

## Setup Instructions

### 1. Get your SerpApi Key
1. Sign up at [SerpApi.com](https://serpapi.com/).
2. Copy your **API Key** from your private dashboard.

### 2. Find Google Scholar Author IDs
1. Go to [Google Scholar](https://scholar.google.com/).
2. Search for an author and click their profile.
3. Look at the URL. The ID is the string of characters after `user=`. 
   - *Example:* `https://scholar.google.com/citations?user=h1AbC2_AAAAJ` → The ID is `h1AbC2_AAAAJ`.

### 3. Installation
Open your terminal in this folder and install the required library:
```bash
pip install -r requirements.txt
```

### 4. Configuration
Open config.json and fill in your specific details:

api_key: Your SerpApi key.

author_ids: A list of IDs (e.g., ["ID1", "ID2"]).

start_year / current_year: The range of publications to fetch.


## How to Run
Execute the program from your terminal:

```bash
python main.py
```

**Note: Every page of articles and every DOI search uses 1 SerpApi credit. Monitor your usage at SerpApi.com.**
