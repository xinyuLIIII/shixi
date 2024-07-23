# 接口文档

## 接口授权

请在Http Request Header中加入"Authorization: ${auth_code}"

## AIS相关接口

### 获取附近的船舶

**GET** /apserver/ais/ships-nearby?mmsi=${mmsi-param}

**Response**

只有HTTP STATUS CODE为200且返回数据中code=0时，为正常返回，其他的都是异常情况

```
{
    "code": 0,
    "ships": [
        {
            "longitude": 113.5129165649414,
            "latitude": 23.01758575439453,
            "speed": 0,
            "heading": 0,
            "maritimeMobileServiceIdentity": "413876176",
            "timestamp": "2024-06-03 11:04:57",
            "decodeTimestamp": "2024-06-03 11:17:00"
        },
        ...
    ]
}
```

## 船舶视频相关接口

### 获取船舶摄像头列表

**GET** /apserver/ship-video/cameras?shipName=${shipName}

**Response**

只有HTTP STATUS CODE为200且返回数据中code=0时，为正常返回，其他的都是异常情况

```
{
    "code": 0,
    "cameras": [
        {
            "mmsi": "xxx",
            "terminalId": "xxx",
            "deviceNo": "xxx",
            "shipName": "xxx",
            "deviceName": "xxx",
            "shipCode": "xxx",
            "deviceStatus": 1,
            "channelList": [
                {
                    "deviceNo": "xxx",
                    "deviceName": "驾驶台(彩色)"
                },
                {
                    "uuid": "xxx",
                    "deviceNo": "xxx",
                    "isNvr": 0,
                    "fromNvr": "xxx",
                    "channelId": 0,
                    "deviceName": "驾驶舱",
                    "ratio": "1280*720"
                },
                {
                    "uuid": "xxx",
                    "deviceNo": "xxx",
                    "isNvr": 0,
                    "fromNvr": "xxx",
                    "channelId": 1,
                    "deviceName": "船头",
                    "ratio": "1280*720"
                }
            ],
            "shipNo": "xxx",
            "nvrStatus": -1,
            "shipId": 5137
        },
        ...
    ]
}
```


### 获取摄像头的实时视频流

**GET** /apserver/ship-video/video-url?deviceNo=${deviceNo}

**Response**

只有HTTP STATUS CODE为200且返回数据中code=0时，为正常返回，其他的都是异常情况

```
{
    "code": 0,
    "video": {
        "isH265": true,
        "url": "xxxxx",
        "ratio": "1280*720"
    }
}
```