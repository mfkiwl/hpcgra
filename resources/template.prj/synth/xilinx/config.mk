VIVADO := $(XILINX_VIVADO)/bin/vivado
$(TEMP_DIR)/kernel_top.xo: scripts/package_kernel.tcl scripts/gen_xo.tcl ../../src/kernel_top.v ../../src/cgra_acc.v
	mkdir -p $(TEMP_DIR)
	$(VIVADO) -mode batch -source scripts/gen_xo.tcl -tclargs $(TEMP_DIR)/kernel_top.xo kernel_top $(TARGET) $(DEVICE) $(XSA) $(NUM_M_AXIS)
	
