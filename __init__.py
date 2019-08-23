import os
import json
import urllib
import hashlib
import requests
import traceback
import subprocess

from gitleaks_tool.utils import default_output, run_command, make_folder, clone_repo, git_grep

AUTHOR = {
    "name": "NIHAL RAI"
}

# Github api url from searching code
API = "https://api.github.com/search/code?"


class Gitleaks:
    def __init__(self, query, token):

        self.query = query
        self.token = token

    def get_tool_name(self):
        
        return {
                "tool-name": "gitleak"
            }

    def send_request(self, url):

        headers = {"Authorization": "token %s" % (self.token)}
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=20)

        if response.status_code in range(200,300):
            return json.loads(response.content)
        
        return {}

    def search_query(self):

        query = urllib.urlencode({'q': '%s' % (self.query)})
        url = API + query

        return self.send_request(url)

    def get_commit(self, commits_url):

        commits_url = commits_url.replace("{/sha}", "/master")
        contents = self.send_request(commits_url)
        
        # Response of commits_url is a list of details of all commits
        if not contents or not contents.has_key("sha"):
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
            if content.has_key("login"):
                data["name"] = content["login"]
            if content.has_key("html_url"):
                data["link"] = content["html_url"]
            if content.has_key("contributions"):
                data["contributions"] = content["contributions"]
            
            if data.has_key("name") and data.has_key("link") and data.has_key("contributions"):
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

        if not content or not content.has_key("items"):
            return {}

        # Empty list to append the findings
        data = []

        items = content["items"]
        
        for item in items:
            repo = {}
            
            if item.has_key("repository"):
                if item["repository"].has_key("name"):
                    repo["name"] = item["repository"]["name"]
                
                if item["repository"].has_key("html_url"):
                    repo["link"] = item["repository"]["html_url"]
                    
                if item["repository"].has_key("contributors_url"):
                    repo["contributors"] = self.get_contributors(item["repository"]["contributors_url"])
                
                if item["repository"].has_key("commits_url"):
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
        