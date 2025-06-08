import cv2
import numpy as np

cap = cv2.VideoCapture("/dev/Ball_Recognition/video2")
if not cap.isOpened():
    print("カメラが開けません")
    exit()

def detect_largest_contour(mask, label, color, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)
            cv2.putText(frame, label, (int(x - radius), int(y - radius - 10)),
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

    # ノイズ除去（1回にして感度高め）
    for mask in [mask_red, mask_blue, mask_yellow]:
        mask[:] = cv2.erode(mask, None, iterations=1)
        mask[:] = cv2.dilate(mask, None, iterations=1)

    # 一番大きい輪郭だけ描画
    detect_largest_contour(mask_red, "Red", (0, 0, 255), frame)
    detect_largest_contour(mask_blue, "Blue", (255, 0, 0), frame)
    detect_largest_contour(mask_yellow, "Yellow", (0, 255, 255), frame)

    # 表示
    cv2.imshow("Largest Ball Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

