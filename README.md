# framework-cmsis-atmelsam

This is very loosely based on "platformio/framework-cmsis-atmel" -> https://github.com/arduino/ArduinoModule-CMSIS-Atmel.  The main reasons for separating this from the above, are:
 - ArduinoModule-CMSIS-Atmel is basically no longer updated/active
 - The SAMC21 addition in the "ArduinoModule-CMSIS-Atmel" does not match the folder structure of all the other chip families in the entire remainder of the platform, which would wreck unnecessary havoc with a "general" build script
 - The "official" CMSIS header structure for the entire SAM series has changed considerably since 2015, and would break anything referencing the original "framework-cmsis-atmel"

This is intended for use with the "CMSIS" framework for building with "platformio/platform-atmelsam", and is NOT compatible with any Arduino-based frameworks.

For the most part, the CMSIS headers and build systems are based on the PACKs available from either https://www.keil.arm.com/devices/ or https://packs.download.microchip.com/.  Once downloaded, rename the ".pack" to ".zip", and extract the necessary folders from each one, renaming folders if necessary to match the framework standard.

Notice that some CMSIS processor family folders have suffixes (e.g. "_d") to indicate the chip revision.  If there is more than one folder for the family, these suffixes need to match up with the suffixes on the header files.  (If there is only one folder for the family, it is assumed to be the correct one, regardless of processor part number suffix.)

No processor support is planned for SAM "CPUs" that usually end up running Buildroot Linux or similar, e.g. this is just for the MCUs with internal FLASH memory that can be programmed with a CMSIS-DAP or similar.  (They also have a significantly different build system.)

v1.0.0: Based on PACKs downloaded from https://packs.download.microchip.com/ on 2025/12/18
