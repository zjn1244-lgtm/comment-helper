# ARCHITECTURE.md

# 系统架构设计文档

## 一、技术栈选择

### Python

用途：

* 核心业务逻辑
* 评论分类
* 数据处理

选择原因：

* 学习成本低
* 生态成熟
* 与Pandas和Streamlit兼容性好

---

### Streamlit

用途：

* 页面展示
* 用户交互

选择原因：

* 前后端一体
* 开发速度快
* 适合个人工具项目

---

### Pandas

用途：

* CSV读取
* Excel读取
* 数据清洗
* 数据筛选与排序

选择原因：

* 表格处理能力强
* MVP开发效率高

---

### SQLite

用途：

* 评论数据存储
* 状态持久化

选择原因：

* 零运维
* 单文件部署
* 适合轻量项目

---

### Streamlit Community Cloud

用途：

* 在线部署

选择原因：

* 免费
* 配置简单
* 支持GitHub自动部署

---

## 二、项目目录结构

```text
comment_ops_tool/

├── app.py
├── requirements.txt
├── README.md
├── PRD.md
├── ARCHITECTURE.md
├── .gitignore

├── data/
│   ├── app.db
│   └── sample_comments.csv

├── pages/
│   ├── 1_评论分析.py
│   └── 2_收藏夹.py

├── core/
│   ├── database.py
│   ├── importer.py
│   ├── classifier.py
│   ├── filters.py
│   └── utils.py

├── services/
│   └── comment_service.py

├── config/
│   ├── settings.py
│   └── keywords.py

├── exports/
│   └── .gitkeep

└── tests/
    └── test_classifier.py
```

---

## 三、核心模块说明

### app.py

应用入口。

职责：

* 上传文件
* 初始化系统
* 页面导航

---

### importer.py

职责：

* 读取CSV
* 读取Excel
* 字段标准化
* 数据清洗

输入：

* 上传文件

输出：

* 标准评论数据

---

### classifier.py

职责：

* 风险评论识别
* 值得回复评论识别
* 高互动评论识别

输出：

* system_tag

---

### filters.py

职责：

* 标签筛选
* 状态筛选
* 点赞排序
* 回复排序

---

### database.py

职责：

* SQLite连接
* 建表
* CRUD操作

---

### comment_service.py

职责：

* 业务流程编排
* 调用分类器
* 调用数据库
* 对页面提供统一接口

---

## 四、数据模型设计

### comments

```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment_id TEXT,
    username TEXT,
    content TEXT,
    likes INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    created_at TEXT,
    system_tag TEXT,
    note TEXT,
    is_saved INTEGER DEFAULT 0,
    is_processed INTEGER DEFAULT 0,
    imported_at TEXT
);
```

### 字段说明

| 字段           | 类型      | 说明    |
| ------------ | ------- | ----- |
| id           | INTEGER | 主键    |
| comment_id   | TEXT    | 评论ID  |
| username     | TEXT    | 用户名   |
| content      | TEXT    | 评论内容  |
| likes        | INTEGER | 点赞数   |
| replies      | INTEGER | 回复数   |
| created_at   | TEXT    | 发布时间  |
| system_tag   | TEXT    | 系统标签  |
| note         | TEXT    | 备注    |
| is_saved     | INTEGER | 是否收藏  |
| is_processed | INTEGER | 是否已处理 |
| imported_at  | TEXT    | 导入时间  |

---

## 五、系统调用关系

```text
页面层（Pages）

↓

Comment Service

↓

Core Modules

├── importer
├── classifier
├── filters
└── database

↓

SQLite
```

原则：

* 页面不直接写SQL
* 页面不直接写分类逻辑
* 页面只调用Service层

---

## 六、代码规范

### 单一职责原则

一个文件只负责一类功能。

例如：

* importer.py → 导入
* classifier.py → 分类
* database.py → 数据库

---

### 一个函数只做一件事

例如：

```python
load_file()

clean_row()

classify_comment()

save_comments()
```

---

### 命名规范

统一英文命名。

例如：

```python
is_processed

is_saved

get_comments()

mark_comment_as_processed()
```

---

### 返回值规范

查询：

```python
DataFrame
List
```

单条记录：

```python
Dict
```

更新操作：

```python
True / False
```

---

### 配置集中管理

settings.py：

```python
DB_PATH = "data/app.db"

EXPORT_DIR = "exports/"
```

避免硬编码路径。

---

### 开发原则

先跑通

↓

先上线

↓

再优化

避免过度设计。
