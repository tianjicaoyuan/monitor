1.修改配置文件。
其中test文件主要用来测试，如何通过python程序修改树莓派的配置文件。
test.py调用test.sh，test.sh负责修改test.txt文件。

2. 添加网络摄像机主要分为三步：
	首先需要安装hostapd和DHCP，并配置相关文件。参考地址http://wiki.jikexueyuan.com/project/raspberry-pi/wifi.html。
	1.将无线网络的名称和密码添加到相应的网络配置文件中=input_network.sh
	2.修改两个网络配置文件，通过互换两个配置文件的名称。dhcpcd.sh和interfaces.sh。
	3.重启树莓派
	
3.camera_pi.py文件主要用来产生image流。可对image流的相关参数进行设置，没有声音缺点。


