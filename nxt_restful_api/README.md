#NXT Restful API
odoo Restful API from appnxt.com

Odoo 的RESTful风格接口模块

# 使用
```
1. 下载源码
2. 将整个nxt_restful_api目录放到你的addons目录下，
3. 更新模块列表，安装模块，
4. 通过RESTful方式访问接口
   1. 获取Session
   2. 请求数据/方法
```

# 接口定义

```
/api/v2/auth                   POST         - 登录返回会话参数 
/api/v2/<model>                GET          - 读取对象全部数据 (可选参数：domain, fields, offset, limit, order)
/api/v2/<model>/<id>           GET          - 读取一个记录 (可选参数：fields)
/api/v2/<model>                POST         - 创建一个记录
/api/v2/<model>/<id>           PUT          - 更新一个记录
/api/v2/<model>/<id>           DELETE       - 删除一个记录
/api/v2/<model>/<id>/<method>  PUT/POST     - 调研对象方法 (可选参数)
```
使用说明
```
1. Before calling /api/v2/auth, call /web?db=*** otherwise web service is not found
2. session_id=headers.session_id || session_info.session_id or headers={'X-Openerp-Session-Id':session_id}
```
Odoo交流QQ群: 19794653
官方网址: http://appnxt.com
