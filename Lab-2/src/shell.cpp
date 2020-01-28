#include "shell.hpp"

bool DEBUG = false;

void DebugPrint(const char *message)
{
    if (DEBUG)
        printf("%s\n", message);
}

void Shell::ForkError()
{
    perror("fork() failed)");
    exit(EXIT_FAILURE);
}

void Shell::CloseError()
{
    perror("Couldn't close file descriptor");
    exit(EXIT_FAILURE);
}

void Shell::Execute(char *argv[], int number_of_commands, int read_pipe[2], int write_pipe[2], int all_pipes[][2])
{
    pid_t pid;

    switch (pid = fork())
    {
    case -1:
        ForkError();
    case 0:
        // if read_pipe is not null
        //     then duplicate read_pipe (e.g. dup2) for STDIN
        // if write_pipe is not null
        //     then duplicate write_pipe (e.g. dup2) for STDOUT
        // Close pipes.

        if(read_pipe != NULL) {
            if (dup2 (read_pipe[READ], STDIN_FILENO) == -1) perror ("dup2");
        }
        if(write_pipe != NULL) {
            if (dup2 (write_pipe[WRITE], STDOUT_FILENO) == -1) perror ("dup2");
        }
        if (close (read_pipe[READ]) == -1) perror ("close");
        if (close (write_pipe[WRITE]) == -1) perror ("close");

        execvp(argv[0], argv);
        perror("execvp");
        exit(EXIT_FAILURE);

    default:
        char buffer[MAX_BUFFER];
        sprintf(buffer, "Pid of %s: %d\n", argv[0], pid);
        DebugPrint(buffer);
        break;
    }
}

void Shell::ExecuteCommands(char *argvs[MAX_COMMANDS][MAX_ARGV], const size_t &number_of_commands, int all_pipes[][2])
{
    // 1. Cases to cover in a loop; for i = 0 to number_of_commands
    // |-------------------------------------------------------------------
    // |     COMMAND         |     READ PIPE        |    WRITE PIPE       |
    // |-------------------------------------------------------------------
    // | Only 1 command      |       null           |      null           |
    // |-------------------------------------------------------------------
    // | First command       |       null           |   current pipe      |
    // |-------------------------------------------------------------------
    // | Last command        |     previous pipe    |      null           |
    // |-------------------------------------------------------------------
    // | Middle command      |     previous pipe    |   current pipe      |
    // --------------------------------------------------------------------

    // 2. Close pipes.

    for (int i = 0; i < number_of_commands; i++) {

    }
    delete[] all_pipes;
}

void Shell::GetLine(char *buffer, size_t size)
{
    getline(&buffer, &size, stdin);
    buffer[strlen(buffer) - 1] = '\0';
}

void Shell::WaitForAllCommands(const size_t &number_of_commands)
{
    // for i = 0 to number_of_commands
    //     call wait()
    for (int i = 0; i < number_of_commands; i++) {
        
    }

}

void Shell::InitializePipes(int all_pipes[][2], const size_t &number_of_commands)
{
    // for i = 0 to number_of_commands
    //     init all_pipes[i]
    for (int i = 0; i < number_of_commands; i++) {

    }
}

void Shell::ClosePipes(int all_pipes[][2], const size_t &number_of_commands)
{
    // for i = 0 to number_of_commands
    //     close read and write ends for pipes
    for (int i = 0; i < number_of_commands; i++) {

    }
    delete[] all_pipes;
}

void Shell::Run()
{
    int number_of_commands = 0;
    char *argvs[MAX_COMMANDS][MAX_ARGV];
    const size_t size = 128;
    char line[size];

    while (true)
    {
        printf(" >> ");

        Shell::GetLine(line, size);

        number_of_commands = Parser::Parse(line, argvs);

        char buffer[MAX_BUFFER];
        sprintf(buffer, "%d commands parsed.\n", number_of_commands);
        DebugPrint(buffer);

        if (DEBUG)
            Parser::PrintArguments(argvs);

        int(*all_pipes)[2] = new int[number_of_commands][2];
        Shell::InitializePipes(all_pipes, number_of_commands);

        ExecuteCommands(argvs, number_of_commands, all_pipes);
        Shell::WaitForAllCommands(number_of_commands);

        delete[] all_pipes;
    }

    exit(EXIT_SUCCESS);
}