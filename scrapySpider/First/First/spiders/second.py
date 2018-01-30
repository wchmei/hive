import scrapy
from First.items import FirstItem

class Lagou(scrapy.Spider):
    name = "sean"
    start_urls = [
        "https://www.lagou.com/"
    ]

    cookie = {
        'user_trace_token': '20180125171249-e9fd92ef-01af-11e8-9b13-525400f775ce',
        'LGUID': '20180125171249-e9fd95ac-01af-11e8-9b13-525400f775ce',
        'index_location_city' : '%E5%85%A8%E5%9B%BD',
        'JSESSIONID' : 'ABAAABAAAIAACBI12C18146575F6E864E976386E7CDF11A',
        '_gid' : 'GA1.2.710431785.1517274340',
        'LGSID' : '20180130145254-323cde27-058a-11e8-a0f2-525400f775ce',
        'PRE_UTM' : '',
        'PRE_HOST' : 'blog.csdn.net',
        'PRE_SITE' : 'http%3A%2F%2Fblog.csdn.net%2Fdangsh_%2Farticle%2Fdetails%2F78587729',
        'PRE_LAND' : 'https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F',
        'SEARCH_ID' : '26434cfc03bd497b89c1d78798a2c9db',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6' : '1517274340,1517295174,1517295224,1517295233',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6' : '1517295233',
        'LGRID' : '20180130145353-557a33c1-058a-11e8-a0f2-525400f775ce'}
    def parse(self , response):
        for item in response.xpath('//div[@class="menu_box"]/div/dl/dd/a'):
            jobClass = item.xpath('text()').extract()
            jobUrl = item.xpath("@href").extract_first()

            oneItem = FirstItem()
            oneItem["jobClass"] = jobClass
            oneItem["jobUrl"] = jobUrl
            # print(jobUrl)
            # yield oneItem

            # jobUrl https://www.lagou.com/zhaopin/Java/2/?filterOption=3
            # https://www.lagou.com/zhaopin/Java/
            # print(jobUrl)
            for i in range(30):
                
                jobUrl2 = jobUrl + str(i+1)
                # print(jobUrl2)
                try:
                    yield scrapy.Request(url = jobUrl2  ,cookies=self.cookie , meta = {"jobClass":jobClass} , callback=self.parse_url)
                except:
                    pass
                    
    def parse_url(self , response):
        jobClass = response.meta["jobClass"]

        # print(title)
        for sel2 in response.xpath('//ul[@class="item_con_list"]/li'):
            jobName = sel2.xpath('div/div/div/a/h3/text()').extract()
            jobPlace = sel2.xpath('div/div/div/a/span/em/text()').extract()
            jobMoney = sel2.xpath('div/div/div/div/span/text()').extract()
            jobNeed = sel2.xpath('div/div/div/div/text()').extract() 
            jobNeed = jobNeed[2].strip() 
            jobCompany = sel2.xpath('div/div/div/a/text()').extract()
            jobCompany =jobCompany[3].strip()


            jobType = sel2.xpath('div/div/div/text()').extract()
            jobType = jobType[7].strip()

            jobSpesk = sel2.xpath('div[@class="list_item_bot"]/div/text()').extract()
            jobSpesk =jobSpesk[-1].strip()



            Item = FirstItem()
            Item["jobName"] = jobName
            Item["jobPlace"] = jobPlace
            Item["jobMoney"] = jobMoney
            Item["jobNeed"] = jobNeed
            Item["jobCompany"] = jobCompany
            Item["jobType"] = jobType
            Item["jobSpesk"] = jobSpesk
            # print(oneItem["jobName"])
            yield Item
            

            