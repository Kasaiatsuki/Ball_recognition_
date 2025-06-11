import cv2

cap = cv2.VideoCapture("/dev/video2")
if not cap.isOpened():
    print("カメラが開けません")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームが取得できません")
        break

    cv2.imshow("webカメラ映像", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
