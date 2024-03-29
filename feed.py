import feedparser
import time
import re
from os import path


def open_readme():
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
        readme = f.read()
    return readme

def write_readme(updated):
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(updated)

def modify_readme(readme, text, identifier=''):
    start_tag = f'{identifier}_START'
    end_tag = f'{identifier}_END'
    return re.sub(f'(?<=<!-- {start_tag} -->).*?(?=<!-- {end_tag} -->)', text, readme, flags=re.DOTALL)


def list_recent_posts(feed):
    """
    List the recent posts from the RSS feed.
    """
    posts = []
    feed = feedparser.parse(feed)
    for entry in feed.entries:
        title = entry['title']
        link = entry['link']
        published = time.strftime('%d %b, %Y', entry['published_parsed'])
        posts.append(f"><samp>[{title}]({link})</samp><br>\n><samp>{published}</samp>")
    return '\n' + '\n\n'.join(posts) + '\n'


def main():
    posts = list_recent_posts("https://priyankt.com/feed.xml")
    original = open_readme()
    updated = modify_readme(original, posts, identifier='BLOG')
    write_readme(updated)


if __name__ == '__main__':
    main()
