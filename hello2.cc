// testing things

#include <iostream>
#include <string>
#include <vector>
using namespace std;


struct msg_struct {
    string prefix;
    string command;
    vector<string> args;
    string text;
};

void split_msg_line(string& line, msg_struct& line_parts) {

//    cout << text;

    line_parts.prefix = "HOHOHO!";

    if (line[0] == 'H') {
        cout << "HOHOHO";
    }


// if text is set as const, this gives a compile error, consequently
//    text = "GOGO.";

}

int main() {

    msg_struct line_parts_out;

    string hello_str = "Hello Function!";

    split_msg_line(hello_str, line_parts_out);

    cout << line_parts_out.prefix << endl;

    cout << hello_str << endl;

}
