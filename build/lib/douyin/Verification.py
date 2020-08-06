# -*- coding:utf-8 -*-
import hashlib
import time

byteTable1 = "D6 28 3B 71 70 76 BE 1B A4 FE 19 57 5E 6C BC 21 B2 14 37 7D " \
             "8C A2 FA 67 55 6A 95 E3 FA 67 78 ED 8E 55 33 89 A8 CE 36 B3 " \
             "5C D6 B2 6F 96 C4 34 B9 6A EC 34 95 C4 FA 72 FF B8 42 8D FB " \
             "EC 70 F0 85 46 D8 B2 A1 E0 CE AE 4B 7D AE A4 87 CE E3 AC 51 " \
             "55 C4 36 AD FC C4 EA 97 70 6A 85 37 6A C8 68 FA FE B0 33 B9 " \
             "67 7E CE E3 CC 86 D6 9F 76 74 89 E9 DA 9C 78 C5 95 AA B0 34 " \
             "B3 F2 7D B2 A2 ED E0 B5 B6 88 95 D1 51 D6 9E 7D D1 C8 F9 B7 " \
             "70 CC 9C B6 92 C5 FA DD 9F 28 DA C7 E0 CA 95 B2 DA 34 97 CE " \
             "74 FA 37 E9 7D C4 A2 37 FB FA F1 CF AA 89 7D 55 AE 87 BC F5 " \
             "E9 6A C4 68 C7 FA 76 85 14 D0 D0 E5 CE FF 19 D6 E5 D6 CC F1 " \
             "F4 6C E9 E7 89 B2 B7 AE 28 89 BE 5E DC 87 6C F7 51 F2 67 78 " \
             "AE B3 4B A2 B3 21 3B 55 F8 B3 76 B2 CF B3 B3 FF B3 5E 71 7D " \
             "FA FC FF A8 7D FE D8 9C 1B C4 6A F9 88 B5 E5"


def getXGon(url, stub, cookies=""):
    NULL_MD5_STRING = "00000000000000000000000000000000"
    sb = ""
    if len(url) < 1:
        sb = NULL_MD5_STRING
    else:
        sb = encryption(url)
    if len(stub) < 1:
        sb += NULL_MD5_STRING
    else:
        sb += stub
    if len(cookies) < 1:
        sb += NULL_MD5_STRING
    else:
        sb += encryption(cookies)
    index = cookies.find("sessionid=")
    if index == -1:
        sb += NULL_MD5_STRING
    else:
        sessionid = cookies[index + 10:]
        if sessionid.__contains__(';'):
            endIndex = sessionid.index(';')
            sessionid = sessionid[:endIndex]
        sb += encryption(sessionid)
    return sb


def encryption(url):
    obj = hashlib.md5()
    obj.update(url.encode("UTF-8"))
    secret = obj.hexdigest()
    return secret.lower()


def initialize(data):
    myhex = 0
    byteTable2 = byteTable1.split(" ")
    for i in range(len(data)):
        hex1 = 0
        if i == 0:
            hex1 = int(byteTable2[int(byteTable2[0], 16) - 1], 16)
            byteTable2[i] = hex(hex1)
        elif i == 1:
            temp = int("D6", 16) + int("28", 16)
            if temp > 256:
                temp -= 256
            hex1 = int(byteTable2[temp - 1], 16)
            myhex = temp
            byteTable2[i] = hex(hex1)
        else:
            temp = myhex + int(byteTable2[i], 16)
            if temp > 256:
                temp -= 256
            hex1 = int(byteTable2[temp - 1], 16)
            myhex = temp
            byteTable2[i] = hex(hex1)
        if hex1 * 2 > 256:
            hex1 = hex1 * 2 - 256
        else:
            hex1 = hex1 * 2
        hex2 = byteTable2[hex1 - 1]
        result = int(hex2, 16) ^ int(data[i], 16)
        data[i] = hex(result)
    for i in range(len(data)):
        data[i] = data[i].replace("0x", "")
    return data


