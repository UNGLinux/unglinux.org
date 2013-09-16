#!/usr/bin/env python3.3
from __future__ import print_function
import argparse
import json
import os
import pystache
import requests
import aniso8601
import datetime
import time
import sys

def output_html_to_path(dir_, vec):
    renderer = pystache.Renderer()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "index.mustache.html"), "r") as template:
        t = template.read()
    if sys.version_info.major == 2:
        t = t.decode("utf-8")
    with open(os.path.join(dir_, "index.html"), "w") as index:
        index.write(renderer.render(t, vec))

def recache_repo(cacheing_session, cache, name):
    api_r = cacheing_session.get("https://api.github.com/repos/{0}/{1}/commits".format(*name.split("/", 1)))
    try:
        raw = api_r.json()
    except ValueError:
        print("warning: GitHub API returned invalid JSON for {0}.".format(name))
        return []
    pool = set(a["sha1"] for a in cache if a["name"] == name)
    for co in raw[0:30]:
        if co["sha"] in pool:
            continue
        repo_baseurl = "https://github.com/{0}".format(name)
        DEFAULT_AUTHOR = {
            "html_url": "",
            "avatar_url": "assets/images/unknown_author.png",
            "login": co["commit"]["author"]["name"]
        }
        if not co["author"]:
            co["author"] = DEFAULT_AUTHOR
        if not co["committer"]:
            co["committer"] = DEFAULT_AUTHOR
        dt = aniso8601.parse_datetime(co["commit"]["author"]["date"]).replace(tzinfo=None)
        cache.append({
            "sha1": co["sha"],
            "author-page": co["author"]["html_url"],
            "avatar-url": co["author"]["avatar_url"],
            "author-name": co["author"]["login"],
            "github": repo_baseurl,
            "name": name,
            "author-date": co["commit"]["author"]["date"],
            "commit-message": co["commit"]["message"],
            "committer-is-author": co["author"]["login"] == co["committer"]["login"],
            "committer-name": co["committer"]["login"],
            "_nsam-sortkey": dt.timestamp() if sys.version_info.major == 3 else (dt - datetime.datetime(1970, 1, 1)).total_seconds()
        })

def main(args):
    print("Reading nsamrc...")
    with open(args.config, "r") as cf:
        values = json.load(cf)
    print("Loading cache...", end=" ")
    override_repos = 0
    try:
        with open("nsamlite-cache", "r") as cache_file:
            cache = json.load(cache_file)
        print("done.")
    except IOError:
        print("no cache! Will create one.")
        override_repos = 1
        cache = []
    cacheing_session = requests.Session()
    for repo in values["repositories"]:
        if not args.repo or repo["name"] in args.repo or override_repos:
            print("Checking {0}...".format(repo["name"]))
            recache_repo(cacheing_session, cache, repo["name"])
    print("Caching done. Sorting and compiling...")
    cache.sort(key=lambda o: o["_nsam-sortkey"], reverse=1)
    cache = cache[0:30]
    with open("nsamlite-cache", "w") as dump:
        json.dump(cache, dump)
    values["info"] = {"update": time.strftime("%d %b, %Y (%A) %H:%M:%S")}
    values["github-events"] = cache
    output_html_to_path(os.path.abspath(args.out), values)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate NSAMirror static pages.", epilog="Copyright 2013 stalcorp LLC. All rights reserved.")
    parser.add_argument("-o", metavar="filename", dest="out", type=str, help="output path", default=".")
    parser.add_argument("-c", metavar="filename", dest="config", type=str, help="config file to use", default="nsamrc.json")
    parser.add_argument("repo", type=str, help="repositories to hit", nargs="*")
    a = parser.parse_args()
    main(a)
