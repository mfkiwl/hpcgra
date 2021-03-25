#include <hpcgra/hpcgra.h>

typedef  std::vector<unsigned short, aligned_allocator<unsigned short>> vector_u16;

#define NUM_CHANNELS 2

int main(int argc, char *argv[]);

bool read_file(std::string file, vector_u16 &data);

