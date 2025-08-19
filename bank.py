# -*- coding: utf-8 -*-
"""
 @Author: xiaoyao
 @FileName: 判断银行卡.py
 @CreateDateTime: 2024/2/4 14:43
 @SoftWare: PyCharm
 # @Comment : 
"""
import pandas as pd
from pathlib import Path
import requests
import os
from tqdm import tqdm

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Content-Type': 'application/json'
}
bank_abb = {
    "CDB": "国家开发银行", "ICBC": "中国工商银行", "ABC": "中国农业银行", "BOC": "中国银行",

    "CCB": "中国建设银行", "PSBC": "中国邮政储蓄银行", "COMM": "交通银行", "CMB": "招商银行",

    "SPDB": "上海浦东发展银行", "CIB": "兴业银行", "HXBANK": "华夏银行", "GDB": "广东发展银行",

    "CMBC": "中国民生银行", "CITIC": "中信银行", "CEB": "中国光大银行", "EGBANK": "恒丰银行",

    "CZBANK": "浙商银行", "BOHAIB": "渤海银行", "SPABANK": "平安银行", "SHRCB": "上海农村商业银行",

    "YXCCB": "玉溪市商业银行", "YDRCB": "尧都农商行", "BJBANK": "北京银行", "SHBANK": "上海银行",

    "JSBANK": "江苏银行", "HZCB": "杭州银行", "NJCB": "南京银行", "NBBANK": "宁波银行", "HSBANK": "徽商银行",

    "CSCB": "长沙银行", "CDCB": "成都银行", "CQBANK": "重庆银行", "DLB": "大连银行", "NCB": "南昌银行",

    "FJHXBC": "福建海峡银行", "HKB": "汉口银行", "WZCB": "温州银行", "QDCCB": "青岛银行", "TZCB": "台州银行",

    "JXBANK": "嘉兴银行", "CSRCB": "常熟农村商业银行", "NHB": "南海农村信用联社", "CZRCB": "常州农村信用联社",

    "H3CB": "内蒙古银行", "SXCB": "绍兴银行", "SDEB": "顺德农商银行", "WJRCB": "吴江农商银行", "ZBCB": "齐商银行",

    "GYCB": "贵阳市商业银行", "ZYCBANK": "遵义市商业银行", "HZCCB": "湖州市商业银行", "DAQINGB": "龙江银行",

    "JINCHB": "晋城银行JCBANK", "ZJTLCB": "浙江泰隆商业银行", "GDRCC": "广东省农村信用社联合社",

    "DRCBCL": "东莞农村商业银行", "MTBANK": "浙江民泰商业银行", "GCB": "广州银行", "LYCB": "辽阳市商业银行",

    "JSRCU": "江苏省农村信用联合社", "LANGFB": "廊坊银行", "CZCB": "浙江稠州商业银行", "DYCB": "德阳商业银行",

    "JZBANK": "晋中市商业银行", "BOSZ": "苏州银行", "GLBANK": "桂林银行", "URMQCCB": "乌鲁木齐市商业银行",

    "CDRCB": "成都农商银行", "ZRCBANK": "张家港农村商业银行", "BOD": "东莞银行", "LSBANK": "莱商银行",

    "BJRCB": "北京农村商业银行", "TRCB": "天津农商银行", "SRBANK": "上饶银行", "FDB": "富滇银行",

    "CRCBANK": "重庆农村商业银行", "ASCB": "鞍山银行", "NXBANK": "宁夏银行", "BHB": "河北银行",

    "HRXJB": "华融湘江银行", "ZGCCB": "自贡市商业银行", "YNRCC": "云南省农村信用社", "JLBANK": "吉林银行",

    "DYCCB": "东营市商业银行", "KLB": "昆仑银行", "ORBANK": "鄂尔多斯银行", "XTB": "邢台银行", "JSB": "晋商银行",

    "TCCB": "天津银行", "BOYK": "营口银行", "JLRCU": "吉林农信", "SDRCU": "山东农信", "XABANK": "西安银行",

    "HBRCU": "河北省农村信用社", "NXRCU": "宁夏黄河农村商业银行", "GZRCU": "贵州省农村信用社",

    "FXCB": "阜新银行", "HBHSBANK": "湖北银行黄石分行", "ZJNX": "浙江省农村信用社联合社", "XXBANK": "新乡银行",

    "HBYCBANK": "湖北银行宜昌分行", "LSCCB": "乐山市商业银行", "TCRCB": "江苏太仓农村商业银行",

    "BZMD": "驻马店银行", "GZB": "赣州银行", "WRCB": "无锡农村商业银行", "BGB": "广西北部湾银行",

    "GRCB": "广州农商银行", "JRCB": "江苏江阴农村商业银行", "BOP": "平顶山银行", "TACCB": "泰安市商业银行",

    "CGNB": "南充市商业银行", "CCQTGB": "重庆三峡银行", "XLBANK": "中山小榄村镇银行", "HDBANK": "邯郸银行",

    "KORLABANK": "库尔勒市商业银行", "BOJZ": "锦州银行", "QLBANK": "齐鲁银行", "BOQH": "青海银行",

    "YQCCB": "阳泉银行", "SJBANK": "盛京银行", "FSCB": "抚顺银行", "ZZBANK": "郑州银行", "SRCB": "深圳农村商业银行",

    "BANKWF": "潍坊银行", "JJBANK": "九江银行", "JXRCU": "江西省农村信用", "HNRCU": "河南省农村信用",

    "GSRCU": "甘肃省农村信用", "SCRCU": "四川省农村信用", "GXRCU": "广西省农村信用", "SXRCCU": "陕西信合",

    "WHRCB": "武汉农村商业银行", "YBCCB": "宜宾市商业银行", "KSRB": "昆山农村商业银行", "SZSBK": "石嘴山银行",

    "HSBK": "衡水银行", "XYBANK": "信阳银行", "NBYZ": "鄞州银行", "ZJKCCB": "张家口市商业银行", "XCYH": "许昌银行",

    "JNBANK": "济宁银行", "CBKF": "开封市商业银行", "WHCCB": "威海市商业银行", "HBC": "湖北银行",

    "BOCD": "承德银行", "BODD": "丹东银行", "JHBANK": "金华银行", "BOCY": "朝阳银行", "LSBC": "临商银行",

    "BSB": "包商银行", "LZYH": "兰州银行", "BOZK": "周口银行", "DZBANK": "德州银行", "SCCB": "三门峡银行",

    "AYCB": "安阳银行", "ARCU": "安徽省农村信用社", "HURCB": "湖北省农村信用社", "HNRCC": "湖南省农村信用社",

    "NYNB": "广东南粤银行", "LYBANK": "洛阳银行", "NHQS": "农信银清算中心", "CBBQS": "城市商业银行资金清算中心"

}
# 卢恩算法
def luhn_algorithm(card_number):
    digits = [int(digit) for digit in str(card_number)]
    checksum = digits[-1]
    digits = digits[:-1][::-1]

    for i in range(0, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    total = sum(digits) + checksum
    return total % 10 == 0


def validate_bank_card(card_number):
    if card_number.isnumeric() and len(card_number) > 15:
        if luhn_algorithm(card_number):
            return True
    return False


def get_bank(cardNo):
    url = "https://ccdcapi.alipay.com/validateAndCacheCardInfo.json"
    params = {
        "_input_charset": "utf-8",
        "cardNo": cardNo,
        "cardBinCheck": "true",
    }

    try:
        response = requests.get(url=url, params=params, headers=HEADERS, timeout=40)
        response.raise_for_status()
        result = response.json()
        bank = result["bank"]
    except requests.RequestException as e:
        return None, '请求出错', str(e)
    except KeyError:
        return None, '银行卡信息未找到', 'KeyError'

    bank_name = bank_abb.get(bank, bank)
    return bank_name, 'OK', ''


def process_single_card():
    card_number = input("请输入银行卡号: ").strip()
    if not validate_bank_card(card_number):
        print(f"无效卡号: {card_number}")
        return
    bank_name, status, error = get_bank(card_number)
    if status == 'OK':
        print(f"卡号: {card_number}, 所属银行: {bank_name}, 长度: {len(card_number)}")
    else:
        print(f"获取银行卡信息出错 {card_number}: {error}")


def process_file():
    file_path = Path("E:/python/data/第一轮调单.csv")
    output_path = file_path.with_name("疑似控制返现汇总.csv")

    # 自动检测编码
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="gb18030")

    results = []
    for index, row in tqdm(df.iterrows(), total=len(df), desc="处理中", unit="条"):
        card_number = str(row['交易对手账卡号']).strip()
        if validate_bank_card(card_number):
            bank_name, status, error = get_bank(card_number)
            if status == 'OK':
                results.append({'CardNumber': card_number, 'BankName': bank_name, 'Length': len(card_number)})
            else:
                print(f"\n获取银行卡信息出错 {card_number}: {error}")
        else:
            print(f"\n无效卡号: {card_number}")

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n结果已保存到: {output_path}")


if __name__ == '__main__':
    print("请选择处理模式：")
    print("1. 单个卡号")
    print("2. 批量文件")
    choice = input("请输入选项(1/2): ").strip()
    if choice == "1":
        process_single_card()
    elif choice == "2":
        process_file()
    else:
        print("无效选择！")