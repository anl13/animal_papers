###
### The original *.txt files are not elegant. 
### Therefore I change all of them to several json files to save space. 
### 2025.06.20 
### Liang An 
### 

import json 
from paper import Paper, g_badges
import os 

def load_txt_write_json():
    papers = []
    folder = "./data/papers/"
    paper_names = os.listdir(folder)
    for paper_name in paper_names:
        print(paper_name)
        with open(folder + paper_name, 'r') as f: 
            lines = f.readlines() 
        paper = Paper()
        paper.parse_lines(lines)
        papers.append(paper)

    papers.sort(key=lambda p: (p.adddate, p.year, p.article), reverse=True)

    ## old ones 
    jsonfile = "./data/jsons/paper_old.json"
    json_dict = []
    for paper in papers: 
   
        if paper.year <= 2024:
            json_dict.append(paper.to_json()) 
    with open(jsonfile, 'w') as f: 
        json.dump(json_dict, f, indent="\t")

    ## 2025 papers
    jsonfile = "./data/jsons/paper_2025.json"
    json_dict = []
    for paper in papers: 
        if paper.year == 2025:
            json_dict.append(paper.to_json()) 
    with open(jsonfile, 'w') as f: 
        json.dump(json_dict, f, indent="\t")

if __name__ == "__main__": 
    load_txt_write_json() 