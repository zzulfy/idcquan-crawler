# IDCquan 产业名录爬虫

## 项目介绍

本项目用于爬取 https://www.idcquan.com/ 网站的产业名录数据，包括：
- IDC服务商名录
- 云服务商名录
- 设备厂商名录
- 数据中心机房
- 数据中心园区

## 文件说明

### 数据文件
- **idcquan_产业名录.xlsx** - 最终爬取结果，完整版（137行）
- **idcquan_产业名录_测试版.xlsx** - 测试版（5行）

### 爬虫脚本
- **main.py** - 生成Excel的脚本（只爬取名称）

### 依赖文件
- **requirements.txt** - Python依赖包列表

## Excel数据结构

### Sheet列表
- **全部数据** - 唯一的Sheet

### 列名
1. **IDC服务商** - 137条记录
2. **云服务商** - 18条记录
3. **设备厂商** - 46条记录
4. **数据中心机房** - 130条记录
5. **数据中心园区** - 5条记录

## 使用方法

### 1. 安装依赖
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 运行爬虫
```bash
# 生成完整版Excel
python main.py
```

## 数据统计

| 分类 | 数量 |
|------|------|
| IDC服务商 | 137 |
| 云服务商 | 18 |
| 设备厂商 | 46 |
| 数据中心机房 | 130 |
| 数据中心园区 | 5 |
| **总计** | **336** |

## 数据中心园区列表

1. 贵州贵安
2. 乌兰察布
3. 宁夏中卫
4. 河北张北
5. 江苏南通

## 技术栈

- Python 3
- requests - HTTP请求
- BeautifulSoup4 - HTML解析
- pandas - 数据处理
- openpyxl - Excel文件操作

## 注意事项

- 请合理控制爬取频率，避免给网站造成压力
- 数据仅供参考，请以官网最新信息为准
- 请遵守网站的robots.txt规则
