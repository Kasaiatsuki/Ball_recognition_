import cv2
import numpy as np

# 実寸：ボールの直径（cm）
REAL_DIAMETER = 6.5
# 実距離：ボールとカメラの距離（cm）
KNOWN_DISTANCE = 70.0  # ←あなたが実際に測った距離に変えてください！

cap = cv2.VideoCapture("/dev/video2")
if not cap.isOpened():
    print("カメラが開けません")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # テニスボールの色範囲（必要に応じて調整）
    lower_yellow = np.array([71, 142, 139])
    upper_yellow = np.array([139, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        if radius > 10:
            pixel_diameter = radius * 2
            # 焦点距離の計算式
            focal_length = (pixel_diameter * KNOWN_DISTANCE) / REAL_DIAMETER

            # 結果の表示
            print(f"画面上の直径: {pixel_diameter:.2f} px")
            print(f"計算された焦点距離: {focal_length:.2f} px")

            # 画面にも描画
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, f"Focal: {focal_length:.2f}px", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Calibration", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

