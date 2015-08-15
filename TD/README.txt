TD
===============

Entry in PyWeek #12  <http://www.pyweek.org/20/>
URL: https://pyweek.org/e/CandL-FAB-20/
Team: CandL
Members: Luke Paireepinart and Courtney Peters
License: see LICENSE.txt
Artwork: Courtney Peters
Sound effects: http://www.bfxr.net/
Music: http://wrathgames.com/blog/free-development-resources/music/
License: The MIT License

Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py

Dependencies
--------------------
Pygame
Python 2.7.10


How to Play the Game
--------------------

Buy weapons and keep the nano robots from stealing all your data! If you lose
all the data at the top right, you lose the game!


Development notes
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload
