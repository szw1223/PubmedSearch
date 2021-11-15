# # handle = Entrez.einfo(db="pubmed", term="alzheimer's desease") # or esearch, efetch, ...
# # record = Entrez.read(handle)
# # # for field in record["DbInfo"]["FieldList"]:
# # #     print("%(Name)s, %(FullName)s, %(Description)s" % field)
# # print(record['DbInfo']['Count'])
# # print(record['DbInfo'].keys())
# # handle.close()

# handle = Entrez.esummary(db="pubmed", id="19304878", retmode="xml")
# records = Entrez.parse(handle)
# for record in records:
#     # each record is a Python dictionary or list.
#     print(record)

import numpy as np
from Bio import Medline, Entrez
from collections import Counter
import http.client
import sys

from docx import Document
from docx.shared import Inches

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# handle_0 = Entrez.esearch(db="pubmed", term="drug therapy[Subheading] AND adverse effects[Subheading] AND humans[MeSH Terms]", retmax=306431)
Entrez.email = "hexing@ufl.edu"

def main():
    handle_0 = Entrez.esearch(db="pubmed",
                              term="abp, alzheimer's[MeSH Terms] AND (2021/10/01[Date - Publication] : 2021/12/31[Date - Publication])",
                              ptyp="Review", usehistory="y", retmax=306431)
    record = Entrez.read(handle_0)
    idlist = record["IdList"]
    print("Total: ", record["Count"])
    No_Papers = len(idlist)
    webenv = record['WebEnv']
    query_key = record['QueryKey']

    total = No_Papers
    step = 10
    print("Result items:", total)
    with open("./Data_PubMed/PBDE1.txt", 'w') as f:
        for start in range(0, total, step):
            print("Download record %i to %i" % (start + 1, int(start + step)))
            handle_1 = Entrez.efetch(db="pubmed", retstart=start, rettype="medline", retmode="text",
                                     retmax=step, webenv=webenv, query_key=query_key)
            records = Medline.parse(handle_1)
            records = list(records)
            for index in np.arange(len(records)):
                id = records[index].get("PMID", "?")
                title = records[index].get("TI", "?")
                title = title.replace('[', '').replace('].', '')
                abstract = records[index].get("AB", "?")
                if 'BACKGROUND:' in abstract or 'OBJECTIVE:' in abstract or 'PURPOSE:' in abstract:
                    print(('AB: %s') % abstract)
                    f.write('PMID: ' + id + "\n" + 'Title: ' + title + "\n" + 'Abstract: ' + "\n" + abstract + "\n" + '\n')
