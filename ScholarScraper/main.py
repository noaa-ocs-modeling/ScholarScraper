import configparser
from collections import defaultdict
from scraper import ScholarScraper

def main():
    config = configparser.ConfigParser()
    config.read('config.conf')
    
    settings = {
        "api_key": config.get('SERPAPI', 'api_key'),
        "author_ids": [i.strip() for i in config.get('SETTINGS', 'author_ids').split(',')],
        "start_year": config.getint('SETTINGS', 'start_year'),
        "current_year": config.getint('SETTINGS', 'current_year'),
        "journal_keywords": [k.strip().lower() for k in config.get('KEYWORDS', 'journals').split(',')],
        "conf_keywords": [k.strip().lower() for k in config.get('KEYWORDS', 'conferences').split(',')],
        "skip_keywords": [k.strip().lower() for k in config.get('KEYWORDS', 'preprints').split(',')],
        "report_keywords": [k.strip().lower() for k in config.get('KEYWORDS', 'reports').split(',')],
        "output_file": config.get('SETTINGS', 'output_file')
    }

    scraper = ScholarScraper(settings)
    print("🚀 Starting search and deduplication...")
    results = scraper.run()

    organized_data = defaultdict(lambda: defaultdict(list))
    for p in results:
        cat = p['type'].upper()
        year = str(p['year']) if p.get('year') else "Unknown Year"
        organized_data[cat][year].append(p)

    output_path = settings['output_file']
    categories_to_print = ["JOURNAL", "CONFERENCE", "REPORT", "OTHER"]

    with open(output_path, 'w', encoding='utf-8') as f:
        for cat_name in categories_to_print:
            if cat_name in organized_data:
                f.write("====================================\n")
                f.write(f"CATEGORY: {cat_name} PUBLICATIONS\n")
                f.write("====================================\n")
                
                years = sorted([y for y in organized_data[cat_name].keys() if y.isdigit()], reverse=True)
                if "Unknown Year" in organized_data[cat_name]:
                    years.append("Unknown Year")

                for yr in years:
                    f.write("--------------------\n")
                    f.write(f"Year: {yr}\n")
                    for paper in organized_data[cat_name][yr]:
                        f.write(f"  Title: {paper['title']}\n")
                        f.write(f"  Authors: {paper.get('authors', 'Not Listed')}\n")
                        f.write(f"  {paper['link']}\n") # No "Link:" prefix
                
                f.write("--------------------\n\n")
    
    print(f"✅ Success! Report saved to {output_path}")

if __name__ == "__main__":
    main()