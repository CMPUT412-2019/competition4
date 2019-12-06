# Competition 4

This project shares much of its code with our previous competitions, [competition 2](https://github.com/cmput412-2019/cmput412-competition2) and [competition 3](https://github.com/cmput412-2019/competition3). We refer back to those competitions for many details of our report.

## Setup and building

Installation instructions are identical to those in [competition 3](https://github.com/cmput412-2019/competition3#setup-and-building), except
  - The code should be procured by cloning this repository, instead of from the competition 3 release (however, the map from that release should still be used).
  - A block of styrofoam should be attached to the front bumper of the robot to aid box-pushing.

## Running the code

Plug in the Kobuki base, RGB-D camera, and webcam. Open two terminals (e.g. in `tmux`), with `setup.bash` sourced in each of them as per the previous instructions. Then in the first terminal, run

    roslaunch competition4 competition4.launch
    
and in the second,

    export PYTHONPATH=$pwd:$PYTHONPATH
    python src/competition4/scripts/competition4.py

## Method

