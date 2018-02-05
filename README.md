# national_data_spider

---

<h3 id="Process">进度</h3>

* 进度
    * 2018-02-05
        * 完成MySQL和MongoDB的写入方法可以将数据写入到数据库中

    * 2018-01-28
        * 临时在请求里面加了一个参数可以获取任意年份区间的数据
    
    * 2018-01-28
        * MySQL,MongoDB的写入都已经完成(分类爬虫,数据爬虫的待完成)
        * MySQL和MongoDB双数据源可以通过conf/db.json中的Enable字段进行启用/关闭

    * 2018-01-24
        * 更新一部分代码
            * 解决此前的log文件位置不正确的问题
            * 加入了MySQL的配置(暂时不支持表名自定义, 数据库名可以自定义)
    
    * 2018-01-22
        * 上传代码发布第一版测试
        
    * 2018-01-20
        * 搁置了两个礼拜终于弄有空弄一下了
        * 目前完成了年度数据的接口
            
    * 2017-12-28
        * 暂时搁浅
        * 原因:
            ```html
            一开始很难说清楚是啥问题(后来查明白是参数的问题)
            奇怪的是网页的请求的参数一模一样，reqUrl也一样都没用
            是我在reqUrl上修改了一个参数与之和header里面的对应就可以了
            ```

---

<h3 id="Structure">项目结构</h3>

```python

# national_data_spider --- (根目录)
## conf --- (配置文件夹)
## db_connect --- (数据库连接类)
## logger --- (日志中心)
## spiders --- (爬虫类)
## utils --- (工具类)
# starter.py --- (启动类)

```

---

<h3 id="Guide">使用说明</h3>

* Python版本: Python 3.4.4
* 系统版本: Windows 10 x64
* MongoDB数据库版本: MongoDB 3.4.6
* Python库:
    * pymysql：
    * pymongo: 3.6.0
    * requests: 2.18.4
* 数据库暂时只支持MongoDB. MySQL会在下个版本支持

```Bash
    # 启动方法(根目录输入命令)
    # windows下默认python3环境的就
    python starter.py 
    
    # linux下存在python3的
    python3 starter.py 
    
    # 接下来就是命令参数了
    -c 或者 --category: 爬去分类的json存储到数据库(功能已完善)
    -i 或者 --pid: 获取某个id下的数据存储到数据库(暂时还有点鸡肋)
```

<h3 id="Configuration">配置说明</h3>

* 配置文件在conf文件夹中(可以完全自定义MySQL和MongoDB)
* 默认开启MongoDB和MySQL的连接

---

<h3 id="Chat">题外话</h3>

* 可能会查水表的爬虫~ Url就不说了自己去里面转一下吧

---

<h3 id="Future">后续开发</h3>

* ~~后续完善MongoDB数据库的连接使用~~
* ~~开发MySQL的连接~~
* 分类爬虫数据支持写入到excel导出(导出Excel这个待完成)
* ~~数据爬虫的MySQL和MongoDB写入待完成~~