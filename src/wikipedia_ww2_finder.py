#!/usr/bin/env python3

from bs4 import BeautifulSoup
import bs4
import subprocess
import sys

body_content = bs4.SoupStrainer(id="bodyContent")
MAX_DEPTH = 10
GOAL = "/wiki/World_War_II"
LINK_HEAD = "https://en.wikipedia.org"


class GetToWW2FromARandomWikiPage:

    def __init__(self, link):
        self.links_queue = []
        self.start = link
        self.links_queue.append((self.start, 0, []))
        self.get_to_ww2()

    def get_to_ww2(self):
        if self.start == GOAL:
            self.print_path(0, [])
            print(LINK_HEAD+self.start)
            exit(0)
        while self.links_queue.__len__() != 0:
            current_link = self.links_queue.pop(0)
            if current_link[1] > MAX_DEPTH:
                print("FAIL")
                return
            self.add_links_from_current_page(current_link[0], current_link[1], current_link[2])

    def add_links_from_current_page(self, link, current_depth, current_path):
        try:
            page = subprocess.check_output(["curl", "-L", LINK_HEAD + link], stderr=subprocess.DEVNULL).decode("utf-8")
        except subprocess.CalledProcessError:
            return
        except TypeError:
            return
        a_tags = BeautifulSoup(page, "html.parser", parse_only=body_content).find_all('a')
        for tag in a_tags:
            href = tag.get('href')
            if href == GOAL:
                self.print_path(current_depth + 1, current_path)
                print(LINK_HEAD+link)
                print(LINK_HEAD+href)
                exit(0)
            new_link = (href, current_depth + 1, list(current_path))
            new_link[2].append(link)
            self.links_queue.append(new_link)

    def print_path(self, depth, path):
        print("SUCCESS for\t\t"+LINK_HEAD+self.start+"\nNUM CLICKS:\t\t"+str(depth))
        print("PATH FROM\t\t"+LINK_HEAD+self.start+"\nTO\t\t\t"+LINK_HEAD+GOAL)
        for l in path:
            print(LINK_HEAD+l)


def get_random_page():
    return subprocess.check_output(["curl", "-Ls", "-w %{url_effective}",
                                    "https://en.wikipedia.org/wiki/Special:Random"
                                    ]).decode("utf-8").splitlines()[-1][25:]


if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        GetToWW2FromARandomWikiPage(get_random_page())
    else:
        GetToWW2FromARandomWikiPage(sys.argv[1])
