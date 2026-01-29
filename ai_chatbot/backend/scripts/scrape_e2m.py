from rag_service import scrape_and_ingest
import sys

def main():
    url = "https://www.e2msolutions.com/"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    print(f"Starting scraping for: {url}")
    count = scrape_and_ingest(url, depth=2)
    print(f"Successfully ingested {count} chunks.")

if __name__ == "__main__":
    main()
