"""
Querying the PubMed API and export the returned papers' title, author names, abstract and URL
into two separate files: a CSV file and a TXT file.
"""

from Bio import Entrez
import textwrap
import pandas as pd

# Wrapper of 100 max characters for abstract text wrapping
wrapper = textwrap.TextWrapper(width=100)

# Max number of papers for the query
MAX_PAPERS = 100

def search_pubmed(query):
    """
    Function for querying PubMed API using Entrez
    :param query: str, the query
    :return: dict, record with the papers' details
    """
    Entrez.email = "example@gmail.com"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=MAX_PAPERS)
    record = Entrez.read(handle)

    return record

def fetch_details(pmids):
    """
    Function for fetching the details of the papers using their PMIDs
    :param pmids: list, with the PMIDs of the papers
    :return: dict, with details of the papers as returned from their respective XML files
    """
    ids = ','.join(pmids)
    Entrez.email = "example@gmail.com"
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
    results = Entrez.read(handle)

    return results

if __name__ == '__main__':

    # The query used:
    # KEYWORDS  :   "ADNI", "MRI", "CNN", "classification"
    # WHERE     :   Title and Abstract of the paper
    # LANGUAGE  :   English papers only
    query = 'ADNI[tiab] AND MRI[tiab] AND CNN[tiab] AND classification[tiab] AND English[Language]'

    # -----------------------------------
    # PubMed
    # -----------------------------------

    # Querying the PubMed API
    pm_results = search_pubmed(query)

    # Get a list with the PMIDs of the papers
    pmids = pm_results['IdList']

    # Fetch a dictionary with details of each paper
    pm_papers = fetch_details(pmids)

    # Base URL for the papers
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"

    # Initialize a dictionary for the titles, author names, abstracts and URL
    # This dictionary will later be used for constructing the data frame to be exported as csv
    columns = ['titles', 'authors', 'abstracts', 'links']
    data = {col: [] for col in columns}

    # Opening the txt file for writing
    with open(f'pubmed_papers_max_{MAX_PAPERS}.txt', 'w', encoding='utf-8') as f:

        # Writing the total number of papers found during the querying
        f.write(100 * '-' + '\n')
        f.write(f'PubMed: {len(pmids)} entries' + '\n')

        # The same but for the console
        print(100 * '-')
        print(f'PubMed: {len(pmids)} entries')

        for i, (paper, pmid) in enumerate(zip(pm_papers['PubmedArticle'], pmids)):

            # For each paper finding the title, authors' name, abstract and URL of the current paper
            # and appending it to the respective list in the dictionary

            # Current paper's title
            title = paper['MedlineCitation']['Article']['ArticleTitle']
            data['titles'].append(title)

            # Current paper's authors' names
            authors = paper['MedlineCitation']['Article']['AuthorList']

            # Constructing a string with all the authors' names
            authors_string = ''
            for author in authors:
                if 'LastName' in author and 'ForeName' in author:
                    authors_string += f"{author['LastName']}, {author['ForeName']}" + ' ; ' # using separator ';'

            data['authors'].append(authors_string)

            # Current paper's abstract
            summary = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]

            # Using the wrapper to wrap the text for easy reading
            wrapped_summary = '\n'.join(wrapper.wrap(text=summary))
            data['abstracts'].append(wrapped_summary)

            # Constructing the URLs using the PMIDs
            article_urls = base_url + pmid
            data['links'].append(article_urls)

            # Print the results in the console
            print(100 * '-')
            print(f'{i+1}) Title: {title}', end=2 * '\n')
            print(f'Summary:\n{wrapped_summary}', end=2 * '\n')
            print(f'Link:\n{article_urls}')
            print(100 * '-', end=2 * '\n')

            # Write the results in the txt file
            f.write(100 * '-' + '\n')
            f.write(f'{i+1}) Title: {title}' + 2*'\n')
            f.write(f'Authors: {authors_string}' + 2*'\n')
            f.write(f'Summary:\n{wrapped_summary}' + 2*'\n')
            f.write(f'Link:\n{article_urls}' + '\n')
            f.write(100 * '-' + '\n')

    # Make the data frame with the details
    df = pd.DataFrame(data)

    # Exporting the data to a csv file
    df.to_csv('pubmed_papers_details.csv', index=False)

