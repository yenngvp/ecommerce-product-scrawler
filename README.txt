
ProductZ project
Goal: Building spiders for crawling products from e-commerce web sites. Then it will be integrated to ProjectGo functionality.



redis-cli -p 3679
config set stop-writes-on-bgsave-error no
source ~/go.sh

== 1-1
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=0 -a val2=14 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=0 -a val2=14 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=0 -a val2=14 -a pdomain=adayroi.com product

== 1-2
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=15 -a val2=29 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=15 -a val2=29 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=15 -a val2=29 -a pdomain=adayroi.com product

== 1-3
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=30 -a val2=44 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=30 -a val2=44 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=30 -a val2=44 -a pdomain=adayroi.com product

== 1-4
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=45 -a val2=59 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=45 -a val2=59 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=45 -a val2=50 -a pdomain=adayroi.com product

== 1-5
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=60 -a val2=74 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=60 -a val2=74 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=60 -a val2=74 -a pdomain=adayroi.com product

== 1-6
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=75 -a val2=89 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=75 -a val2=89 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=75 -a val2=89 -a pdomain=adayroi.com product

== 1-7
screen -S lazada
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=90 -a val2=100 -a pdomain=lazada.vn product
screen -S tiki
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=90 -a val2=100 -a pdomain=tiki.vn product
screen -S adayroi
scrapy crawl -a host_id=1 -a thread_id=1 -a val1=90 -a val2=100 -a pdomain=adayroi.com product