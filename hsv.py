import cv2
import numpy as np

def nothing(x):
    pass


cap = cv2.VideoCapture(2)

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 400, 300)

# トラックバー作成（Hは0〜179, S/Vは0〜255）
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Original", 640, 480)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Mask", 640, 480)
cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Result", 640, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ぼかし→HSV変換
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # トラックバーから値を取得
    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")
    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])

    # マスク作成
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 表示
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

