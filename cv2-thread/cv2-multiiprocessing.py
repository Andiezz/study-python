# using cv2 to play video
import threading
import time
import cv2
import multiprocessing as mp


class VideoPlayerService:
    def __init__(self, image_width=640, image_height=640) -> None:

        self.playing_video_process = None

        self.image_width = image_width
        self.image_height = image_height

    def start_play_local_video_process(self, video_name="site-tour.mp4", duration=None):
        self.playing_video_process = mp.Process(
            target=self.play_local_video, args=(video_name,)
        )
        self.playing_video_process.start()

        if duration is not None:
            time.sleep(duration / 1000)
            self.stop_playing_video()

    def play_local_video(self, video_name, video_folder=""):
        print("Start playing video from")
        cap = cv2.VideoCapture(video_folder + video_name)
        fps = cap.get(cv2.CAP_PROP_FPS)

        desired_height = 480
        desired_width = 960

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (desired_width, desired_height))

            cv2.imshow("frame", frame)

            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

    def stop_playing_video(self):
        self.playing_video_process.terminate()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        video_player_service = VideoPlayerService()
        video_player_service.start_play_local_video_process("site-tour.mp4", 10000)

        video_player_service = VideoPlayerService()
        video_player_service.start_play_local_video_process("site-tour.mp4", 10000)
    except Exception as e:
        print(e)
