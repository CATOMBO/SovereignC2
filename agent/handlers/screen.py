import mss
import base64
import io
from datetime import datetime
from PIL import Image

def handle_screenshot():
    with mss.mss() as sct:
                        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                        screenshot = sct.grab(monitor)
                        
                        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                        
                        buffer = io.BytesIO()
                        img.save(buffer, format="JPEG")
                        
                        encoded = base64.b64encode(buffer.getvalue()).decode()
                        filename = f"screenshot_{datetime.now().strftime('"%d-%m-%Y_%H-%M-%S"')}.jpeg"
                        
    return {"status": "success",
            "output": {filename: "screenshot.jpe",
                       "data": encoded}}