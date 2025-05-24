# Literature-Finders

The scripts were used for launching a literature review, with the main focus on the study of CNN models, which use MRIs of the ADNI database in order to classify patients according to the stage of AD disease. For this purpose the databases used were PubMed and ArXiv.

## Requirements

```
python==3.8.18
biopython==1.83
pandas==1.3.4
requests==2.31.0
beautifulsoup4==4.12.3
```

## Repository Structure

In the `scripts` directory the files used for querying the ArXiv and PubMed APIs and exporting the returned papers' title, author names, abstract and URL into two separate files (a CSV file and a TXT file) are located.

In the `txt` and `csv` directories the two exported files from each script can be located.
