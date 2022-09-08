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

from Message import *
from StpSwitch import *


class Switch(StpSwitch):
    """
    This class defines a Switch that can can send and receive spanning tree
    messages to converge on a final, loop-free forwarding topology. This class
    is a child class of the StpSwitch class. To remain within the spirit of
    the project, the only inherited members functions a student is permitted
    to use are:

    switchID: int
        the ID number of this switch object)
    links: list
        the list of switch IDs connected to this switch object)
    send_message(Message msg)
        Sends a Message object to another switch)

    Student code MUST use the send_message function to implement the algorithm.
    A non-distributed algorithm will not receive credit.

    Student code should NOT access the following members, otherwise they may violate
    the spirit of the project:

    topolink: Topology
        a parameter passed to initialization function
    topology: Topology
        a link to the greater topology structure used for message passing
    """

    def __init__(self, idNum, topolink, neighbors):
        """
        Invokes the super class constructor (StpSwitch), which makes available to this object the following members:
        switchID: int
            the ID number of this switch object
        links: list
            the list of swtich IDs connected to this switch object
        """
        super(Switch, self).__init__(idNum, topolink, neighbors)
        self.root = idNum
        self.active_links = set()
        self.switchThrough = idNum
        self.distance = 0
        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      USE self.send_message(msg) to send this.
        #      DO NOT USE self.topology.send_message(msg)

        # root = id of the switch thought to be the root by the origin switch
        # distance = the distance from the origin to the root node
        # origin =  the ID of the origin switch
        # destination = the ID of the destination switch
        # pathThrough = Boolean value indicating the path to the claimed root from the origin passes through the destination
        self.output_status()
        for neighbour in self.links:
            message = Message(self.root, 0, self.switchID, neighbour, False)
            self.send_message(message)
            self.output_ini_msg(message, True)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        print('\nProcess Message: ' + 'SWITCH-> ID: ' + str(self.switchID))
        print('     Message Information: ')
        self.output_ini_msg(message)
        print('     Before: ')
        self.output_status()

        notifyNeighbour = False
        curr_switchThrough = self.switchThrough

        hasSameRoot = self.root == message.root
        hasSameRootAndDistance = hasSameRoot & (self.distance == message.distance + 1)
        hasSmallerRoot = self.root > message.root
        hasSmallerDistance = self.distance > (message.distance + 1)
        hasDiffPath = hasSameRootAndDistance & (message.origin != self.switchThrough) & message.pathThrough
        pathTrueButNoOriginInALinks = hasSameRootAndDistance & message.pathThrough & (
                message.origin not in self.active_links)
        pathFalseButHasOriginInALinks = hasSameRootAndDistance & (not message.pathThrough) & (
                message.origin in self.active_links)
        originLessThanSwitchThrough = hasSameRootAndDistance & (
                message.origin < self.switchThrough)

        # root
        if hasSmallerRoot:
            self.root = message.root
            notifyNeighbour = True

        # distance
        if hasSmallerRoot | hasSmallerDistance:
            self.distance = message.distance + 1
            notifyNeighbour = True

        # switch through ?? compare id value to get smaller one
        if hasDiffPath:
            self.switchThrough = min(curr_switchThrough, message.origin)
            notifyNeighbour = True

        if hasSmallerRoot | hasSmallerDistance | originLessThanSwitchThrough:
            self.switchThrough = message.origin
            notifyNeighbour = True

        # active links
        if message.pathThrough & hasSameRoot:
            self.active_links.add(message.origin)

        if originLessThanSwitchThrough:
            self.active_links.remove(curr_switchThrough)
            self.active_links.add(message.origin)

        if hasSmallerRoot | hasSmallerDistance | hasDiffPath | pathTrueButNoOriginInALinks | pathFalseButHasOriginInALinks:
            if hasSmallerRoot | hasSmallerDistance:
                self.active_links.clear()
                self.active_links.add(message.origin)
            elif hasDiffPath:
                self.active_links.remove(self.switchThrough)
                self.active_links.add(message.origin)
            elif pathTrueButNoOriginInALinks:
                self.active_links.add(message.origin)
            elif pathFalseButHasOriginInALinks:
                self.active_links.remove(message.origin)

        print('     After: ')
        self.output_status()

        if notifyNeighbour:
            for neighbour in self.links:
                pt = neighbour == self.switchThrough
                message = Message(self.root, self.distance, self.switchID, neighbour, pt)
                self.send_message(message)
                self.output_ini_msg(message)
        return

    def output_ini_msg(self, message, isInit=False):
        title = ''
        if isInit:
            title = '      Init_Message-> '
        print(title +
              ' Root: ' + str(message.root) +
              ' Distance: ' + str(message.distance) +
              ' Origin: ' + str(message.origin) +
              ' Destination: ' + str(message.destination) +
              ' PathThrough: ' + str(message.pathThrough)
              )
        return

    def output_status(self):
        ns = ', '.join([str(x) for x in self.links])
        alks = ', '.join([str(x) for x in self.active_links])
        print('SWITCH-> '
              'ID: ' + str(self.switchID) +
              ' root: ' + str(self.root) +
              ' distance: ' + str(self.distance) +
              ' neighbours: ' + ns +
              ' activeLinks: ' + alks +
              ' switchThrough: ' + str(self.switchThrough)
              )
        return

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulaton is complete.  Output the links included in the
        #      spanning tree by increasing destination switch ID on a single line.
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        res = ''
        orderedLinks = self.active_links
        sorted(orderedLinks)
        for link in orderedLinks:
            res += (str(self.switchID) + ' - ' + str(link) + ', ')
        return res
