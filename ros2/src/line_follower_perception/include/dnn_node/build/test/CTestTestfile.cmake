# CMake generated Testfile for 
# Source directory: /home/jetson/ros2/src/line_follower_perception/include/dnn_node/test
# Build directory: /home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(dnn_node-gtest "/usr/bin/python3" "-u" "/opt/ros/foxy/share/ament_cmake_test/cmake/run_test.py" "/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test_results/dnn_node/dnn_node-gtest.gtest.xml" "--package-name" "dnn_node" "--output-file" "/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/ament_cmake_gtest/dnn_node-gtest.txt" "--command" "/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test/dnn_node-gtest" "--gtest_output=xml:/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test_results/dnn_node/dnn_node-gtest.gtest.xml")
set_tests_properties(dnn_node-gtest PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test/dnn_node-gtest" TIMEOUT "60" WORKING_DIRECTORY "/home/jetson/ros2/src/line_follower_perception/include/dnn_node/build/test" _BACKTRACE_TRIPLES "/opt/ros/foxy/share/ament_cmake_test/cmake/ament_add_test.cmake;118;add_test;/opt/ros/foxy/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/foxy/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/jetson/ros2/src/line_follower_perception/include/dnn_node/test/CMakeLists.txt;5;ament_add_gtest;/home/jetson/ros2/src/line_follower_perception/include/dnn_node/test/CMakeLists.txt;0;")
subdirs("../gtest")
