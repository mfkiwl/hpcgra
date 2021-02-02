#include "xcl2.hpp"
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

typedef  std::vector<unsigned short, aligned_allocator<unsigned short>> vector_u16;

#define NUM_CHANNELS 8

bool read_file(std::string file, vector_u16 &data){
    std::string line;
    unsigned short aux[32];
    
    if(file.substr(file.size()-4,4) == ".bit"){
        std::ifstream MyReadFile(file);
        while(getline(MyReadFile,line)) {
            for(int i=0,j=31;i < 128;i+=4){
                unsigned short x = std::stoul(line.substr(i,4), nullptr, 16);
                aux[j--] = x;
            }
            for(int i=0;i < 32;i++){
                data.push_back(aux[i]);
            }
        }
        MyReadFile.close();
    }else if(file.substr(0,2) == "in"){
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

int main(int argc, char **argv) {
	if (argc != 3) {
		std::cout << "Usage: " << argv[0] << " <XCLBIN File> <CGRA bitstream file>" << std::endl;
		return EXIT_FAILURE;
	}

	std::string binaryFile = argv[1];
    std::string bitstreamFile = argv[2];
    
	cl_int err;
	cl::CommandQueue q;
	cl::Context context;
	cl::Kernel kernel_top;

	vector_u16 inputs[NUM_CHANNELS];
	vector_u16 outputs[NUM_CHANNELS];

    read_file(bitstreamFile,inputs[0]);

	for (int j = 0; j < NUM_CHANNELS; ++j) {
        std::stringstream ss;
        ss << "in" << j << ".txt";
        read_file(ss.str(),inputs[j]);
    }
    for (int j = 0; j < NUM_CHANNELS; ++j) {
        std::stringstream ss;
        ss << "out" << j << ".txt";
        read_file(ss.str(),outputs[j]);
    }

	// OPENCL HOST CODE AREA START
	// Create Program and Kernel
	
	auto devices = xcl::get_xil_devices();

	// read_binary_file() is a utility API which will load the binaryFile
	// and will return the pointer to file buffer.
	auto fileBuf = xcl::read_binary_file(binaryFile);
	cl::Program::Binaries bins { { fileBuf.data(), fileBuf.size() } };
	bool valid_device = false;
	for (unsigned int i = 0; i < devices.size(); i++) {
		auto device = devices[i];
		// Creating Context and Command Queue for selected Device
		OCL_CHECK(err, context = cl::Context(device, NULL, NULL, NULL, &err));
		OCL_CHECK(err,
				q = cl::CommandQueue(context, device, CL_QUEUE_PROFILING_ENABLE, &err));

		std::cout << "Trying to program device[" << i << "]: "
				<< device.getInfo<CL_DEVICE_NAME>() << std::endl;
		cl::Program program(context, { device }, bins, NULL, &err);
		if (err != CL_SUCCESS) {
			std::cout << "Failed to program device[" << i
					<< "] with xclbin file!\n";
		} else {
			std::cout << "Device[" << i << "]: program successful!\n";
			OCL_CHECK(err,
					kernel_top = cl::Kernel(program, "rtl_kernel_loopback_8",
							&err));
			valid_device = true;
			break; // we break because we found a valid device
		}
	}
	if (!valid_device) {
		std::cout << "Failed to program any device found, exit!\n";
		exit(EXIT_FAILURE);
	}

    std::vector<cl::Memory> buffer_r(NUM_CHANNELS);
    std::vector<cl::Memory> buffer_w(NUM_CHANNELS);

	// Allocate Buffer in Global Memory
	for (int i = 0; i < NUM_CHANNELS; ++i) {
        
        auto vector_size_bytes =  inputs[i].size() * sizeof(unsigned short);
        OCL_CHECK(err,buffer_r[i] = cl::Buffer(context, CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY, vector_size_bytes, inputs[i].data(), &err));
        
        vector_size_bytes =  outputs[i].size() * sizeof(unsigned short);
        OCL_CHECK(err, buffer_w[i] = cl::Buffer(context, CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY, vector_size_bytes, outputs[i].data(), &err));
	}

// 	Set the Kernel Arguments
	int arg_id = (NUM_CHANNELS * 2);
	for (int i = 0; i < NUM_CHANNELS; ++i) {
        
        int in_s = inputs[i].size()/32;
        int out_s = outputs[i].size()/32;
        
		OCL_CHECK(err, err = kernel_top.setArg(i, in_s));
		OCL_CHECK(err, err = kernel_top.setArg(i+NUM_CHANNELS, out_s));
		OCL_CHECK(err, err = kernel_top.setArg(arg_id, buffer_r[i]));
		OCL_CHECK(err, err = kernel_top.setArg(arg_id + 1, buffer_w[i]));
		arg_id += 2;
	}
	
	// Copy input data to device global memory
	OCL_CHECK(err, err = q.enqueueMigrateMemObjects(buffer_r,0/* 0 means from host*/));

	// Launch the Kernel
	OCL_CHECK(err, err = q.enqueueTask(kernel_top));

	// Copy Result from Device Global Memory to Host Local Memory
	OCL_CHECK(err, err = q.enqueueMigrateMemObjects(buffer_w, CL_MIGRATE_MEM_OBJECT_HOST));

    OCL_CHECK(err, err = q.finish());
    
	// OPENCL HOST CODE AREA END
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
        for (int i = 0; i < size; i++) {
            std::cout << outputs[c][i] << " ";
        }
        std::cout << std::endl;
    }
	return EXIT_SUCCESS;
}
