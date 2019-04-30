# coding:utf-8
import scrapy
import time 
import requests
import os
from scrapy.http import Request
#from tutorial.compression import The_compression

global false, null, true
false = null = true = ''

session = requests.Session() 
t = time.time() 

def timeqj(now_str1,now_str2):
    
    timeArray = time.strptime(now_str1 , "%Y-%m-%d")
    timeStamp = str(int(time.mktime(timeArray)))+"000"

    timeArray1 = time.strptime( now_str2+' 23:59:59' , "%Y-%m-%d %H:%M:%S")
    timeStamp1 = str(int(time.mktime(timeArray1)))+"999"

    return timeStamp,timeStamp1
now = time.strftime("%Y-%m-%d", time.localtime())
#xztime = timeqj(now,now)
#('1554480000000', '1554566399999')
print('请输入时间区间,如2019-04-08 2019-04-09以空格分开,然后按回车即可。不输入就直接回车,默认时间区间是今天。时间区间最好是最近的')
time_input = input()
if time_input == '': 
    xztime = timeqj(now,now)

else:    
    xztime = timeqj(time_input.split(' ')[0],time_input.split(' ')[1])

fb = open('cookie.txt','r').read()

dt = {}
for ii in fb.split(';'):
    dt[ii.split('=')[0]] = ii.split('=')[1]

#print(dt)

f = open('不常用.txt','r').readlines()
f1 = []
for n in f:
    if n != '\n' :
        #print(n)
        kl = n.replace('\n','') 
           
        f1.append(kl)

#print(type(f))

