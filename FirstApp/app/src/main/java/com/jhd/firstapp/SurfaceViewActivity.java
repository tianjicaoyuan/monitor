package com.jhd.firstapp;

import android.app.Activity;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;


import java.io.IOException;

public class SurfaceViewActivity extends Activity {
    private SurfaceView mSurfaceView;
    private MediaPlayer mediaPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.surface_view);
        Button mButtonStart;
        mSurfaceView = findViewById(R.id.surfaceView1);
        mButtonStart = findViewById(R.id.button_start_surfaceView);
        mButtonStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(mediaPlayer==null){
                    mediaPlayer = new MediaPlayer();
                }
                mediaPlayer.reset();
                try {
                    //Sets the data source (file-path or http/rtsp URL) to use,设置播放文件的路径
                    Intent intent =getIntent();
                    String url = intent.getStringExtra("videoAddress");
                    mediaPlayer.setDataSource(url);
                    //Sets the audio stream type for this MediaPlayer，设置流的类型，此为音乐流
                    mediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
                    //Sets the SurfaceHolder to use for displaying the video portion of the media，设置播放的容器
                    mediaPlayer.setDisplay(mSurfaceView.getHolder());
                    mediaPlayer.prepare();
                    //Interface definition for a callback to be invoked when the media source is ready for playback
                    mediaPlayer.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
                        @Override
                        public void onPrepared(MediaPlayer mp) {
                            mp.start();
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
