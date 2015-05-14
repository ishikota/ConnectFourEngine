ConnectFour Engine
=============================
  
ConnectFour engine written in Python.  
You can play with three kinds of computer programs,  
  
1. MiniMax - use MiniMax algorithm with Alpha-Beta Pruning  
2. UCT MCTS - use MonteCarloTreeSearch algorithm with UCT algorithm.  
3. Ogirinal MCTS - improved MCTS computer program.  
  
Set up and Run script
--------
First, download ConnectFour project file and change dicectory to ConnectFour/src/ui.  
Here, we assume that you cloned ConnectFour project to your HOME directory.  
Then run vs.py script.  
**Do not forget to change you directory to `ConnectFour/src/ui` before run script. (It will cause some error.)**  
```
cd $HOME/ConnectFour/src/ui
python vs.py
```

Game settings 
--------
First you will be asked that first player is human (you) or computer.
```$
> FIRST PLAYER IS ...
	1: HUMAN
	2: COMPUTER
```
If you choose 2 (COMPUTER) then choose computer algorithm.
```
> WHAT STRATEGY DOES COMPUTER USE ?
	1: MiniMax (IterativeDeepening)
	2: Flat MonteCarloTreeSearch
	3: Arranged MonteCarloTreeSearch
```
Next, set computer strength.

If you choose 1 (MiniMax algorithm) then choose max depth of search in MiniMax algorithm. 
```
> INPUT MAX DEPTH OF MINIMAX ([1,10] is recommended)...
```
Deeper max depth takes longer thinking time.  
I recommend you **NOT to set max depth more than 10**. (It takes very long time to make a move.)

If you choose 2 or 3 (MonteCarloTreeSearch) then choose the number of playout in MCTS.
```
>INPUT THE NUMBER OF PLAYOUT IN MONTE-CALRO-TREE-SEARCH.
```
MCTS algorithm would make better move as the number of playout increases.
But on the other hand, it takes longer thinking time.  
  
Next choose second player and set its strength in the same way.
```
> SECOND PLAYER IS ...
  1: HUMAN
  2: COMPUTER
```

Start ConnectFour !!
--------

Current board state will be displayed in each turn.  
```
   - - - - X - - 
   - - - - O - - 
   - - - - O - - 
   - - - O X - - 
   - X - X O - - 
   - O X O X - - 
   1 2 3 4 5 6 7 
```
  
Each square state is represented by three character.  
  
1. O : First player  
2. X : Second player  
3. - : Empty square  

You make a move by input the number of column you want to make a move (from 1 to 7) !!  

And if you want to finish the game, input 0 as your input like below.
```
--- TURN [ FIRSTPLAYER (O) ] ---
INPUT > 
0
> ARE YOU SURE TO QUIT THE GAME? (y/n)
y
> FINISH THE GAME
```
  
Enjoy ConnectFour !!

