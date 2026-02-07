import os
import argparse
import datetime
import pickle 


def create_badges(): 
    animal_types = ["dog", "cat", "quadruped", "bird", "fly", "mouse", "monkey", "mouse lemur", "primate", "pig", "gerbil", "rodent"]
    badges = {} 
    for animal in animal_types: 
        animal_label = animal.replace(" ", "%20")
        badge_string = "https://img.shields.io/badge/animal-{}-yellowgreen".format(animal_label)
        badge_string2 = '<a href="{}" align="bottom"><img src="{}"></a>'.format(badge_string, badge_string)
        badges.update({animal:badge_string2})
    data_types = ["surface", "mesh", "3d", "2d"]
    for data in data_types: 
        data_label = data.replace(" ", "%20")
        badge_string = "https://img.shields.io/badge/datatype-{}-9cf".format(data_label)
        badge_string2 = '<a href="{}" align="bottom"><img src="{}"></a>'.format(badge_string, badge_string)
        badges.update({data:badge_string2})
    topic_types = ["face", "behavior", "brain", "dataset", "social", "ecology", "review"]
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
        self.grade = None

    def parse_lines(self, lines):
        items = lines[0:7]
        [self.title, self.year, self.paper, self.project, self.article, self.teaser, self.grade] = items
        self.title = self.title.strip()
        self.year = self.year.strip()
        self.paper = self.paper.strip()
        self.project = self.project.strip()
        self.article = self.article.strip()
        self.teaser = self.teaser.strip()
        self.grade = self.grade.strip()

        self.keywords = lines[7][9:].strip().split(',')
        for i in range(len(self.keywords)):
            self.keywords[i] = self.keywords[i].strip()
        self.adddate = lines[8][9:].strip()
        
        if self.project != "none":
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

    def parse_json(self, value):
        self.title = value["title"].strip()
        self.year = value["year"]
        self.paper = value["paper_link"].strip()
        self.project = value["project_page"].strip()
        self.teaser = value["teaser"].strip()
        self.article = value["journal"].strip() 
        self.adddate = value["adddate"].strip() 
        self.keywords = value["keyword"] # list 
        self.grade = value["grade"]
        
        if self.project != "none":
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

        author_records = value["authors"]
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

    def to_json(self): 
        json_dict = {
            "title": self.title, 
            "year": self.year, 
            "paper_link": self.paper, 
            "project_page": self.project, 
            "teaser": self.teaser, 
            "journal": self.article, 
            "authors": [], 
            "adddate": self.adddate, 
            "keyword": self.keywords,
            "grade": self.grade
        }
        for i, (author, url) in enumerate(zip(self.authors, self.author_urls)):
            if len(url) > 0: 
                json_dict["authors"].append(author + "+" + url) 
            else: 
                json_dict["authors"].append(author)
        return json_dict 
    
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
                content += '<a href="%s"><font size=2.5>%s</font></a>, \n' % (url, author)
            else:
                content += '<font size=2.5>%s</font>, \n' % author
        if self.author_urls[-1]:
            content += '<a href="%s"><font size=2.5>%s</font></a><br>\n' % (self.author_urls[-1], self.authors[-1])
        else:
            content += '<font size=2.5>%s</font><br>\n' % self.authors[-1]
        return content

    def write_md(self, md):
        paper_md = '<tbody> <tr> <td align="left" width=250>\n'
        paper_md += '<a href="%s"><img src="teasers_small1/%s"/></a></td>\n' % (self.imgurl, self.teaser)
        paper_md += '<td align="left" width=550><em>%s</em><br>\n' % self.title
        paper_md = self.add_authors(paper_md)
        paper_md += '<font size=2.5>In %s %d </font>' % (self.article, self.year)
        if self.grade != "none" and self.grade != "poster":
            paper_md += ('(<b><font size=2.5>' + self.grade +'</font></b>)')
                
        paper_md += '<br>\n'
        if self.paper:
            paper_md += '<a href="%s"><img src="data/paper.png"></a> \n' % self.paper
        
        if self.project != "none":
            paper_md += '<a href="%s"><img src="data/project.png"></a>\n' % self.project

        for label in self.keywords: 
            if label in list(g_badges.keys()):
                paper_md += g_badges[label]

        paper_md += '</td></tr></tbody>\n\n\n'
        md += paper_md
        return md

    # use https://shields.io/#your-badge to create your own badge 