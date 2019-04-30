# 001
使用Scrapy 爬取自己已关注店铺的动态（文案和图片），可以添加店铺黑名单和品牌黑名单，还可以手动设置时间区间
spiders目录下
/spiders
  __init__.py
  cookie.txt
  szwego.py
  不常用.txt
  
cookie.txt 保存自己微商相册cookie的txt (使用Scrapy登陆后的cookie是不完整的cookie）
szwego.py 爬虫程序
不常用.txt 店铺黑名单
品牌黑名单在代码里面设置 是个变量
