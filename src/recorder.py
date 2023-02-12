import numpy as np
import typing
import moviepy.editor as editor
import os.path
import enum
import cv2
import random
import string
import os

def random_string(length: int=10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

class BaseExport:
    
    """
    Base class for exporting
    """
    
    frames: typing.Union[np.ndarray, str]= []
        
    def push(self, frame: np.ndarray) -> None:
        """
        Push a frame to the stack
        """
        raise NotImplementedError()
    
    def export(self) -> editor.ImageSequenceClip:
        """
        Export the frames to a ImageSequenceClip
        """
        raise NotImplementedError()
    
    def cleanup(self) -> None:
        """
        Cleanup the frames
        """
        raise NotImplementedError()

class ExportAsDisk(BaseExport):
    
    """
    This class exports the frames to disk and then exports them to a ImageSequenceClip.
    This is recommended for large frames/long video/lots of frames per second and low-end computers
    """
    
    count = 0
    folder_name = random_string()
    os.makedirs(os.path.join(os.path.dirname(__file__), "frames/"+folder_name))
    
    def push(self, frame: np.ndarray):
        path = os.path.join(os.path.dirname(__file__), "frames/"+self.folder_name+"/")
        cv2.imwrite(f"{path}frame_{self.count}.png", frame)
        self.frames.append(path+"frame_"+str(self.count)+".png")
        self.count += 1
        
    def export(self):
        return editor.ImageSequenceClip(self.frames, fps=60)
    
    def cleanup(self):
        path = os.path.join(os.path.dirname(__file__), "frames/"+self.folder_name+"/")
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        os.rmdir(path)
    
class ExportAsMemory(BaseExport):
    
    """
    This class exports the frames to memory and then exports them to a ImageSequenceClip
    Recommended for small frames/short video/few frames per second and high-end computers.
    Warning: This can cause memory issues if you have a lot of frames. We talking 1 gigabyte for 1000 frames.
    """
    
    def push(self, frame: np.ndarray):
        self.frames.append(frame)
        
    def export(self):
        return editor.ImageSequenceClip(self.frames, fps=60)
    
    def cleanup(self):
        self.frames = []

class ExportMethod(enum.Enum):
    disk = ExportAsDisk()
    memory = ExportAsMemory()

class OutputExport(enum.IntEnum):
    video = 0
    gif = 1

class Recorder:
    """
    A class to record video
    """
    
    def __init__(self, size: tuple[int,int], fps: int=60, filename: str="output.avi", method: ExportMethod=ExportMethod.disk) -> None:
        self.size = size
        self.fps = fps
        self.filename = filename
        self.audio: list[np.ndarray] = [] # this is fine and all
        self.method: typing.Union[ExportAsDisk, ExportAsMemory] = method.value
    def update(self, frame: np.ndarray, audio:typing.Union[editor.AudioClip, np.ndarray] =None):
        if not audio:
            audio = editor.AudioClip(lambda _: 0, duration=1/self.fps) # silence
        self.method.push(frame)
        self.audio.append(audio)
    def export(self):
        a = self.method.export()
        if not self.filename.endswith(".gif"):
            a.audio = editor.CompositeAudioClip(self.audio)
            a.write_videofile(self.filename, fps=self.fps, codec="libx264")
        else:
            a.write_gif(self.filename, fps=self.fps)
        self.method.cleanup()