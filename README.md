# BilibiliSuitBuy [b站装扮购买]

**B站装扮购买全模拟(96%) [有效]**

需要把python升级到3.10.x

**不想更新了，希望这个主打python语言socket库的购买脚本可以帮助到你，水视频去了**

------------------------------------------------

**听说是理论最快，我是找不到还有比socket还快的方法了，平均40ms-90ms，而标准库同地区延迟普遍在100ms-200ms之间，高下立判**

**此装扮购买脚本本体不包括计时器、登陆、自动读取开售时间等操作**

**但写还是会写出来放在单独的文件里，要用的话自己搭积木**

**什么年代了还在用传统http请求库**

**socket实现，包括计时器**

**我大意了啊，没有闪fiddler classic不支持http2.0，都是http1.1**

**此装扮购买脚本使用的均为http1.1, 不过2.0向下兼容1.1问题不大**

已经没有意思了，不更新了，玉玉了，有比socket更快的方法再叫我回来

------------------------------------------------

**特点：**

不要再把这个脚本和外面那些用http标准库的脚本搞混

我这个用的是socket，不是requests或者net/http那些

你可以使用socket来提前进行和服务器的数据交换

而不是等待倒计时结束才开始创建一个tcp，然后开始数据交换

我们都知道HTTP协议是基于TCP协议的应用层传输协议

说到TCP是否可以使用socket来提前进行连接

客户端这边时间一到就直接发送报文

再优化优化，提前生成报文头和报文体啥的

再把整个报文切割成 n-1 : 1 的大小

这样我们可以提前连接后再提前发送那n-1的报文

等待开售时间一到我们只需要发送那1bit的数据

这样我们就把原本开售时间到后繁琐的步骤简化为只需要发送1bit数据，然后接收响应就行

------------------------------------------------

- [x] **qr code login**
- [x] **access_key**
- [x] **cookies**
- [x] **x-bili-aurora-eid**
- [x] **x-bili-trace-id**
- [ ] **HTTP2.0**

------------------------------------------------

<font size=4>**运行（python-socket）：**</font>

```

# ./python/buy-requests.py

def main():
    suit_buy = SuitBuy(
        http_message_file="./message/message.txt",

        # 可选
        add_month="-1",
        buy_num="1",
        coupon_token="",
        host="api.bilibili.com",
        f_source="shop",
        shop_from="feed.card",
        sale_time=round(time.time())
    )

    # 跳出本地计时器后
    
    suit_buy.Link()  # 连接到服务器
    suit_buy.SendMessageHeader()  # 提前发送数据
    
    # 等待服务器计时退出后
    
    suit_buy.SendMessageBody()  # 发送剩余数据
    response = suit_buy.Receive()  # 接收响应
    print(response)


if __name__ == '__main__':
    main()
```

不急一个一个看

| key               | value       | default          |
|-------------------|-------------|------------------|
| http_message_file | fiddler报文路径 | None             |
| add_month         | 购买时长        | -1               |
| buy_num           | 购买数量        | 1                |
| host              | 地址          | api.bilibili.com |
| f_source          | 购买源头        | shop             |
| shop_from         | 进入源头        | feed.card        |
| sale_time         | 购买/开售 时间    | 当前时间             |
| coupon_token      | 优惠卷         | None             |

这次舍弃了很多不必要的参数, 只需要填写```http_message_file```的值即可运行

相比requests库来实现简化了更多步骤

**抓包教程最下面有**

------------------------------------------------

~~<font size=4>**运行（python-requests）：**</font>~~

~~弃了，太慢了，虽然还是比绿色用户快就是~~

~~安装 ```requests``` ``` pip install requests ```~~

~~同python-socket~~

------------------------------------------------
<font size=4>**运行（golang-socket）：**</font>

~~你这go怎么这么像python啊~~

~~ssl可能还存在问题，但python版的应该没啥了~~

```
func main() {
	var FilePath string = "./buy_suit/http-message/HTTP1.1Message.txt" // 报文文件路径
	var SaleTime = time.Now().Unix()                                   // 装扮开售时间

	var config *Config = &DefaultConfig
	(*config).Host = "api.bilibili.com"
	(*config).ShopFrom = "feed.card"
	(*config).FSource = "shop"
	(*config).BuyNum = 1
	(*config).AddMonth = -1
	(*config).CouponToken = ""

	var SuitBuyC *SuitBuy = new(SuitBuy).init(FilePath, SaleTime, config)

	// 跳出本地计时器

	SuitBuyC.LinkSever()  // 连接到服务器
	SuitBuyC.SendHeader() // 发送n-1的头数据

	// 跳出服务器计时器

	SuitBuyC.SendBody() // 发出剩下的数据

	// 打印响应
	var Response string = SuitBuyC.ReceiveResponse()
	fmt.Printf("%v", Response)
}
```

| key                   | value       | default           |
|-----------------------|-------------|-------------------|
| FilePath          | fiddler报文路径 | None              |
| SaleTime    | 购买/开售 时间    | time.Now().Unix() |
| (*config).AddMonth    | 购买时长        | -1                |
| (*config).BuyNum      | 购买数量        | 1                 |
| (*config).Host        | 地址          | api.bilibili.com  |
| (*config).FSource     | 购买源头        | shop              |
| (*config).ShopFrom    | 进入源头        | feed.card         |
| (*config).CouponToken | 优惠卷         | None              |

**抓包教程最下面有**

------------------------------------------------

**抓包教程：**

~~[抓包教程(新)](https://www.bilibili.com/video/BV1Re411g7f5/)先看着，有时间找个新电脑录个~~

锁定url为 ```/x/garb/v2/mall/suit/detail``` 的包, 选中后点击 ```Raw```

```ctrl+a```全选```ctrl+c```复制, 然后创建一个文本文件```ctrl+v```粘贴进去 最后```ctrl+s```保存

保存的文件就是http报文的文件

------------------------------------------------

**参考**

[test/http2-test.py](https://python-hyper.org/projects/h2/en/stable/plain-sockets-example.html)

------------------------------------------------

**总结：**

**python-sokcet-buy 2022/09/08-now **

**python-requests-buy 2022/01/13-now **

你先百度百度http1.x到http2都是基于什么的再说哪个脚本快啥的，这根本就不是一个类型

你问我为什么不开，我没钱，我没账号，我没设备，我没渠道，我啥都没有，我开个✓8

~~不是我说， [爬娘](https://space.bilibili.com/647193094)真的是，只有被人举办的才封，演起来没动的屁事没有~~

~~？你先开的~~

~~多线程 / 异步是错误的~~
