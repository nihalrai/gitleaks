import json
import time
import random
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    url = "https://github.com/search?q="
    keywords = ["godigit", "godisit", "go"]
    data = []
    i = 1
    while(i < 100):
        new_url = url + random.choice(keywords)
        response = requests.get(new_url, verify=False, allow_redirects=True, timeout=10)
        
        if response.status_code == 429:
            time.sleep(30)
            response = requests.get(new_url, verify=False, allow_redirects=True, timeout=10)
        
        data_s = ({
            "url": new_url,
            "status": response.status_code
        })
        i = i + 1
        data.append(data_s)
        print data_s
    print data

if __name__ == "__main__":
    main()