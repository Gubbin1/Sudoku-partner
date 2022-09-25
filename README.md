# Sudoku Helper App
Sudoku puzzles consist of a 9x9 grid, which much be filled with digits 1 through 9 appearing only once in every row, column, and 3x3 grid. 

This app was created with **Python 3.10**, using **Kivy 2.1**. Be sure to install the Kivy library before trying to run this project.
## About
I have always liked working on puzzles, and I thought this would be an interesting project. I wanted to build a program to solve sudoku puzzles using the actual methods that I would use to solve it, rather than solve it through brute force. I designed it to check for available moves given a puzzle, and show the user what the next possible move would be to progress in solving the puzzle. This app should be used as a partner to a sudoku puzzle. The user can enter a puzzle when they are having trouble finding thier next move, and get a hint to move on. Many sudoku apps have this feature, but what is unique about THIS app is that it can be used as a partner to pen and paper puzzles. The user can also click the "More Info" button to get a detailed description of how to recognize possible moves of that particular pattern.
The app was designed with a mobile interface in mind, as the eventual goal for this project is to integrate the phone camera with text recognition to make entering in puzzles much easier. That camera functionality is outside the scope of what I planned to do with this project for now, but it is built in such a way that adding that functionality shouldn't require too much re-designing.

## Layout
The GUI of this project was made entirely using Kivy. The largest area of the screen is taken up by the puzzle. Above the puzzle is an area that displays all of the possible options of a selected cell. Below is the number pad for puzzle entry, and buttons for using the app. To the right are a collection of example puzzles that were used mostrly for testing, but also serve as a helpful example of how the app works through a puzzle. The layout scales automatically with the window.

## Usage
