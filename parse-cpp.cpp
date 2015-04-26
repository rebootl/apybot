// parsing IRC message in c++

#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <fstream>
#include <sstream>
//using namespace std;


struct msg_struct {
    std::string prefix;
    std::string command;
    std::vector<std::string> args;
    std::string text;
};

void split_msg_line(std::string& line, msg_struct& line_parts) {

    // (string and vector are empty by default!
    // still have to set it in the else or it will stay
    // at the value of the last run...)

    // get prefix
    if (line[0] == ':') {
        std::size_t pref_break_pos = line.find(' ');

        // set prefix
        line_parts.prefix = line.substr(1, pref_break_pos-1);

        line = line.substr(pref_break_pos+1);
        //std::cout << line << std::endl;
    }
    else {
        line_parts.prefix.clear();
    }

    // get text
    std::size_t text_break_pos = line.find(" :");
    if (text_break_pos != std::string::npos) {
        // set text
        line_parts.text = line.substr(text_break_pos+2);

        line = line.substr(0, text_break_pos);
        //std::cout << '"' << line << '"' << std::endl;
    }
    else {
        line_parts.text.clear();
    }

    // get command
    // (clear args vector!)
    line_parts.args.clear();
    std::size_t command_end_pos = line.find(' ');
    if (command_end_pos != std::string::npos) {
        line_parts.command = line.substr(0, command_end_pos);

        line = line.substr(command_end_pos+1);
        //std::cout << '"' << line << '"' << std::endl;

        // parse args
        // http://stackoverflow.com/questions/236129/split-a-string-in-c
        int start = 0, end = 0;
        while ((end = line.find(' ', start)) != std::string::npos) {
            line_parts.args.push_back(line.substr(start, end - start));
            start = end + 1;
        }
        line_parts.args.push_back(line.substr(start));
    }
    // else command=line
    else {
        line_parts.command = line;
    }


}

int main() {

    // initialize output structure
    msg_struct line_parts_out;

    // line examples
    //std::string regi_str = ":orwell.freenode.net 001 pybot_ :Welcome to the freenode Internet Relay Chat Network pybot_";
    //std::string regi_str = "001 :hoho";
    //std::string regi_str = "001 gaga abc :Welcome to the freenode Internet Relay Chat Network pybot_";

    // read file line by line
    // http://stackoverflow.com/questions/7868936/read-file-line-by-line
    std::ifstream infile("output.file.big");

    // process line by line
    std::string line;
    while (std::getline(infile, line)) {

        split_msg_line(line, line_parts_out);

        // concise output
/*        std::cout << "p: " << '"' << line_parts_out.prefix << '"';
        std::cout << " c: " << '"' << line_parts_out.command << '"';

        std::cout << " a: [ ";

        std::vector<std::string>::iterator it;
        for (it=line_parts_out.args.begin(); it<line_parts_out.args.end(); it++)
            std::cout << '"' << *it << '"' << ' ' ;

        std::cout << "]";

        std::cout << " t: " << '"' << line_parts_out.text << '"' << std::endl;
*/
        // verbose output
/*        std::cout << "prefix: " << '"' << line_parts_out.prefix << '"' << std::endl;
        std::cout << "text: " << '"' << line_parts_out.text << '"' << std::endl;
        std::cout << "command: " << '"' << line_parts_out.command << '"' << std::endl;

        std::cout << "args: [ ";

        std::vector<std::string>::iterator it;
        for (it=line_parts_out.args.begin(); it<line_parts_out.args.end(); it++)
            std::cout << '"' << *it << '"' << ' ' ;

        std::cout << "]" << std::endl;
*/
    }

}
