
# Fifteen Puzzle with IDA* Solver
A Pygame-based sliding puzzle to demonstrate the classic Fifteen Puzzle. Move the blank tile around using the arrow keys or let the built-in IDA* solver do the work. It even shows a fun "Solving..." animation in the meantime, so the game never freezes up!

## Features

- **Interactive Sliding Puzzle**: Move tiles manually with the arrow keys.
- **Background IDA* Solver**: Press "S" to let the solver find the solution.  
- **Animated Moves**: Watch each tile slide smoothly.
- **Non-Freezing UI**: While the solver runs, a changing "Solving..." message displays so the game stays responsive.
- **Easy Scramble**: Press "Space" to scramble the puzzle again and reset your moves.

## Dependencies

- **Python 3.x**
- **Pygame**

## Getting Started

1. **Head over to the releases page**  
   - Download the source code of the latest release.  
   - Install the required dependencies using pip:
     ```bash
     pip install pygame
     ```
   - Extract the contents of the file and run the `main.py` script to start the application.

2. **OR clone the repository to your local machine**:
   ```bash
   git clone https://github.com/your-username/Fifteen-Puzzle-IDAsolver.git
   ```
   - Install the required dependencies:
     ```bash
     pip install pygame
     ```
   - Run the `main.py` script:
     ```bash
     python main.py
     ```

3. **OR press the green '<> Code' button** and download the ZIP file:
   - Extract the contents of the ZIP file into one folder.
   - Run the `main.py` script to start the application.

## Usage

- **Arrow Keys**: Move the blank tile up, down, left, or right.
- **Space**: Scramble the puzzle with a certain number of random moves.
- **S**: Start the IDA* solver. The game will display "Solving..." to let you know the solver is working.
- **Live Animation**: Once the solver finishes, tiles will slide automatically to the correct solution.

## Credits

- Made by Harshil (vSparkyy)
- Fonts used: Montserrat Regular & Bold
- Inspired by the classic Fifteen Puzzle game.

## Contributing

Contributions are welcome! If you find any issues or want to add more features (like extra puzzle sizes or different heuristics), feel free to create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
