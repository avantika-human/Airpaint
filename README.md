# ✋ AR Air Painter

Draw in the air using just your index finger and a webcam. No touch, no mouse — just your hand.

## Demo
Move your index finger up to draw. Put it down to stop. Press ESC to quit.

## How It Works
- **MediaPipe** detects your hand and tracks landmarks in real time
- The tip of your index finger (landmark 8) acts as the brush
- If your index finger is raised, it draws — if lowered, it lifts the brush
- The drawing is overlaid on the live webcam feed using **OpenCV**

## Tech Stack
- Python
- OpenCV
- MediaPipe

## Run It
```bash
pip install opencv-python mediapipe
python test22.py
```

## Controls
| Action | Gesture |
|--------|---------|
| Draw | Index finger up |
| Stop drawing | Index finger down |
| Clear canvas | Ctrl + C |
| Quit | ESC |
