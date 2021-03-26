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

bool read_arch(string &arch_file, pe_t* pe) {

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

    

    Json::Value data;
    std::ifstream ifs;
    ifs.open(arch_file);
    Json::CharReaderBuilder builder;
    JSONCPP_STRING errs;
    if (!parseFromStream(builder, ifs, &data, &errs)) {
        std::cout << errs << std::endl;
        return false;
    }
    ifs.close();

    
    int size_pe = data["pe"].size();
    int size_neighbors = 0;
    int size_elastic_queue = 0;
    int size_isa = 0;
    
    cout << size_pe << endl;

    pe = new pe_t[size_pe];
    
    for (int i = 0; i < size_pe; ++i) {
        pe[i].id = data["pe"][i]["id"].asInt();
        pe[i].type = map_type[data["pe"][i]["type"].asString()];
        
        size_neighbors = data["pe"][i]["neighbors"].size();
        for (int j = 0; j < size_neighbors; ++j) {
            pe[i].neighbors.push_back(data["pe"][i]["neighbors"][j].asInt());
        }

        pe[i].routes = data["pe"][i]["routes"].asInt();

        for (int j = 0; j < size_elastic_queue; ++j) {
            pe[i].elastic_queue.push_back(data["pe"][i]["elastic_queue"][j].asInt());
        }

        pe[i].acc = data["pe"][i]["acc"].asBool();

        for (int j = 0; j < size_elastic_queue; ++j) {
            pe[i].isa.push_back(map_isa[data["pe"][i]["isa"][j].asString()]);
        }

        cout << pe[i].id << endl;
    }

    return true;
}

#endif
