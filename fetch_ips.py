import requests
from bs4 import BeautifulSoup
import re

def get_ips():
    # --- 网址列表：支持 HTML 网页和纯文本 (TXT) 链接 ---
    urls = [
        "https://www.wetest.vip/page/cloudflare/address_v6.html",
        "https://bestcf.pages.dev/cfyes/ipv6.txt"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.wetest.vip/'
    }
    
    all_ip_list = []

    # 兼容完整的 IPv6 正则（包含带有 :: 双冒号缩写的标准格式）
    ipv6_pattern = r'(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}|(?:::[0-9a-fA-F]{1,4}){1,7}|::'

    for url in urls:
        try:
            print(f"正在抓取: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = 'utf-8'
            
            current_site_ips = []

            # 1. 判断是否为纯文本文件（如 .txt 结尾）
            if url.endswith('.txt'):
                lines = response.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # 如果文本行里本身就带有了 [IP]#标记，直接保留或规范化格式
                    if ':' in line:
                        # 提取行内的 IPv6 地址部分
                        matches = re.findall(ipv6_pattern, line)
                        for ip in matches:
                            if len(ip) > 10 and ip.count(':') >= 2:
                                current_site_ips.append(f"[{ip}]#BestCF")
            else:
                # 2. 如果是 HTML 网页，尝试从表格 (td) 抓取
                soup = BeautifulSoup(response.text, 'html.parser')
                cells = soup.find_all('td')
                for cell in cells:
                    text = cell.get_text(strip=True)
                    if text.count(':') >= 2:
                        if re.match(r'^[0-9a-fA-F:]+$', text):
                            current_site_ips.append(f"[{text}]#Wetest")

                # 3. 如果表格没抓到（数据在 JS 变量中），对网页全文进行正则扫描
                if not current_site_ips:
                    matches = re.findall(ipv6_pattern, response.text)
                    for ip in matches:
                        if len(ip) > 10 and ip.count(':') >= 2:
                            current_site_ips.append(f"[{ip}]#Wetest")

            print(f"从 {url} 成功提取到 {len(current_site_ips)} 个候选 IP")
            all_ip_list.extend(current_site_ips)
            
        except Exception as e:
            print(f"抓取 {url} 时出错: {e}")

    # --- 去重并保存 ---
    if all_ip_list:
        # 使用 dict.fromkeys 在去重的同时保持原始抓取顺序
        final_ips = list(dict.fromkeys(all_ip_list))
        
        with open("ipv6.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_ips))
        print(f"\n全部抓取完成！共写入 {len(final_ips)} 个唯一 IPv6 地址到 ipv6.txt")
    else:
        print("\n未能在任何网址抓取到有效地址，请检查网络或目标页面。")

if __name__ == "__main__":
    get_ips()
