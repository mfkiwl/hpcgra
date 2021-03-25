#include <host.h>


int main(int argc, char *argv[]){

    if (argc != 4) {
        std::cout << "Usage: " << argv[0] << " <XCLBIN File> <Kernel name> <CGRA bitstream file>" << std::endl;
        return EXIT_FAILURE;
    }
    
    std::string binaryFile = argv[1];
    std::string kernel_name = argv[2];
    std::string bitstreamFile = argv[3];
    
    auto cgra_acc = CgraFpga(NUM_CHANNELS,NUM_CHANNELS);
    
    cgra_acc.cgra_fpga_init(binaryFile, kernel_name, bitstreamFile);
    
    vector_u16 inputs[NUM_CHANNELS];
    vector_u16 outputs[NUM_CHANNELS];

    for (int j = 0; j < NUM_CHANNELS; ++j) {
        std::stringstream ss;
        ss << "in" << j << ".txt";
        read_file(ss.str(),inputs[j]);
        cgra_acc.createInputQueue(j,inputs[j].size()*2);
        auto ptr = cgra_acc.getInputQueue(j);
        memcpy(ptr,inputs[j].data(),inputs[j].size()*2);        
    }
    for (int j = 0; j < NUM_CHANNELS; ++j) {
        std::stringstream ss;
        ss << "out" << j << ".txt";
        read_file(ss.str(),outputs[j]);
        cgra_acc.createOutputQueue(j,outputs[j].size()*2);
    }
    
    cgra_acc.cgra_execute();
    
    for(int c = 0; c < NUM_CHANNELS;c++){
        std::cout << std::endl << "IN" << c << ": ";
        int size = inputs[c].size();
        for (int i = 0; i < size; i++) {
            std::cout << inputs[c][i] << " ";
        }
        std::cout << std::endl;
    }

    for(int c = 0; c < NUM_CHANNELS;c++){
        std::cout << std::endl << "OUT" << c << ": ";
        int size = outputs[c].size();
        auto ptr = (short *)cgra_acc.getOutputQueue(c);
        for (int i = 0; i < size; i++) {
            std::cout << ptr[i] << " ";
        }
        std::cout << std::endl;
    }
    
    cgra_acc.print_report();
    cgra_acc.cleanup();
    
}

bool read_file(std::string file, vector_u16 &data){
    std::string line;   
    if(file.substr(0,2) == "in"){
        std::ifstream MyReadFile(file);
        while(getline(MyReadFile,line)) {
            unsigned short x = std::stoul(line, nullptr, 10);
            data.push_back(x);
        }
        MyReadFile.close();
    }else if(file.substr(0,3) == "out"){
        std::ifstream MyReadFile(file);
        getline(MyReadFile,line);
        int x = std::stoul(line, nullptr, 10);
        for(int i = 0;i < x;i++){
            data.push_back(0);
        }
        MyReadFile.close();
    }else {
        std::cout << "[Error] Input file not found: " << file << std::endl;       
        return false;
    }

    return true;    
}

