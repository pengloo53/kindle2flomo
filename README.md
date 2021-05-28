# kindle2flomo
import kindle notes to flomo.

访问地址：http://kindle2flomo.90byte.com/index.html

<img width="1145" alt="image" src="https://user-images.githubusercontent.com/5508125/120009242-54d12580-c00e-11eb-81ed-819c91de3612.png">


## 调用接口
没有认证，没有负载，请温柔对待，尽量帮到有需要的人。

### 解析笔记

请求：

```
POST http://kindle2flomo.90byte.com/parse
Content-type: multipart/form-data
{
    "file": File
}
```

返回：

```json
{
    "book_title": "不拘一格：网飞的自由与责任工作法",
    "result":[
        {
            "highlight": "网飞文化的核心是“人才重于流程，创新高于效率，自由多于管控”。必须理解，这样的文化建立在一个非常重要的基础上：创造力需要自由，但自由又不能被滥用。所以网飞只招“成年人”，即那些理解自由意味着更大责任的",
            "note": "根本的问题放在了人才招聘上，而大多数公司都不重视这个环节。",
            "tags": "#kindle/不拘一格：网飞的自由与责任工作法"
        },
        {
            "highlight": "判断力几乎可以解决所有模棱两可的问题，而流程",
            "note": "判断力的重要性",
            "tags": "#kindle/不拘一格：网飞的自由与责任工作法"
        }
    ]
}
```

### 导入 Flomo
请求：

```
POST http://kindle2flomo.90byte.com/post
Content-type: multipart/form-data
{
    "api": "https://flomoapp.com/iwh/MzIzNQ/d03863c4eda974594e78a8488e1bb4b4/",
    "delimiter": "+++++++++",
    "is_order": "false",    // true or false
    "data": result   // 上个接口返回的result（数组）
}
```

返回：

```json
{
    "code": 0,
    "message": "总共 2 条，全部导入完成。"
}
```

## 自己部署
1. 进入 `server` 目录，启动 `server.py` 服务
2. 修改 `index.html` 异步请求的地址
3. 浏览器打开 `index.html` 即可
