import requests
from bs4 import BeautifulSoup
import re

def get_ips():
    # --- 在这里增加或修改你的网址列表 ---
    urls = [
        "https://www.wetest.vip/page/cloudflare/address_v6.html",
        # "https://另一个提供IP的网址.com/page.html" # 示例：可以直接在后面加
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_ip_list = []

    for url in urls:
        try:
            print(f"正在抓取: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            cells = soup.find_all('td')
            
            current_site_ips = []
            
            # 1. 尝试从表格抓取
            for cell in cells:
                text = cell.get_text(strip=True)
                if text.count(':') >= 2 and not text.endswith('::'):
                    if re.match(r'^[0-9a-fA-F:]+$', text):
                        current_site_ips.append(f"[{text}]#Wetest")

            # 2. 如果表格没抓到，尝试正则抓取
            if not current_site_ips:
                matches = re.findall(r'(([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4})', response.text)
                current_site_ips = [f"[{m[0]}]#Wetest" for m in matches if len(m[0]) > 15]
            
            all_ip_list.extend(current_site_ips)
            
        except Exception as e:
            print(f"抓取 {url} 时出错: {e}")

    # --- 去重并保存 ---
    if all_ip_list:
        # 使用 list(dict.fromkeys()) 在去重的同时保持原始抓取顺序
        final_ips = list(dict.fromkeys(all_ip_list))
        
        with open("ipv6.txt", "w") as f:
            f.write("\n".join(final_ips))
        print(f"全部抓取完成，共获得 {len(final_ips)} 个唯一地址")
    else:
        print("未能在任何网址抓取到有效地址")

if __name__ == "__main__":
    get_ips()
