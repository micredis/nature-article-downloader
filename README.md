# Nature Article Downloader 

A Python script to download and save articles from the journal Nature based on user input for a specific educational task. This non-CLI script navigates through a specified number of pages, identifies articles of the specified type, and saves them as text files in a structured directory format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Beautiful Soup 4
- requests

Install the required packages using pip:

```bash
  pip3 install beautifulsoup4 requests
```

### Running the Script

1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the script using Python:
```bash
  python3 scraper.py
```

Follow the prompts to specify the number of pages to download and the type of article to look for.

## Project Structure

- **`download_resource`**: Downloads the HTML content of a specified URL.
- **`get_article_link_and_description`**: Parses HTML to find and return article link and description.
- **`save_as_textfile`**: Saves article content from URL to a text file.
- **`search_articles`**: Searches for articles of a specified type in the HTML file.
- **`title_to_filename`**: Converts article title to a filename-friendly format.
- **`request_page_count`**: Prompts user for the number of pages to download and validates input.
- **`extract_and_save_articles`**: Processes and saves articles from multiple pages of a specified type.
- **`main`**: The entry point of the script, gathering user input and initiating the article downloading process.

## Disclaimer

This script is created for an educational task and is designed to work specifically with the journal Nature's article listing. It's not intended as a universal solution for downloading articles from other websites or for bypassing any restrictions on access to content. The script operates within the confines of the task description and is shared for educational purposes only.
