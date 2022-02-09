import cv2

cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)
i = 0

while True:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    if not ret or not ret2:
        print("failed to grab frame")
        break
    cv2.imshow("frame", frame)
    cv2.imshow("frame2", frame2)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        cv2.imwrite('frameA'+str(i)+'.png', frame)
        cv2.imwrite('frameB'+str(i)+'.png', frame2)
        i += 1

cap.release()
cap2.release()
cv2.destroyAllWindows()