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
# This defines a Message sent from one node to another using Spanning Tree Protocol.
# Students should not modify this file.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

class Message(object):

    def __init__(self, claimedRoot, distanceToRoot, originID, destinationID, pathThrough):
        # root = id of the switch thought to be the root by the origin switch
        # distance = the distance from the origin to the root node
        # origin =  the ID of the origin switch
        # destination = the ID of the destination switch
        # pathThrough = Boolean value indicating the path to the claimed root from the origin passes through the destination
        self.root = claimedRoot
        self.distance = distanceToRoot
        self.origin = originID
        self.destination = destinationID
        self.pathThrough = pathThrough

    # Member function that returns True if the message is properly formed, and False otherwise
    def verify_message(self):
        valid = True

        if self.pathThrough != True and self.pathThrough != False:
            valid = False
        if isinstance(self.root, int) is False or isinstance(self.distance, int) is False or \
                isinstance(self.origin, int) is False or isinstance(self.destination, int) is False:
            valid = False

        return valid
