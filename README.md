# free_996_product_list
记录没有加班文化的公司及其产品

# 小红书评论爬虫

这是一个用于爬取小红书帖子评论的Python脚本。

## 环境设置

1. 创建并激活conda环境：
```bash
conda create -n xhs python=3.9
conda activate xhs
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装Chrome浏览器（如果尚未安装）

## 使用方法

1. 激活环境：
```bash
conda activate xhs
```

2. 运行脚本：
```bash
python main.py
```

## 功能说明

- 自动爬取小红书帖子的评论信息
- 支持无限滚动加载更多评论
- 将评论数据保存为JSON格式
- 包含评论者用户名、评论内容、发布时间和点赞数

## 注意事项

- 请遵守小红书的使用条款和robots协议
- 建议在爬取时设置适当的延迟，避免对服务器造成压力
- 如遇到反爬虫机制，可能需要更新脚本中的选择器
