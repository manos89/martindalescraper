import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import XMLFeedSpider
import xmltodict,json,time,re

from martindale.items import MartindaleItem


class QuotesSpider(scrapy.Spider):
    name = "martindale"




    def start_requests(self):
        self.urls=[]
        self.cities=[]
        starting_url="https://www.martindale.com/sitemap_profiles.xml"
        yield scrapy.Request(url=starting_url, callback=self.parse_first_xml,priority=1)
        self.urls=list(set(self.urls))

        # for url in self.urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        Established=""
        try:
            exp_classes=response.css("div.experience-section")
        except:
            exp_classes=[]
        for exp in exp_classes:
            lbl=exp.css("div.experience-label::text").extract_first()
            if "Established" in lbl:
                Established=exp.css("div.experience-value::text").extract_first()
        data_found=re.search('d\+json">.+} <', response.body.strip().replace("\n",""))
        json_data=(str(data_found.group(0)).replace('d+json"> ',''))
        End=json_data.find("</script>")
        json_data=json_data[:End]
        json_data=json.loads(json_data)
        l = ItemLoader(item=MartindaleItem(), response=response)
        l.add_value('url', response.request.url)
        l.add_value('name', json_data["name"])
        try:
            l.add_value('people1', json_data["employee"][0]["name"]+"|"+json_data["employee"][0]["jobTitle"])
        except:
            l.add_value('people1', "")
        try:
            l.add_value('people2', json_data["employee"][1]["name"]+"|"+json_data["employee"][1]["jobTitle"])
        except:
            l.add_value('people2', "")
        try:
            l.add_value('people3', json_data["employee"][2]["name"]+"|"+json_data["employee"][2]["jobTitle"])
        except:
            l.add_value('people3', "")
        try:
            l.add_value('first_name', json_data["employee"][0]["name"].split(" ")[0])
        except:
            l.add_value('first_name', "")
        l.add_value('year_established', Established)
        try:
            l.add_value('size', len(json_data["employee"]))
        except:
            l.add_value('size',"")
        l.add_value('practises', ','.join(json_data["makesOffer"]))
        try:
            l.add_value('phone1', json_data["telephone"][0])
        except:
            l.add_value('phone1', "")
        try:
            l.add_value('phone2', json_data["telephone"][1])
        except:
            l.add_value('phone2', "")
        l.add_value('website', json_data["sameAs"])
        try:
            l.add_value('county', json_data["address"]["addressCountry"])
        except:
            l.add_value('county', "")
        try:
            l.add_value('postal_code', json_data["address"]["postalCode"])
        except:
            l.add_value('postal_code', "")
        try:
            l.add_value('town', json_data["address"]["addressLocality"])
        except:
            l.add_value('town', "")
        try:
            l.add_value('stars', json_data["aggregateRating"]["ratingValue"])
        except:
            l.add_value('stars', "")
        try:
            l.add_value('number_of_stars', json_data["aggregateRating"]["reviewCount"])
        except:
            l.add_value('number_of_stars', "")
        l.add_value('recommendation_number', "")
        l.add_value('recommendation_percentage', "")
        return l.load_item()


    def parse_first_xml(self, response):
        obj = xmltodict.parse(response.body)
        monString = json.dumps(obj)
        json_data = json.loads(monString)
        for d in json_data["sitemapindex"]["sitemap"]:
            if "firm_usa" in d["loc"]:
                yield scrapy.Request(url=d["loc"], callback=self.parse_second_xml)


    def parse_second_xml(self, response):
        obj = xmltodict.parse(response.body)
        monString = json.dumps(obj)
        json_data = json.loads(monString)
        for d in json_data["urlset"]["url"]:
            yield scrapy.Request(url=d["loc"], callback=self.parse)
            self.urls.append(d["loc"])
            print(len(self.urls))
