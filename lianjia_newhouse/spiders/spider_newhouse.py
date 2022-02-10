# -*- coding: utf-8 -*-
import scrapy,math,re
from lianjia_newhouse.items import LianjiaNewhouseItem


class SpiderNewhouseSpider(scrapy.Spider):
    name = 'spider_newhouse'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']
    count = 0
    city_count = 0
    access_city_list = []
    area_name_flag = False

    def parse(self, response):
        province_city_divs = response.xpath("//div[@class='city_province']")
        for province_city_li in province_city_divs:
            province = province_city_li.xpath(".//div[@class='city_list_tit c_b']/text()").get()
            if province == '安徽':
            # if True:
                city_lis = province_city_li.xpath("./ul/li")
                for li in city_lis:
                    self.city_count+=1
                    # print('city_count',self.city_count)
                    city = li.xpath("./a/text()").get()
                    city_url = li.xpath("./a/@href").get()
                    city_no = city_url.split('//')[1].split('.')[0]
                    if city_no == 'hf':
                    # if True:
                        request_url = 'https://'+city_no+'.fang.lianjia.com/loupan/'
                        yield scrapy.Request(request_url, meta={'info':(province, city, city_url, city_no, request_url)}, callback=self.access_city)

    def access_city(self, response):
        province, city, city_url, city_no, request_url = response.meta.get('info')
        if request_url == response.url:
            self.access_city_list.append(city)
            city_area = response.xpath("//div[@class='filter-by-area-container']/ul/li")
            # total_area_sales_count = response.xpath("//div[@class='resblock-have-find']/span[@class='value']")
            # if total_area_sales_count:
            #     total_area_sales_count = int(total_area_sales_count.xpath("./text()").get())
            # else:
            #     total_area_sales_count = 0
            area_sales_count = 0
            find_str = response.text.find('为您找到')
            if find_str != -1:
                b = re.search(r'''<span class="value ">\d+</span>''', response.text)
                total_area_sales_count = re.search(r'\d+', b.group()).group()
                total_area_sales_count = int(total_area_sales_count)
                print(total_area_sales_count)
                print(response.url)
                print('---------------------------------------------------------------------')
            if city_area:
                for area in city_area:
                    self.count+=1
                    area_name = area.xpath("./text()").get()
                    area_end_url = area.xpath("./@data-district-spell").get()
                    area_end_url = response.urljoin(area_end_url)
                    yield scrapy.Request(area_end_url, meta={'info': (total_area_sales_count, province, city, area_name)}, callback=self.get_url_for_page)
            else:
                self.area_name_flag = True
                self.get_url_for_page(response)

    def get_url_for_page(self, response):
        total_area_sales_count, province, city, area_name = response.meta.get('info')
        if self.area_name_flag:
            area_name = ''
            self.area_name_flag = False

        area_sales_count = 0
        find_str = response.text.find('为您找到')
        if find_str != -1:
            b = re.search(r'''<span class="value ">\d+</span>''', response.text)
            area_sales_count = re.search(r'\d+', b.group()).group()
            area_sales_count = int(area_sales_count)
            print(area_sales_count)
            print(response.url)
            print('---------------------------------------------------------------------')
        if area_sales_count > 0:
            total_page = math.ceil(area_sales_count/10)
            page_index = 1
            page_url = response.url+'/pg'
            area_detail_url = page_url+str(page_index)
            yield scrapy.Request(area_detail_url, meta={'total_area_sales_count':total_area_sales_count,'area_sales_count':area_sales_count,
                                                        'province':province, 'city':city, 'area_name':area_name,
                                                        'page_index':page_index, 'total_page':total_page,
                                                        'page_url':page_url},
                                 callback=self.get_detail_for_page)

    def get_detail_for_page(self, response):
        province = response.meta.get('province')
        city = response.meta.get('city')
        total_area_sales_count = response.meta.get('total_area_sales_count')
        area_sales_count = response.meta.get('area_sales_count')
        area_name = response.meta.get('area_name')

        page_url = response.meta.get('page_url')
        page_index = int(response.meta.get('page_index'))
        total_page = int(response.meta.get('total_page'))
        print(response.url, page_index)

        xiaoqu_lis = response.xpath("//ul[@class='resblock-list-wrapper']/li")
        for li in xiaoqu_lis:
            xiaoqu_name = li.xpath(".//div[@class='resblock-name']/a")
            if xiaoqu_name:
                xiaoqu_name = xiaoqu_name.xpath("./text()").get()
            else:
                xiaoqu_name = ''
            xiaoqu_price = li.xpath(".//div[@class='main-price']/span[@class='number']")
            if xiaoqu_price:
                xiaoqu_price = xiaoqu_price.xpath("./text()").get()
            else:
                xiaoqu_price = ''
            price_danwei = li.xpath(".//div[@class='main-price']/span[@class='desc']")
            if price_danwei:
                price_danwei = price_danwei.xpath("./text()").get().replace(' ', '')
            else:
                price_danwei = ''
            xiaoqu_address = ''
            detail_url = response.urljoin(li.xpath(".//div[@class='resblock-name']/a/@href").get())
            xiaoqu_address_list = li.xpath(".//div[@class='resblock-location']//text()").getall()
            if xiaoqu_address_list:
                for address in xiaoqu_address_list:
                    a = address.replace(' ', '').replace('\n', '')
                    xiaoqu_address += a
                # print(province, city, total_area_sales_count, area_name, area_sales_count, xiaoqu_name, xiaoqu_price+price_danwei, xiaoqu_address)
            else:
                xiaoqu_address = ''
            item = LianjiaNewhouseItem(
                province=province,
                city=city,
                total_sales=total_area_sales_count,
                area_name=area_name,
                area_sales=area_sales_count,
                xiaoqu_name=xiaoqu_name,
                xiaoqu_price=xiaoqu_price,
                xiaoqu_address=xiaoqu_address,
                price_danwei=price_danwei,
                page_url=response.url,
                detail_url=detail_url
            )
            yield item
        page_index += 1
        if page_index <= total_page:
            yield scrapy.Request(page_url+str(page_index), meta={'total_area_sales_count': total_area_sales_count,
                                                        'area_sales_count': area_sales_count,
                                                        'province': province, 'city': city, 'area_name': area_name,
                                                        'page_index': page_index, 'total_page': total_page,
                                                        'page_url': page_url},
                                 callback=self.get_detail_for_page)
