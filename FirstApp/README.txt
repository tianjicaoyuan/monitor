这是android APP的开发程序，开发者可根据该程序对APP进行改进与修改。

第一步：首先需要安装android studio。

可搜索教程安装。
问题一是注意在BUILD，exception，DEployment,下的gradle，
勾选上enable enbeded maven repository.
第二个是在构建项目时无法找到 Build Tools revision 28.0.2时，修改APP的build gradle文件添加
compileSdkVersion 28
buildToolsVersion "28.0.3"
第一次重构可能会出问题，再重新运行一次即可。
注意SDK的版本，如果需要安装第三方播放器vitamio，那么minSdkVersion 14
targetSdkVersion 22，目标SDK版本必须小于22.才可支持。
注意项目安装路径最好为英文路径。
需要配置好SDK和jdk。


可操作文件：
app下的main文件夹。java文件包，每一个java文件对应一个activity，
每一个activity对应一个res/layout下的布局控制文件。res文件夹存储APP的资源，assets也存储了
APP的资源，不过是web app的资源主要包括js，css库等资源和只可在HTML5页面访问的资源。APP界面与
HTML文件相对应。
res还可存储缓存在APP端的视频，通过R.ID访问。AndroidManifest.xml主要对几个activity的注册设置。


MainAcivity.java主要是控制web view的，web view会运行多个HTML5页面。
videoActivity主要是利用mediaplayer播放器播放HLS流。

参数人为设置与调整：
存储服务器必须处在公网或者与APP处在局域网下才可通信。
第一个是所有assets文件夹下的HTML文件中的ajax请求中的URL必须设置好，这个是存储服务器的IP地址。

关于settings.html还未完成，还有Message.html。

目前实现的功能主要是：登录与注册，主页面显示摄像机，历史视频查询与回放，实时视频播放。




