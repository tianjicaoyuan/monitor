package com.jhd.firstapp;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.view.KeyEvent;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;
    @SuppressLint("JavascriptInterface")
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED);
        init();
    }
    @SuppressLint("SetJavaScriptEnabled")
    private void init(){
        webView = findViewById(R.id.webView1);
        WebSettings settings = webView.getSettings();
        if(Build.VERSION.SDK_INT>=Build.VERSION_CODES.LOLLIPOP){
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        }
        settings.setJavaScriptEnabled(true);//设置WebView属性,运行执行js脚本
        settings.setLoadWithOverviewMode(true); // 缩放至屏幕的大小
        settings.setUseWideViewPort(true); //将图片调整到适合webview的大小
        settings.setSupportZoom(true); //支持缩放，默认为true。是下面那个的前提。
        settings.setBuiltInZoomControls(true); //设置内置的缩放控件。若为false，则该WebView不可缩放
        settings.setDisplayZoomControls(false); //隐藏原生的缩放控件
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);//优使用webview中缓存
        settings.setAllowFileAccess(true);//设置可以访问文件
        settings.setJavaScriptCanOpenWindowsAutomatically(true);//支持通过JS打开新窗口
        settings.setLoadsImagesAutomatically(true);//支持自动加载图片
        settings.setPluginState(WebSettings.PluginState.ON);
        settings.setDefaultTextEncodingName("utf-8");
        webView.setWebViewClient(new WebViewClient(){
            //设置在webView点击打开的新网页在当前界面显示,而不跳转到新的浏览器中
            @Override
            public boolean shouldOverrideUrlLoading(WebView view,String url){
                view.loadUrl(url);
                return true;
            }
            //@Override
            //public void onPageFinished(WebView view, String url)
            //{
                //super.onPageFinished(view, url);
                //String jquery = readJs("bootstrap/js/jquery.js");
                //String bootstrap = readJs("bootstrap/js/bootstrap.min.js");
                //String bootstrapValidator = readJs("bootstrap/js/bootstrapValidator.js");
                //view.loadUrl("javascript:" + jquery);
                //view.loadUrl("javascript:" + bootstrap);
                //view.loadUrl("javascript:" + bootstrapValidator);
            //}

        });
        webView.setWebChromeClient(new WebChromeClient(){
            //设置弹出对话框显示
            @Override
            public boolean onJsAlert(WebView view, String url, String message, final JsResult result){
                AlertDialog.Builder b= new AlertDialog.Builder(MainActivity.this);
                b.setTitle("");
                b.setMessage(message);
                b.setPositiveButton("确定", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        result.confirm();
                    }
                });
                b.setCancelable(false);
                b.create().show();
                return true;
            }
        });
        webView.addJavascriptInterface(new AndroidtoJs(),"videoActivity");//设置与js交互
        webView.loadUrl("file:///android_asset/login.html");//设置打开APP的入口页面
    }
    //设置回退点击，下方的
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    //退出APP的清除机制
    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.loadDataWithBaseURL(null, "", "text/html", "utf-8", null);
            webView.clearHistory();

            ((ViewGroup) webView.getParent()).removeView(webView);
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
    //点击相应按钮，即可调用videoActivity播放HLS流，视频流，P为传入的变量
    public class AndroidtoJs{
        @SuppressLint("javascriptInterface")
        @JavascriptInterface
        public void show(final String p){
            MainActivity.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Intent intent = new Intent(MainActivity.this,videoActivity.class);
                    intent.putExtra("videoAddress",p);
                    startActivity(intent);
                }
            });
        }
    }
}
