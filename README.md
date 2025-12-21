# 学个毛生信

[![GitHub](https://img.shields.io/badge/GitHub-bioinfo--for--dummies-blue?logo=github)](https://github.com/h4rvey-g/bioinfo-for-dummies)
[![Quarto](https://img.shields.io/badge/Made%20with-Quarto-75AADB?logo=quarto)](https://quarto.org)

> **AI时代的生物信息学实践指南** — 最小化编程，最大化AI使用

## 📖 关于本书

这是一本面向**零编程基础**的生物信息学入门书籍，特别为临床医生和生命科学研究人员设计。在AI时代，本书提倡一种新的学习理念：

- 🎯 **技术生态的广域认知** — 知道某个工具/方法的存在比精通它更重要
- 🔍 **强大的检索能力** — 能够找到针对问题的最佳解决方案
- 🏗️ **成为架构师而非实验员** — 专注于"做什么"而不是"怎么做"

## 👥 适合人群

- 临床医学专业人员，希望利用生物信息学工具进行数据分析，但缺乏编程经验
- 生命科学研究人员，想要快速掌握生物信息学分析方法
- 医学生和研究生，寻求高效的生物信息学研究方式
- 任何对生物信息学感兴趣但不想深入学习编程的人士

## 📚 内容结构

### 第一部分：AI工具

- **AI对话工具** — 如何使用ChatGPT等工具辅助研究
- **AI编程工具** — 利用AI完成代码编写和调试
- **AI服务** — 其他AI辅助服务的使用

### 第二部分：环境与工具

- **IDE** — 集成开发环境的选择和配置
- **终端** — 命令行操作基础
- **环境管理** — 软件包和依赖管理
- **版本控制** — Git基础与协作
- **流程管理** — 工作流程和流程管理工具

### 第三部分：生信实战

- 实际生物信息学分析案例
- 从数据获取到结果解读的完整流程

## 🚀 快速开始

### 在线阅读

访问在线版本：[学个毛生信](https://b4d.h4rvey.com/)

### 本地构建

本书使用 [Quarto](https://quarto.org) 构建。要在本地预览或构建本书：

1. **安装 Quarto**

   ```bash
   # 访问 https://quarto.org/docs/get-started/ 下载安装
   ```

2. **克隆仓库**

   ```bash
   git clone https://github.com/h4rvey-g/bioinfo-for-dummies.git
   cd bioinfo-for-dummies
   ```

3. **预览书籍**

   ```bash
   quarto preview
   ```

4. **渲染为HTML**

   ```bash
   quarto render --to html
   ```

5. **渲染为PDF**
   ```bash
   quarto render --to pdf
   ```
   > PDF 渲染需要 XeLaTeX 与 CJK 字体（推荐 Noto 系列）。在 Ubuntu 上可安装：
   > `sudo apt-get install fonts-noto fonts-noto-cjk`
   > 若使用 Beautybook 模板，还需安装 ctex 与相关包：
   > `tlmgr install ctex pgf tcolorbox tabularray thmtools thm-restate cncolours ninecolors bropd imakeidx titlesec titletoc ulem varwidth adjustbox pifont mathrsfs extarrows anyfontsize appendix enumitem`

## 📊 统计

查看本书的[访问统计](https://cloud.umami.is/share/eFyIpuQq1Nhdxj77)

## ☕ 支持本书

如果本书对您有所帮助，可以考虑请作者喝杯咖啡 😋

<img src="img/qr_code.jpg" width="300">
