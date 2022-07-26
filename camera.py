import io
import simplejpeg
import time
from picamera2 import Picamera2, Preview
from base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
            camera = Picamera2()
            config = camera.create_preview_configuration()
            camera.configure(config) 
            
            camera.start_preview (Preview.DRM)
            camera.start()
            output_buffer = io.BytesIO()

            while True:
                  array = camera.capture_array()
                  buf = simplejpeg.encode_jpeg (array, colorspace='RGBX')

                  output_buffer.seek(0)
                  output_buffer.write(buf)

                  yield  output_buffer.getvalue()

                  output_buffer.seek(0)
                  output_buffer.truncate()
            camera.stop_preview(Preview.DRM)
            camera.stop()
