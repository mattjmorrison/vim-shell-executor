import subprocess
import random
import os


def get_command_from_first_line(line):
    if line.startswith("#!"):
        return line[2:]
    return line


def get_program_output_from_buffer_contents(buffer_contents):
    input_file = '/tmp/vim-exec-buffer-{}.log'.format(random.randint(0, 999))
    error_file = '/tmp/vim-exec-buffer-error-{}.log'.format(random.randint(0, 999))
    results_file = '/tmp/vim-exec-buffer-results-{}.log'.format(random.randint(0, 999))
    write_buffer_contents_to_file(input_file, buffer_contents[1:])
    command = get_command_from_first_line(buffer_contents[0])
    execute_file_with_specified_shell_program(command, input_file, error_file, results_file)
    errors = read_file_lines(error_file)
    std_out = read_file_lines(results_file)
    new_buf = errors + std_out
    return new_buf


def write_buffer_contents_to_file(file_name, contents):
    with open(file_name, "w") as f:
        for line in contents:
            f.write(line + "\n")


def execute_file_with_specified_shell_program(shell_command, input_file, error_file, results_file):
    try:
        subprocess.check_call("{0} {1} {2} > {3} 2> {4}".format(
            shell_command,
            redirect_or_arg(shell_command),
            input_file,
            results_file,
            error_file),
            shell=True
        )
    except:
        pass


def redirect_or_arg(shell_command):
    redirect_or_agr = "<"
    if shell_command == "coffee":
        redirect_or_agr = ""
    return redirect_or_agr


def read_file_lines(file_to_read):
    if os.path.isfile(file_to_read):
        with open(file_to_read, "r") as f:
            return [l.rstrip('\n') for l in f.readlines()]
