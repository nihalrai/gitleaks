import re
import os
import json
import subprocess
import hashlib
import traceback

# Git binary path
GIT_PATH = "/usr/bin/git"

# Threads count required to clone repositories
thread_count = 5


def default_output():

    return json.dumps({
        "tool": "gitleaks",
        "type": "failure",
        "data": "",
        "error": ""
    })


def run_command(command):
    
    try:
        cmd    = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        output = cmd.communicate()
        
        if cmd.returncode != 0 or output[1]:
            return False
        
        return (output[0].strip("\n"))
    except:
        traceback.print_exc()
        return False


def make_folder(file_name):
    
    path = os.path.join("/tmp", hashlib.sha1(file_name).hexdigest())
    
    if os.path.exists(path):
        return path
    
    run_command("mkdir %s" % (path))

    if not os.path.exists(path):
        return False
    
    return path


def clone_repo(repo_data, folder):
        
    # Count the clone success
    count = 0
    
    for data in repo_data:
        try:
            link = data["link"] + ".git"
            repo_name = link.split("/")[-1].replace(".git", "")
            filename = os.path.join(folder, repo_name)
            
            # Check for last commit if repo already cloned already present using git rev-parse HEAD
            # https://stackoverflow.com/questions/949314/how-to-retrieve-the-hash-for-the-current-commit-in-git
            if os.path.exists(filename):
                try:
                    last_commit = run_command("%s -C %s rev-parse HEAD" % (GIT_PATH, filename))

                    # run_command method returns bool type if failed
                    last_commit = last_commit.strip("\n") if type(last_commit) == str else ""
                    # Hash of last commit and detected commit will be equate to avoid same commit
                    if last_commit and (data["commit"] == last_commit):
                        print ("Not cloning %s " % (link))
                        count += 1
                        data["cloned"] = "True"
                        data["cloned-path"] = filename
                        continue

                    # HEAD means the repo is either not completely cloned or the git tree is not correct
                    if last_commit == "HEAD":
                        run_command("rm -rf %s" % (filename))
                    
                    # Delete the file if exist but last commit is not equal to the 
                    # cloned latest commit therefor reclone it.
                    run_command("rm -rf %s" % (filename))

                except:
                    traceback.print_exc()
                    continue
                
            clone = run_command("%s clone %s %s" % (GIT_PATH, link, filename))

            if clone:
                count += 1
                data["cloned"] = "True"
                data["cloned-path"] = filename

        except:
            traceback.print_exc()
            continue

    return count, repo_data


def git_grep(repo_data):
    
    # Grep output to return
    output = {}
    # List of repo_path
    repo_path = []

    for data in repo_data:
        if data.has_key("cloned-path"):
            repo_path.append(data["cloned-path"])

    # https://github.com/dxa4481/truffleHog/blob/dev/scripts/searchOrg.py#L10
    search = {
        "regex": {
            "subdomain": r"/^[a-zA-Z0-9][a-zA-Z0-9.-]+[a-zA-Z0-9]$/",
            "slack-token": r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
            "aws-keys": r"AKIA[0-9A-Z]{16}",
            "email-id": r"\S+@\S+"
        },
        "patterns": [
            "password",
            "credentials",
            "username",
            "*.api.*",
            "*.key.*",
            "token"
        ]
    }

    for key, value in search["regex"].items():
        match = []
        for data in repo_data:
            repo_path = data["cloned-path"]
            result = run_command("%s -C %s grep -i %s" % (GIT_PATH, repo_path, value))
            if result:
                match.append(result)
        if len(match) > 0:
            output[key] = match

    match = []
    for value in search["patterns"]:
        for data in repo_data:
            repo_path = data["cloned-path"]
            result = run_command("%s -C %s grep -i -e %s" % (GIT_PATH, repo_path, value))
            if result and type(result) == dict:
                match.append(result)
    output["patterns-match"] = match

    return output
