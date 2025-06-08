import cv2
import numpy as np

# 焦点距離と実際のボールの直径（仮定）
FOCAL_LENGTH = 700.0  # 単位: ピクセル
REAL_DIAMETER = 6.5   # 単位: cm（例: 卓球ボール）

cap = cv2.VideoCapture("/dev/video0")
if not cap.isOpened():
    print("カメラが開けません")
    exit()

def detect_largest_contour(mask, label, color, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        if radius > 10:
            diameter_px = radius * 2
            distance = (REAL_DIAMETER * FOCAL_LENGTH) / diameter_px

            # 描画と距離表示
            cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)
            cv2.putText(frame, f"{label} {distance:.2f}cm",
                        (int(x - radius), int(y - radius - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # 🔴 赤色（色が薄くても検出しやすいよう緩めに）
    lower_red1 = np.array([0, 30, 30])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 30, 30])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # 🔵 青色
    lower_blue = np.array([90, 80, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # 🟡 黄色
    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([40, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # マスクを統合（bitwise OR）
    combined_mask = cv2.bitwise_or(mask_red, mask_blue)
    combined_mask = cv2.bitwise_or(combined_mask, mask_yellow)

    # ノイズ除去
    combined_mask = cv2.erode(combined_mask, None, iterations=1)
    combined_mask = cv2.dilate(combined_mask, None, iterations=1)

    # 1番大きい輪郭を描画（色は固定でも可）
    detect_largest_contour(combined_mask, "Ball", (0, 255, 0), frame)


    # 表示
    cv2.imshow("Largest Ball Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

