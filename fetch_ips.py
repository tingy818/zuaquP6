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
            # 规则：包含至少 2 个冒号且不以 :: 结尾
            if text.count(':') >= 2 and not text.endswith('::'):
                if re.match(r'^[0-9a-fA-F:]+$', text):
                    # 在这里为地址加上 [ ]
                    ip_list.append(f"[{text}]")

        # 备选正则方案也同步加上 [ ]
        if not ip_list:
            matches = re.findall(r'(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4})', response.text)
            ip_list = [f"[{m[0]}]" for m in matches]

        if ip_list:
            final_ips = sorted(list(set(ip_list)))
            with open("ipv6.txt", "w") as f:
                f.write("\n".join(final_ips))
            print(f"成功抓取并格式化 {len(final_ips)} 个 IPv6 地址")
        else:
            print("未能提取到有效地址")
            
    except Exception as e:
        print(f"脚本执行出错: {e}")

if __name__ == "__main__":
    get_ips()
