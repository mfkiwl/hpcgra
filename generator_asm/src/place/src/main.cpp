#include <Graph.h>
#include <buffer.h>
#include <routing.h>
//#include <get_critical_path.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <ctime>
#include <chrono>
#include <algorithm> 
#include <fstream>
#include <omp.h>
#include <map>
#include <data>
//#include <annealing.h>
//#include <instance.h>
#include <read_arch.h>

#define NGRIDS 2

using namespace std;
using namespace std::chrono;

int main(int argc, char** argv) {
    srand (time(NULL));
    
    double *randomvec = new double[1000000];
    for(int i = 0; i < 1000000; i++){
        randomvec[i] = (double) rand() / (double)(RAND_MAX);
    }
    //Cria a estrutura do grafo com os vetores (A, v e v_i) à partir do grafo g
    string path_dot = "", name = "", path_arch= "";

    if (argc > 2) {
        name = argv[1];
        path_dot = argv[2]; 
        path_arch = argv[3];
    } else {
        printf("ERROR: ./place <name> <path_to_dot.dot> <path_to_arch.json>\n");
        printf("./place mac ../dot/mac.dot ../arch/cgra_4x4.json \n");
        return 1;
    }

    vector<int> pe_in, pe_out, pe_basic; 

    vector<pe_t> pe;

    // read arch
    if (!read_arch(path_arch, pe)) return 1;

    for (int i = 0; i < pe.size(); ++i) {
        if (pe[i].type == 0 || pe[i].type == 2) pe_in.push_back(pe[i].id);
        else if (pe[i].type == 1 || pe[i].type == 2) pe_out.push_back(pe[i].id);
        else pe_basic.push_back(pe[i].id);
    }

    for (int i = 0; i < pe_in.size(); ++i) printf("%d ", pe_in[i]);
    printf("\n");
    
    Graph g(path_dot);

    const int SIZE_NODES = g.num_nodes();
    const int SIZE_EDGES = g.num_edges();
    const int GRID_SIZE = pe.size();
    const int TOTAL_GRID_SIZE = GRID_SIZE * GRID_SIZE;

    // Verify if the number of nodes is sufficiently to arch 
    if (pe.size() < SIZE_NODES) {
        printf("Architecture of size not sufficient for the size of the graph.\n");
        return 1;
    }

    int *h_edgeA = new int[SIZE_EDGES];
    int *h_edgeB = new int[SIZE_EDGES];
    vector<pair<int,int>> edge_list = g.get_edges();
    vector<int> A;
    int *v = new int[SIZE_NODES];
    int *v_i = new int[SIZE_NODES];

    //Matriz de booleanos para identificar ios e mults
    for(int i = 0; i < SIZE_NODES; i++){
        v[i] = 0; 
        v_i[i] = 0;
    }

    //Preenche a estrutura do grafo
    int n1, n2;
    for(int i = 0; i < edge_list.size(); i++){
        n1 = edge_list[i].first;
        n2 = edge_list[i].second;
        h_edgeA[i] = n1;
        h_edgeB[i] = n2;
        v[n1]++;
        if(n1 != n2) v[n2]++;
    }

    for(int i=1; i < SIZE_NODES; i++){
        v_i[i] = v_i[i-1] + v[i-1];
    }

    for(int i = 0; i < SIZE_NODES; ++i){
        for(int j = 0; j < SIZE_EDGES; ++j){
            if (h_edgeA[j] != h_edgeB[j]) {
                if(h_edgeA[j] == i) A.push_back(h_edgeB[j]);
                if(h_edgeB[j] == i) A.push_back(h_edgeA[j]);
            } else {
                if(h_edgeA[j] == i) A.push_back(h_edgeB[j]);
            }
        }
    }

    //Variáveis para o placement
    int cost = 100000;    
    
    int *grid = new int[TOTAL_GRID_SIZE * NGRIDS];
    int *edges_cost = new int[SIZE_EDGES * NGRIDS];
    int *buffers = new int[SIZE_EDGES * NGRIDS];
    int *pos_x = new int[SIZE_NODES * NGRIDS];
    int *pos_y = new int[SIZE_NODES * NGRIDS];
    int *results = new int[NGRIDS];
    
    fill_data(NGRIDS, SIZE_EDGES, SIZE_NODES, TOTAL_GRID_SIZE,
    edges_cost, buffers, pos_x, pos_y, grid);
    
    double time_total = 0.0;
    int cost_min = -1;
    
    printf("ola\n");

    vector<int> inputs = g.get_inputs();
    vector<int> outputs = g.get_outputs();
    vector<int> basic;

    for (int i = 0; i < SIZE_NODES; ++i) {
        if (find(inputs.begin(), inputs.end(), i) == inputs.end()
        && find(outputs.begin(), outputs.end(), i) == outputs.end()){
            basic.push_back(i);
        }
    }

    for (int n = 0; n < NGRIDS; ++n){
        
        printf("N %d\n", n);

        random_data(TOTAL_GRID_SIZE, NGRIDS, SIZE_EDGES, n, grid, 
        inputs, outputs, basic, pe_in, pe_out, pe_basic);

        for (int j = 0; j < SIZE_EDGES; ++j) {
        printf("%d %d\n", h_edgeA[j], h_edgeB[j]);
    }
        
        

        /*
        for (int j = 0; j < g.get_inputs().size(); ++j) {
            printf("%d ", local_swap[j]);
        }
        printf("\n");*/

    }
    


        /*
        bool *setNodes;
        setNodes = new bool[nodes];
        for(int j=0; j<nodes; j++){
            setNodes[j] = false;
        }
        for(int j=0; j<nodes; j++){
            if(io[j]==false || mults[j]==false) continue;
            for(int t=0; t<gridSize; t++){
                if(borders[t]==true && pattern[t]==true && setNodes[j]==false && grid[i][t]==255){
                    grid[i][t]=j;
                    setNodes[j] = true;
                    break;
                }
            }
        }
        for(int j=0; j<nodes; j++){
            if(io[j]==false || setNodes[j]==true) continue;
            for(int t=0; t<gridSize; t++){
                if(borders[t]==true  && grid[i][t]==255){
                    grid[i][t]=j;
                    setNodes[j] = true;
                    break;
                }
            }
        }
        for(int j=0; j<nodes; j++){
            if(mults[j]==false || setNodes[j]==true) continue;
            for(int t=0; t<gridSize; t++){
                if(pattern[t]==true && grid[i][t]==255){
                    grid[i][t]=j;
                    break;
                }
            }
        }
        for(int j=0; j<nodes; j++){
            if(others[j]==false || setNodes[j]==true) continue;
            for(int t=0; t<gridSize; t++){
                if(grid[i][t]==255){
                    grid[i][t]=j;
                    break;
                }
            }
        }
        for(int j=0; j<gridSize; j++){
            for(int t=0; t<gridSize; t++){
                double aleat = ((rand()%1000)/1000.0);
                if(aleat > 0.5 && (io[j]&&io[t]&&mults[j]&&mults[t])){
                    int temp = grid[i][j];
                    grid[i][j] = grid[i][t];
                    grid[i][t] = temp;
                }
                if(aleat > 0.5 && (others[j]&&others[t])){
                    int temp = grid[i][j];
                    grid[i][j] = grid[i][t];
                    grid[i][t] = temp;
                }  
            }
        }
        
        
        
        for(int t=0; t<nGrids; t++){
            for(int i=0; i<gridSize; i++){
                for(int j=0; j<nodes; j++){
                    if(j==grid[t][i]) {
                        positions[t][j]=i;
                    }
                }
            }
        }       
        //fclose(fptr);
        auto start = high_resolution_clock::now();

        #pragma omp parallel for
        for (int i = 0; i < nGrids; ++i) {
            int cost = gridCost(edges, dim, h_edgeA, h_edgeB, positions[i], k, table);
            
            results[i] = cost;
            if(cost == 0) continue;

            annealing2(i, nodes, dim, gridSize, cost, grid[i], positions[i], v_i, v, A, k, io, borders, mults, others, pattern, results, randomvec, table);
        }
        auto stop = high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = (stop-start);
        //auto duration = duration_cast<seconds>(stop - start);

        time_total[k] = duration.count();
 
        int totalTime=0;
        for(int i=0; i<nGrids; i++){
            Instance temp(grid[i], positions[i], gridSize, nodes, dim, results[i][1], k);
            instances[k].push_back(temp);
            //if(results[i][1]>=0) costs.push_back(results[i][1]);
            //totalTime += results[i][2];
        }
        //cost_min[k] = *min_element(costs.begin(), costs.end());
        
        //construct edges_cost
        edgesCostConstructor(g, manh, edges_cost[k], grid, positions, k, dim, nGrids, tablemesh, table1hop, tablechess1hop, tablechessmesh, tablehex); 
         
        int *gridFlat = new int[NGRIDS*gridSize];
        int *positionsXFlat = new int[NGRIDS*nodes];
        int *positionsYFlat = new int[NGRIDS*nodes];
        //vector<bool> successfulRoutings(nGrids, true);
        for(int i=0; i<nGrids; i++){
            for(int j=0; j<gridSize; j++){
                gridFlat[i*gridSize + j] = grid[i][j];
            }
            for(int j=0; j<nodes; j++){
                positionsXFlat[i*nodes + j] = positions[i][j]%dim;
                positionsYFlat[i*nodes + j] = positions[i][j]/dim;
            }
        }
        routing(gridSize, edges, nodes, edge_list, edges_cost[k], positionsXFlat, positionsYFlat, NGRIDS, k, successfulRoutings[k], instances[k]);

        int minBuff = buffer(g, activeFifos[k], manh, edges_cost[k], buffers[k], successfulRoutings[k], instances[k]);
        //cout << minBuff << " ";

        //printGrid(0,grid,dim, gridSize);
        int bestIdx = 0;
        int lowest = 100000;
        for(int i=0; i<instances[k].size(); i++){
            int current = instances[k][i].getLongestFIFO();
            if(current < lowest){
                lowest = current;
                bestIdx = i;
            } 
        }
        
        int a, b, sum = 0;
        for (int i = 0; i < edges; ++i) {
            a = edge_list[i].first; 
            b = edge_list[i].second; 
            
            //printf("%d->%d %d\n", a, b, edges_cost[k][bestIdx][make_pair(a,b)]);
            sum += edges_cost[k][bestIdx][make_pair(a,b)];
        }

        instances[k][bestIdx].writePES();
        instances[k][bestIdx].writeGrid();
        //printBestSol(instances[k][bestIdx], k, gridSize, dim);
        //printBestSolClean(instances[k][bestIdx], k, gridSize, dim);
        //cout << argv[2] << endl;
        
        printf("%s,%.2f,%d,%.2lf\n", argv[2], 1.0*sum/edges, lowest, time_total[k]);
    }
    */

   /*
    delete h_edgeA;
    delete h_edgeB;
    delete v;
    delete v_i;*/

    //writeFile(activeFifos, argv[2], gridSize, successfulRoutings);
   
    //printf("%s,%d,%d,%d,%d,%.2lf,%.2lf,%.2lf,%.2lf\n", argv[2], cost_min[0], cost_min[1], cost_min[2], cost_min[3], time_total[0], time_total[1], time_total[2], time_total[3]);
    
    
    delete v;
    delete v_i;
    delete grid;
    delete edges_cost;
    delete buffers;
    delete pos_x;
    delete pos_y;
    delete results;
    
    return 0;
}