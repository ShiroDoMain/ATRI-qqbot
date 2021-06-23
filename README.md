# ATRI Project
## 使用注解
Hi！  
这是一个基于mirai框架，graia SDK的qqbot  
您只需要在cfg.json文件里设置bot参数即可

## 配置
>cfg.json:  
>>  botConfig:  
>>>   botName:bot的名称
>>>   nameRouse:默认true，设置为true时可以通过设定的botName交互  
>>>   qq:Bot的qq  
>>>   authKey:Bot的authKey  
>>>   host:Bot的地址  
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
>>  qqai:  
>>>   enable:默认false，指定为true时可以使用与腾讯ai对接的appid和key进行情景对话  
>>>   appid:int，提供的id  
>>>   appkey:qqai提供的key  
>>  
>>  sticker:  
>>>    enable:默认true，设置为true时bot可以触发回复指定的sticker  
>>>    path:stickers存放位置  
>>  
>>  storage:文件存放位置，默认为storage  
>>  
>>  setu:  
>>>   enable:默认false，指定为true时触发来点涩图事件  
>>>   path:涩图的存放位置 
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
(重构后以下功能皆暂未实现，请等待后续更新)  
- 以图搜图  
- 以图搜番  
- 查询疫情
- 查询天气 
- 摸头
- 基础闲聊
- ~~随机涩图~~
- 还有好多好多功能(~~我忘了~~)
## 使用须知  
~~注意身体~~

## Note
另一[开源项目](https://github.com/ShiroDoMain/TimeBot)，可自行搭配使用

# 鸣谢
感谢 [GraiaProject](https://github.com/GraiaProject) 的 [graia](https://github.com/GraiaProject/Application) 和 [mamoe](https://github.com/mamoe) 的 [mirai](https://github.com/mamoe/mirai)项目给我们带来了快乐
