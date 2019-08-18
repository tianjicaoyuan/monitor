WebCamera的功能：
对图像进行Vibe运动检测算法，若有运动情况，则直接录制并上传20s的高清视频。
产生image流，并响应给客户端。
产生hls流
添加网络摄像机。

WebCamera的组成：
	cameraServer.py
	cameraClient.py
	Nginx+ffmpeg
	
	
1.首先配置树莓派的网络环境：
	配置摄像头的驱动，确保摄像头处于正常状态。
	有线网卡：设置为静态ip地址，一般为192.168.2.3，与PC电脑构成局域网，
	           远程登录树莓派，从而控制并调试程序。LINUX系统使用ssh登录，windows
			   系统使用远程桌面连接。登录的用户名为pi，密码是raspberry。
	无线网卡：设置为DHCP自动分配ip地址，但是根据配置文件的不同，网络模式有sat和AP。
	sat模式主要用来添加网络摄像机。
	AP模式主要是正常工作状态。
	问题是是否需要重启树莓派，还是仅仅重启相关网卡程序即可，若仅仅重启相关网卡程序，即可将添加网络摄像机程序放在这里
	实现。
	
2.安装python的虚拟环境，需要PIL库，flask库等。
cameraServer.py: 以flask为主的服务器程序，视图函数有：添加网络摄像机，产生image流并返回，设置数据库中参数。
cameraClient.py: 需要PIL库，获取二维图像。一个死循环函数。


3.配置nginx+ffmpeg产生hls流的环境
树莓派下载并按照X264源码
树莓派下载并安装ffmpeg源码
ffmpeg可以调用树莓派的硬件编码器

下载并安装nginx，划分内存空间存放切片文件，编写hls.sh脚本，执行。

详细细节请参考文件nginx-hls流。


开机自启动的程序：camClient 的MD.py, 将上传网络摄像机信息的程序结合到MD.py中。
				  cameraServer的main.py，
				  nginx
编写一个restart.sh文件，同时执行多个python程序，放在桌面自启动程序里。注意其中的python要指定相应虚拟环境中的python。

/home/pi/.config/ 目录下新建一个名为autostart文件夹
在autostart目录下新建camera.desktop文件，文件内容如下：
[Desktop Entry]

Type=Application

Name=testboot

NoDisplay=true

Exec=/home/pi/camera.sh 
