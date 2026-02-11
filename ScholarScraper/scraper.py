import serpapi
from serpapi import GoogleSearch

class ScholarScraper:
    def __init__(self, config_dict):
        self.api_key = config_dict['api_key']
        self.author_ids = config_dict['author_ids']
        self.start_year = config_dict['start_year']
        self.current_year = config_dict['current_year']
        self.journals = config_dict['journal_keywords']
        self.confs = config_dict['conf_keywords']
        self.skips = config_dict['skip_keywords']
        self.reports = config_dict['report_keywords']

    def parse_article(self, article):
        pub = article.get("publication", "")
        title = article.get("title", "").lower()
        link = article.get("link", "").lower()
        low_pub = pub.lower()
        
        if any(k in low_pub for k in self.skips): 
            return None

        p_type = "Other"
        
        # Strictly uses keywords from your config.conf
        # Checks against Title, Publication string, and URL Link
        if any(k in low_pub or k in title or k in link for k in self.reports):
            p_type = "Report"
        elif any(k in low_pub or k in title for k in self.confs):
            p_type = "Conference"
        elif any(k in low_pub or k in title for k in self.journals):
            p_type = "Journal"

        pub_year = None
        try:
            year_candidate = pub.split(", ")[-1].strip()
            if year_candidate.isdigit() and len(year_candidate) == 4:
                pub_year = int(year_candidate)
        except:
            pass
            
        return {"type": p_type, "year": pub_year}

    def run(self):
        all_pubs = []
        seen_titles = set() # For deduplication
        
        for aid in self.author_ids:
            search = GoogleSearch({
                "engine": "google_scholar_author",
                "author_id": aid,
                "api_key": self.api_key,
                "sort": "pubdate"
            })
            articles = search.get_dict().get("articles", [])
            
            for art in articles:
                title = art.get("title")
                # Deduplication: Skip if we already found this paper title
                if title.lower() in seen_titles:
                    continue
                
                info = self.parse_article(art)
                if info:
                    # Filter by year range
                    if info['year'] and not (self.start_year <= info['year'] <= self.current_year):
                        continue
                        
                    seen_titles.add(title.lower())
                    all_pubs.append({
                        **info,
                        "title": title,
                        "authors": art.get("authors"),
                        "link": art.get("link")
                    })
        return all_pubs