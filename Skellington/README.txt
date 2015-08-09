This is the game project skeleton generator called Skellington.

It was developed for PyWeek (http://pyweek.org/) but is also useful outside
of that challenge.

It will create a new project directory for you given some short name
containing:

- a new python package directory for your code with the short name you
  supplied and a __main__.py stub file to start off your main game code
- a "run_game.py" python script to run your game
- a "data" directory to place all your game images, sounds, fonts, map
  files, etc. in and a module in your game code package to access files in
  that directory
- a set of configuration files which are used to bundle your game up for
  distribution to others
- a bunch of documentation files; the most important of these are the
  README.txt and LICENSE.txt files (see http://pyweek.org/s/rules for
  pointers about licenses)

To create your game skeleton you should run the create_skeleton.py script.

To create files to distribute to others use the setup.py script in your
game directory. It may generate one of a number of files:

- sdist; build a source dist -- everyone should upload one of these
- py2exe; build an exe for Windows
- py2app; build an app for OS X
- cx_freeze; build a linux binary (not implemented)

Once you're ready to upload your game to the challenge you may use the
pyweek-upload.py script in your game's directory.
