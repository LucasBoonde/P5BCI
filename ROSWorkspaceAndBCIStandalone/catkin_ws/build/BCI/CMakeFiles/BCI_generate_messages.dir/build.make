# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/kasper/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/kasper/catkin_ws/build

# Utility rule file for BCI_generate_messages.

# Include the progress variables for this target.
include BCI/CMakeFiles/BCI_generate_messages.dir/progress.make

BCI_generate_messages: BCI/CMakeFiles/BCI_generate_messages.dir/build.make

.PHONY : BCI_generate_messages

# Rule to build all files generated by this target.
BCI/CMakeFiles/BCI_generate_messages.dir/build: BCI_generate_messages

.PHONY : BCI/CMakeFiles/BCI_generate_messages.dir/build

BCI/CMakeFiles/BCI_generate_messages.dir/clean:
	cd /home/kasper/catkin_ws/build/BCI && $(CMAKE_COMMAND) -P CMakeFiles/BCI_generate_messages.dir/cmake_clean.cmake
.PHONY : BCI/CMakeFiles/BCI_generate_messages.dir/clean

BCI/CMakeFiles/BCI_generate_messages.dir/depend:
	cd /home/kasper/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/kasper/catkin_ws/src /home/kasper/catkin_ws/src/BCI /home/kasper/catkin_ws/build /home/kasper/catkin_ws/build/BCI /home/kasper/catkin_ws/build/BCI/CMakeFiles/BCI_generate_messages.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : BCI/CMakeFiles/BCI_generate_messages.dir/depend

