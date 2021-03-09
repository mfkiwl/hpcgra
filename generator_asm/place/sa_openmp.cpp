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

#define NGRIDS 1000
#define RANDOM_SIZE 1000000
#define MAX_VALUE -1

using namespace std;
using namespace std::chrono;

int results[NGRIDS][4];
double randomvec[RANDOM_SIZE];

int table1hop[18][18] = 
{{0,  0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8},  
 {0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9},  
 {0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9},  
 {1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10},  
 {1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10},  
 {2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11},  
 {2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11},  
 {3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12},  
 {3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12},  
 {4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13},  
 {4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13},  
 {5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14},  
 {5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14},  
 {6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15},  
 {6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15},  
 {7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16},  
 {7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16},
 {8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17}};

int tablemesh[18][18] =
{{0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16},  
 {0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17},  
 {1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18},  
 {2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},  
 {3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},  
 {4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21},  
 {5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22},  
 {6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23},  
 {7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24},  
 {8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25},  
 {9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26},  
 {10,11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27},  
 {11,12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28},  
 {12,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29},  
 {13,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30},  
 {14,15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31},  
 {15,16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32},
 {16,17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33}};

int tablechess1hop[18][18] = 
{{0,  0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8},  
 {0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9},  
 {0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9},  
 {1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10},  
 {1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10},  
 {2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11},  
 {2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11},  
 {3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12},  
 {3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12},  
 {4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13},  
 {4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13},  
 {5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14},  
 {5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14},  
 {6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15},  
 {6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15},  
 {7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16},  
 {7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16},
 {8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17}};

int tablechessmesh[18][18] =
{{0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8},  
 {0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9},  
 {1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9},  
 {1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10},  
 {2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10},  
 {2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11},  
 {3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11},  
 {3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12},  
 {4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12},  
 {4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13},  
 {5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13},  
 {5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14},  
 {6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14},  
 {6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15},  
 {7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15},  
 {7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16},  
 {8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16},
 {8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17}};

int tablehex[18][18] =
{{0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16},  
 {0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17}, 
 {1,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17},  
 {2,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18},  
 {3,  3,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18},   
 {4,  4,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},  
 {5,  5,  5,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},  
 {6,  6,  6,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},  
 {7,  7,  7,  7,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},  
 {8,  8,  8,  8,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21},  
 {9,  9,  9,  9,  9,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21},  
 {10,10, 10, 10, 10, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22},  
 {11,11, 11, 11, 11, 11, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22},  
 {12,12, 12, 12, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23},  
 {13,13, 13, 13, 13, 13, 13, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23},  
 {14,14, 14, 14, 14, 14, 14, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24},  
 {15,15, 15, 15, 15, 15, 15, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24}};

void printGraphInfo(int nodes, int edges, int *h_edgeA, int *h_edgeB, vector<int> &A, int *v, int *v_i){
    printf("NODES: %d EDGES: %d\n", nodes, edges);
    for (int i = 0; i < edges; ++i) printf("%d -> %d\n", h_edgeA[i], h_edgeB[i]);    
    printf("v: ");
    for (int i = 0; i < nodes; ++i) printf("%d ", v[i]);
    printf("\n");
    printf("v_i: ");
    for (int i = 0; i < nodes; ++i) printf("%d ", v_i[i]);
    printf("\n");
    printf("A: ");
    for (int i = 0; i < A.size(); ++i) printf("%d ", A[i]);
    printf("\n\n");
}

void printPlacementInfo(int nodes, int gridSize, int *grid, int *positions, int cost){
    printf("grid: ");
    for (int i = 0; i < gridSize; ++i) printf("%d ", grid[i]);
    printf("\n");
    printf("positions: ");
    for (int i = 0; i < nodes; ++i) printf("%d ", positions[i]);
    printf("\n");
    printf("cost: %d", cost);
    printf("\n\n");
}

