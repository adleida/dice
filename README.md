dice
====

### 安装:
```bash
$ git clone https://github.com/adleida/dice.git
$ cd dice
$ sudo python3 setup.py install
$ sudo pip install httpie
```
### 帮助系统:
```bash
$ dice -h
```
>- *-p:* 指定dice运行时的port(默认值为: 6060)
>- *-c:* 指定dice运行时的config文件(默认为:/usr/local/lib/python3.4/dist-packages/dice/res/dice.yaml)
>- *-v:* 获取dice 当前的版本号

### 运行:
```bash
$ dice -p 6001
```

### Restful API:
**1. 查看dice 是否正常运行**
```
url: localhost:6001/v1/
method: GET
```
**ex:**
```bash
$ http GET http://localhost:6001/v1/
```
若接受到以下信息，表明dice已经启动：
```
HTTP/1.0 200 OK
Content-Length: 87
Content-Type: application/json
Date: Wed, 10 Jun 2015 09:27:24 GMT
Server: Werkzeug/0.10.4 Python/3.4.2

{
    "Message": "WELCOME TO AD DICE",
    "time stamp": 1433928444.4769697,
    "version": "0.0.3"
}
```
**2. 向dice 发送bid request**
```
url: localhost:6001/v1/bid/<did:string>
method: POST
```

1. 若POST data 为空，dice 返回403：

**ex:**
```bash
$ http POST http://localhost:6001/v1/bid/123 
```
**response:**
```
{
    "message": "Forbidden",
    "status": 403
}
```
2. url中 的did在adexchange 未注册，dice返回404

**ex:**
```bash
$ http POST http://localhost:6001/v1/bid/123 < request.json
```
**response:**
```
{
    "message": "Not Found. You have requested this URI [/v1/bid/123] but did you mean /v1/bid/<string:did> ?",
    "status": 404
}
```
3. did, request都正确， dice返回random的response：

 **ex:**
```bash
$ http POST http://localhost:6001/v1/bid/556e8773c44b1a7dfaee5ec3 < request.json
```
**response:**
```
{
    "adm": [
        {
            "id": "556e89c8c44b1a7eeabe0428",
            "price": 4.119358292207556,
            "tracking_url": [
                "http://www.cristgrimes.com/",
                "http://fay.info/"
            ]
        },
        {
            "click_through_url": [
                "http://www.konopelski.com/",
                "http://www.breitenbergreichel.net/"
            ],
            "id": "556e89c8c44b1a7eeabe042b",
            "price": 1.9474910060930013,
            "tracking_url": [
                "http://miller.biz/",
                "http://whitemonahan.net/"
            ]
        }
    ],
    "did": "556e8773c44b1a7dfaee5ec3",
    "id": "",
    "is_test": 1,
    "nurl": "http://dsp:6001/v1/notice/556e8773c44b1a7dfaee5ec3"
}
```

**3. 向dice 发送bid notice**
```
url: localhost:6001/v1/notice/<did:string>
method: POST
```
**ex:**
```bash
$ http POST http://localhost:6001/v1/notice/556e8773c44b1a7dfaee5ec3
```
**response:**
```
{
    "message": "556e8773c44b1a7dfaee5ec3 get notice",
    "timestamp": 1433930598.8850908
}
```
