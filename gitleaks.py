import os
import json
import urllib
import hashlib
import requests
import traceback
import subprocess


from utils import default_output, run_command, make_folder, clone_repo, git_grep


# Github api url from searching code
API = "https://api.github.com/search/code?"


class Gitleaks:

    def __init__(self, query, token):
        self.query = query
        self.token = token

    def send_request(self, url):

        headers = {
            "Authorization": "token %s" % (self.token)
        }
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=20)

        if response.status_code in range(200, 300) and 'json' in str(response.headers['content-type']):
            content = json.loads(response.content)

            # In case of pagination the header return in response consist of link key
            # that usually have keys like last, previous and next which further have key named url
            # {
            #   'prev': {
            #               'url': 'https://api.github.com/search/code?q=go&page=1',
            #               'rel': 'prev'
            #           },
            #  'last': {
            #               'url': 'https://api.github.com/search/code?q=go&page=34',
            #               'rel': 'last'},
            #  'first': {
            #               'url': 'https://api.github.com/search/code?q=go&page=1',
            #               'rel': 'first'
            #           },
            #   'next': {
            #               'url': 'https://api.github.com/search/code?q=go&page=3',
            #   'rel': 'next'
            #           }
            # }

            if response.links and 'last' in response.links and 'url' in response.links['last']:
                last_page = response.links['last']['url'].split('=')[-1]
                for page in range(2, int(last_page) + 1):
                    try:
                        response = requests.get(url + "&page=%s" % (page), headers=headers, allow_redirects=False, timeout=20)
                        if response.status_code in range(200, 300) and 'json' in str(response.headers['content-type']):
                            content.update(json.loads(response.content))
                    except:
                        traceback.print_exc()
                        continue
            return content
        
        return {}

    def search_query(self):

        query = urllib.urlencode({'q': '%s' % (self.query)})
        url = API + query

        return self.send_request(url)

    def get_commit(self, commits_url):

        commits_url = commits_url.replace("{/sha}", "/master")
        contents    = self.send_request(commits_url)
        
        # Response of commits_url is a list of details of all commits
        if not contents or "sha" not in contents:
            return ""

        return contents["sha"]
    
    def get_contributors(self, contributors_url):
        contents = self.send_request(contributors_url)
        
        # Response of contributors_url is a list of hashes of all contributors
        if not contents:
            return []
        
        contributors = []

        for content in contents:
            data = {}
            if "login" in content:
                data["name"] = content["login"]
            if "html_url" in content:
                data["link"] = content["html_url"]
            if "contributions" in content:
                data["contributions"] = content["contributions"]
            
            if "name" in data and "link" in data and "contributions" in data:
                contributors.append(data)
        
        return contributors

    def get_output(self, data, output):
        
        # Create a unique folder using sha1 hash of self.query
        folder = make_folder(self.query)
        
        if not folder:
            return False

        count, data = clone_repo(data, folder)

        # No repositories is cloned
        if count == 0:
            return False
        
        output["type"] = "success"
        output["clone-path"] = folder
    
        output["data"] = data
        output["clone-stats"] = "%s of %s are cloned" % (count, len(data))

        return output
    
    def get_repositories(self):

        # Search query
        content = self.search_query()

        if not content or "items" not in content:
            return {}

        # Empty list to append the findings
        data  = []
        items = content["items"]
        
        for item in items:
            repo = {}
            
            if "repository" in item:
                if "name" in item["repository"]:
                    repo["name"] = item["repository"]["name"]
                
                if "html_url" in item["repository"]:
                    repo["link"] = item["repository"]["html_url"]
                
                if "contributors_url" in item["repository"]:
                    repo["contributors"] = self.get_contributors(item["repository"]["contributors_url"])
                
                if "commits_url" in item["repository"]:
                    repo["commit"] = self.get_commit(item["repository"]["commits_url"])
                
                # Append only when all data required are found and if it is not in data
                if sorted(["name", "link", "commit", "contributors"]) == sorted(list(repo)) and repo not in data:
                    data.append(repo)
            break
        return data

    def search(self):
        
        output = json.loads(default_output())

        try:
            data = self.get_repositories()

            if not data:
                return output

            final_output = self.get_output(data, output)

            if not final_output:
                return output
            
            print final_output["data"]
            # Search in clone repo to get sensitive data
            matched = git_grep(final_output["data"])
            print matched
            if matched:
                final_output["sensitive-info"] = matched
            
            return final_output

        except:
            traceback.print_exc()
            return output

    def run(self):
        
        return json.dumps((self.search()), indent=4)
