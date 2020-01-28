#include "shell.hpp"

bool DEBUG = true;

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
        if(read_pipe != nullptr) {
            if (dup2 (read_pipe[READ], STDIN_FILENO) < 0) {
                perror("Error with dup2 in the read pipe");
                exit(EXIT_FAILURE);
            }
        }
        if(write_pipe != nullptr) {
            if (dup2 (write_pipe[WRITE], STDOUT_FILENO) < 0) {
                perror("Error with dup2 in the write pipe");
                exit(EXIT_FAILURE);
            }
        }

        ClosePipes(all_pipes, number_of_commands);

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
    for (size_t i = 0; i < number_of_commands; ++i) {
        if(number_of_commands == 1) {
            Execute(argvs[i], number_of_commands, nullptr, nullptr, all_pipes);
        }
        else if(i == number_of_commands - 1) {
            Execute(argvs[i], number_of_commands, all_pipes[i - 1], nullptr, all_pipes);
        }
        else if(i == 0) {
            Execute(argvs[i], number_of_commands, nullptr, all_pipes[i], all_pipes);
        }
        else {
            Execute(argvs[i], number_of_commands, all_pipes[i - 1], all_pipes[i], all_pipes);
        }
    }

    ClosePipes(all_pipes, number_of_commands);
}

void Shell::GetLine(char *buffer, size_t size)
{
    getline(&buffer, &size, stdin);
    buffer[strlen(buffer) - 1] = '\0';
}

void Shell::WaitForAllCommands(const size_t &number_of_commands)
{
    for (size_t i = 0; i < number_of_commands; i++) {
        int status;
        wait(&status);
    }

}

void Shell::InitializePipes(int all_pipes[][2], const size_t &number_of_commands)
{
    for (size_t i = 0; i < number_of_commands; i++) {
        if(pipe(all_pipes[i]) < 0) {
            perror("init pipes failed");
            exit(0);
        }
    }
}

void Shell::ClosePipes(int all_pipes[][2], const size_t &number_of_commands)
{
    for (size_t i = 0; i < number_of_commands; i++) {
        if(close(all_pipes[i][READ]) < 0) {
            perror("Error closing pipes");
            exit(0);
        }
        if(close(all_pipes[i][WRITE]) < 0) {
            perror("Error closing pipes");
            exit(0);
        }
    }
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