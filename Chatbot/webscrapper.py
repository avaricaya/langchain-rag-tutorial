import argparse
import requests 
import markdownify
from bs4 import BeautifulSoup

def main():
    ##parses arguments (website url)
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="The URL.")
    args = parser.parse_args()
    url = args.url

    ##Gets webpage html
    response = requests.get(url) 
    text = response.text

    ##gets webpage title
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.title.string[0:20]

    ## convertes html to markdown
    md = markdownify.markdownify(text, heading_style="ATX") 

    ##prints markdown to indicated path
    path = "cs_data/" + title +".md"
    with open(path, 'w') as file:
        file.write(md)
        
    


if __name__ == "__main__":
    main()