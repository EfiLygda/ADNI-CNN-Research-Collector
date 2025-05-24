"""
Querying the ArXiv API and export the returned papers' title, author names, abstract and URL
into two separate files: a CSV file and a TXT file.

Using: https://info.arxiv.org/help/api/basics.html
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Max number of papers for the query
MAX_PAPERS = 100

def search_arxiv(query):
    """
    Function for querying the ArXiv API. It also outputs the results to two files (CSV and TXT) and in the console
    :param query: str, with the query
    :return: dict, with the papers' details
    """

    # The base url for querying ArXiv
    base_url = "http://export.arxiv.org/api/query?"

    # Using "all" for searching the keywords in the title and abstract of the paper
    search_query = f"all:{query}"

    # Starting from the first result
    start = 0

    # The url used for querying (the results are sorted in descending order according to their relevance)
    url = f"{base_url}search_query={search_query}&start={start}&max_results={MAX_PAPERS}&sortBy=relevance&sortOrder=descending"

    # Requesting the url
    response = requests.get(url)

    # Converting the returned HTML to XML
    soup = BeautifulSoup(response.text, 'xml')

    # Find all elements identified as entry
    entries = soup.find_all('entry')

    # Initialize a dictionary for the titles, author names, abstracts and URL
    # This dictionary will later be used for constructing the data frame to be exported as csv
    columns = ['titles', 'authors', 'abstracts', 'links']
    data = {col: [] for col in columns}

    # Opening the txt file for writing
    with open(f'arxiv_papers_max_{MAX_PAPERS}.txt', 'w', encoding='utf-8') as f:

        # Writing the total number of papers found during the querying
        f.write(100 * '-' + '\n')
        f.write(f'ArXiv: {len(entries)} entries' + '\n')

        # The same but for the console
        print(100 * '-')
        print(f'ArXiv: {len(entries)} entries')

        for i, entry in enumerate(entries):

            # For each paper finding the title, authors' name, abstract and URL of the current paper
            # and appending it to the respective list in the dictionary

            # Retrieving all the ArXiv urls for each paper

            # Returns list with elements as <id>URL</id> -> needs cleaning
            ids = entry.find_all('id')

            # If a URL was found -> getting the URL as the text of the element
            if ids: ids = [i.text for i in ids][0]
            data['links'].append(ids)

            # Same as before finding the title element, getting its text and cleaning it
            title = entry.find('title').text.strip().replace('\n', '')
            data['titles'].append(title)

            # Finding all the authors' elements, getting their text and cleaning them
            authors = [author.text.strip() for author in entry.find_all('author')]
            data['authors'].append(authors)

            # Getting the current abstract
            summary = entry.find('summary').text
            data['abstracts'].append(summary)

            # Print the results in the console
            print(100 * '-')
            print(f'{i + 1}) Title: {title}', end=2 * '\n')
            print(f'Authors: {" ; ".join(authors)}', end=2 * '\n')
            print(f'Summary:\n{summary}', end=2 * '\n')
            print(f'Link:\n{ids}')
            print(100 * '-', end=2 * '\n')

            # Write the results in the txt file
            f.write(100 * '-' + '\n')
            f.write(f'{i+1}) Title: {title}' + 2*'\n')
            f.write(f'Authors: {" ; ".join(authors)}' + 2*'\n')
            f.write(f'Summary:\n{summary}' + 2*'\n')
            f.write(f'Link:\n{ids}' + '\n')
            f.write(100 * '-' + '\n')

    return data

if __name__ == '__main__':

    # The query used:
    # KEYWORDS  :   "ADNI", "MRI", "CNN", "classification"
    # WHERE     :   Title and Abstract of the paper
    query = 'ADNI AND MRI AND CNN AND classification'

    # Querying the ArXiv API
    ax = search_arxiv(query)

    # Make the data frame with the details
    df = pd.DataFrame(ax)

    # Exporting the data to a csv file
    df.to_csv('arxiv_papers_details.csv', index=False)





