#ifndef __DATA__H
#define __DATA__H

void fill_data(const int NGRIDS, const int SIZE_EDGES, 
    const int SIZE_NODES, const int TOTAL_GRID_SIZE,
    int *edges_cost, int *buffers, int *pos_x, int *pos_y,
    int *grid) {
        
    // Fill zero in the data
    for (int k = 0; k < NGRIDS; k++) {
        for (int i = 0; i < SIZE_EDGES; ++i) {
           edges_cost[k*SIZE_EDGES+i] = 0;
           buffers[k*SIZE_EDGES+i] = 0;
        }
        for (int i = 0; i < SIZE_NODES; ++i) {
            pos_x[k*SIZE_NODES+i] = -1; // -1 is empty
            pos_y[k*SIZE_NODES+i] = -1;
        }
        for (int i = 0; i < TOTAL_GRID_SIZE; ++i) {
            grid[k*TOTAL_GRID_SIZE+i] = -1; // -1 is empty
        }
    }
}

void random_data(const int TOTAL_GRID_SIZE, const int NGRIDS,
    const int SIZE_EDGES, const int n, int *grid, 
    vector<int> &inputs, vector<int> &outputs, vector<int> &basic,
    vector<int> &pe_in, vector<int> &pe_out, vector<int> &pe_basic) {

    random_shuffle( pe_in.begin(), pe_in.end() );
    random_shuffle( pe_out.begin(), pe_out.end() );
    random_shuffle( pe_basic.begin(), pe_basic.end() );

    for (int j = 0; j < pe_in.size(); ++j) {
        grid[n*TOTAL_GRID_SIZE+pe_in[j]] = inputs[j];
    }
    for (int j = 0; j < pe_out.size(); ++j) {
        grid[n*TOTAL_GRID_SIZE+pe_out[j]] = outputs[j];
    }
    for (int j = 0; j < pe_basic.size(); ++j) {
        grid[n*TOTAL_GRID_SIZE+pe_basic[j]] = basic[j];
    }

    for (int j = 0; j < NGRIDS*TOTAL_GRID_SIZE; ++j) printf("%d ", grid[j]);
    printf("\n");
}

#endif