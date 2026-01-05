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
        
        # 使用 BeautifulSoup 精准解析网页表格
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 寻找所有的单元格
        cells = soup.find_all('td')
        ip_list = []
        
        for cell in cells:
            text = cell.get_text(strip=True)
            # 规则：必须包含冒号，且长度要够长（排除掉类似 2606:4700:: 这种短前缀）
            # 完整的 IPv6 通常至少包含 5 个以上的冒号
            if text.count(':') >= 2 and not text.endswith('::'):
                # 进一步验证是否符合 IPv6 字符特征
                if re.match(r'^[0-9a-fA-F:]+$', text):
                    ip_list.append(text)

        # 如果通过表格没抓到，启动正则全文搜索作为备选
        if not ip_list:
            # 匹配 8 段完整的 IPv6
            matches = re.findall(r'(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4})', response.text)
            ip_list = [m[0] for m in matches]

        if ip_list:
            # 去重并排序
            final_ips = sorted(list(set(ip_list)))
            with open("ipv6.txt", "w") as f:
                f.write("\n".join(final_ips))
            print(f"成功抓取到 {len(final_ips)} 个完整 IPv6 地址")
        else:
            print("未能提取到有效地址，请检查网页内容")
            
    except Exception as e:
        print(f"脚本执行出错: {e}")

if __name__ == "__main__":
    get_ips()
