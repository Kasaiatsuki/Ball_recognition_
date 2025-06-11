# ボール認識のセットアップコード

# 概要
* Ball_recognition_ は以下の機能を提供します.
  * PCの内臓カメラやUSB接続をしたWEBカメラの動作確認
  * ボールの適切なHSV閾値の設定
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
---
# PCの内臓カメラやWEBカメラの動作確認
```bash
ls /dev/video*
```
出てきた番号を camera.py の
```bash
cap = cv2.VideoCapture()
```
の( )に入力してください.
* "/Ball_Recognition/video2"のように入力することも可能です.
* 入力する番号は内臓カメラの場合は 0 か 1 が多くWEBカメラだと 2 の場合が多いです.
```bash
pytno3 camera.py
```
で実行するとGUIにカメラの映像が映ります.

---
# ボールの適切なHSV閾値の設定
以下のコードを実行するとHSVの閾値の調整タブ(Trackbars)とカメラ映像タブとHSVの閾値を調整した後の読み取れる映像タブの３つが開かれます.

```bash
python3 hsv.py
```
HSVの閾値の調整タブ(Trackbars)をいじって自分の好きなボールのHSVの閾値を調節してください.

![HSV](images/Screenshot%20from%202025-06-08%2022-29-23.png)

## トラックバーの意味

| トラックバー名 | 意味         | 使い方                                                                 |
|----------------|--------------|------------------------------------------------------------------------|
| LH             | Lower Hue    | 検出したい色相の下限                        |
| LS             | Lower Saturation | 色の鮮やかさの下限. を大きくするとくすんだ色を除外              |
| LV             | Lower Value  | 明るさの下限. 暗い影などを除外したい時に上げる                        |
| UH             | Upper Hue    | 検出したい色相の上限.                        |
| US             | Upper Saturation | 色の鮮やかさの上限. 255でOKなことが多い                             |
| UV             | Upper Value  | 明るさの上限. 255で問題ないことが多い                                |

## 実行例
![zikkourei](images/Screenshot%20from%202025-06-11%2015-19-00.png)

---
# ボールの色認識

```bash
python3 ball1.py
```
* このプログラムは赤,青,黃色の3色のボールを同時に認識できるようになっています.
* デフォルトではこの３色ですがHSVの閾値設定を増やせば認識できる色も増やすことができます.

---

# カメラの適切な焦点距離の設定
このコードは次のボールとカメラとの距離を測るコードに使う焦点距離を計算するコードです.

```bash
vi calibraition.py
```
* REAL_KIAMETERにボールの直径(cm),KNOWN_DISTANCEに実際のボールとカメラセンサの距離(cm)を入力してください.
```bash
python3 calibration.py
```
* 代表点３個の値の平均値をとったほうが正確かも.(30cm,50cm,70cmなど)
## 実行例
![zikkourei３](images/Screenshot%20from%202025-06-11%2015-48-52.png)

---

# ボールとカメラとの距離測定
* このコードはボールとカメラの距離を測るコードです.
* カメラの解像度にもよりますがうまくいくと5cm〜180cm以上の範囲で距離を測ることができます.
```bash
vi ball_distance.py
```
ボールの直径,カメラの焦点距離,HSV閾値設定を入力してください.
```bash
python3 ball_distance.py
```

## 実行例
![zikkourei2](images/Screenshot%20from%202025-06-11%2016-50-46.png)

---

# ライセンスと著作権

* このソフトウェアパッケージは，3条項BSDライセンスの下，再頒布および使用が許可されます．
* © 2025 Atsuki Kasai
