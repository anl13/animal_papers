import os
import argparse
import datetime
import pickle 
from paper import Paper, g_badges
import commentjson as json 

def read_papers():
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
    with open("data/paper_list.pkl", 'wb') as f:
        pickle.dump(papers,f) 
    return papers

def read_papers_json(): 
    papers = [] 
    folder = "./data/jsons" 
    json_list = os.listdir(folder) 
    for jsonfile in json_list: 
        print("Load ", jsonfile) 
        with open(os.path.join(folder, jsonfile), 'r') as f: 
            jsondict = json.load(f) 
        
        for value in jsondict: 
            paper = Paper() 
            paper.parse_json(value)
            papers.append(paper) 
    with open("data/paper_list.pkl", 'wb') as f: 
        pickle.dump(papers, f) 
    return papers 

def add_date(content):
    date_str = 'Last updated in %s' % datetime.date.today().strftime("%b %Y")
    content += date_str
    return content

def write_papers(papers, header_file=None, end_file=None, TYPE='md'):
    mtd_str = 'write_' + TYPE.lower()
    content = ''
    # add header file
    if header_file and os.path.exists(header_file):
        with open(header_file, 'r') as hfile:
            content = hfile.read()

    content += '\n<br>\n\n'
    if (TYPE=='md'):
        content += '<table>'
    for paper in papers:
        content = getattr(paper, mtd_str)(content)
    if (TYPE=='md'):
        content += '</table>'
    content += '\n<br>\n\n'
    content = add_date(content)
    content += '\n<br>\n\n'
    if end_file and os.path.exists(end_file):
        with open(end_file, 'r') as efile:
            content += efile.read()

    return content


if __name__ == '__main__':
    # example usage (markdown):    python compile_cat_papers.py -t md -o README
    # example usage (html):        python compile_cat_papers.py -t html -o cat_papers
    parser = argparse.ArgumentParser(description='Compile cat papers.')
    parser.add_argument('-t', '--type', choices=['md'], help='type of output file (md)', default='md')
    parser.add_argument('-o', '--output', default=None, help='name of the output file')
    args = parser.parse_args()
    
    TYPE = args.type   # html, md
    if not args.output:
        if args.type == 'md':
            args.output = 'README'
        # if args.type == 'html':
        #     args.output = 'animal_papers'

    out_file = '%s.%s' % (args.output, args.type)  # output file
    # print('Write %s file <%s>' % (TYPE.upper(), out_file))
    WORK_DIR = 'data/'
    # input & output
    header_file = os.path.join(WORK_DIR, 'header.%s' % TYPE)
    end_file = os.path.join(WORK_DIR, 'end.%s' % TYPE)
    # load papers

    ### uncomment this line to compile paper_list.pkl from txt files. 
    papers = read_papers_json()
    with open("data/paper_list.pkl", 'rb') as f: 
        papers = pickle.load(f)

    # sort papers
    papers.sort(key=lambda p: (p.adddate, p.year, p.article), reverse=True)
    # papers.sort(key=lambda p: (p.year, p.article), reverse=True)

    # write papers
    print(out_file)
    with open(out_file, 'w') as f:
        md_content = write_papers(papers, header_file, end_file, TYPE=TYPE)
        f.write(md_content)
