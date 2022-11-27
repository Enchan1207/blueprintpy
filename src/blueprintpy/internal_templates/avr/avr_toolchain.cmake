#
# CMake AVR toolchain with arduino-cli
#
# 2022 @Enchan1207
#
cmake_minimum_required(VERSION 3.0)

# #
# # toolchain commands configuration
# #

# specify tools directory of arduino-cli
set(ARDUINOCLI_ROOT "")

if(DEFINED ENV{ARDUINOCLI_ROOT})
    set(ARDUINOCLI_ROOT "$ENV{ARDUINOCLI_ROOT}")
else()
    if(APPLE)
        set(ARDUINOCLI_ROOT "~/Library/Arduino15")
    elseif(UNIX)
        set(ARDUINOCLI_ROOT "~/.arduino15")
    else()
        set(ARDUINOCLI_ROOT "~/AppData/Local/Arduino15")
    endif()
endif()

get_filename_component(ARDUINOCLI_ROOT "${ARDUINOCLI_ROOT}" ABSOLUTE)

if(NOT EXISTS ${ARDUINOCLI_ROOT})
    message(FATAL_ERROR
        "tools directory of arduino-cli not found. (expected: ${ARDUINOCLI_ROOT})\n"
        "Solution:\n"
        "1. check if arduino-cli and avr core were installed\n"
        "2. please set correct path to environment variable ARDUINOCLI_ROOT if you installed arduino-cli to custom directory\n"
    )
endif()

# Find each tools variants from arduino-cli
file(GLOB AVRGCC_VARIANTS ${ARDUINOCLI_ROOT}/packages/arduino/tools/avr-gcc/*)
file(GLOB AVRDUDE_VARIANTS ${ARDUINOCLI_ROOT}/packages/arduino/tools/avrdude/*)

# If multiple variants hit, choose latest version
list(SORT AVRGCC_VARIANTS ORDER DESCENDING)
list(SORT AVRDUDE_VARIANTS ORDER DESCENDING)
list(GET AVRGCC_VARIANTS 0 AVRGCC_ROOT)
list(GET AVRDUDE_VARIANTS 0 AVRDUDE_ROOT)

if(NOT AVRGCC_ROOT)
    message(FATAL_ERROR "avr-gcc and some commands couldn't found.")
endif()
if(NOT AVRDUDE_ROOT)
    message(FATAL_ERROR "avrdude couldn't found.")
endif()

set(AVRGCC_BIN ${AVRGCC_ROOT}/bin)
set(AVRDUDE_BIN ${AVRDUDE_ROOT}/bin)

# #
# # configure CMake for AVR
# #

# paths, constants
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR avr)
set(CMAKE_CROSS_COMPILING 1)

set(CMAKE_C_COMPILER "${AVRGCC_BIN}/avr-gcc" CACHE PATH "gcc" FORCE)
set(CMAKE_CXX_COMPILER "${AVRGCC_BIN}/avr-g++" CACHE PATH "g++" FORCE)
set(CMAKE_LINKER "${AVRGCC_BIN}/avr-ld" CACHE PATH "linker" FORCE)

set(CMAKE_NM "${AVRGCC_BIN}/avr-nm" CACHE PATH "nm" FORCE)
set(CMAKE_OBJCOPY "${AVRGCC_BIN}/avr-objcopy" CACHE PATH "objcopy" FORCE)
set(CMAKE_OBJDUMP "${AVRGCC_BIN}/avr-objdump" CACHE PATH "objdump" FORCE)

set(CMAKE_AR "${AVRGCC_BIN}/avr-ar" CACHE PATH "ar" FORCE)
set(CMAKE_STRIP "${AVRGCC_BIN}/avr-strip" CACHE PATH "strip" FORCE)
set(CMAKE_RANLIB "${AVRGCC_BIN}/avr-ranlib" CACHE PATH "ranlib" FORCE)

set(AVRDUDE "${AVRDUDE_BIN}/avrdude" CACHE PATH "avrdude" FORCE)

# compiler flags
set(COMMON_FLAGS "-mmcu=${AVR_MCU} -DF_CPU=${AVR_FCPU}")

if(CMAKE_BUILD_TYPE STREQUAL "Release")
    set(OPTIMIZATION_FLAGS "-Os")
else()
    set(OPTIMIZATION_FLAGS "-Os -g")
endif()

set(COMPILER_FLAGS "${COMMON_FLAGS} ${OPTIMIZATION_FLAGS}")
set(LINKER_FLAGS "${COMMON_FLAGS} -lc")

# avrdude settings
set(AVRDUDE_CONF ${AVRDUDE_ROOT}/etc/avrdude.conf)

if(NOT AVRDUDE_BAUDRATE)
    set(AVRDUDE_BAUDRATE 19200)
endif()

if(NOT AVRDUDE_PROGRAMMER)
    set(AVRDUDE_PROGRAMMER "avrisp")
endif()

# #
# # custom macros
# #

# configure target for AVR
macro(target_configure_for_avr target_name)
    set_target_properties(${target_name} PROPERTIES
        COMPILE_FLAGS "${COMPILER_FLAGS}"
        LINK_FLAGS "${LINKER_FLAGS}"
    )

    target_include_directories(${target_name} PUBLIC
        ${AVRGCC_ROOT}/avr/include
    )

    target_link_directories(${target_name} PUBLIC
        ${AVRGCC_ROOT}/avr/lib
    )   
endmacro()

# add_executable
macro(add_executable_avr target_name)
    add_executable(${target_name})
    target_configure_for_avr(${target_name})

    # add flash target
    if(DEFINED AVRDUDE_PORT)
        add_custom_target(flash-${target_name}
            COMMAND ${AVRDUDE}
                -C ${AVRDUDE_CONF}
                -c ${AVRDUDE_PROGRAMMER} -b ${AVRDUDE_BAUDRATE} -P ${AVRDUDE_PORT}
                -p ${AVRDUDE_MCU} -U flash:w:${target_name}
            DEPENDS ${target_name}
        )
    else()
        message(WARNING "uploading port is not specified (AVRDUDE_PORT is not set). flash target won't be created.")
    endif()
endmacro()

# add_library
macro(add_library_avr target_name)
    add_library(${target_name})
    target_configure_for_avr(${target_name})
endmacro()
