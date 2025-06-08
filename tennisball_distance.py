import cv2
import numpy as np

# テニスボール直径 [cm] と焦点距離 [ピクセル]
REAL_DIAMETER = 6.7
FOCAL_LENGTH = 1051.6  # ※これは仮値。キャリブレーションすればより正確に

# カメラの起動（番号は必要に応じて変更）
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("カメラが開けません")
    exit()

def detect_tennis_ball(mask, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        if radius > 10:  # ノイズ除去
            diameter_px = radius * 2
            distance = (REAL_DIAMETER * FOCAL_LENGTH) / diameter_px

            # 描画
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, f"{distance:.2f}cm", (int(x - radius), int(y - radius - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # ターミナルに出力
            print(f"距離: {distance:.2f} cm")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # テニスボールの色に合わせたHSV範囲（調整済み）
    lower_yellow = np.array([25, 60, 100])
    upper_yellow = np.array([45, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # ノイズ除去
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    detect_tennis_ball(mask, frame)

    cv2.imshow("Tennis Ball Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

