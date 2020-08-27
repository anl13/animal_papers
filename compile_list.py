import csv
import os
import argparse
import datetime


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

    def parse_lines(self, lines):
        items = lines[0:7]
        [self.title, self.year, self.paper, self.project, self.article, ainfo, self.teaser] = items

        if self.project:
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
        author_records = ainfo.split(';')
        self.authors = []
        self.author_urls = []
        for author_r in author_records:
            pos_id = author_r.find('+')
            author = ''
            url = ''
            if pos_id > 0:
                author = author_r[:pos_id]
                url = author_r[pos_id + 1:]
            else:
                author = author_r
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

    def write_html(self, html):
        paper_html = '<table><tbody><tr><td>\n'
        paper_html += '<a href="%s"><img src="teasers/%s"/ border=1 width=210></a></td>\n' % (self.imgurl, self.teaser)
        paper_html += '<td width="20"></td>\n<td valign="middle" width="680">'
        paper_html += '<strong>%s</strong>\n' % self.title
        paper_html += '<p class="content">'
        paper_html = self.add_authors(paper_html)
        paper_html += 'In %s %d<br>\n' % (self.article, self.year)
        if self.paper:
            paper_html += '<strong><a href="%s">[Paper]</a></strong> \n' % self.paper
        if self.project:
            paper_html += '<strong><a href="%s">[Project]</a></strong>\n' % self.project
        paper_html += '</p></tr></tbody></table><br>\n\n'
        html += paper_html
        return html

    def write_md(self, md):
        paper_md = '<table> <tbody> <tr> <td align="left" width=250>\n'
        paper_md += '<a href="%s"><img src="teasers/%s"/></a></td>\n' % (self.imgurl, self.teaser)
        paper_md += '<td align="left" width=550>%s<br>\n' % self.title
        paper_md = self.add_authors(paper_md)
        paper_md += 'In %s %d<br>\n' % (self.article, self.year)
        if self.paper:
            paper_md += '<a href="%s">[Paper]</a> \n' % self.paper
        if self.project:
            paper_md += '<a href="%s">[Project]</a>\n' % self.project
        paper_md += '</td></tr></tbody></table>\n\n\n'
        md += paper_md
        return md


def read_papers():
    papers = []
    folder = "./data/papers/"
    paper_names = os.listdir(folder)
    for paper_name in paper_names:
        with open(folder + paper_name, 'r') as f: 
            lines = f.readlines() 
        paper = Paper()
        paper.parse_lines(lines)
        papers.append(paper)
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
    for paper in papers:
        content = getattr(paper, mtd_str)(content)
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
    parser.add_argument('-t', '--type', help='type of output file (md or html)', default='html')
    parser.add_argument('-o', '--output', default=None, help='name of the output file')
    args = parser.parse_args()
    
    TYPE = args.type   # html, md
    if not args.output:
        if args.type == 'md':
            args.output = 'README'
        if args.type == 'html':
            args.output = 'animal_papers'

    out_file = '%s.%s' % (args.output, args.type)  # output file
    # print('Write %s file <%s>' % (TYPE.upper(), out_file))
    WORK_DIR = 'data/'
    # input & output
    header_file = os.path.join(WORK_DIR, 'header.%s' % TYPE)
    end_file = os.path.join(WORK_DIR, 'end.%s' % TYPE)
    csv_file = os.path.join(WORK_DIR, 'reference.csv')  # ./usr/local/google/home/junyanz/Projects/CatPapers/reference.csv'
    # load papers
    papers = read_papers()

    # sort papers
    papers.sort(key=lambda p: p.title)
    papers.sort(key=lambda p: (p.year, p.article), reverse=True)

    # write papers
    with open(out_file, 'w') as f:
        md_content = write_papers(papers, header_file, end_file, TYPE=TYPE)
        f.write(md_content)