def handle(data):
    for i in range(len(data)):
        byte1 = data[i]
        if len(byte1) < 2:
            byte1 += '0'
        else:
            byte1 = data[i][1] + data[i][0]
        if i < len(data) - 1:
            byte1 = hex(int(byte1, 16) ^ int(data[i + 1], 16)).replace("0x", "")
        else:
            byte1 = hex(int(byte1, 16) ^ int(data[0], 16)).replace("0x", "")
        byte1 = byte1.replace("0x", "")
        a = (int(byte1, 16) & int("AA", 16)) / 2
        a = int(abs(a))
        byte2 = ((int(byte1, 16) & int("55", 16)) * 2) | a
        byte2 = ((byte2 & int("33", 16)) * 4) | (int)((byte2 & int("cc", 16)) / 4)
        byte3 = hex(byte2).replace("0x", "")
        if len(byte3) > 1:
            byte3 = byte3[1] + byte3[0]
        else:
            byte3 += "0"
        byte4 = int(byte3, 16) ^ int("FF", 16)
        byte4 = byte4 ^ int("14", 16)
        data[i] = hex(byte4).replace("0x", "")
    return data


def x_gorgon(ts, inputBytes):
    data1 = ['3', '61', '41', '10', '80', '0']
    data2 = inputs(ts, inputBytes)
    data2 = initialize(data2)
    data2 = handle(data2)
    for i in range(len(data2)):
        data1.append(data2[i])

    xGorgonStr = ""
    for i in range(len(data1)):
        temp = data1[i] + ""
        if len(temp) > 1:
            xGorgonStr += temp
        else:
            xGorgonStr += "0"
            xGorgonStr += temp
    return xGorgonStr


def inputs(ts, inputBytes):
    result = []
    for i in range(4):
        if inputBytes[i] < 0:
            temp = hex(inputBytes[i]) + ''
            temp = temp[6:]
            result.append(temp)
        else:
            temp = hex(inputBytes[i]) + ''
            result.append(temp)
    for i in range(4):
        result.append("0")
    for i in range(4):
        if inputBytes[i + 32] < 0:
            # result.append(hex(inputBytes[i + 32]) + '')[6:]
            pass
        else:
            result.append(hex(inputBytes[i + 32]) + '')
    for i in range(4):
        result.append("0")
    tempByte = hex(int(ts)) + ""
    tempByte = tempByte.replace("0x", "")
    for i in range(4):
        a = tempByte[i * 2:2 * i + 2]
        result.append(tempByte[i * 2:2 * i + 2])
    for i in range(len(result)):
        result[i] = result[i].replace("0x", "")
    return result


def str_to_byte(strs):
    length = len(strs)
    str2 = strs
    bArr = []
    i = 0
    while i < length:
        a = str2[i]
        b = str2[1 + i]
        c = ((str2hex(a) << 4) + str2hex(b))
        bArr.append(c)
        i += 2
    return bArr


def str2hex(s):
    odata = 0
    su = s.upper()
    for c in su:
        tmp = ord(c)
        if tmp <= ord('9'):
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata


def time_stamp(unit=1):
    rticket = str(time.time() * unit).split(".")[0]
    return (str(rticket))


