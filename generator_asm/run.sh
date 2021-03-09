set -e
#mkdir benchmarks/results/mac

GRAPH=(
    mac
)

for ((i=0; i < ${#GRAPH[@]}; i++)) do

    DOT=benchmarks/dot/${GRAPH[i]}.dot
    LIST=benchmarks/list/${GRAPH[i]}.in
    PLACE=benchmarks/results/${GRAPH[i]}/${GRAPH[i]}_1hop.place

    # GENERATOR DOT -> LIST
    python3 benchmarks/dot_to_list.py $DOT > $LIST

    # PLACE
    echo "PLACEMENT EXECUTING"
    export OMP_NUM_THREADS=4
    g++ place/sa_openmp.cpp -O3 -fopenmp -o place.exe 
    ./place.exe $LIST mac

    # ROUTE
    echo "ROUTING EXECUTING"
    python3 route/routing.py 1 $DOT $LIST $PLACE

done