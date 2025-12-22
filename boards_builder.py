# Little script to enumerate every available MCU in the CMSIS support, and generate
#PlatformIO "generic" board files for each one.
#written by Sid L., 2025-12-18

from glob import glob
from pathlib import Path
import os
import re

def GetFileParameterNumber(filedata, keyword_loc, target_str = "_("):
	if (keyword_loc != -1):
		# Determine where the newline is, and cut the string there.
		#This prevents possible overflow, e.g. returning ANY hexadecimal value in the header.
		#If it's not on this line, fail!
		line_end = filedata.find("\n", keyword_loc)
		line_str = filedata[keyword_loc:line_end]
		# Our target is usually like this: "_UINT32_(0x00040000)"
		# For SAMRs, though, it's "_UL_(0x00040000)"
		val_start = line_str.find(target_str) 
		if (val_start != -1):
			line_str = line_str[(val_start + len(target_str)) : line_str.find(")")]
			return int(line_str, 0)    # will crash if it finds a non-numeric character, annoyingly.  BASIC would just stop parsing ;-)
		else:
			print("Get Parameter Keyword invalid parameter line: '" + line_str + "'")

	return 0


num_mcus = 0
for full_filename in glob('./**/include/sam*.h', recursive=True):
	# the above glob WILL find all of the "sam.h" files, unfortunately.
	filename = os.path.basename(full_filename)
	filepath = os.path.dirname(full_filename)
	
	if (filename == "sam.h"):
		continue

	flash_size = 0
	ram_size = 0
	cpu_type = ""
	cpu_freq = 0
	part_number = filename[:-2]			# remove the ".h"

	with open(full_filename) as f:
		filedata = f.read()
		# Find where in the header file the necessary parameters are given:
		#   - FLASH size
		#   - RAM size
		#   - Processor core type
		#   - Maximum speed

		# FLASH size
		flash_size = GetFileParameterNumber(filedata, filedata.find("FLASH_SIZE"))

		# RAM size
		ram_size_loc = filedata.find("HSRAM_SIZE")          #often "HSRAM_SIZE", but not always
		if (ram_size_loc == -1):
			ram_size_loc = filedata.find("RAMC0_SIZE")      # SAMD, SAMHA,
			if (ram_size_loc == -1):
				ram_size_loc = filedata.find("RAM_SIZE")    # ("IRAM_SIZE"): SAME70, SAMG, SAMR, SAMS, SAMV

		ram_size = GetFileParameterNumber(filedata, ram_size_loc)

		# Processor type.  TODO: might be able to crop everything after "core_c" and just append that out?  It's the same.
		if "core_cm0plus.h" in filedata:
			cpu_type = "cortex-m0plus"
		elif "core_cm4.h" in filedata:
			cpu_type = "cortex-m4"      # ref: platform-atmelsam/boards/adafruit_feather_m4.json
		elif "core_cm7.h" in filedata:
			cpu_type = "cortex-m7"      # ref: https://github.com/platformio/platform-ststm32/blob/develop/boards/portenta_h7_m7.json
		elif "core_cm23.h" in filedata:
			cpu_type = "cortex-m23"     # ref: https://github.com/CommunityGD32Cores/platform-gd32/blob/main/boards/genericGD32E230C4.json
		else:
			print(filename + " > Unrecognized CPU type")


	# Open the "system_[part number].c" file to get the INITIAL clock frequency.
	#This unfortunately is not the MAXIMUM clock frequency.  Not sure where that spec is found.
	with open(filepath + "/../gcc/system_" + part_number + ".c") as f:
		filedata = f.read()
		cpu_freq = GetFileParameterNumber(filedata, filedata.find("__SYSTEM_CLOCK"), " (")

	# Get the processor family to add to the #define list, making it easy to port code based on the family
	family = str(list(Path(filepath).parents)[-2])
	fam_suf = family.find("_")
	if (fam_suf != -1):
		family = family[: fam_suf]

	print("Family: " + family + ": " + part_number + ": FLASH: " + str(flash_size) + ", RAM: " + str(ram_size) + ", " + cpu_type + " @ " + str(cpu_freq))
	if (flash_size != 0 and ram_size != 0 and cpu_type != ""):
		# we have the necessary specs: generate an output board definition

		# OpenOCD target is a bit of a guess here.  Set a default unless a specific known
		#family is selected with different configs.
		# https://github.com/openocd-org/openocd/tree/master/tcl/target
		openocd_target = "at91samdXX"		# Valid at least for SAMC and SAMD.
		if ("samg5" in part_number):
			opencd_target = "at91samg5x"
		elif ("sama5" in part_number):
			openocd_target = "at91sama5d2"

		with open("../boards/generic" + part_number.upper() + ".json", "wt") as f:
			f.write("{\n")																			# {
			f.write("  \"build\": {\n")																#   "build": {
			f.write("    \"cpu\": \"{}\",\n".format(cpu_type))										#     "cpu": "cortex-m0plus",
			f.write("    \"f_cpu\": \"{}L\",\n".format(cpu_freq))									#     "f_cpu": "48000000L",
			f.write("    \"mcu\": \"{}\",\n".format(part_number))									#     "mcu": "samc21e17a",
			f.write("    \"extra_flags\": \"-D__{}__ -D__{}__\"\n".format(part_number.upper(), family.upper()))		#     "extra_flags": "-D__SAMC21E17A__ -D__SAMC21__"
			f.write("  },\n")																		#   },
			f.write("  \"debug\": {\n")																#   "debug": {
			f.write("    \"jlink_device\": \"AT{}\",\n".format(part_number.upper()))				#     "jlink_device": "ATSAMC21E17",
			f.write("    \"openocd_chipname\": \"at91{}\",\n".format(part_number))					#     "openocd_chipname": "at91samc21e17",
			f.write("    \"openocd_target\": \"{}\",\n".format(openocd_target))						#     "openocd_target": "at91samdXX",
			f.write("    \"svd_path\": \"AT{}.svd\"\n".format(part_number.upper()))					#     "svd_path": "ATSAMC21E17A.svd"
			f.write("  },\n")																		#   },
			f.write("  \"frameworks\": {\n")														#   "frameworks": {
			f.write("    \"cmsis\": {\n")															#     "cmsis": {
			f.write("      \"package\": \"framework-cmsis-atmelsam\",\n")							#       "package": "framework-cmsis-atmelsam",
			f.write("      \"script\": \"builder/frameworks/cmsis.py\",\n")							#       "script": "builder/frameworks/cmsis.py",
			f.write("      \"description\": \"CMSIS bare metal\",\n")								#       "description": "CMSIS bare metal",
			f.write("      \"homepage\": \"\",\n")													#       "homepage": "",
			f.write("      \"title\": \"Atmel/Microchip CMSIS framework for SAM MCUs\"\n")			#       "title": "Atmel/Microchip CMSIS framework for SAM MCUs"
			f.write("    }\n")																		#     }
			f.write("  },\n")																		#   },
			f.write("  \"name\": \"{} ({:.0f}k RAM, {:.0f}k FLASH)\",\n".format(part_number.upper(), ram_size / 1024, flash_size / 1024))	#   "name": "SAMC21E17A (16k RAM, 128k FLASH)",
			f.write("  \"upload\": {\n")															#   "upload": {
			f.write("    \"maximum_ram_size\": {},\n".format(ram_size))								#     "maximum_ram_size": 16384,
			f.write("    \"maximum_size\": {},\n".format(flash_size))								#     "maximum_size": 131072,
			f.write("    \"protocol\": \"cmsis-dap\",\n")											#     "protocol": "cmsis-dap",
			f.write("    \"protocols\": [\n")														#     "protocols": [
			f.write("      \"cmsis-dap\",\n")														#       "cmsis-dap",
			f.write("      \"blackmagic\",\n")														#       "blackmagic",
			f.write("      \"jlink\",\n")															#       "jlink",
			f.write("      \"atmel-ice\"\n")														#       "atmel-ice"
			f.write("    ]\n")																		#     ]
			f.write("  },\n")																		#   },
			f.write("  \"url\": \"https://www.microchip.com/en-us/product/at{}\",\n".format(part_number))	#   "url": "https://www.microchip.com/en-us/product/atsamc21e17a",
			f.write("  \"vendor\": \"Atmel/Microchip\"\n")											#   "vendor": "Atmel/Microchip"
			f.write("}\n")																			# }
			num_mcus += 1
	else:
		print("Unable to find all necessary parameters for '" + part_number + "', skipping")

print("Generated board definitions for {} MCUs".format(num_mcus))