class RenrenSpider(scrapy.Spider):
    name = "renren"
    allowed_domains = ['www.szwego.com']
    start_urls = ['https://www.szwego.com']
    global xztime
    global f1
    global dt
    
    cookies = dt
    #print(cookies)
    
    imgint = 0
    
    lj = r'E:\代码\共享'
    
    pp = ['杜嘉班纳','DG','LV','驴家','高田贤三','kenzo','1v','路易威登','D*G','杜家','louis vuitton','Dolce & Gabbana','kz','DG.','Louis Vuitto*','D&G','路易威','L*V路易威登','L*V','kenz*','KEN','L*ouis Vuitton路*易威登','路*易威登','L*ouis Vuitton','LV路易威登','Louis Vuttion','L*ouis V*uitton','驴','路易','驴牌','L@V(路易威@登）','LV(路易威@）','DG（杜嘉班纳）','L# 路易威#','louis vuitton','Louis Vuitto＊??【路易威＊】','Louis Vuiton','LouisVuitton','KENZO','Loui*  Vitto*','LV 路易威*','Dolce&Gabbana','D*olce&G*abbana']#品牌黑名单
    
    shop_hs_list = f1

    cp_int = 0
    
    shop_list = []
    
    shop_int = 0
    
    jtling = xztime[0]

    jtshier = xztime[1]
    
    #tp = The_compression()

    def imgyz(self,urllist):
        dt = []
        for i in urllist:
            
            t_2 = session.get(i)
            
            if int(t_2.status_code) == 404:
                #print(i['link'])
                ink1 = i.split('_')[1]
                for e in range(1,100):
                    t_1 = session.get(i.replace(ink1,ink1.replace('00','%02d' % e)))
                    if int(t_1.status_code) == 200:
                        dt.append(i.replace(ink1,ink1.replace('00','%02d' % e)))         
            elif int(t_2.status_code) == 200:
                dt.append(i)  
                  
        return dt
    
    #获取店铺信息
    def start_requests(self):

        page1 = 0
        
        while True:

            page1 += 1
            if page1 == 15:

                return
            #time.sleep(2)
            print('店铺列表第',page1,'页')
            #https://www.szwego.com/service/album/get_album_list.jsp?act=attention&search_value=&page_index=1&tag_id=&_=1556154364200
            #https://www.szwego.com/service/album/get_album_list.jsp?act=attention&search_value=&page_index=14&tag_id=&_=1556153911610
            yield scrapy.Request(url='https://www.szwego.com/service/album/get_album_list.jsp?act=attention&search_value=&page_index='+str(page1)+'&tag_id=&_='+str(int(round(t * 1000))),cookies = self.cookies,callback=self.shop_text,dont_filter=True)

            #raise SystemExit

    #解析店铺数据 获取动态数据
    def shop_text(self,response):
        jxshop = eval(response.body)
        print(jxshop)
        if jxshop["result"]["shop_list"] == []:
            return
            
        #print(jxshop) 
           
        fa = jxshop["result"]["shop_list"]
        i = 0            

        page2 = 0
        while True:

            if page2 ==  20:
            #if page == 2:
                if i == (len(fa)-1):
                    break
                    return
                    
                i += 1
                page2 = 0
                continue
               
            shop_id = fa[i]['shop_id']
            shop_name = fa[i]['shop_name']
            #print(shop_name)
            page2 += 1
            if shop_name in self.shop_hs_list or shop_name == '我的相册' or shop_name in self.shop_list:
                i += 1
                page2 = 0
                continue
    
                 
            print('动态列表第',page2,'页') 
            
            yield scrapy.Request(url='https://www.szwego.com/service/album/get_album_themes_list.jsp?act=single_album&query_type=new&shop_id='+shop_id+'&search_value=&search_img=&start_date=&end_date=&tag=[]&page_index='+str(page2)+'&from_id=&_='+str(int(round(t * 1000))),cookies = self.cookies,callback=self.dynamic_text,dont_filter=True) 
            #print('1')
            
    #解析动态数据
    def dynamic_text(self,response):
        jxdynamic = eval(response.body)
        for i in jxdynamic["result"]["goods_list"]:
            dynamic_title = i['title']#动态文案
            if dynamic_title == '' or '视频' in dynamic_title or i['imgs'] == [] or i['videoUrl'] != '' or len(dynamic_title) <= 5:
                continue
                
            a = 0

            for n in self.pp:
                if n in dynamic_title:
                    a += 1
                    break

            if a == 1:        
                continue
                
            #print(dynamic_title)    
            dynamic_imgs  = i['imgsSrc']#动态全部图片
            if len(dynamic_imgs) < 5:
                continue
            
            dynamic_imglist = self.imgyz(dynamic_imgs)
            #print(dynamic_imglist)

            dynamic_time_stamp  = i['time_stamp']#动态的时间戳
            shop_name  = i['shop_name']#店铺名称
            if int(self.jtshier) <= int(dynamic_time_stamp):#大于等于23：59点时间
                self.shop_list.append(shop_name)
                break
                return
            if int(self.jtling) >= int(dynamic_time_stamp): 
                self.shop_list.append(shop_name)
                break
                return
            
            yield self.os_xz(shop_name,dynamic_time_stamp,dynamic_title,dynamic_imglist) 

    #创建店铺名称文件夹 创建动态时间戳文件夹 下载动态文案和图片
    def os_xz(self,shop_name,dynamic_time_stamp,dynamic_title,dynamic_imgs):
        if  shop_name not in os.listdir(self.lj):  

            os.makedirs(self.lj+'\\'+shop_name)


        if str(dynamic_time_stamp) not in os.listdir(self.lj+'\\'+shop_name):
            os.makedirs(self.lj+'\\'+shop_name+'\\'+str(dynamic_time_stamp))
        else: 
            return

        f_1 = open(self.lj+'\\'+shop_name+'\\'+str(dynamic_time_stamp)+'\\'+'1.txt' ,'wb')
        f_1.write(dynamic_title.encode()) 
        f_1.close()
        self.cp_int += 1
        print('第',self.cp_int,'套产品') 

        for n in dynamic_imgs: 
            self.imgint += 1
            print('第',self.imgint,'张图片')
            f_2 = open(self.lj+'\\'+shop_name+'\\'+str(dynamic_time_stamp)+'\\'+str(self.imgint)+'.jpg' ,'wb') 
            #print(n)
            #print(n.replace('86','800'))       
            try:
                requests.adapters.DEFAULT_RETRIES = 5         
                t_2 = session.get(n).content#获取图片链接的二进制源码          

            except:
                requests.adapters.DEFAULT_RETRIES = 5
                t_2 = session.get(n,timeout=30).content

            f_2.write(t_2)
            f_2.close()                  