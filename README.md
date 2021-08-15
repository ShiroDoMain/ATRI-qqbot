# ATRI Project
## 使用注解
Hi！  
这是一个基于 [mirai](https://github.com/mamoe/mirai) 框架协议，[graia](https://github.com/GraiaProject/Application) SDK和 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 的qqbot  
您需要在cfg.json文件里设置bot参数

## 配置
>cfg.json:  
>>  botConfig:  
>>>  botName:bot的名称
>>>  nameRouse:默认true，设置为true时可以通过设定的botName交互  
>>>  qq:Bot的qq  
>>>  authKey:Bot的authKey  
>>>   host:Bot的地址  
>>>   ws:默认true，以websocket方式监听  
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
>>  Akinator:
>>    enable:默认true,指定为true时开启网络天才
>>    command:str列表,指定触发命令
>>
>>  chatBot:  
>>>   enable: 默认true,指定为true时开启对话机器人  
>>>   at:默认true,指定为true时被at触发对话  
>>>   nameRouse:默认true,指定为true时检测到对话中有bot名字触发对话机器人  
>>>   badRequest:请求异常时触发对话  
>>>   quote:默认false,指定true时回复相关对话  
>>>   shield:int数组,不在指定群组触发对话  
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


## 功能
目前实现的功能有  
(重构后以下部分功能暂未实现，请等待后续更新)  
- 以图搜图  
- 以图搜番  
- ~~查询疫情~~  
- ~~查询天气~~   
- 摸头
- 基础闲聊 
- ~~随机涩图~~
- 还有好多好多功能(~~我忘了~~)
## 使用须知  
此开源项目遵循mirai社区规定开源协议AGPLv3  
~~注意身体~~

## Note
另一开源项目[TimeBot](https://github.com/ShiroDoMain/TimeBot)，可自行搭配使用  

# 鸣谢
感谢 [GraiaProject](https://github.com/GraiaProject) 的 [graia](https://github.com/GraiaProject/Application) 和 [mamoe](https://github.com/mamoe) 的 [mirai](https://github.com/mamoe/mirai)项目给我们带来了快乐

# Changelog  
>  \[2021-07-22]:腾讯ai关闭了机器人示例，删除对应的接口  
>  \[2021-07-28]:合并来自[Siltal](https://github.com/Siltal)的pr  
>  \[2021-07-30]:添加了吃啥  
>  \[2021-08-14]:添加对话机器人，修改依赖  
