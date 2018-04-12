from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import urllib2
import json
import glob

json_directory = "/Users/chirag/Workspace/CourtListener/sample_ca9/"

def get_file_paths():
    file_paths = []
    for paths in glob.glob(json_directory + "*.json"):
        file_paths.append(paths)

    return file_paths

def open_json(filename):
    with open(filename) as json_file:
        content = json.load(json_file)

    return content

def get_html_content(json_content):
    html_content = json_content.get("html_with_citations")
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

def get_case_details(soup):
    # Get center tags for case id and case names
    case_id = ''
    case_name = ''
    center_tags = soup.find_all("center")

    for lines in center_tags:
        # print lines.get_text()
        try:
            if "No." in lines.get_text():
                # print lines
                case_id = lines.get_text().encode("utf-8")

            h1_tags = lines.find("h1") # For case names
            if h1_tags:
                # print h1_tags.get_text()
                names = h1_tags.get_text().encode("utf-8")
                case_name = names
        except:
            case_id = "Not Found"

    return case_id, case_name

def get_citation_details(soup):

    opinions_cited_id = []
    opinions_cited_links = []

    citation_tags = soup.find_all(class_='citation')

    for lines in citation_tags:
      #print lines
        try:
            data_id = lines["data-id"].encode("utf-8")
            links = lines.a['href'].encode("utf-8")

            opinions_cited_id.append(data_id)
            opinions_cited_links.append(links)
        except:
            print "Citation details Not found"

    # Include only unique ids in the list
    opinions_cited_id = list(set(opinions_cited_id))
    opinions_cited_links = list(set(opinions_cited_links))

    return opinions_cited_id, opinions_cited_links

def main():
    dataset_dict = {}

    case_id = []
    case_name = []
    opinion_id = []
    opinion_link = []

    file_paths = get_file_paths()
    for files in file_paths:
        print "Extracting file : {}".format(files)
        content = open_json(files)
        soup = get_html_content(content)
        case_id_str, case_name_str = get_case_details(soup)
        case_id.append(case_id_str)
        case_name.append(case_name_str)

        opinions_cited_id, opinions_cited_links = get_citation_details(soup)

        opinion_id.append(opinions_cited_id)
        opinion_link.append(opinions_cited_links)

    # Store to dict
    dataset_dict["Case_ID"] = case_id
    dataset_dict["Case_Name"] = case_name
    dataset_dict["Opinions_cited"] = opinion_id
    dataset_dict["Opinions_links"] = opinion_link

    # Convert to DataFrame
    df = pd.DataFrame(dataset_dict)

    # Store as csv
    df.to_csv("dataset.csv", index=None)

main()
