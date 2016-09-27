## Introduction:

This is a little project I had in mind to learn more about Python and to get closer to the pygame library.
It's more or less your typical 2D-Sidescrolling space shooter. Nothing out of the ordinary here. Yet.

## Common abbreviations:

et = Enemy Type

dmg = Damage

prj = Projectile

l, r, u, d = Left, Right, Up, Down, works in combinations (l/r | u/d)

## Changelog:

(Please .md, render nicely.)

| Date | Time | Change | Type |
| ---- | ---- | ------ | ---- |
| 17.08.2016 | 15:48 | Added ShipMovement, added controls for player (W,A,S,D). | Code |
| 22.08.2016 | 12:00 | Massive class rework (pools, improved movement etc.) | Code |
| 29.08.2016 | 17:00 | Updated functions, classes, movement calls, rewrote some comments | Code |
| 06.09.2016 | 16:30 | Added collision (Not efficient, not at all, but effective.), added test enemy class, added lists for easier accessability. Slight code cleanup. | Code |
| 23.09.2016 | 15:00 | Added seperate .py files for classes and settings, removed them from the game logic .py file | Code |
|            | 16:19 | Made code more pythonic (yay) and slightly more efficient, (re)added new class (Particles) | Code |
| 27.09.2016 | 14:35 | Added blitting to functionality. You can now effectively render images on surfaces (atm only for ships) | Code |
|            | 15:20 | Added two ship images for testing | GFX |
|            | 15:25 | Renamed classes.py to helper.py. Moved playermovement function to helper.py. Moved sprites to spaceshooter.py | Code |
|            | 17:09 | Added new comments, explaining functions/classes in more detail (WIP) | Code |