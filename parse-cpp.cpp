// parsing IRC message in c++

#include <iostream>
#include <string>
#include <vector>
//using namespace std;


struct msg_struct {
    std::string prefix;
    std::string command;
    std::vector<std::string> args;
    std::string text;
};

void split_msg_line(std::string& line, msg_struct& line_parts) {

    if (line[0] == ':') {
        std::cout << "HOHOHO";
    }



}

int main() {

    msg_struct line_parts_out;

    std::string regi_str = ":orwell.freenode.net 001 pybot_ :Welcome to the freenode Internet Relay Chat Network pybot_";

    split_msg_line(regi_str, line_parts_out);

    std::cout << line_parts_out.prefix << std::endl;

//    std::cout << regi_str << std::endl;

}
