"""
/*
 * Copyright © 2022 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6250 Computer Networks
 * Instructors: Maria Konte
 * Head TAs: Johann Lau and Ken Westdorp
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However,
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials
 * (including exam keys, project requirements, etc.) and do not distribute them
 * to anyone not enrolled in the class. Use of any previous semester course
 * materials, such as tests, quizzes, homework, projects, videos, and any other
 * coursework, is prohibited in this course.
 */
"""

# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Spanning Tree Switch that serves as a Parent class to the switch class to be
# implemented by the student.  It abstracts details of sending messages and verifying topologies.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *


class StpSwitch(object):

    def __init__(self, idNum, topolink, neighbors):
        # switchID = id of the switch (lowest value determines root switcha nd breaks ties.)
        # topology = backlink to the Topology class. Used for sending messages.
        #   as follows: self.topology.send_message(message)
        # links = a list of the switch IDs linked to this switch.
        self.switchID = idNum
        self.topology = topolink
        self.links = neighbors

    # Invoked at initialization of topology of switches, this does NOT need to be invoked by student code.
    def verify_neighbors(self):
        """ Verify that all your neighbors has a backlink to you. """
        for neighbor in self.links:
            if self.switchID not in self.topology.switches[neighbor].links:
                raise Exception(str(neighbor) + " does not have link to " + str(self.switchID))

    # Wrapper for message passing to prevent students from having to access self.topology directly.
    def send_message(self, message):
        self.topology.send_message(message)
