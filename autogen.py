############################################################################
# Branch Hinting Tool
#
# Copyright (c) 2015, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
###########################################################################

import os
import constants



def start(args, verbose, build, run):
    """
    1. replaces -O2 with -O0 and -fprofile-generate with --coverage.
    2. builds the project.
    3. run workload with binary obtained at step 1
    4. redo initial configuration for Makefile
    """
    old_opt_flag = "-O2"
    new_opt_flag = "-O0"
    old_prof_flag = "-fprofile-generate"
    new_prof_flag = "--coverage"
    oldpath = None


    if 'path' in args and args['path']:
        oldpath = os.getcwd()
        if verbose:
            print "Changing directory to " + args['path']
        os.chdir(args['path'])

    if 'dest' in args and args['dest']:
        print "LCOV destination folder: " + args['dest']
        command = "rm -r " + os.path.join(args['dest'], "/lcov_results")
        os.system(command)
        print command

        command = "mkdir -p " + os.path.join(args['dest'], "lcov_results/html")
        os.system(command)
        print command

    if verbose:
        for key in args:
            print key + ":" + args[key]

    if build:
        print "Build instrumented binaries ..."
        print "    Patch the Makefile ..."
        command = "sed \"s/" + old_opt_flag + "/" + new_opt_flag \
                  + "/g\"" " \"Makefile\" > Makefile.copy"
        os.system(command)
        if verbose:
            print command

        os.system("cp Makefile.copy Makefile")

        command = "sed \"s/" + old_prof_flag + "/" + new_prof_flag \
                  + "/g\"" " \"Makefile\" > Makefile.copy"
        os.system(command)
        if verbose:
            print command

        os.system("cp Makefile.copy Makefile")
        os.system("make clean")
        if verbose:
            print constants.Constants.IR.to_string()

        command = constants.Constants.IR.get_rule("Makefile.RULE")
        print "Make binaries: " + command
        if not verbose:
            command += " > /dev/null"
        os.system(command)

    if run:

        command = "find . -name \\*.gcda | xargs rm -f"
        print "Cleanup old statistics ..."
        print "    " + command
        os.system(command)

#        os.system("pwd")
        command = constants.Constants.IR.get_rule("Config.COMMAND")
        print "Start training ..."
        print "    " + command

        if not verbose:
            command += " > /dev/null"
        os.system(command)

    if oldpath:
        os.chdir(oldpath)

    #os.system("rm Makefile.copy")
