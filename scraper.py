import string
import requests
import os
import shutil

from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_resource(url, filename):
    """Downloads the content at specified URL to a file."""
    try:
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Failed to retrieve {url}: {e}')
        return

    if not response.content:
        print(f'No content to download from {url}')
        return

    try:
        with open(filename, 'wb') as raw_page:
            raw_page.write(response.content)
    except Exception as e:
        print(f'Failed to save {filename}: {e}')
        return


def get_article_link_and_description(html_resource):
    """Parses HTML to find and return article link and description."""
    try:
        soup = BeautifulSoup(html_resource, 'html.parser')
    except Exception as e:
        print(f'Failed to parse HTML: {e}')
        return None, None

    anchor = soup.find('a', {'data-track-action': 'view article'})
    if anchor is not None:
        link = anchor['href']
        description = anchor.text
        return link, description
    return None, None


def save_as_textfile(url, tag, attributes):
    """Saves article content from URL to a text file."""
    try:
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Failed to retrieve {url}: {e}')
        return

    if not response.content:
        print(f'No content to download from {url}')
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f'Failed to parse HTML: {e}')
        return

    title = soup.find('title').text
    resource = soup.find(tag, attributes)
    if resource is not None:
        filename = title_to_filename(title)
        byte_content = resource.text.encode('utf-8')
        try:
            with open(filename, 'wb') as file:
                file.write(byte_content)
        except Exception as e:
            print(f'Failed to save {filename}: {e}')
            return


def search_articles(absolute_url, html_file, article_type):
    """Searches for articles of a specified type in the HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    except Exception as e:
        print(f'Failed to open or parse {html_file}: {e}')
        return

    # Iterate through all articles, filter by type, and save to text files
    articles = soup.find_all('article')
    for article in articles:
        article_type_span = article.find('span', {'data-test': 'article.type'})
        if article_type_span is not None:
            current_article_type = article_type_span.text
            if current_article_type == article_type:
                relative_link, _ = get_article_link_and_description(str(article))
                if relative_link:
                    full_url = urljoin(absolute_url, relative_link)
                    save_as_textfile(full_url, 'p', {'class': 'article__teaser'})


def title_to_filename(title):
    """Converts article title to a filename-friendly format."""
    title_no_punctuation = title.translate(str.maketrans('', '', string.punctuation))
    words = title_no_punctuation.split()
    return f'{"_".join(words)}.txt'


def request_page_count():
    """Prompts user for the number of pages to download and validates input."""
    number_of_pages = input('Enter the number of pages to download: ')
    while not number_of_pages.isdigit():
        number_of_pages = input('Invalid input. Enter the number of pages to download: ')
    return int(number_of_pages)


def extract_and_save_articles(url, pages_count, article_type):
    """Processes and saves articles from multiple pages of a specified type."""
    html_filename = 'source.html'
    for i in range(pages_count):
        dir_name = f'Page_{i + 1}'
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        os.chdir(dir_name)
        link = f'{url}&page={i + 1}'
        download_resource(link, html_filename)
        search_articles(link, html_filename, article_type)
        os.chdir('..')
    print('Saved all articles.')


def main():
    journal_url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    pages_to_download = request_page_count()
    type_of_article = input('Enter the type of article (e.g., News, Editorial, etc.): ')
    extract_and_save_articles(journal_url, pages_to_download, type_of_article)


if __name__ == "__main__":
    main()
