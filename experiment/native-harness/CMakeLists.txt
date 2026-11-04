cmake_minimum_required(VERSION 3.18)

project(FPrimeNativeSbomExperiment NONE)

foreach(required_variable IN ITEMS FPRIME_FRAMEWORK_PATH FPRIME_PROJECT_ROOT FPRIME_INSTALL_DEST PYTHON TOOLCHAIN_NAME)
    if(NOT DEFINED ${required_variable} OR "${${required_variable}}" STREQUAL "")
        message(FATAL_ERROR "Required experiment variable is unset: ${required_variable}")
    endif()
endforeach()

# Load and invoke the native F Prime SBOM target from the frozen, read-only
# upstream tree.  This harness intentionally contains no replacement SBOM logic.
include("${FPRIME_FRAMEWORK_PATH}/cmake/target/sbom.cmake")
sbom_add_global_target(sbom)

