import requests
from bs4 import BeautifulSoup
import re

def get_ips():
    url = "https://www.wetest.vip/page/cloudflare/address_v6.html"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        cells = soup.find_all('td')
        ip_list = []
        
        for cell in cells:
            text = cell.get_text(strip=True)
            # 规则：包含至少 2 个冒号且不以 :: 结尾，确保是完整地址
            if text.count(':') >= 2 and not text.endswith('::'):
                if re.match(r'^[0-9a-fA-F:]+$', text):
                    # 在这里加上 [ ] 和 #Wetest 标签
                    ip_list.append(f"[{text}]#Wetest")

        # 备选正则方案也同步加上 [ ] 和 #Wetest
        if not ip_list:
            # 匹配 8 段或缩写形式的完整 IPv6
            matches = re.findall(r'(([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4})', response.text)
            # 过滤掉短于 15 字符的（通常是网段前缀）
            ip_list = [f"[{m[0]}]#Wetest" for m in matches if len(m[0]) > 15]

        if ip_list:
            # 去重
            seen = set()
            final_ips = [x for x in ip_list if not (x in seen or seen.add(x))]
            
            # 为了防止抓取到不一致的内容，这里取消了 sorted 排序，按网页原始优选顺序保存
            with open("ipv6.txt", "w") as f:
                f.write("\n".join(final_ips))
            print(f"成功抓取并格式化 {len(final_ips)} 个带标签的 IPv6 地址")
        else:
            print("未能提取到有效地址")
            
    except Exception as e:
        print(f"脚本执行出错: {e}")

if __name__ == "__main__":
    get_ips()