int increment_cost(int ifrom, int jfrom, int ito, int jto, int arch) {

    int distManhattanI = abs(jto - jfrom);
    int distManhattanJ = abs(ito - ifrom);

    switch (arch) {
    case 0:
        return tablemesh[distManhattanI][distManhattanJ];
        break;
    case 1:
        return (abs(jfrom-ifrom)%2==0) ? tablechess1hop[distManhattanI][distManhattanJ] : tablechessmesh[distManhattanI][distManhattanJ];
        break;
    case 2:
        return table1hop[distManhattanI][distManhattanJ];
        break;
    case 3:
        return tablehex[distManhattanI][distManhattanJ];
        break;
    default: 
        return tablemesh[distManhattanI][distManhattanJ];
        break;
    }
}

int gridCost(int edges, int dim, int *h_edgeA, int *h_edgeB, int *positions, int arch){
    int cost_ = 0, increment=0, distManhattanI, distManhattanJ, chess;
    for(int k=0; k<edges; k++){
        int ifrom = positions[h_edgeA[k]]/dim; 
        int jfrom = positions[h_edgeA[k]]%dim; 
        int ito = positions[h_edgeB[k]]/dim; 
        int jto = positions[h_edgeB[k]]%dim;
    
        cost_ += increment_cost(ifrom, jfrom, ito, jto, arch);
    }
    return cost_;
}

void annealing2(int iresult, int nodes, int dim, int gridSize, int &cost, int *grid, int *positions, int *v_i, int *v, vector<int> &A, int arch){
    
    int currentCost = cost, nextCost, swapCount=0;
    
    int localGrid[gridSize];
    int localPositions[nodes];
    
    for(int i=0; i < gridSize; ++i) localGrid[i] = grid[i];
    for(int i=0; i < nodes; ++i) localPositions[i] = positions[i];    
    
    //random vector index
    double random, valor;
    int randomctrl = 0;
    double T = 100;
    int ifrom, jfrom, ito, jto;
    int old1, old2, node1, node2;
    int position;
    bool no_empty1, no_empty2;

    while(T >= 0.00001){
        for(int i = 0; i < gridSize; ++i){
            for(int j = i+1; j < gridSize; ++j){    

                node1 = localGrid[i];
                node2 = localGrid[j];

                //if we're looking at 2 empty spaces, skip                   
                if(node1 == MAX_VALUE && node2 == MAX_VALUE)
                    continue;
                
                no_empty1 = (node1 != MAX_VALUE);
                no_empty2 = (node2 != MAX_VALUE);
                
                nextCost = currentCost;
                //remove cost from object edges                
                if(no_empty1){
                    for(int k=0, n = v[node1]; k < n; ++k){
                        position = localPositions[node1];
                        ifrom = position / dim; 
                        jfrom = position % dim;
                        position = localPositions[A[v_i[node1]+k]]; 
                        ito = position / dim; 
                        jto = position % dim;
                
                        nextCost -= increment_cost(ifrom, jfrom, ito, jto, arch); 
                    }
                }
                if(no_empty2){
                    for(int k=0, n = v[node2]; k < n; ++k){
                        position = localPositions[node2];
                        ifrom = position / dim; 
                        jfrom = position % dim;
                        position = localPositions[A[v_i[node2]+k]]; 
                        ito = position / dim; 
                        jto = position % dim; 

                        nextCost -= increment_cost(ifrom, jfrom, ito, jto, arch);  
                    }
                }
                
                //swap positions
                old1 = i;
                old2 = j;
                if(no_empty1) localPositions[node1] = old2;
                if(no_empty2) localPositions[node2] = old1;
                localGrid[j] = node1;
                localGrid[i] = node2;
                
                //recalculate cost
                if(no_empty1){
                    for(int k=0, n = v[node1]; k < n; ++k){
                        position = localPositions[node1];
                        ifrom = position / dim; 
                        jfrom = position % dim;
                        position = localPositions[A[v_i[node1]+k]]; 
                        ito = position / dim; 
                        jto = position % dim; 

                        nextCost += increment_cost(ifrom, jfrom, ito, jto, arch);                          
                    }
                }
                if(no_empty2){
                    for(int k=0, n = v[node2]; k < n; ++k){
                        position = localPositions[node2];
                        ifrom = position / dim; 
                        jfrom = position % dim;
                        position = localPositions[A[v_i[node2]+k]]; 
                        ito = position / dim; 
                        jto = position % dim; 

                        nextCost += increment_cost(ifrom, jfrom, ito, jto, arch);   
                    }
                } 
                
                //parameter for annealing probability
                valor = exp(-1.0*(nextCost - currentCost)/T);
                
                //random number between 0 and 1
                random = randomvec[randomctrl];
                randomctrl = (randomctrl > RANDOM_SIZE-1) ? 0 : randomctrl + 1;

                //if cost after changes is less than before or if cost is higher but we're in the annealing probanility range, return
                if(nextCost <= currentCost || random <= valor){
                    currentCost = nextCost;
                    swapCount++;
                } else { //else, undo changes and stay with previous cost
                    if(no_empty1) localPositions[node1] = old1;
                    if(no_empty2) localPositions[node2] = old2;
                    localGrid[j] = node2;
                    localGrid[i] = node1;
                }
            }
            if(cost == 0) break;             
            T *= 0.999;
        }
        //if(cost == 0) break;   
        //aqui T*=0.999;
    }

    for(int i=0; i < gridSize; ++i) grid[i] = localGrid[i];
    for(int i=0; i < nodes; ++i) positions[i] = localPositions[i]; 
    
    results[iresult][1] = currentCost;
    results[iresult][2] = 0;
    results[iresult][3] = swapCount;
}


