import requests
import lxml.html
import json
import re
 
url = 'https://www.hyperia.sk'
karieraurl = "/kariera"

class Positions:
    #get the url
    def __init__(self,url):
        self.url = url + karieraurl

    #returns the document from the site
    def getDoc(self):
        response = requests.get(self.url)
        return lxml.html.fromstring(response.content.decode("utf-8"))

    #gathers data from the site
    def getInfo(self):
        section = self.getDoc().xpath('//section[@id="positions"]')[0]
        self.text = section.xpath('.//div/div/div/h3/text()')
        self.links = section.xpath('.//div/div/div/div/a/@href')

        #gathers details for each position
        self.positions = list()
        for i in range(len(self.links)):
            self.positions.append(Details(url + self.links[i]))
            self.positions[i].getInfo()

    #formats the data into a dictionary
    def formatData(self):
        self.data = [{"title" : title, "place" : ' '.join(position.location), "salary" : ' '.join(position.salary), "contract_type" : ' '.join(position.contract), "contact_email" : position.email}
            for title,position in zip(self.text,self.positions)
        ]
    
    #writes the dictionary into a json file
    def writeData(self):
        res = json.dumps(self.data, indent=4, ensure_ascii=False).encode('utf8')
        f = open('positions.json', 'w')
        f.write(res.decode())
        f.close()

class Details(Positions):
    def __init__(self,url):
        self.url = url

    #similar as in parent class
    def getInfo(self):
        section = self.getDoc().xpath('//section[@class="position-hero"]')[0]
        self.location = section.xpath('./div/div/div/div[1]/p/text()')
        self.salary = section.xpath('./div/div/div/div[2]/p/text()')
        self.contract = section.xpath('./div/div/div/div[3]/p/text()')
        self.email = self.getEmail()
        
    #using regex we find the email adress 
    def getEmail(self):
        self.rawEmail = self.getDoc().xpath('//div[@class="container position-contact"]')[0]
        self.rawEmail = re.search(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.rawEmail.text_content())
        return self.rawEmail.group()

positions = Positions(url)
print("Gathering data...")
positions.getInfo()
print("Formatting...")
positions.formatData()
print("Writing...")
positions.writeData()
print("Done!")

