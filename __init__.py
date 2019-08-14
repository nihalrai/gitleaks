import os
import json
import urllib
import hashlib
import requests
import traceback
import subprocess

AUTHOR = {
    "name": "NIHAL RAI"
}


class Gitleaks:
    def __init__(self, query, token):

        self.query = query
        self.token = token

    def default_output(self):
        
        return json.dumps({
                "tool": "gitleaks",
                "type": "failure",
                "data": "",
                "error": ""
            })

    def get_tool_name(self):
        
        return {
                "tool-name": "gitleak"
            }
    
    def run_command(self, command):
        cmd       = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        cmd.wait()
        
        output, _ = cmd.communicate()

        print output, _
        
        if cmd.returncode != 0:
            return False
    
        return True
    
    def make_folder(self):
        
        path = os.path.join("/tmp", hashlib.sha1(self.query).hexdigest())
        
        if os.path.exists(path):
            self.run_command("rm -rf %s" % (path))
        
        self.run_command("mkdir %s" % (path))

        if not os.path.exists(path):
            return False
        
        return path

    def clone_repo(self, repo_data, folder):
        
        # Git binary path
        GIT_PATH = "/usr/bin/git"
        # Count the clone succes
        count = 0

        for data in repo_data:
            try:
                link = data["link"] + ".git"
                repo_name = link.split("/")[-1].replace(".git", "")
                filename = os.path.join(folder, repo_name)

                clone = self.run_command("%s clone %s %s" % (GIT_PATH, link, filename))

                if clone:
                    count += 1
            except:
                traceback.print_exc()
                continue

        return count

    def send_request(self, url):

        headers = {"Authorization": "token %s" % (self.token)}
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=20)

        if response.status_code in range(200,300):
            return json.loads(response.content)
        
        return {}

    def search_query(self):

        query = urllib.urlencode({'q': '%s' % (self.query)})
        url = "https://api.github.com/search/code?" + query

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

                # Append only all data required are found
                if sorted(["name", "link", "commit", "contributors"]) == sorted(list(repo)) and repo not in data:
                    data.append(repo)
                print repo
        
        # Create a unique folder using sha1 hash of self.query
        folder = self.make_folder()

        if folder:
            count  = self.clone_repo(data, folder)
        else:
            count = 0

        return data, count

    def search(self):
        
        output = json.loads(self.default_output())
        try:
            data, count = self.get_repositories()
            
            if not data:
                return output
                
            output["type"] = "success"
            output["data"] = data
            output["clone-stats"] = "%s of %s are cloned" % (count, len(data))
            
            return output
        
        except:
            traceback.print_exc()
            return output

    def run(self):
        
        return json.dumps((self.search()), indent=4)
        