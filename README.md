# Sudoku Helper App
### Video Demo: https://youtu.be/I-S9k-p43vo

### Description
Sudoku puzzles consist of a 9x9 grid, which much be filled with digits 1 through 9 appearing only once in every row, column, and 3x3 grid. 

This app was created with **Python 3.10**, using **Kivy 2.1**. Be sure to install the Kivy library before trying to run this project.
## About
I have always liked working on puzzles, and I thought this would be an interesting project. I wanted to build a program to solve sudoku puzzles using the actual methods that I would use to solve it, rather than solve it through brute force. I designed it to check for available moves given a puzzle, and show the user what the next possible move would be to progress in solving the puzzle. This app should be used as a partner to a sudoku puzzle. The user can enter a puzzle when they are having trouble finding thier next move, and get a hint to move on. Many sudoku apps have this feature, but what is unique about THIS app is that it can be used as a partner to pen and paper puzzles. The user can also click the "More Info" button to get a detailed description of how to recognize possible moves of that particular pattern.
The app was designed with a mobile interface in mind, as the eventual goal for this project is to integrate the phone camera with text recognition to make entering in puzzles much easier. That camera functionality is outside the scope of what I planned to do with this project for now, but it is built in such a way that adding that functionality shouldn't require too much re-designing.

## Layout
The GUI of this project was made entirely using Kivy. The largest area of the screen is taken up by the puzzle. Above the puzzle is an area that displays all of the possible options of a selected cell. Below is the number pad for puzzle entry, and buttons for using the app. To the right are a collection of example puzzles that were used mostly for testing, but also serve as a helpful example of how the app works through a puzzle. 

Once the puzzle has been "Locked in", number entry becomes impossible, as the app enters hint mode. Where the buttons once were is now a scrolling list of the history of moves found by the app. At the bottom of the window is a slider which can be used to scroll through the history of the puzzle. Pressing the "More info" button will change the screen to a description of the highlighted move.

The layout scales automatically with the window, feel free to try scaling freely.

## Usage
To enter a puzzle, simply click on the desired cell, and then click the desired number. When operating on PC entering numbers via keyboard is also supported. 

## Description of files:
main.py contains the python needed for the layout of the app, the logic for the buttons, and the "more info" page in all of its incarnations. 

methods.py contains the classes for "puzzle", "history", and "cell" along with all of the different "methods" for finding the next available move in a sudoku puzzle. I did not implement every possible method for solving a sudoku puzzle, but I provided enough to be sufficient to solve any puzzle up to the extremely difficult. I would like to return to this project and fill it out with more methods at some point, but I would first want to impliment camera capture and text recognition. 

# The cell class
Cells are the individual squares that make up a puzzle. The cell class includes the "toggle button" from the Kivy library which enables user interaction, information on what numbers are still possible for that cell at that time, the cell's own index, and which 3x3 block the cell belongs to. This class also hosts a number of useful functions, such as filling the cell in with an answer, updating related cells, and finding other cells which are within it's own influence. 

# The puzzle class
The puzzle class holds the 81 "cells" that make up a puzzle in a 2D array, along with useful information such as a function for finding a cell by index, and a function for coloring in cells based on a given "history"

# The history class
The history class is simply a holder for a dictionary that has all of the information for a move that the app finds. It includes the name of the method used, the index of the cells which were used to find the move, the cells which are updated as a result of the move, and whether the move was found in a row, column, or box. A new instance of this class is created with each found move, and is stored in a list in order to enable scrolling through the history of the solved puzzle.

# The methods
I included enough methods for finding moves to solve the vast majority of sudoku puzzles. There are more moves which I may want to add at a later time, but the ones included are enough to be useful, and adding new methods is not too difficult. 
The methods included are (Listed in order of complexity):
1. Naked Single.
    - When a cell has only one option, it can be filled in with that option.
2. Hidden Single.
    - When a cell is the only cell in its row/column/block that could possibly be a certain value, it can be filled in with that value.
3. Naked Pair.
    - When two cells in the same row/column/block have only two possible options, and those options match, those numbers can be eliminated from all other cells in their row/column/block.
4. Hidden Pair.
    - When a pair of possible values appear only in a pair of cells in a row/column/block, all other options can be eliminated from that pair of cells. 
5. Locked Candidate.
    - If a certain value in a row/column is only possible in one block, then it can be removed from the rest of the cells in that block.
6. Pointing Tuple.
    - If a certain value in a block is only possible in one row/column, then it can be removed from the rest of the cells in that row/column.
7. Naked Triple.
    - The same as naked pairs but three values in three cells. There is an increase in complexity as all three cells don't necessarily need to contain all three possible values.
8. Hidden Triple.
    - The same as hidden doubles with the same increased complexity found in naked triples.
9. X Wing.
    - When two pairs of cells in two seperate rows/columns also share the same columns/rows that possibility can be removed from those columns/rows.
10. Y Wing.
    - When one cell with possibilities A and B sees two cells with possibilities B C and A C respectively, all cells that can see all three can remove C from their possibilities. 
11. Simple Coloring.
    - Finds a chain of cells for a given value, and "colors" them alternating colors. Any cells seeing cells in the chain of both colors can remove the value.