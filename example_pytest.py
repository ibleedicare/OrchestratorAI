import subprocess

# Define the command to run pytest
pytest_cmd = 'pytest -qx generated/'

# Run pytest using subprocess
process = subprocess.Popen(pytest_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Get the output and error messages
stdout, stderr = process.communicate()

# Print the output and error messages
print(stdout.decode('utf-8'))
print(stderr.decode('utf-8'))

# Get the return code of pytest
return_code = process.returncode

# Check if pytest passed or failed
if return_code == 0:
    print('All tests passed!')
else:
    print('Tests failed!')
    print(stdout.decode('utf-8'))

