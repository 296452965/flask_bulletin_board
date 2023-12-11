基于flask+mysql+bootstrap的信息管理系统
# 基于flask+mysql+bootstrap的信息管理系统
## 项目特点及功能
- 由于现在只会一些基础的H5语言，会简单使用Bootstrap框架，因此前台页面使用了别人制作好的模板页面，借鉴了[光年模板](http://www.itshubao.com/doc-lyear/lyear.html)
- 小项目，通过按照框架搭建，结构应该是比较清晰的，比较适合入门了解flask框架
- 实现了分角色（用户和管理员）登录逻辑、数据的CRUD和前端表格展示，可视化图表展示并且接通后台数据
- mysql, sqlalchemy, 蓝图, 类视图，函数视图，表格分页都有用到
- 用户页面基于权限展示不同数据
- 管理员对用户账户的管理
- 数据导出到excel
- 使用了flask-login
- 使用了flask-sqlalchemy
- 使用了flask-wtf
## 项目如何运行？
- 首先根据requirements.txt文件安装项目依赖
- 在pycharm中调试运行的话，需要配置工作目录
- 需要和apache服务器配合使用的话，参考博文[【Flask实战】Apache+WSGI在内网Windows环境下部署Flask项目（艰难爬坑总结）](https://blog.csdn.net/chengyikang20/article/details/124433033)
## 效果展示
![首页](https://user-images.githubusercontent.com/31033705/159453136-67787fa9-ee6a-44dc-a554-c9108dc2f0e2.png)
![表格页面](https://user-images.githubusercontent.com/31033705/159453554-8d9332fb-c6a8-4c07-bad8-9432d0c5ff90.png)
![表单页面](https://user-images.githubusercontent.com/31033705/159453565-5b15d185-f76c-4d08-8fa2-9ff5277eb65d.png)
![登录页面](https://user-images.githubusercontent.com/31033705/159454209-93cfcc2d-3c04-4b81-b8a9-909e506daff2.png)
## TODOLIST
- 用户修改个人密码
- 增加二级单位分类
- 图表的统计及展示
- 增加新的人员统计功能
## 与我联系
- 项目还在进行中，交流沟通可以加微信：cyk-21
- CSDN博客：一个甜甜的大橙子
- 微信公众号：一个甜甜的大橙子
- 知识星球：知识的朋友
