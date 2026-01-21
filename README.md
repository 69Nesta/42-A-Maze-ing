*This project has been created as partof the 42 curriculum by mthetcha, rpetit.*

# Description

This project is based on algorithms and visual rendering using MLX. The project retrieves a configuration to generate a maze, displays it, and then generates the solution to connect the entrance to the exit.


# Instructions

Use `make run` to compile all and start the project

## Structure
```
.
├── Makefile
├── a_maze_ing.py
├── config.txt
├── src
│   ├── All algo and parsing Files
│   └── diplay
│		└── All display Files
└── README.md

```

## Config.txt
```
# Width of the maze in cells (horizontal size)
WIDTH = 50

# Height of the maze in cells (vertical size)
HEIGHT = 34

# Entry point of the maze (x, y coordinates)
# This is where the player/solver starts
ENTRY = 0, 0

# Exit point of the maze (x, y coordinates)
# This is where the maze is solved
EXIT = 45, 28

# File name where the generated maze will be saved
OUTPUT_FILE = "maze.txt"

# If True, generate a "perfect" maze
# A perfect maze has exactly one path between any two points (no loops)
PERFECT = True

# Seed for the random number generator
# Using the same seed will always generate the same maze
# Set to None or change the number for a different maze
# If set you cant not generate a new maze on display
MAZE_SEED = 0

# Enable or disable animation during maze generation
# True = show generation step-by-step
# False = generate instantly
ANIMATE_MAZE_GENERATION = True

# Speed of the maze generation animation in milliseconds
# Higher value = slower animation
# Lower value = faster animation
MAZE_GENERATION_SPEED = 10

# Enable or disable animation during maze solving
# True = show the solving process step-by-step
# False = solve instantly
ANIMATE_MAZE_SOLVING = True

# Speed of the maze solving animation in milliseconds
# Higher value = slower animation
# Lower value = faster animation
MAZE_SOLVING_SPEED = 10

# Enable or disable debug mode
DEBUG_MODE = False

# Show fps 
SHOW_FPS = True
```

# Resources

- **Online documentations** : General research and algorithm understanding
- **Peer-to-peer learning** : Code reviews and discussions
- **Visualization maze generation** : https://professor-l.github.io/mazes/
- **Understanding maze generation** : https://en.wikipedia.org/wiki/Maze_generation_algorithm

# Technical explanation

### Backtracking Generation

Move a head randomly from the start to the exit, creating its path by breaking walls. If the head is blocked in a dead end, the algorithm moves backward until it can move again and generate the rest of the maze. *(by mthetcha)*

### Prim Generation

This algorithm generates a maze from a starting cell by randomly exploring neighboring cells that have not yet been visited, removing the walls between connected cells as it goes.
It maintains a list of cells “to be explored” and continues until all accessible cells have been incorporated into the maze. *(by mthetcha)*


#### **We chose these algorithms because they allow us to keep the 42 logo and generate around it, unlike other algorithms that go over the 42 logo.**


### Algorithm that makes the maze imperfect

The algorithm scans the entire generated maze to find dead ends, extending 30% of them to create loops while maintaining an aesthetic maze that does not resemble a grid. *(by mthetcha)*

### A Star Pathfinding

This algorithm traverses the maze by gradually exploring the squares accessible from a given point, avoiding revisiting those already processed.
As soon as it reaches the starting square, it reconstructs and returns the most optimized reverse path to follow. *(by rpetit)*

### Animation display

Each change in the maze generation and pathfinding path is saved in a list, which is then read in order to display the animation as it was generated. *(by rpetit)*

### Reusable parts

The generation algorithms are in classes that are reusable, the display and parsing are also independent.

# Team and project management

### Repartitions
- **mthetcha**: Algorithmic part
- **rpetit**: Visual and parsing part

This distribution was decided at the start and remained in place throughout the project.
# Advanced features

### Color pick
It is possible to choose the color of the 42 logo using a color picker. *(by rpetit)*

### Algorithms Switch

It is possible to choose which algorithm to use thanks to a switch button. *(by rpetit)*
