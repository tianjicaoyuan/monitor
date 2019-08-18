存储服务器功能用途： 

该程序架构包含：nginx+gunicorn+flask程序。目前gunicorn只能在linux上运行，无法在windows上运行。
nginx作为代理服务器也作为web服务器。gunicorn作为web服务器，
flask程序为开发程序，负责处理请求并返回结果。该存储服务器的功能主要包含以下部分：
用户登录与注册；接收上传视频，接收网络摄像机信息请求；接收历史视频信息请求；对视频进行人脸识别。


存储服务器环境安装需求：必须在Linux系统下，除非不使用nginx+gunicorn，
这样也可以简单部署，无需考虑高并发情况。windows系统下所需软件均在soft文件夹中
................
nignx程序下载安装
gunicorn程序下载安装
mysql程序下载与安装
ffmpeg程序下载安装

...................
flask开发程序是用python语言编写的，需要安装第三方python库。
首先需要下载一个Anaconda4.6.14，Anaconda是PYthon版本和第三库管理的平台工具，可以利用
Anaconda配置多种python版本的虚拟环境，针对多个应用程序的运行。

.................................................................
配置虚拟环境基于python3.6.7版本，因为python3.6支持dlib库安装，python3.7不支持，后面会
用到人脸识别程序。运行程序时，使用虚拟环境中的python.exe运行该程序。
在Anaconda Prompt界面运行以下命令：
conda create --name virtualname python=3.6 新建虚拟环境
conda activate virtualname 进入或激活虚拟环境

............................
python项目中必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号。以便新环境部署。
(venv) $ pip freeze >requirements.txt 生成依赖包文件
(venv) $ pip install -r requirements.txt 安装依赖包文件

程序需要人为设置或修改参数的几个点：
config.py中修改：邮箱发送变量，数据库连接地址。
main/views.py中修改：uploads中的上传路径和ffmpeg路径


存储服务器使用：
在虚拟环境中执行： python manage.py
在浏览器端输入服务器IP地址：http://192.168.2.1:5050/login 即可访问登录页面



