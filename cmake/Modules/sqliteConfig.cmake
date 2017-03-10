INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SQLITE sqlite)

FIND_PATH(
    SQLITE_INCLUDE_DIRS
    NAMES sqlite/api.h
    HINTS $ENV{SQLITE_DIR}/include
        ${PC_SQLITE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SQLITE_LIBRARIES
    NAMES gnuradio-sqlite
    HINTS $ENV{SQLITE_DIR}/lib
        ${PC_SQLITE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SQLITE DEFAULT_MSG SQLITE_LIBRARIES SQLITE_INCLUDE_DIRS)
MARK_AS_ADVANCED(SQLITE_LIBRARIES SQLITE_INCLUDE_DIRS)

