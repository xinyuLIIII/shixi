#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dnn_node::dnn_node" for configuration ""
set_property(TARGET dnn_node::dnn_node APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(dnn_node::dnn_node PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdnn_node.so"
  IMPORTED_SONAME_NOCONFIG "libdnn_node.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS dnn_node::dnn_node )
list(APPEND _IMPORT_CHECK_FILES_FOR_dnn_node::dnn_node "${_IMPORT_PREFIX}/lib/libdnn_node.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
