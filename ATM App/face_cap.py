import cv2
import face_recognition
import time

class Capture():
    clicked = 0
    def capture(self):
        
        # Get a reference to webcam 
        #video_capture = cv2.VideoCapture("/dev/video1")
        video_capture = cv2.VideoCapture(0)

        start_time = time.perf_counter()
        # Initialize variables
        face_locations = []

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      #frame[:, :, ::-1]
            # Find all the faces in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            # print(face_locations)

            # Display the results
            # for top, right, bottom, left in face_locations:
            #     # Draw a box around the face
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame,(220, 100),( 420, 300), (0, 0, 255), 2)

            # Display the resulting image
            cv2.imshow('Scan your face', frame)

            # Hit 'c' on the keyboard to capture and quit! only when face is recognised
            stop_time = time.perf_counter() - start_time
            # print(stop_time)

            if cv2.waitKey(1) and stop_time>5:
                if face_locations:
                    cv2.imwrite('face.jpg',frame)
                    self.clicked = 1
                    print('clicked..................')
                    break
                if stop_time>10:
                    break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()




