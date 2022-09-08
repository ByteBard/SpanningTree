#!/usr/bin/python

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
# Usage:
# Generically, it is run as follows:
#     python run_spanning_tree.py <topology_file> <log_file>
# For instance, to run jellyfish_topo.py and log to jellyfish.log that we created, use the following:
#     python run_spanning_tree.py jellyfish_topo jellyfish.log
# Note how the topology file doesn't have the .py extension.
#
# Students should not modify this file.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

import sys
from Topology import *

if len(sys.argv) != 3:
    print("Syntax:")
    print("    python run_spanning_tree.py <topology_file> <log_file>")
    exit()

# Populate the topology
topo = Topology(sys.argv[1])

# Run the topology.
topo.run_spanning_tree()

# Close the logfile
topo.log_spanning_tree(sys.argv[2])
