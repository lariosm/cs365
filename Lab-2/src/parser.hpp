#ifndef PARSER_HPP
#define PARSER_HPP

const int MAX_COMMANDS = 16;
const int MAX_ARGV = 16;

class Parser
{
public:
    static int Parse(char *str, char *argvs[MAX_COMMANDS][MAX_ARGV]);
    static void PrintArguments(char *argvs[MAX_COMMANDS][MAX_ARGV]);

private:
    static void PrintArgument(char *argv[]);
    static void ParseCommands(char *str, const char *delim, char *cmds[]);
    static bool Empty(char *str);
    static char *LeftTrim(char *s);
    static char *RightTrim(char *str);
    static char *Trim(char *str);
    static void GetArgument(char *str, const char *delim, char *argv[]);
};

#endif // PARSER_HPP
