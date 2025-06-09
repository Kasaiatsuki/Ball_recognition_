# ボールの色認識のセットアッププログラム

# 概要
* Ball_recognition_ は以下の機能を提供します.
  * PCの内臓カメラやUSB接続をしたWEBカメラの動作確認
  * 対象にするボールの適切なHSV閾値の設定
  * ボールの色認識
  * カメラの適切な焦点距離の設定
  * ボールとカメラとの距離測定
---
# 動作環境
* Ubuntu 22.04.05LTS
---
# インストール方法
OpenCVをインストールしていない方は以下を実行してください.
```bash
sudo apt update
sudo apt install python3-opencv
```
インストールを既にされてる方は以下を実行してください.
```bash
git clone https://github.com/Kasaiatsuki/Ball_recognition_.git
cd Ball_recognition_
```
