# Script for making binary Python executables.

#############
# EDIT HERE #
#############

# To add something follow the below format:
# py_executables+=("exe_name:module_path:entry_function")
py_executables=()
py_executables+=("download_words:wordle_solver.download_words:main")
py_executables+=("cli:wordle_solver.cli:main")


##########################
# DO NOT EDIT BELOW HERE #
##########################

# Save PYTHONPATH to use in all binaries.
python_path="PYTHONPATH=$(pwd)/src"

# Make a test executable.
echo "#!/bin/bash\n$python_path python3 -m pytest test/\$@" > bin/test
chmod +x bin/test

# Check if there are any additional executables to make.
if [ ${#py_executables[@]} == 0 ]; then
    exit 0
fi

# If there are, make executables for each.
for command in "${py_executables[@]}"; do
    # Get all components and make sure there are enough.
    IFS=":" read -a separated_values <<< "$command"
    if [ ${#separated_values[@]} != 3 ]; then
        echo "ERROR: expected 3 components"
        exit 0
    fi

    # Extract components.
    script_name=${separated_values[0]}
    module_path=${separated_values[1]}
    entry_function=${separated_values[2]}

    # Now make the script.
    echo "#!/bin/bash\n$python_path python3 -c \"from $module_path import $entry_function;$entry_function()\" \$@"> bin/$script_name
    chmod +x bin/$script_name
done


