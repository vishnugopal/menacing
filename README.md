# Menacing v0.9
    
Welcome to Menacing. Menacing is an emulation of MENACE
developed in 1960 by an English biologist named Donald
Michie. It stays fairly true to the original MENACE
simulation, and has both positive and negative
reinforcements. To learn more about MENACE, go to
http://www.atarimagazines.com/v3n1/matchboxttt.html

To run:

    python menacing.py --init
    python menacing.py --train 100

More complete usage:

    Usage
    
        menacing [params]
        --state
          gets the current state of the matchboxes
        --reset
        --init
          resets the saved matchboxes to a dumb version.
        --train [iterations]
          trains the matchboxes using computer vs. computer.
          iterations defaults to 200.
        --debug enables debug mode
        

