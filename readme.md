# AI Wechat 助手

## 安装

```shell
pip install -r requirements.txt
```

## 运行

执行目录下的 `main.py`

## 使用前须知
使用前请先注册申请文心千帆或者讯飞大模型的 API 应用，切换模型修改 `main.py` 中 `USE_AI` 的值，1 是”科大讯飞“，2
是”文心千帆“，如果都不选择则会调用一个免费的朋友圈文案生成接口。

- [讯飞大模型申请地址](https://www.xfyun.cn/)
- [文心千帆申请地址](https://cloud.baidu.com/wenxin.html)

开启之后会监听所有微信消息，并自动回复所有消息。本项目仅供娱乐和学习使用~