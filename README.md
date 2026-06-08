# README.md

# 评论区运维助手（Comment Ops Helper）

## 项目简介

评论区运维助手（Comment Ops Helper）是一款面向短视频评论区运营场景的评论筛选与处理辅助工具。

通过对评论进行自动分类、筛选、排序和状态管理，帮助运营人员快速发现值得回复的评论、风险评论和高价值评论，减少人工翻找成本，提高评论区运营效率。

项目核心目标：

* 降低评论筛选时间
* 提高评论处理效率
* 建立评论处理闭环
* 沉淀高价值评论资产

---

## 核心功能

### 评论数据导入

支持：

* CSV
* Excel

### 评论自动分类

自动识别：

* 风险评论
* 值得回复评论
* 普通评论

### 评论筛选与排序

支持：

* 标签筛选
* 状态筛选
* 点赞排序
* 回复排序
* 时间排序

### 评论状态管理

支持：

* 标记已处理
* 取消已处理

### 收藏功能

支持：

* 收藏评论
* 收藏夹管理
* 导出收藏结果

### 评论搜索

支持关键词搜索评论内容。

---

## 技术栈

| 类型    | 技术                        |
| ----- | ------------------------- |
| 编程语言  | Python                    |
| Web框架 | Streamlit                 |
| 数据处理  | Pandas                    |
| 数据库   | SQLite                    |
| 部署平台  | Streamlit Community Cloud |

---

## 如何运行

### 1. 克隆项目

```bash
git clone https://github.com/yourname/comment_ops_tool.git

cd comment_ops_tool
```

### 2. 创建虚拟环境

```bash
python -m venv venv
```

Windows：

```bash
venv\Scripts\activate
```

Mac/Linux：

```bash
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动项目

```bash
streamlit run app.py
```

浏览器访问：

```text
http://localhost:8501
```

---

## MVP范围

当前版本聚焦：

* 上传评论
* 自动分类
* 筛选排序
* 状态管理
* 收藏导出

暂不包含：

* 用户登录系统
* 多人协作
* AI语义分析
* 抖音API直连

---

## 项目工作流

上传评论文件

↓

自动分类

↓

筛选值得回复评论

↓

复制评论内容

↓

抖音网页版 Ctrl + F

↓

定位评论并回复

↓

标记已处理

↓

收藏高价值评论

↓

导出结果
