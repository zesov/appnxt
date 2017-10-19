#nxt restful api
odoo restful api from appnxt.com

Odoo 的RESTful风格接口模块

# 特性

# 使用
1. 下载源码
2. 将整个nxt_restful_api目录放到你的addons目录下，
3. 更新模块列表，安装模块，
4. 通过RESTful方式访问接口
   1. 获取token
   2. 请求数据

详细说明：...



## 接口名称 获取授权码

### 1) 请求地址

>http://d10c.y.appnxt.com/api/v1.0/get_token?a=admin&s=admin&d=d10c

### 2) 调用方式：HTTP get

### 3) 接口描述：

* 接口描述详情

### 4) 请求参数:

#### GET参数:
| 字段名称 | 字段说明 |   类型   |  必填  |   备注 |
| ---- | :--: | :----: | :--: | ---: |
| a    | 用户名  | string |  Y   |    - |
| s    |  密码  | string |  Y   |    - |
| d    | 数据库  | string |  Y   |    - |



### 5) 请求返回结果:

```
{
    "token": "aHR0cDovL2QxMC5hcHBueHQuY29tLGQxMGMsYWRtaW4sMSwxNTAxMTYxMDk3",
    "message": "",
    "success": true
}
```


### 6) 请求返回结果参数说明:
| 字段名称    | 字段说明  |   类型   |  必填  |   备注 |
| ------- | :---: | :----: | :--: | ---: |
| token   | token | string |  Y   |    - |
| message |  消息   | string |  Y   |    - |
| success | 成功标志  | string |  Y   |    - |

二、


## 接口名称 获取Odoo记录

### 1) 请求地址

>http://d10c.y.appnxt.com/api/v1.0/res.partner?&token=aHR0cDovL2QxMC5hcHBueHQuY29tLGQxMGMsYWRtaW4sMSwxNTAxMTYxMDk3&fields=['name','phone']&per_page=3&page=2

### 2) 调用方式：HTTP get

### 3) 接口描述：

* 接口描述详情
  请求URL地址格式/api/v1.0/model_name
### 4) 请求参数:

#### GET参数:
| 字段名称     | 字段说明  |   类型   |  必填  |   备注 |
| -------- | :---: | :----: | :--: | ---: |
| token    |  授权码  | string |  Y   |    - |
| fields   | 返回字段  | string |  Y   |    - |
| per_page | 每页记录数 | string |  Y   |    - |
| page     |  当前页  | string |  Y   |    - |



### 5) 请求返回结果:

```
{
    "success": true,
    "result": [
        {
            "phone": "(+886) (02) 4162 2023",
            "id": 7,
            "name": "ASUSTeK"
        },
        {
            "phone": "+32 10 588 558",
            "id": 8,
            "name": "Agrolait"
        },
        {
            "phone": "+86 21 6484 5671",
            "id": 9,
            "name": "China Export"
        }
    ],
    "per_page": 3,
    "message": "",
    "total": 44,
    "page": 2
}
```


### 6) 请求返回结果参数说明:
| 字段名称     | 字段说明  |   类型   |  必填  |   备注 |
| -------- | :---: | :----: | :--: | ---: |
| success  | 成功标志  | string |  Y   |    - |
| result   |  结果   | string |  Y   |    - |
| per_page | 每页记录数 | string |  Y   |    - |
| message  |  消息   | string |  Y   |    - |
| total    | 记录总数  | string |  Y   |    - |
| page     |  当前页  | string |  Y   |    - |

三、


## 接口名称 创建记录

### 1) 请求地址

>http://d10c.y.appnxt.com/api/v1.0/res.partner

### 2) 调用方式：HTTP post

### 3) 接口描述：

* 接口描述详情

### 4) 请求参数:


#### POST参数:
| 字段名称  | 字段说明  |   类型   |  必填  |   备注 |
| ----- | :---: | :----: | :--: | ---: |
| name  |  姓名   | string |  Y   |    - |
| email | email | string |  Y   |    - |
| token |  授权码  | string |  Y   |    - |



### 5) 请求返回结果:

```
{
    "message": "",
    "result": 49,
    "success": true
}
```


### 6) 请求返回结果参数说明:
| 字段名称    | 字段说明 |   类型   |  必填  |   备注 |
| ------- | :--: | :----: | :--: | ---: |
| message |  消息  | string |  Y   |    - |
| result  |  结果  | string |  Y   |    - |
| success | 成功标志 | string |  Y   |    - |


四、


## 接口名称 记录更新接口

### 1) 请求地址

>http://d10c.y.appnxt.com/api/v1.0/res.partner/49

### 2) 调用方式：HTTP put

### 3) 接口描述：

* 接口描述详情

### 4) 请求参数:


#### POST参数:
| 字段名称  | 字段说明  |   类型   |  必填  |   备注 |
| ----- | :---: | :----: | :--: | ---: |
| name  |  名称   | string |  Y   |    - |
| email | email | string |  Y   |    - |
| token |  授权码  | string |  Y   |    - |



### 5) 请求返回结果:

```
{
    "message": "",
    "result": true,
    "success": true
}
```


### 6) 请求返回结果参数说明:
| 字段名称    | 字段说明 |   类型   |  必填  |   备注 |
| ------- | :--: | :----: | :--: | ---: |
| message |  消息  | string |  Y   |    - |
| result  |  结果  | string |  Y   |    - |
| success | 成功标志 | string |  Y   |    - |



Odoo交流QQ群: 19794653
官方网址: http://appnxt.com
