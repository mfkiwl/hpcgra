
SRCS="../../src/cgra_acc.v" "../../src/testbench_sim.v"

build:
	iverilog -f iverilog.cmd $(SRCS) -o simv
sim: build
	./simv
wave: sim
	gtkwave `find . -name inter.vcd`&>/dev/null &
clean:
	rm -rf *.vcd simv
	