int main(int argc, char** argv) {
    srand (time(NULL));
    
    //graph variables 
    for(int i=0; i < RANDOM_SIZE; ++i) randomvec[i] = (double)rand() / (double)(RAND_MAX);
    
    int nodes, edges;
    int *h_edgeA, *h_edgeB;
    vector<int> A;
    int *v, *v_i;

    //placement variables
    int dim, gridSize;
    //grids random simple
    int **grid;             
    int cost = 100000;   
    //READING INPUT
    if(argc < 3){
        cout << "erro de entrada" << endl;
        return 0;
    }

    FILE *fptr;
	fptr = fopen(argv[1],"r");
    if (fptr == NULL) {
        printf("Error! opening file\n");
        exit(1);
    }
    //INPUT READ
    int c = 0, n1, n2;
    //NUMERO DE GRIDS
    int nGrids = NGRIDS;  
    while(fscanf(fptr, "%d %d", &n1, &n2) != EOF) {
        if (c == 0) {
		    nodes = n1;
            edges = n2;
            h_edgeA = new int[edges];
            h_edgeB = new int[edges];
            v = new int[nodes];
            v_i = new int[nodes];
            for(int i=0; i<nodes; i++){
                v[i]=0; v_i[i]=0;
            }
        } else {
            h_edgeA[c-1] = n1;
            h_edgeB[c-1] = n2;
            v[n1]++;
            if(n1!=n2) v[n2]++;
        }
      c++;
    }
    
    dim = ceil(sqrt(nodes));
    gridSize = dim*dim;
    const int num_arch = 4;
    double time_total[num_arch] = {0.0, 0.0, 0.0, 0.0};
    int cost_min[num_arch] = {-1,-1,-1, -1};

    //Aloca memoria pros grids
    grid = new int*[nGrids];
    for(int i=0; i<nGrids; i++) grid[i] = new int[gridSize];

    for (int k = 0; k < num_arch; ++k) {

        //Preenche os grids
        for(int i=0; i<nGrids; i++){
            for(int j=0; j<gridSize; j++){
                if(j < nodes) grid[i][j] = j;
                else grid[i][j] = MAX_VALUE;
            }
            for (int j=gridSize-1; j>0; --j) swap (grid[i][j],grid[i][(j+rand()%gridSize)%gridSize]);
        }

        for(int i=1; i<nodes; i++){
            v_i[i] = v_i[i-1] + v[i-1];
        }

        for(int i=0; i<nodes; i++){
            for(int j=0; j<edges; j++){
                if (h_edgeA[j] != h_edgeB[j]) {
                    if(h_edgeA[j]==i) A.push_back(h_edgeB[j]);
                    if(h_edgeB[j]==i) A.push_back(h_edgeA[j]);
                } else {
                    if(h_edgeA[j]==i) A.push_back(h_edgeB[j]);
                }
            }
        }
        
        int positions[nGrids][nodes];
        for(int ll=0; ll < nGrids; ll++){
            for(int i=0; i < gridSize; i++){
                for(int j=0; j < nodes; j++){
                    if(j == grid[ll][i]) positions[ll][j] = i;
                }
            }
        }

        auto start = high_resolution_clock::now();

        #pragma omp parallel for
        for (int i = 0; i < nGrids; ++i) {
            int cost = gridCost(edges, dim, h_edgeA, h_edgeB, positions[i], k);
            // printPlacementInfo(nodes, gridSize, grid[i], positions[i], cost);
            results[i][0] = cost;
            if(cost == 0){
                results[i][1] = cost;
                results[i][2] = 0;
                results[i][3] = 0;
                
                continue;
            }
            annealing2(i, nodes, dim, gridSize, cost, grid[i], positions[i], v_i, v, A, k);
        }
        auto stop = high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = (stop-start);
        //auto duration = duration_cast<seconds>(stop - start);

        time_total[k] = duration.count()/1000;
        string name = argv[2];
        if (k == 0) name = name + "/" + name + "_mesh.place";
        else if (k == 1) name = name + "/" + name + "_chess.place";
        else if (k == 2) name = name + "/" + name + "_1hop.place";
        else if (k == 3) name = name + "/" + name + "_hex.place";

        ofstream wfile;
        wfile.open("benchmarks/results/"+name);
        for(int i = 0; i < nGrids; i++){
            for(int j=0; j < gridSize; j++){
                wfile << grid[i][j] << " ";
            }
            wfile << "\n";
        }
        wfile.close();

        // ofile << "-----" << endl;
        // for(int i=0; i<nGrids; i++){
        //     ofile << gridCost(edges, dim, h_edgeA, h_edgeB, positions[i], k) << endl;
        // }
        // ofile << "-----" << endl;
        /*for(int i; i<nGrids; i++){
            for(int j=0; j<gridSize; j++){
                cout << grid[i][j] << " ";
            }
            cout << endl;
        }*/ 
        
        /*
        ofile << "Init\t" << "A2\t" << "t2\t" << "swap2\t" << endl;
        for(int i=0; i<nGrids; i++){
            for(int j=0; j<4; j++){
                ofile << results[i][j] << "\t";
            }
            ofile << endl;
        }
        */
        vector<int> costs;    
        int totalTime=0;
        for(int i=0; i<nGrids; i++){
            if(results[i][1]>=0) costs.push_back(results[i][1]);
            totalTime += results[i][2];
        }
        cost_min[k] = *min_element(costs.begin(), costs.end());

    }

    delete h_edgeA;
    delete h_edgeB;
    delete v;
    delete v_i;

    //ofile << "Menor custo: " << *min_element(costs.begin(), costs.end()) << endl;
    //ofile << "Tempo Total: " << totalTime << endl;
    //ofile.close();

    printf("time spent (s)     : %7.3lf\n\n", time_total[0]);

    //printf("%s,%d,%d,%d,%d,%.2lf,%.2lf,%.2lf,%.2lf\n", argv[2], cost_min[0], cost_min[1], cost_min[2], cost_min[3], time_total[0], time_total[1], time_total[2], time_total[3]);

    return 0;
}