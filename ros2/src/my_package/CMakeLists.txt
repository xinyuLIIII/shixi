cmake_minimum_required(VERSION 3.5)
project(my_package)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(jsoncpp REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

set(dependencies
    rclcpp
    jsoncpp
    Boost
)

# Add executable
add_executable(gps_imitate_server src/gps_imitate_server.cpp)

# Link libraries
target_link_libraries(gps_imitate_server
  ${Boost_SYSTEM_LIBRARY}
  jsoncpp_lib)

ament_target_dependencies(gps_imitate_server ${dependencies})

# Install executables
install(TARGETS
  gps_imitate_server
  DESTINATION lib/${PROJECT_NAME})

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
