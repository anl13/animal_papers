import csv
import os
import argparse
import datetime
import pickle 

def create_badges(): 
    animal_types = ["dog", "cat", "quadruped", "bird", "fly", "mouse", "monkey", "mouse lemur", "primate"]
    badges = {} 
    for animal in animal_types: 
        animal_label = animal.replace(" ", "%20")
        badge_string = "https://img.shields.io/badge/animal-{}-yellowgreen".format(animal_label)
        badge_string2 = '<a href="{}" align="bottom"><img src="{}"></a>'.format(badge_string, badge_string)
        badges.update({animal:badge_string2})
    data_types = ["dense surface", "mesh", "3d", "2d"]
    for data in data_types: 
        data_label = data.replace(" ", "%20")
        badge_string = "https://img.shields.io/badge/datatype-{}-9cf".format(data_label)
        badge_string2 = '<a href="{}" align="bottom"><img src="{}"></a>'.format(badge_string, badge_string)
        badges.update({data:badge_string2})
    topic_types = ["face", "behavior", "brain", "dataset"]
    for topic in topic_types: 
        topic_label = topic.replace(" ", "%20")
        badge_string = "https://img.shields.io/badge/topic-{}-orange".format(topic_label)
        badge_string2 = '<a href="{}" align="bottom"><img src="{}"></a>'.format(badge_string, badge_string)
        badges.update({topic:badge_string2})
    return badges
g_badges = create_badges()

class Paper():
    def __init__(self):
        self.title = 'cat'
        self.year = 1900
        self.paper = None
        self.project = None
        self.article = 'SIGGRAPH'
        self.teaser = 'tmp.png'
        self.authors = None
        self.author_urls = None
        self.imgurl = None
        self.poster = None

    def parse_lines(self, lines):
        items = lines[0:7]
        [self.title, self.year, self.paper, self.project, self.article, self.teaser, self.poster] = items
        self.title = self.title.strip()
        self.year = self.year.strip()
        self.paper = self.paper.strip()
        self.project = self.project.strip()
        self.article = self.article.strip()
        self.teaser = self.teaser.strip()
        self.poster = self.poster.strip()

        self.keywords = lines[7][9:].strip().split(',')
        for i in range(len(self.keywords)):
            self.keywords[i] = self.keywords[i].strip()
        self.adddate = lines[8][9:].strip()
        
        if self.project is not "none":
            self.imgurl = self.project
        elif self.paper:
            self.imgurl = self.paper
        else:
            print('ERROR: no paper/project')
        if not self.title:
            print('ERROR: no title')
        if not self.article:
            print('ERROR: no article')
        if not self.year:
            print('ERROR: no year')

        self.year = int(float(self.year))

        author_records = lines[9:]
        self.authors = []
        self.author_urls = []
        for author_r in author_records:
            pos_id = author_r.find('+')
            author = ''
            url = ''
            if author_r == '':
                continue 
            if pos_id > 0:
                author = author_r[:pos_id]
                url = author_r[pos_id + 1:]
                author = author.strip()
                url = url.strip()
            else:
                author = author_r.strip()
            self.authors.append(author)
            self.author_urls.append(url)

        author_name = self.authors[0]    # get teaser name
        last_name = author_name.split(' ')[-1]
        if not self.teaser:
            self.teaser = '%s%d.jpg' % (last_name, self.year)

    def __str__(self):
        tmp = '[Title]: %s\n' % self.title
        tmp += '[Year]: %d\n' % self.year
        tmp += '[Paper]: %s\n' % self.paper
        tmp += '[Project]: %s\n' % self.project
        tmp += '[URL]: %s\n' % self.imgurl
        tmp += 'In %s\n' % self.article
        tmp += '[Teaser]: %s\n' % self.teaser
        for i, (author, url) in enumerate(zip(self.authors, self.author_urls)):
            tmp += '[Author %d]: %s at %s\n' % (i, author, url)

        return tmp

    def add_authors(self, content):
        for author, url in zip(self.authors[:-1], self.author_urls[:-1]):
            if url:
                content += '<a href="%s">%s</a>, \n' % (url, author)
            else:
                content += '%s, \n' % author
        if self.author_urls[-1]:
            content += '<a href="%s">%s</a><br>\n' % (self.author_urls[-1], self.authors[-1])
        else:
            content += '%s<br>\n' % self.authors[-1]
        return content

    def write_md(self, md):
        paper_md = '<tbody> <tr> <td align="left" width=250>\n'
        paper_md += '<a href="%s"><img src="teasers/%s"/></a></td>\n' % (self.imgurl, self.teaser)
        paper_md += '<td align="left" width=550>%s<br>\n' % self.title
        paper_md = self.add_authors(paper_md)
        paper_md += 'In %s %d ' % (self.article, self.year)
        if self.poster != "none" and self.poster != "poster":
            paper_md += ('(<b>' + self.poster +'</b>)')
                
        paper_md += '<br>\n'
        if self.paper:
            paper_md += '<a href="%s">[Paper]</a> \n' % self.paper
        
        if self.project != "none":
            paper_md += '<a href="%s">[Project]</a>\n' % self.project

        for label in self.keywords: 
            if label in list(g_badges.keys()):
                paper_md += g_badges[label]

        paper_md += '</td></tr></tbody>\n\n\n'
        md += paper_md
        return md

    # use https://shields.io/#your-badge to create your own badge 

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
    # papers = read_papers()
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
