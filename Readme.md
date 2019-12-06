# Competition 4

This project shares much of its code with our previous competitions, [competition 2](https://github.com/cmput412-2019/cmput412-competition2) and [competition 3](https://github.com/cmput412-2019/competition3). We refer back to those competitions for many details of our report.

## Setup and building

Installation instructions are identical to those in [competition 3](https://github.com/cmput412-2019/competition3#setup-and-building), except
  - The code should be procured by cloning this repository, instead of from the competition 3 release (however, the map from that release should still be used).
  - A block of styrofoam should be attached to the front bumper of the robot to aid box-pushing.
  - [ar_track_alvar](https://wiki.ros.org/ar_track_alvar) should be installed, as well as any other packages which are missing.

## Running the code

Plug in the Kobuki base, RGB-D camera, and webcam. Open two terminals (e.g. in `tmux`), with `setup.bash` sourced in each of them as per the previous instructions. Then in the first terminal, run

    roslaunch competition4 competition4.launch
    
and in the second,

    export PYTHONPATH=$pwd:$PYTHONPATH
    python src/competition4/scripts/competition4.py

## Method

### Re-used components

We re-use the following components from previous competitions:

  - [Line following](https://github.com/CMPUT412-2019/cmput412-competition2#line-following)
  - [Changing state at red lines](https://github.com/CMPUT412-2019/cmput412-competition2#changing-state-at-red-lines)
  - [Turning](https://github.com/CMPUT412-2019/cmput412-competition2#turning)
  - [Stopping](https://github.com/CMPUT412-2019/cmput412-competition2#stopping)
  - [Mapping and localization](https://github.com/CMPUT412-2019/competition3/blob/master/Readme.md#mapping-and-localization)
  - [Waypoint navigation](https://github.com/CMPUT412-2019/competition3/blob/master/Readme.md#waypoint-navigation)
  - [Identifying and moving toward AR tags](https://github.com/CMPUT412-2019/competition3/blob/master/Readme.md#identifying-and-moving-toward-ar-tags)
  - [Off-ramp and on-ramp](https://github.com/CMPUT412-2019/competition3/blob/master/Readme.md#off-ramp-and-on-ramp)
  - [Searching for a matching shape](https://github.com/CMPUT412-2019/competition3/blob/master/Readme.md#searching-for-a-matching-shape)


### Searching for AR cube and target marker

Before performing box-pushing, the robot must know the location of the AR cube and the target AR tag. To accomplish this, we constantly scan for updates to the estimated pose of the AR tags as given by [ar_track_alvar](https://wiki.ros.org/ar_track_alvar). The latest estimate for a particular tag is saved, giving the robot persistent knowledge of these locations. To ensure the robot has seen all required AR tags, it travels back and forth between two waypoints. At each waypoint, the robot slowly performs a full turn. At any point during this turn, if both AR tags have been located, the search is immediately terminated. In practice, both tags are often located before the robot even reaches the first search waypoint, so the search terminates immediately after reaching that waypoint.


### Box-pushing

We define the target position of the box as a point 40cm in front of the AR tag at the goal square. We then project a line from this point through the center of the box, and navigate 70cm behind the box along this line. The robot then moves along this line until its projected position of the box is at the goal. We control the robot's direction to ensure it is always facing the goal, regardless of any torque from the box. Once this is finished, the robot backs up until it can see the box again, and if the box is sufficiently far from the goal, the box-pushing process repeats.

