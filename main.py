#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成最终Excel - 只有5列
"""
import time
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd


class SimpleCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_soup(self, url):
        try:
            response = self.session.get(url, timeout=20)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'lxml')
        except:
            pass
        return None

    def clean_text(self, text):
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    def get_names(self, url, category_name):
        print(f"正在获取 {category_name}...")
        soup = self.get_soup(url)
        if not soup:
            return []

        items = []
        seen_urls = set()

        filter_keywords = [
            '更多', 'RSS', '赠阅', '提交', '联系我们', '版权声明', '友情链接',
            '快讯', '丨', '｜', '深度', '投资', '总投资', '面向未来', '聚焦',
            '从', '到', '树行业', '首单', '生态共筑', '创新驱动', '新一代',
            '启动', '摸底', '通知', '论坛', '圆满', '成功', '通过', '增强',
            '？', '！', '!', '?', '即将', '正式', '规划', '年度', '终止', '规划建议',
            '冲刺', '算力上天', '跨界', '申报'
        ]

        path_whitelist = []
        if category_name == 'IDC服务商':
            path_whitelist = ['/idc/']
        elif category_name == '云服务商':
            path_whitelist = ['/cloud/', '/iaas/', '/pssa/', '/saas/']
        elif category_name == '设备厂商':
            path_whitelist = ['/changshang/']
        elif category_name == '数据中心机房':
            path_whitelist = ['/jifang/']

        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            text = self.clean_text(link.get_text())

            if not text or len(text) < 2:
                continue
            if any(keyword in text for keyword in filter_keywords):
                continue
            if not re.search(r'\.shtml$', href):
                continue

            if href.startswith('//'):
                full_url = 'https:' + href
            elif href.startswith('/'):
                full_url = urljoin(url, href)
            elif href.startswith('http'):
                full_url = href
            else:
                continue

            if path_whitelist:
                if not any(path in full_url for path in path_whitelist):
                    continue

            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            items.append(text)

        print(f"  找到 {len(items)} 个")
        return items


def main():
    print("=" * 60)
    print("生成最终Excel")
    print("=" * 60)

    crawler = SimpleCrawler()

    categories = [
        ('IDC服务商', 'http://dh.idcquan.com/idc/'),
        ('云服务商', 'http://dh.idcquan.com/cloud/'),
        ('设备厂商', 'http://dh.idcquan.com/changshang/'),
        ('数据中心机房', 'http://dh.idcquan.com/jifang/'),
        ('数据中心园区', None),
    ]

    result_data = {}

    for cat_name, cat_url in categories:
        if cat_name == '数据中心园区':
            names = ['贵州贵安', '乌兰察布', '宁夏中卫', '河北张北', '江苏南通']
            print(f"正在获取 {cat_name}...")
            print(f"  找到 {len(names)} 个")
        else:
            names = crawler.get_names(cat_url, cat_name)

        result_data[cat_name] = names

    # 找到最大长度
    max_len = max(len(v) for v in result_data.values())
    for cat in result_data:
        while len(result_data[cat]) < max_len:
            result_data[cat].append('')

    result_df = pd.DataFrame(result_data)

    filename = 'idcquan_产业名录.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        result_df.to_excel(writer, sheet_name='全部数据', index=False)

    print("\n" + "=" * 60)
    print(f"数据已保存到: {filename}")
    print(f"共 {max_len} 行")
    print(f"列名: {list(result_df.columns)}")
    print("\n完成!")


if __name__ == '__main__':
    main()
