from bs4 import BeautifulSoup
import re
import os
from collections import deque


def parse(path_to_file):
    with open(path_to_file, encoding="utf-8") as file:
        html = file.read()
        soup = BeautifulSoup(html, "lxml")
        body = soup.find(id="bodyContent")
        img = len(body.find_all("img", width=lambda x: int(x or 0) > 199))
        headers = sum(1 for tag in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) if tag.get_text()[0] in "ETC")
        lists = sum(1 for tag in body.find_all(["ol", "ul"]) if not tag.find_parent(["ol", "ul"]))

        linkslen = 0
        for a in body.find_all("a"):
            current_streak = 1
            for tag in a.find_next_siblings():
                if tag.name == "a":
                    current_streak += 1
                else:
                    break
            linkslen = current_streak if current_streak > linkslen else linkslen
        return [img, headers, linkslen, lists]


def get_links(path):
    adj = {}
    files = set(os.listdir(path="wiki"))
    for page in os.listdir(path="wiki"):
        with open(os.path.join(path, page), encoding="utf-8") as file:
            links = set(re.findall(r"(?<=/wiki/)[\w()]+", file.read()))
        links = links.intersection(files)
        adj.update({page: list(links)})
    return adj


def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque()
    q.append(start)
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                q.append(next)
    return dist.get(end)


def extract(array, res):
    res.append(array[-1])
    if len(array) > 1:
        res = extract(array[-2], res)
    elif len(array) == 1:
        res.append(array[0])
        return res
    return res


def build_bridge(path, start_page, end_page):
    graph = get_links(path)
    short = find_shortest_path(graph, start_page, end_page)
    res = extract(short, [])
    res.reverse()
    res = res[1:]
    return res


def get_statistics(path, start_page, end_page):
    pages = build_bridge(path, start_page, end_page)
    statistic = {page: parse(f"{path}{page}") for page in pages}

    return statistic


if __name__ == '__main__':
    print(parse('wiki/The_New_York_Times'))
