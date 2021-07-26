# kindle2flomo
import kindle notes to flomo.

访问地址：http://kindle2flomo.90byte.com/index.html


## V2.0
升级到了 V2.0 版本，删除了一些特性，新增了一些特性，旨在提供更好的体验，帮助你整理读书笔记，产生更大的价值。

<img width="2044" alt="image" src="https://user-images.githubusercontent.com/5508125/127024184-defb3823-28c3-4f0c-a977-0759adadceb8.png">

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
            "highlight": "这就是“自由与责任”理念的核心。如果有人滥用你给予他们的自由，就必须受到惩罚，而且必须是严厉的惩罚。这样，其他员工才会引以为戒，否则，自由将毫无意义。",
            "note": "大部分公司就是不愿意拉破脸皮，才一片祥和的将就着，耗费精力，这就是内耗。",
            "place": "3下 取消差旅和经费审批 > 位置 1249"
        },
        {
            "highlight": "这确实是一项很有意义的研究。创造性工作要求在一定程度上解放你的大脑。如果你总想着要怎么做才能表现好，才能得到高额的奖金，那么你就缺少开放的认知空间，产生最好的想法和最好创意的可能性也微乎其微。结果，你反倒做得更差。",
            "place": "4 支付行业最高薪资 > 位置 1564"
        },
        {
            "highlight": "了解自身的价值，然后主动去争取应得的报酬，这是我自己的责任啊！",
            "place": "4 支付行业最高薪资 > 位置 1754"
        },
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
    "delimiter": "---------",
    "order": "down",    // up or down
    "note": "MEMO 笔记部分",
    "highlight": "MEMO 标注部分",
    "tag": "#kindle/笔记 #企业"  // 支持多个标签
}
```

返回：

```json
{
    "code": 0,
    "memo":{
        "content": "<p>MEMO 标注部分</p><p>---------</p><p>笔记：MEMO 笔记部分</p><p>#kindle/笔记 #企业</p>",
        "created_at": "2021-07-27 23:44:29",
        "creator_id": 3235,
        "linked_count": 0,
        "linked_memos":[],
        "parent_memo_slug": null,
        "slug": "NDU3MTI1OA",
        "source": "incoming_webhook",
        "tags":[
            "kindle/笔记",
            "企业"
         ]
    },
    "message": "已记录"
}
```

## 自己部署
1. 进入 `server` 目录，启动 `server.py` 服务
2. 修改 `index.html` 异步请求的地址
3. 浏览器打开 `index.html` 即可



## 历史版本

### v1.0

<img width="1145" alt="image" src="https://user-images.githubusercontent.com/5508125/120009242-54d12580-c00e-11eb-81ed-819c91de3612.png">

