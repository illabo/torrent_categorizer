import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup

instant_soups = {}
name_parts = {
    "series":["сериал","Сериал","serie","television","TV-show","tv-show"],
    "movies":["кино","movie"]
}
instant_soup_sources = ["https://rutracker.org/forum/","https://www.limetorrents.info","https://1337x.to"]

def list_links_with(name_contains=[], in_soup=None, orig_url=""):
    links=[]
    if not in_soup:
        return links
    base_url = orig_url
    rel = in_soup.find('link', {'rel': 'canonical'})
    if rel:
        base_url = rel.get('href')
    for lnk in in_soup.find_all("a"):
        nofollow = lnk.get('rel')
        if nofollow==None or not 'nofollow' in nofollow:
            text = lnk.get_text()
            href = lnk.get("href")
            if not text:
                text = ''
            if len(name_contains)==0:
                links.append(urllib.parse.urljoin(base_url, href))
            else:
                for el in name_contains:
                    if href and not 'Случайная раздача' in text:
                        if el in text or el in href:
                            links.append(urllib.parse.urljoin(base_url, href))
    return links

def find_magnet_in(soup=None):
    if not soup:
        return None
    for l in soup.find_all("a"):
        lnk = l.get("href")
        if lnk and "magnet:" in lnk:
            return lnk
    return None

def add_instant_soups(base_url, in_list, urls):
    for u in urls:
        in_list.append(urllib.parse.urljoin(base_url, u))

def prepare_soup(from_link):
    html_noodle = requests.get(from_link).content
    return BeautifulSoup(html_noodle, 'html.parser')

def get_instant_soups(from_source):
    soup = prepare_soup(from_source)
    for k in name_parts.keys():
        if not k in instant_soups:
            instant_soups[k] = []
        add_instant_soups(from_source, instant_soups[k], list_links_with(name_parts[k], soup))

def same_site_link(url):
    for base_url in instant_soup_sources:
        if base_url in url:
            return True
    return False

def main():
    for s in instant_soup_sources:
        get_instant_soups(s)
    with open('magnets.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for k in instant_soups.keys():
            for url in instant_soups[k]:
                for link in list_links_with(["viewtopic","-torrent-","torrent/"], in_soup=prepare_soup(url),  orig_url=url):
                    if same_site_link(link):
                        print('\r',"checking if page contains magnet links: "+link+(" "*15),end="")
                        magnet = find_magnet_in(prepare_soup(link))
                        if magnet:
                            print('\r',"magnet link found: "+magnet+(" "*15),end="")
                            csv_writer.writerow([k, magnet])


if __name__ == '__main__':
    main()