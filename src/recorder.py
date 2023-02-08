import cv2
import numpy as np
import subprocess
class Recorder:
    """
    A class to record video
    """
    
    def __init__(self, size: tuple[int,int], fps: int=60, filename: str="output.avi") -> None:
        self.size = size
        self.fps = fps
        self.filename = filename
        self.video: cv2.VideoWriter = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*"XVID"), self.fps, self.size)
        self.frames: list[np.ndarray] = []
    def update(self, frame: np.ndarray, inverted: bool=True):
        if inverted:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frames.append(frame)
        
    def export(self):
        for frame in self.frames:
            pic = cv2.resize(frame, tuple(reversed(frame.shape[:2])))
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            cv2.imshow("frame",pic)
            cv2.waitKey(1)
            self.video.write(pic)
        cv2.destroyAllWindows()
        self.video.release()