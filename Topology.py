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
# Defines a Topology, which is a collection of switches and links between them. Students should not
# modify this file.  This is NOT a topology like the ones defined in Mininet projects.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Switch import *


class Topology(object):

    def __init__(self, conf_file):
        """Initializes the topology."""
        self.switches = {}
        self.messages = []

        """ This creates all the switches in the Topology from the configuration
            file passed into __init__(). Can throw an exception if there is a
            problem with the config file. """

        try:
            conf = __import__(conf_file)
            for key in list(conf.topo.keys()):
                new_switch = Switch(key, self, conf.topo[key])
                self.switches[key] = new_switch

            # Verify the topology read from file is correct.
            for key in list(self.switches.keys()):
                self.switches[key].verify_neighbors()

        except Exception:
            print(("error importing conf_file " + conf_file))
            raise

    def send_message(self, message):
        if not message.verify_message():
            print("Message is not properly formatted.")
            return

        if message.destination in self.switches[message.origin].links:
            self.messages.append(message)
        else:
            print("Messages can only be sent to immediate neighbors")

    def run_spanning_tree(self):
        # This function drives the simulation of a Spanning Tree.  It first sends the initial
        # messages from each node by invoking send_intial_message.  Afterward, each message
        # is delivered to the destination switch, where process_message is invoked.

        for switch in self.switches:
            self.switches[switch].send_initial_messages()

        while len(self.messages) > 0:
            msg = self.messages.pop(0)
            self.switches[msg.destination].process_message(msg)

    def log_spanning_tree(self, filename):
        # This function drives the logging of the text file representing the spanning tree.
        # It is invoked at the end of the simulation, and iterates through the switches in
        # increasing order of ID and invokes the generate_logstring function.  That string
        # is written to the file as provided by the student code.
        with open(filename, 'w') as out:
            for switch in sorted(self.switches.keys()):
                entry = self.switches[switch].generate_logstring()
                entry += "\n"
                out.write(entry)
            out.close()
