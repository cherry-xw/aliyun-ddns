# aliyun-ddns
1. 本脚本基于阿里云购买的域名，使用AccessKeyID与AccessKeySecret令牌，实时获取当前的外网IP，更新域名解析
2. 如果是使用路由器设备，需要在路由器设置中，将本机的mac地址与路由器dhcp分配的IP绑定，使用dmz主机功能，将外网访问指向当前的电脑
3. 国内常用的web网页端口如：80，443等私人已被禁用，可以使用其他任意端口号

### 阿里云
1. 购买域名
2. 创建解析记录（记录类型A, 主机记录：与配置的HostReacrd相同即可，如www，记录值填0.0.0.0即可）
3. 执行成功后，可使用 [HostReacrd].xxx.com访问你的电脑

### 安装依赖
1. 安装python3.x
2. 安装pip库依赖：`pip install aliyun-python-sdk-core aliyun-python-sdk-alidns`

### 修改配置
1. 登录阿里云
2. 进入控制台
3. 点击右上角头像下拉列表选项：AccessKey管理  
4. 点击右上方：创建AccessKey
5. 将创建的记录值填写到config.json文件中（ps:该信息不要泄露给任何地方，以下数据为虚拟）
```
{
    "AccessKeyID": "LTAI4FofjSr6ijp4LkteK890",
    "AccessKeySecret": "oWBa2do2FCE4lJJ3UpnqvA8OVdkiOr",
    "RegionId": "cn-hangzhou",
    "DomainName": "xxx.com",
    "HostReacrd": "www",
    "Types": "A",
    "CurrentIP": "0.0.0.0"
}
```

### 直接执行
`python start.py`如果在config.log中新增日志中record项有值，说明修改成功，可以到阿里云查看解析记录是否已经改变

### linux
crontab 创建定时任务计划，使用run.sh脚本

### windows
window - 任务计划程序 - 创建任务 - 固定间隔时间触发(eg:每小时) - 调用run.bat脚本