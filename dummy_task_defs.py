#!/usr/bin/python

"""
Dummy Task classes for the Ecoconnect Controller.
See documentation in task.py

This file defines a set of seven dummy tasks, A,B,C,D,E,F, and G
with the following input/output dependencies:

                             (F)--1--2--3--X
                              |       
                      (D)--1--2--3--X
                       |         |
            (A)--1--2--X        (G)--1--2--3--X
                 |  |            |
                 | (C)--1--2--3--X
                 |         |
                 |        (E)--1--2--X
                 |         |       
                (B)--1--2--3--X   

If they run (and generate their postrequisites) at the same rate,
they should start executing in the following order: 

             |   |  |  |   |   |  |
             A   B  C  D   E   F  G 
"""

from task import task
from reference_time import reference_time
from requisites import requisites

import os
import Pyro.core

class A( task ):
    "dummy task A"

    def __init__( self, ref_time, set_finished ):

        self.name = "A"

        self.valid_hours = [ "00", "06", "12", "18" ]

        self.prerequisites = requisites( [] )

        self.postrequisites = requisites( [ 
                 "file A_1_" + ref_time.to_str() + " completed",
                 "file A_2_" + ref_time.to_str() + " completed",
                 "task A completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class B( task ):
    "dummy task B"

    def __init__( self, ref_time, set_finished ):

        self.name = 'B'

        self.valid_hours = [ "00", "06", "12", "18" ]

        self.prerequisites = requisites( [
                "file A_1_" + ref_time.to_str() + " completed"] )

        self.postrequisites = requisites( [ 
                 "file B_1_" + ref_time.to_str() + " completed",
                 "file B_2_" + ref_time.to_str() + " completed",
                 "file B_3_" + ref_time.to_str() + " completed",
                 "task B completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class C( task ):
    "dummy task C"

    def __init__( self, ref_time, set_finished ):

        self.valid_hours = [ "00", "06", "12", "18" ]

        self.name = 'C'

        self.prerequisites = requisites( [
                "file A_2_" + ref_time.to_str() + " completed"] )

        self.postrequisites = requisites( [ 
                 "file C_1_" + ref_time.to_str() + " completed",
                 "file C_2_" + ref_time.to_str() + " completed",
                 "file C_3_" + ref_time.to_str() + " completed",
                 "task C completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class D( task ):
    "dummy task D"

    def __init__( self, ref_time, set_finished ):

        self.valid_hours = [ "00", "06", "12", "18" ]

        self.name = 'D'

        self.prerequisites = requisites( [
                "task A completed for " + ref_time.to_str() ] )

        self.postrequisites = requisites( [ 
                 "file D_1_" + ref_time.to_str() + " completed",
                 "file D_2_" + ref_time.to_str() + " completed",
                 "file D_3_" + ref_time.to_str() + " completed",
                 "task D completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class E( task ):
    "dummy task E"

    def __init__( self, ref_time, set_finished ):

        self.valid_hours = [ "00", "12" ]

        self.name = 'E'

        self.prerequisites = requisites( [
                "file C_2_" + ref_time.to_str() + " completed",
                "file B_3_" + ref_time.to_str() + " completed" ] )

        self.postrequisites = requisites( [ 
                 "file E_1_" + ref_time.to_str() + " completed",
                 "file E_2_" + ref_time.to_str() + " completed",
                 "task E completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class F( task ):
    "dummy task F"

    def __init__( self, ref_time, set_finished ):

        self.valid_hours = [ "06", "18" ]

        self.name = 'F'

        self.prerequisites = requisites( [
                "file D_2_" + ref_time.to_str() + " completed"] )

        self.postrequisites = requisites( [ 
                 "file F_1_" + ref_time.to_str() + " completed",
                 "file F_2_" + ref_time.to_str() + " completed",
                 "file F_3_" + ref_time.to_str() + " completed",
                 "task F completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )


class G( task ):
    "dummy task G"

    def __init__( self, ref_time, set_finished ):

        self.valid_hours = [ "00", "06", "12", "18" ]

        self.name = 'G'

        self.prerequisites = requisites( [
                "file D_3_" + ref_time.to_str() + " completed",
                "task C completed for " + ref_time.to_str() ] )

        self.postrequisites = requisites( [ 
                 "file G_1_" + ref_time.to_str() + " completed",
                 "file G_2_" + ref_time.to_str() + " completed",
                 "file G_3_" + ref_time.to_str() + " completed",
                 "task G completed for " + ref_time.to_str()  ] )

        task.__init__( self, ref_time, set_finished )
