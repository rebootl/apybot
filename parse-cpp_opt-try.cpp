// parsing IRC message in c++

#include <iostream>
#include <string>
#include <vector>
#include <iterator>
//using namespace std;


struct msg_struct {
    std::string prefix;
    std::string command;
    std::vector<std::string> args;
    std::string text;
};

void split_msg_line(const std::string& line, msg_struct& line_parts) {

    // (string and vector are empty by default!)

    std::size_t pref_break_pos;

    // get prefix
    if (line[0] == ':') {
        pref_break_pos = line.find(' ');

        // (set prefix)
        line_parts.prefix = line.substr(1, pref_break_pos-1);
    }
    else {
        pref_break_pos = 0;
    }

    // get text
    std::size_t text_break_pos = line.find(" :");
    if (text_break_pos != std::string::npos) {
        // (set text)
        line_parts.text = line.substr(text_break_pos+2);

        //line = line.substr(0, text_break_pos);
        //std::cout << '"' << line << '"' << std::endl;
    }
    else {
        text_break_pos = line.length();
    }

    // get command
    std::size_t command_end_pos = line.find(' ', pref_break_pos+1);

    // (set command)
    if (pref_break_pos == 0) {
        line_parts.command = line.substr(pref_break_pos, command_end_pos-pref_break_pos);
    }
    else {
        line_parts.command = line.substr(pref_break_pos+1, command_end_pos-pref_break_pos-1);
    }

    // get args
    if (command_end_pos != std::string::npos) {

        std::string line_args = line.substr(command_end_pos+1, text_break_pos-command_end_pos-1);
        // (parse args)
        // based on: http://stackoverflow.com/questions/236129/split-a-string-in-c

        // start: the start of the argument
        // end:   the end of the argument

        int start = 0, end = 0;
        while ((end = line_args.find(' ', start)) != std::string::npos) {
            line_parts.args.push_back(line_args.substr(start, end - start));
            start = end + 1;
        }
        line_parts.args.push_back(line_args.substr(start));
    }

}

int main() {

    msg_struct line_parts_out;

    // (test strings)
//    std::string regi_str = "001";
    std::string regi_str = ":orwell.freenode.net 001 :Welcome to the freenode Internet Relay Chat Network pybot_";
//    std::string regi_str = "001 gaga abc :Welcome to the freenode Internet Relay Chat Network pybot_";

    split_msg_line(regi_str, line_parts_out);

    std::cout << "prefix: " << '"' << line_parts_out.prefix << '"' << std::endl;
    std::cout << "text: " << '"' << line_parts_out.text << '"' << std::endl;
    std::cout << "command: " << '"' << line_parts_out.command << '"' << std::endl;

    std::cout << "args: [ ";

    std::vector<std::string>::iterator it;
    for (it=line_parts_out.args.begin(); it<line_parts_out.args.end(); it++)
        std::cout << '"' << *it << '"' << ' ' ;

    std::cout << "]" << std::endl;

}
