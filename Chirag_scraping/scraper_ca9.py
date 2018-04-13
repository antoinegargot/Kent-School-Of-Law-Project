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

def get_date_submitted(soup):
    date_submitted = ''
    center_tags = soup.find_all("center")
    for dates in center_tags:
        try:
            if "Submitted" in dates.get_text():
                #print dates
                date_submitted = dates.get_text().encode("utf-8")
        except:
            print "Date submitted not found"

    return date_submitted

def get_date_filed(soup):
    date_filed = ''
    center_tags = soup.find_all("center")
    for filed in center_tags:
        try:
            if "Filed" in filed.get_text():
                #print filed
                date_filed = filed.get_text().encode("utf-8")
        except:
            print "Date Filed not found"

    return date_filed

def get_judge_name(soup):
    judge_name = ''
    judge_tag = soup.find_all("p")
    for name in judge_tag:
        try:
            if "District Judge:" in name.get_text():
                #print name
                judge_name = name.get_text().encode("utf-8")
            elif "Circuit Judge:" in name.get_text():
                #print name
                judge_name = name.get_text().encode("utf-8")
        except:
            print "Judge names not found"

    return judge_name

def get_case_cites(soup):
    case_cite = ''
    cite_tag = soup.find_all(class_="case_cite")
    for cite in cite_tag:
        try:
            #print cite.get_text()
            case_cite = cite.get_text().encode("utf-8")
        except:
            print "case cites not found"

    return case_cite

def get_parties(soup):
    parties = ''
    parties_tag = soup.find_all(class_="parties")
    for p in parties_tag:
        try:
            #print p.get_text()
            parties = p.get_text().encode("utf-8")
        except:
            print "Parties not found"

    return parties

def get_docket(soup):       #Same as Case-no.
    docket = ''
    docket_tag = soup.find_all(class_="docket")
    for d in docket_tag:
        try:
            #print d.get_text()
            docket = d.get_text().encode("utf-8")
        except:
            print "Case no. not found"

    return docket
def get_court(soup):
    court = ''
    court_tag = soup.find_all(class_="court")
    for courts in court_tag:
        try:
            #print courts.get_text()
            court = courts.get_text().encode("utf-8")
        except:
            print "Courts data not found"

    return court
def get_dates(soup):
    dates = ''
    date_new = soup.find_all(class_="date")
    for date in date_new:
        try:
            #print date.get_text()
            dates = date.get_text().encode("utf-8")
        except:
            print "Citation not found"

    return dates

def get_indent(soup):
    indent = ''
    indent_tag = soup.find_all(class_="indent")
    for i in indent_tag:
        try:
            indent = i.get_text().encode('utf-8')
        except:
            print "Data not found"

    return indent


def main():
    dataset_dict = {}

    case_id = []
    case_name = []
    opinion_id = []
    opinion_link = []
    date_submitted = []
    date_filed = []
    judge_name = []
    case_cite = []
    parties = []
    docket = []
    court = []
    indent = []
    dates = []

    file_paths = get_file_paths()
    for files in file_paths:
        print "Extracting file : {}".format(files)
        content = open_json(files)
        soup = get_html_content(content)
        case_id_str, case_name_str = get_case_details(soup)
        case_id.append(case_id_str)
        case_name.append(case_name_str)
        date_submitted_str = get_date_submitted(soup)
        date_submitted.append(date_submitted_str)
        date_filed_str = get_date_filed(soup)
        date_filed.append(date_filed_str)
        judge_name_str = get_judge_name(soup)
        judge_name.append(judge_name_str)
        case_cite_str = get_case_cites(soup)
        case_cite.append(case_cite_str)
        parties_str = get_parties(soup)
        parties.append(parties_str)
        docket_str = get_docket(soup)
        docket.append(docket_str)
        court_str = get_court(soup)
        court.append(court_str)
        indent_str = get_indent(soup)
        indent.append(indent_str)
        dates_str = get_dates(soup)
        dates.append(dates_str)

        opinions_cited_id, opinions_cited_links = get_citation_details(soup)

        opinion_id.append(opinions_cited_id)
        opinion_link.append(opinions_cited_links)

    # Store to dict
    dataset_dict["Case_ID"] = case_id
    dataset_dict["Case_Name"] = case_name
    dataset_dict["Opinions_cited"] = opinion_id
    dataset_dict["Opinions_links"] = opinion_link
    dataset_dict["Date Submitted"] = date_submitted
    dataset_dict["Date Filed"] = date_filed
    dataset_dict["Judges Names"] = judge_name
    dataset_dict["Case Cites"] = case_cite
    dataset_dict["Parties"] = parties
    dataset_dict["Docket"] = docket
    dataset_dict["Court"] = court
    dataset_dict["Indent Names"] = indent
    dataset_dict["Date"] = dates
    # Convert to DataFrame
    df = pd.DataFrame(dataset_dict)

    # Store as csv
    df.to_csv("dataset.csv", index=None)

main()
