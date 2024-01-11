# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "BCI: 1 messages, 0 services")

set(MSG_I_FLAGS "-IBCI:/home/kasper/catkin_ws/src/BCI/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(BCI_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_custom_target(_BCI_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "BCI" "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(BCI
  "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/BCI
)

### Generating Services

### Generating Module File
_generate_module_cpp(BCI
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/BCI
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(BCI_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(BCI_generate_messages BCI_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_dependencies(BCI_generate_messages_cpp _BCI_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(BCI_gencpp)
add_dependencies(BCI_gencpp BCI_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS BCI_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(BCI
  "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/BCI
)

### Generating Services

### Generating Module File
_generate_module_eus(BCI
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/BCI
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(BCI_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(BCI_generate_messages BCI_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_dependencies(BCI_generate_messages_eus _BCI_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(BCI_geneus)
add_dependencies(BCI_geneus BCI_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS BCI_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(BCI
  "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/BCI
)

### Generating Services

### Generating Module File
_generate_module_lisp(BCI
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/BCI
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(BCI_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(BCI_generate_messages BCI_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_dependencies(BCI_generate_messages_lisp _BCI_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(BCI_genlisp)
add_dependencies(BCI_genlisp BCI_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS BCI_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(BCI
  "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/BCI
)

### Generating Services

### Generating Module File
_generate_module_nodejs(BCI
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/BCI
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(BCI_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(BCI_generate_messages BCI_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_dependencies(BCI_generate_messages_nodejs _BCI_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(BCI_gennodejs)
add_dependencies(BCI_gennodejs BCI_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS BCI_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(BCI
  "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/BCI
)

### Generating Services

### Generating Module File
_generate_module_py(BCI
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/BCI
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(BCI_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(BCI_generate_messages BCI_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/kasper/catkin_ws/src/BCI/msg/BoolStateBCI.msg" NAME_WE)
add_dependencies(BCI_generate_messages_py _BCI_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(BCI_genpy)
add_dependencies(BCI_genpy BCI_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS BCI_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/BCI)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/BCI
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(BCI_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/BCI)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/BCI
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(BCI_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/BCI)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/BCI
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(BCI_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/BCI)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/BCI
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(BCI_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/BCI)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/BCI\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/BCI
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(BCI_generate_messages_py std_msgs_generate_messages_py)
endif()
