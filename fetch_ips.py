import requests
import re

def get_ips():
    # 目标网址
    url = "https://www.wetest.vip/page/cloudflare/address_v6.html"
    try:
        # 模拟浏览器请求
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        # 匹配标准的 IPv6 地址（包括缩写形式）
        ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))'
        
        # 寻找所有匹配项
        matches = re.findall(ipv6_pattern, response.text)
        # 提取元组中捕获的完整地址并去重排序
        ip_list = sorted(list(set([m[0] for m in matches if m[0]])))
        
        if ip_list:
            # 写入文本文件
            with open("ipv6.txt", "w") as f:
                f.write("\n".join(ip_list))
            print(f"成功获取 {len(ip_list)} 个地址")
        else:
            print("未能提取到有效 IP")
            
    except Exception as e:
        print(f"执行出错: {e}")

if __name__ == "__main__":
    get_ips()
