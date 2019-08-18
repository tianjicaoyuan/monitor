package com.jhd.firstapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.VideoView;


public class videoActivity extends Activity implements View.OnClickListener {
    private VideoView mVideoView;
    private MediaController  mMediaController;
    private Button btn_start;
    private Button btn_pause;
    private Button btn_update;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //intent 是两个activity之间的中间件，来传输信息的，获取视频地址
        Intent intent =getIntent();
        String strPath = intent.getStringExtra("videoAddress");
        //获取APP内部资源的方式，在res文件夹下res/raw/test.m3u8，新建一个文件夹，需要重新build
        //String rawPath = "android.resource://" + getPackageName() + "/" + R.raw.test;
        mMediaController=new MediaController(this);//实例化控制器
        setContentView(R.layout.video_view);
        //三个按钮控制视频
        btn_start  = findViewById(R.id.btn_start);
        btn_pause  = findViewById(R.id.btn_pause);
        btn_update = findViewById(R.id.btn_update);
        btn_start.setOnClickListener(this);
        btn_pause.setOnClickListener(this);
        btn_update.setOnClickListener(this);

        mVideoView = findViewById(R.id.surface_view);
        //设置播放地址 例如："http://172.20.10.8/hls/stream.m3u8"
        mVideoView.setVideoPath(strPath);
        mVideoView.setMediaController( mMediaController); //绑定控制器
        //mVideoView.setOnPreparedListener(mOnPreparedListener);
        //取得焦点 mVideoView.requestFocus(); 设置相关的监听
        //showController.sendEmptyMessageDelayed(0, 1000);
        mVideoView.start();

    }
    public void refresh(){
        onCreate(null);
    }
    @Override
    public void onClick(View v){
        switch (v.getId()) {
            case R.id.btn_start:
                mVideoView.start();
                break;
            case R.id.btn_pause:
                mVideoView.pause();
                break;
            case R.id.btn_update:
                refresh();
                break;
        }
    }

}
