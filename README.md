# 聊天小秘

本项目基于pyside6，使用fluent组件库(https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

与微信有关的接口通过`uiautomation`实现，仅支持Windows系统

介绍（待修改）

## 功能

待添加

## 开发环境

安装依赖库：`pip install -r requirements.txt`

导出依赖库：`pip freeze > requirements.txt`

清除依赖库：`pip uninstall -r requirements.txt -y`

关于`uiautomation`的使用，推荐配合windows自带工具
`C:\Program Files (x86)\Windows Kits\10\bin\10.0.20348.0\x64\inspect.exe`
使用

## 构建

` pyinstaller main.spec`

## 项目目录

* ChatSecretary
  * api - 后端接口
    * we_chat_hacker - 微信接口
  * resource - 各类资源
    * images  - 图标/图片
  * view - 前端界面
  * main.py - 运行入口

## 已知问题

待添加

## Licence

AGPL-3.0