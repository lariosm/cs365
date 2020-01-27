#ifndef SHELL_HPP
#define SHELL_HPP

#include "parser.hpp"

#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/wait.h>

const int READ = 0;
const int WRITE = 1;
const int MAX_BUFFER = 128;

class Shell
{
public:
    static void ForkError();
    static void CloseError();
    static void Execute(char *argv[], int number_of_commands, int read_pipe[2], int write_pipe[2], int all_pipes[][2]);
    static void ExecuteCommands(char *argvs[MAX_COMMANDS][MAX_ARGV], const size_t &number_of_commands, int all_pipes[][2]);
    static void GetLine(char *buffer, size_t size);
    static void WaitForAllCommands(const size_t& n);
    static void Run();
    static void InitializePipes(int all_pipes[][2], const size_t &number_of_commands);
    static void ClosePipes(int all_pipes[][2], const size_t &number_of_commands);
};

#endif