if __name__ == '__main__':

    cookie = 'passport_csrf_token=40e8e4e5e13d7efa4148811dea83b566; d_ticket=6b86663815b4a570d4e9fb2af9156c1ad9cd6; odin_tt=c2979179b87ddbd7363c83eb9da5b990701a6e2ef379168e09d7546515d6c3354f817e2b1e2c3dd77c2ebf80c5ca2e963da3da438fcd5bdb6718489bc0d809b1; sid_guard=57d6890d03d1eb9ade5508328f2b4eb3%7C1591236609%7C5184000%7CMon%2C+03-Aug-2020+02%3A10%3A09+GMT; uid_tt=9b814e610f72bc68dc0fa233390cae76; sid_tt=57d6890d03d1eb9ade5508328f2b4eb3; sessionid=57d6890d03d1eb9ade5508328f2b4eb3'
    token = '0057d6890d03d1eb9ade5508328f2b4eb32877f215a70d614df08bc3be508e5902c59773bb8573a6e40f2d658727d2483121'
    import requests
    from urllib import parse
    ts = time_stamp()
    ts1000 = time_stamp(1000)
    url = 'https://api3-normal-c-hl.amemv.com/aweme/v1/user/follower/list/'
    data = {
        'user_id': '101340455904',
        'sec_user_id': 'MS4wLjABAAAA29PmwbigJvD_RbIuS9sOCslSQEbTZcl0KS45sj_gPWU',
        'max_time': str(ts),
        'count': '20',
        'offset': '0',
        'source_type': '1',
        'address_book_access': '1',
        'gps_access': '1',
        'vcd_count': '0',
        'os_api': '22',
        'device_type': 'SM-N9760',
        'ssmix': 'a',
        'manifest_version_code': '100901',
        'dpi': '240',
        'uuid': '865166020256353',
        'app_name': 'aweme',
        'version_name': '10.9.0',
        'ts': ts,
        'app_type': 'normal',
        'ac': 'wifi',
        'host_abi': 'armeabi-v7a',
        'update_version_code': '10909900',
        'channel': 'aweGW',
        '_rticket': ts1000,
        'device_platform': 'android',
        'iid': '1310263726846926',
        'version_code': '100900',
        'cdid': 'b9ab0c56-b7d8-4871-af6a-8bcd06b424ab',
        'openudid': 'f5682fd7942aadd6',
        'device_id': '4177790051289640',
        'resolution': '1600*900',
        'os_version': '5.1.1',
        'language': 'zh',
        'device_brand': 'samsung',
        'aid': '1128',
        'mcc_mnc': '46000'
    }
    params = parse.urlencode(data)
    print(params)
    stub = encryption(params)
    s = getXGon(params, stub)
    gorgon = x_gorgon(ts, str_to_byte(s))
    print(gorgon)
    headers = {
        'Host': 'api3-normal-c-hl.amemv.com',
        # 'Cookie': 'd_ticket=6b86663815b4a570d4e9fb2af9156c1ad9cd6; odin_tt=c2979179b87ddbd7363c83eb9da5b990701a6e2ef379168e09d7546515d6c3354f817e2b1e2c3dd77c2ebf80c5ca2e963da3da438fcd5bdb6718489bc0d809b1; sid_guard=57d6890d03d1eb9ade5508328f2b4eb3%7C1591236609%7C5184000%7CMon%2C+03-Aug-2020+02%3A10%3A09+GMT; uid_tt=9b814e610f72bc68dc0fa233390cae76; sid_tt=57d6890d03d1eb9ade5508328f2b4eb3; sessionid=57d6890d03d1eb9ade5508328f2b4eb3; install_id=1802844507492382; ttreq=1$ab8843ef0229fa247e96521b6aa0a7ff17bcf709',
        'x-ss-req-ticket': ts1000,
        'x-tt-token': '0057d6890d03d1eb9ade5508328f2b4eb32877f215a70d614df08bc3be508e5902c59773bb8573a6e40f2d658727d2483121',
        'sdk-version': '1',
        'x-ss-dp': '1128',
        'x-tt-trace-id': '00-7e9355ad0d917abcf1417681cb5d0468-7e9355ad0d917abc-01',
        'user-agent': 'com.ss.android.ugc.aweme/110201 (Linux; U; Android 8.1.0; zh_CN; M30; Build/O11019; Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)',
        'x-khronos': ts,
        'x-gorgon': gorgon,
        'x-common-params-v2': 'os_api=27&device_platform=android&device_type=M30&iid=1802844507492382&version_code=110200&app_name=aweme&openudid=1fd7334501c9a854&device_id=2559301471442792&os_version=8.1.0&aid=1128&channel=wandoujia_douyin&ssmix=a&manifest_version_code=110201&dpi=320&cdid=82b4e13a-5867-4afc-95d7-273612d84049&version_name=11.2.0&resolution=720*1432&language=zh&device_brand=OBXIN&app_type=normal&ac=wifi&update_version_code=11209900'
    }

    response = requests.get(url, headers=headers, params=params)

    print(response.url)
    print(response.text)




