# Black Board

A simple digital whiteboard application built with Python and Pygame. Draw, erase, undo/redo, and scroll across an infinite canvas to sketch diagrams, write equations, or take quick notes.

## Screenshots

![Instructions & Shortcuts](https://github.com/umutcanekinci/black-board/blob/main/images/samples/sample-1.png?raw=true)
![Sample Diagram](https://github.com/umutcanekinci/black-board/blob/main/images/samples/sample-2.png?raw=true)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

- Python 3.x  
- [Pygame](https://www.pygame.org/) (2.x or later)

### Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/umutcanekinci/black-board.git
   cd black-board
   ```
   
2. **(Optional) Create a virtual environment**
  ```bash
  python -m venv venv
  # Activate it:
  source venv/bin/activate       # Linux / macOS
  venv\Scripts\activate          # Windows
  ```

3. **Install dependencies**
  ```bash
  pip install pygame
  ```

## Running the Application
  ```bash
  python main.py
  ```

## Features
- Multiple Pen Modes

- Circle Pen

- Linear Pen (draw continuous lines)

- Clickable Linear Pen (point‑and‑click lines)

- Eraser Mode with adjustable radius

- Undo / Redo support

- Infinite, Scrollable Canvas (use mouse wheel to pan)

- On‑screen Shortcuts Overlay and real‑time notifications

## Controls

- Key / Action	Function
- ESC	Exit application
- CTRL + Z	Undo last stroke
- CTRL + Y	Redo last undone stroke
- 1	Switch to Circle Pen
- 2	Switch to Linear Pen
- 3	Switch to Click‑to‑Draw Linear Pen
- 4	Switch to Eraser Mode
- Numpad + / Numpad -	Increase / Decrease pen or eraser size
- Mouse Wheel	Scroll canvas up/down

## Contributing

1. Fork this repository

2. Create your feature branch (git checkout -b feature/my-feature)

3. Commit your changes (git commit -m "Add some feature")

4. Push to the branch (git push origin feature/my-feature)

5. Open a Pull Request

## Authors
Umutcan Ekinci – @umutcanekinci

## License
This project is licensed under the MIT License.

## Contact
For feedback or questions, feel free to reach out at umutcannekinci@gmail.com
