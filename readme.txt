Name                         : Somu LeelaMadhav

Programming Language used    : Python 



------------
Run the code
----------------
Interactive Mode
----------------
python maxconnect4.py interactive inputfile.txt computer-next/human-next [depth_level]

-------------
One-Move Mode
-------------
python maxconnect4.py one-move inputfile.txt output.txt [depth_level]

CODE STRUCTURE
---------------
The class minimax performs the decision-making.
Contains methods makeDecision() which returns minimax's decision,
maxVal() which performs maximizing operations,
minVal() which perfoms minimizing operations, 
and utility() which returns the utility that needs to be maximized or minimized.
	
result() calculates the new state after a particular move
	
possibleMoves() returns the moves that are possible on a state




