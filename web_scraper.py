# web_scraper.py

import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

def scrape_website(source):
    """
    استخراج الأخبار من المواقع التي لا تدعم RSS
    """
    articles = []
    try:
        logger.info(f"Scraping website: {source['name']} - {source['url']}")
        response = requests.get(source['url'], timeout=30)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        if source['name'] == 'kooora.com':
            articles = _scrape_kooora(soup, source)
        else:
            # Generic scraping logic for other sites
            for element in soup.find_all('div', class_='article-item'): # Example class, adjust as needed
                title_element = element.find('h2', class_='article-title')
                link_element = element.find('a', class_='article-link')
                summary_element = element.find('p', class_='article-summary')
                image_element = element.find('img', class_='article-image')

                title = title_element.get_text().strip() if title_element else ''
                link = link_element.get('href') if link_element else ''
                summary = summary_element.get_text().strip() if summary_element else ''
                image_url = image_element.get('src') if image_element else ''

                if link and not link.startswith(('http://', 'https://')):
                    link = urljoin(source['url'], link)
                if image_url and not image_url.startswith(('http://', 'https://')):
                    image_url = urljoin(source['url'], image_url)

                if title and link:
                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'published_date': datetime.now(), # Or extract from page if available
                        'source_name': source['name'],
                        'image_url': image_url
                    })
    except requests.exceptions.RequestException as e:
        logger.error(f"Error scraping {source['name']}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping {source['name']}: {e}")
    return articles

def _scrape_content_with_config(soup, scraping_config):
    """
    Generic function to scrape article content based on a configuration.
    """
    try:
        # Remove unwanted elements first
        unwanted_selectors = scraping_config.get('unwanted_selectors', [])
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()

        # Find the main article content
        content_selectors = scraping_config.get('content_selectors', [])
        article_content = None
        for selector in content_selectors:
            article_content = soup.select_one(selector)
            if article_content:
                break

        # Fallback to finding paragraphs if no specific content container is found
        if not article_content:
            main_divs = soup.find_all('div')
            for div in main_divs:
                paragraphs = div.find_all('p')
                if len(paragraphs) >= 3:  # Heuristic: a div with at least 3 paragraphs is likely the content
                    article_content = div
                    break

        if article_content:
            # Remove unwanted elements from the content
            for unwanted in article_content(['script', 'style', 'nav', 'aside', 'header', 'footer']):
                unwanted.decompose()

            # Remove unwanted interactive links
            for link in article_content.find_all('a'):
                if any(keyword in link.get_text().lower() for keyword in ['قراءة', 'المزيد', 'تابع', 'شاهد', 'اقرأ']):
                    link.decompose()

            # Extract and clean the text
            text = article_content.get_text(separator='\n', strip=True)
            return text if text else None

        return None

    except Exception as e:
        logger.error(f"Error scraping content with config: {e}")
        return None

def scrape_article_content(url, source):
    """
    Extracts article content from a URL using a generic scraping function.
    """
    try:
        logger.info(f"Scraping article content from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Use the generic scraper with the source's specific configuration
        scraping_config = source.get('scraping_config', {})
        return _scrape_content_with_config(soup, scraping_config)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching article content from {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping article content from {url}: {e}")
        return None