#ifndef __READ_ARCH_H
#define __READ_ARCH_H

#include <json/json.h>
#include <fstream>
#include <iostream>
#include <map>

using namespace std;

/* 
    "input" = 0
    "output" = 1
    "inout" = 2
    "basic" = 3
*/

/*
    'add'   : 0
    'sub'   : 1
    'mul'   : 2
    'or'    : 3
    'and'   : 4
    'not'   : 5
    'pass'  : 6
    'muladd': 7
    'mulsub': 8
    'addadd': 9
    'subsub': 10
    'addsub': 11
    'mux'   : 12
*/

typedef struct pe_t {
    int id;
    int type;
    vector<int> neighbors;
    int routes;
    vector<int> elastic_queue;
    bool acc;
    vector<int> isa;
} pe_t;

bool read_arch(string &arch_file) {


    // map to 
    map<string,int> map_type = {{"input", 1}, {"output", 2}, {"inout", 3}, {"basic", 4}};

    // map to isa
    std::map<std::string, int> map_isa = {{"add", 0},
                                        {"sub", 1},
                                        {"mul", 2},
                                        {"or", 3},
                                        {"and", 4},
                                        {"not", 5},
                                        {"pass", 6},
                                        {"muladd", 7},
                                        {"mulsub", 8},
                                        {"addadd", 9},
                                        {"subsub", 10},
                                        {"addsub", 11},
                                        {"mux", 12}};

    pe_t pe;

    Json::Value data;
    std::ifstream ifs;
    ifs.open(arch_file);
    Json::CharReaderBuilder builder;
    JSONCPP_STRING errs;
    if (!parseFromStream(builder, ifs, &data, &errs)) {
        std::cout << errs << std::endl;
        return false;
    }

    pe.id = data["id"].asInt();

    printf("%d\n", pe.id);

    // Todo: Read the arch
    /*
    cout << data['array'] << endl;
    for (int i = 0; i < data['array'].size; ++i) {
        // processa data['array'][i].asInt();
        .asBool();
    }
    */

    ifs.close();
    return true;
}

#endif
