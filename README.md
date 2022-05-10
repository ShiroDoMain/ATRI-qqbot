# ATRI Project
![Mirai-console-Version](https://img.shields.io/badge/mirai--console-2.7.1--dev-brightgreen.svg?style=plastic)  
![Mirai-HTTP-API-Version](https://img.shields.io/badge/mirai--http--api-2.5.0-brightgreen.svg?style=plastic)  
![Karas-Version](https://img.shields.io/badge/Karas-0.1.4-brightgreen.svg?style=plastic)  

## 使用注解  
Hi！  
这是一个基于 [mirai](https://github.com/mamoe/mirai) 框架协议，[karas](https://github.com/ShiroDoMain/karas) SDK和 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 的qqbot  
PS: 使用本项目的前提您需要先启用一个mirai后端([mcl项目地址](https://github.com/iTXTech/mirai-console-loader))和[mah插件](https://github.com/project-mirai/mirai-api-http)  
准备完成后使用使用git拉取本项目  
```shell script
git clone https://github.com/ShiroDoMain/ATRI-qqbot
```
您需要在cfg.json文件里设置bot参数,安装bot所需要的依赖  
```shell script
pip3 install -r requirements.txt
```  
然后运行文件  
```shell script
python3 ATRI.py
```

## 配置
<details>
<summary>cfg.json</summary>

> cfg.json:  
>>  botConfig:  
>>>  botName: 必填,bot的名称  
>>>  qq: 必填,Bot的qq    
>>>  verifyKey:必填.Bot的authKey    
>>>  host:必填,mah的地址  
>>>  port:必填,mah的端口  
>>>  ws:默认true，以websocket方式监听  
>>>  logLevel:日志输出登记。默认info  
>>>  logToFile:  
>>>>   enable:是否输出到文件，默认否  
>>>>   file:日志输出文件，默认为logs/xxxxx.log  
>>>  nameRouse:默认true，设置为true时可以通过设定的botName交互  
>>  
>>  event:  
>>>   groupEvent:默认true，设置为true时监听群组消息  
>>>   friendEvent:默认true，设置为true时监听好友消息  
>>>   tempEvent:默认true，设置为true时监听临时消息  
>>  
>>  master:  
>>>  enable:默认false，设置为true时启用master权限  
>>>  qq:int，指定拥有与群主和管理员相同能操作bot的权限的用户，有且只有一个  
>>
>>  blackList:int列表,bot不想理会的对象  
>>  
>>  sticker:  
>>>    enable:默认true，设置为true时bot可以触发回复指定的sticker  
>>>    path:stickers存放位置  
>>  
>>  storage:文件存放位置，默认为storage  
>>  
>>  setu:  
>>>   enable:默认false，指定为true时触发来点涩图事件  
>>>   flash:默认true，指定为true时发送形式为闪照    
>>>   command:str列表，指定触发命令  
>>>   path:涩图的存放位置  
>>
>>  illustrationSearch:  
>>>   enable:默认true，指定为true时开启以图搜图  
>>>   command:str列表，指定触发命令  
>>
>>  animeSearch:  
>>>   enable:默认true，指定为true时开启以图搜番
>>>   command:str列表,指定触发命令
>>  
>>  chatBot:  
>>>   enable: 默认true,指定为true时开启对话机器人  
>>>   at:默认true,指定为true时被at触发对话  
>>>   nameRouse:默认true,指定为true时检测到对话中有bot名字触发对话机器人  
>>>   badRequest:请求异常时触发对话  
>>>   quote:默认false,指定true时回复相关对话  
>>>   shield:int数组,不在指定群组触发对话  
>>
>>  weather:默认true,指定为true时可以使用天气功能  
>>  
>>  shieldGroup:  
>>>   enable:默认false，指定为true时Bot屏蔽指定群聊
>>>   list:int列表，屏蔽指定群聊   
>>  
>>  onlyGroup:  
>>>   enable:默认false，指定为true时Bot只监听指定群聊消息  
>>>   list:int列表，监听指定群聊  
>>  
>>  shieldFriend:
>>>   enable:默认false，指定为true时Bot不会监听指定好友消息  
>>>   list:int列表，屏蔽指定好友
</details>

## 功能
目前实现的功能有  
(重构后以下部分功能暂未实现，请等待后续更新)  
- 以图搜图  
- 以图搜番  
- ~~查询疫情~~  
- 查询天气  
- 摸头
- 基础闲聊 
- 来点涩图
- 还有好多好多功能(~~我忘了~~)
## 使用须知  
此开源项目遵循mirai社区规定开源协议AGPLv3  
~~注意身体~~

## Note
该项目使用[karas](https://github.com/ShiroDoMain/karas)sdk开发  
另一开源项目[TimeBot](https://github.com/ShiroDoMain/TimeBot) ，可自行搭配使用 

## 开源  
本项目使用[GNU AGPLv3](https://github.com/ShiroDoMain/ATRI-qqbot/blob/master/LICENSE) 协议作为开源许可证  

## 鸣谢
感谢 [mamoe](https://github.com/mamoe) 的 [mirai](https://github.com/mamoe/mirai) 项目给我们带来了快乐

## Changelog  
>  \[2021-07-22]:腾讯ai关闭了机器人示例，删除对应的接口  
>  \[2021-07-28]:合并来自 [Siltal](https://github.com/Siltal) 的pr  
>  \[2021-07-30]:添加了吃啥  
>  \[2021-08-14]:添加对话机器人，修改依赖  
>  \[2021-09-12]:Mirai修复图片发送,更新依赖  
>  \[2021-09-17]:新增每周天气接口  
>  \[2021-09-18]:新增每日天气接口  
>  \[2021-10-05]:修改对话机器人接口,添加注意力机制  
>  \[2021-10-05]:去除网络天才功能，发布了一个可使用版本  
>  \[2021-12-01]:添加好友消息事件  
>  \[2022-05-08]:更换了[karas](https://github.com/ShiroDoMain/karas) 框架  
