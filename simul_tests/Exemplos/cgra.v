

module cgra
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [8-1:0] in_stream0,
  input [8-1:0] in_stream2,
  output [8-1:0] out_stream3
);

  wire [8-1:0] pe0_to_pe1;
  wire [8-1:0] pe0_to_pe2;
  wire [8-1:0] pe1_to_pe0;
  wire [8-1:0] pe1_to_pe3;
  wire [8-1:0] pe2_to_pe0;
  wire [8-1:0] pe2_to_pe3;
  wire [8-1:0] pe3_to_pe1;
  wire [8-1:0] pe3_to_pe2;
  wire [8-1:0] conf_bus_reg_in [0:4-1];
  wire [8-1:0] conf_bus_reg_out [0:4-1];

  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_0
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[0]),
    .out(conf_bus_reg_out[0])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_1
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[1]),
    .out(conf_bus_reg_out[1])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_2
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[2]),
    .out(conf_bus_reg_out[2])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_3
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[3]),
    .out(conf_bus_reg_out[3])
  );


  pe_input_2_2_4_add_sub
  #(
    .id(1)
  )
  pe_0
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_bus_reg_out[0]),
    .stream_in(in_stream0),
    .in0(pe1_to_pe0),
    .in1(pe2_to_pe0),
    .out0(pe0_to_pe1),
    .out1(pe0_to_pe2)
  );


  pe_basic_2_2_4_add_sub
  #(
    .id(2)
  )
  pe_1
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_bus_reg_out[1]),
    .in0(pe0_to_pe1),
    .in1(pe3_to_pe1),
    .out0(pe1_to_pe0),
    .out1(pe1_to_pe3)
  );


  pe_input_2_2_4_add_sub
  #(
    .id(3)
  )
  pe_2
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_bus_reg_out[2]),
    .stream_in(in_stream2),
    .in0(pe0_to_pe2),
    .in1(pe3_to_pe2),
    .out0(pe2_to_pe0),
    .out1(pe2_to_pe3)
  );


  pe_output_2_2_4_add_sub
  #(
    .id(4)
  )
  pe_3
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_bus_reg_out[3]),
    .stream_out(out_stream3),
    .in0(pe1_to_pe3),
    .in1(pe2_to_pe3),
    .out0(pe3_to_pe1),
    .out1(pe3_to_pe2)
  );

  assign conf_bus_reg_in[0] = conf_bus;
  assign conf_bus_reg_in[1] = conf_bus_reg_out[0];
  assign conf_bus_reg_in[2] = conf_bus_reg_out[0];
  assign conf_bus_reg_in[3] = conf_bus_reg_out[1];

endmodule



module reg_pipe #
(
  parameter num_register = 1,
  parameter width = 16
)
(
  input clk,
  input en,
  input rst,
  input [width-1:0] in,
  output [width-1:0] out
);

  reg [width-1:0] regs [0:num_register-1];
  integer i;

  assign out = regs[num_register - 1];

  always @(posedge clk) begin
    if(rst) begin
      regs[0] <= 0;
    end else begin
      if(en) begin
        regs[0] <= in;
        for(i=1; i<num_register; i=i+1) begin
          regs[i] <= regs[i - 1];
        end
      end 
    end
  end

  integer i_initial;

  initial begin
    for(i_initial=0; i_initial<num_register; i_initial=i_initial+1) begin
      regs[i_initial] = 0;
    end
  end


endmodule



module pe_input_2_2_4_add_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  output [8-1:0] out0,
  output [8-1:0] out1,
  input [8-1:0] stream_in
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] in_reg1;
  wire [8-1:0] in_reg2;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [1-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;
  wire [4-1:0] route_sel_in;

  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(stream_in),
    .in1(pe_const),
    .in2(in0),
    .in3(in1),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline0)
  );


  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(stream_in),
    .in1(pe_const),
    .in2(in0),
    .in3(in1),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .en(en),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin0
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in0),
    .out(in_reg1)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin1
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in1),
    .out(in_reg2)
  );


  route_2_3x2
  #(
    .width(8)
  )
  router
  (
    .sel_in(route_sel_in),
    .in0(alu_out),
    .in1(in_reg1),
    .in2(in_reg2),
    .out0(out0),
    .out1(out1)
  );

  wire [11-1:0] conf_alu;
  wire [4-1:0] conf_router;

  pe_conf_reader_alu_width_11_router_width_4
  #(
    .pe_id(id),
    .conf_bus_width(8)
  )
  pe_conf_reader
  (
    .clk(clk),
    .conf_bus(conf_bus),
    .reset(reset),
    .conf_alu(conf_alu),
    .conf_const(pe_const),
    .conf_router(conf_router)
  );

  assign sel_alu_opcode = conf_alu[0:0];
  assign sel_mux_alu0 = conf_alu[2:1];
  assign sel_mux_alu1 = conf_alu[4:3];
  assign sel_elastic_pipeline0 = conf_alu[7:5];
  assign sel_elastic_pipeline1 = conf_alu[10:8];
  assign route_sel_in = conf_router[3:0];

endmodule



module multiplexer_4 #
(
  parameter width = 8
)
(
  input [2-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  input [width-1:0] in3,
  output [width-1:0] out
);

  wire [width-1:0] aux [0:4-1];
  assign aux[0] = in0;
  assign aux[1] = in1;
  assign aux[2] = in2;
  assign aux[3] = in3;
  assign out = aux[sel];

endmodule



module elastic_pipeline_4 #
(
  parameter width = 8
)
(
  input clk,
  input en,
  input [3-1:0] latency,
  input [width-1:0] in,
  output [width-1:0] out
);

  reg [width-1:0] shift_reg [0:12-1];
  integer i;

  always @(posedge clk) begin
    if(en) begin
      shift_reg[0] <= in;
      for(i=1; i<12; i=i+1) begin
        shift_reg[i] <= shift_reg[i - 1];
      end
    end 
  end


  multiplexer_5
  #(
    .width(width)
  )
  mux
  (
    .sel(latency),
    .in0(in),
    .in1(shift_reg[2]),
    .in2(shift_reg[5]),
    .in3(shift_reg[8]),
    .in4(shift_reg[11]),
    .out(out)
  );

  integer i_initial;

  initial begin
    for(i_initial=0; i_initial<12; i_initial=i_initial+1) begin
      shift_reg[i_initial] = 0;
    end
  end


endmodule



module multiplexer_5 #
(
  parameter width = 8
)
(
  input [3-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  input [width-1:0] in3,
  input [width-1:0] in4,
  output [width-1:0] out
);

  wire [width-1:0] aux [0:5-1];
  assign aux[0] = in0;
  assign aux[1] = in1;
  assign aux[2] = in2;
  assign aux[3] = in3;
  assign aux[4] = in4;
  assign out = aux[sel];

endmodule



module alu_2_add_sub #
(
  parameter width = 8
)
(
  input clk,
  input en,
  input [1-1:0] opcode,
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);

  reg [width-1:0] in0_reg;
  reg [width-1:0] in1_reg;
  reg [width-1:0] reg_results [0:2-1];
  reg [width-1:0] add_temp;
  reg [width-1:0] sub_temp;

  always @(posedge clk) begin
    if(en) begin
      in0_reg <= in0;
    end 
    if(en) begin
      in1_reg <= in1;
    end 
    if(en) begin
      add_temp <= in0_reg + in1_reg;
      reg_results[0] <= add_temp;
    end 
    if(en) begin
      sub_temp <= in0_reg - in1_reg;
      reg_results[1] <= sub_temp;
    end 
  end

  assign out = reg_results[opcode];
  integer i_initial;

  initial begin
    in0_reg = 0;
    in1_reg = 0;
    for(i_initial=0; i_initial<2; i_initial=i_initial+1) begin
      reg_results[i_initial] = 0;
    end
    add_temp = 0;
    sub_temp = 0;
  end


endmodule



module route_2_3x2 #
(
  parameter width = 16
)
(
  input [4-1:0] sel_in,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  output [width-1:0] out0,
  output [width-1:0] out1
);


  switch_3_2
  #(
    .width(width)
  )
  switch_3_2
  (
    .sel(sel_in),
    .in0(in0),
    .in1(in1),
    .in2(in2),
    .out0(out0),
    .out1(out1)
  );


endmodule



module switch_3_2 #
(
  parameter width = 16
)
(
  input [4-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  output [width-1:0] out0,
  output [width-1:0] out1
);


  multiplexer_3
  #(
    .width(width)
  )
  mux0
  (
    .in0(in0),
    .in1(in1),
    .in2(in2),
    .sel(sel[1:0]),
    .out(out0)
  );


  multiplexer_3
  #(
    .width(width)
  )
  mux1
  (
    .in0(in0),
    .in1(in1),
    .in2(in2),
    .sel(sel[3:2]),
    .out(out1)
  );


endmodule



module multiplexer_3 #
(
  parameter width = 8
)
(
  input [2-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  output [width-1:0] out
);

  wire [width-1:0] aux [0:3-1];
  assign aux[0] = in0;
  assign aux[1] = in1;
  assign aux[2] = in2;
  assign out = aux[sel];

endmodule



module pe_conf_reader_alu_width_11_router_width_4 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [11-1:0] conf_alu,
  output reg [8-1:0] conf_const,
  output reg [4-1:0] conf_router
);

  reg [17-1:0] conf_reg;
  reg [17-1:0] conf_reg0;
  reg [17-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[9:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[9:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[9:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[9:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[2:0]) begin
        case(conf_reg[5:3])
          3'b1: begin
            conf_alu <= conf_reg[16:6];
          end
          3'b10: begin
            conf_const <= conf_reg[13:6];
          end
          3'b11: begin
            conf_router <= conf_reg[9:6];
          end
          3'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
            conf_router <= 0;
          end
        endcase
      end 
    end 
  end


  initial begin
    reset = 0;
    conf_alu = 0;
    conf_const = 0;
    conf_router = 0;
    conf_reg = 0;
    conf_reg0 = 0;
    conf_reg1 = 0;
    flag = 0;
    conf_valid = 0;
  end


endmodule



module pe_basic_2_2_4_add_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  output [8-1:0] out0,
  output [8-1:0] out1
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] in_reg0;
  wire [8-1:0] in_reg3;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [1-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;
  wire [4-1:0] route_sel_in;

  multiplexer_3
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline0)
  );


  multiplexer_3
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .en(en),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin0
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in0),
    .out(in_reg0)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin1
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in1),
    .out(in_reg3)
  );


  route_2_3x2
  #(
    .width(8)
  )
  router
  (
    .sel_in(route_sel_in),
    .in0(alu_out),
    .in1(in_reg0),
    .in2(in_reg3),
    .out0(out0),
    .out1(out1)
  );

  wire [11-1:0] conf_alu;
  wire [4-1:0] conf_router;

  pe_conf_reader_alu_width_11_router_width_4
  #(
    .pe_id(id),
    .conf_bus_width(8)
  )
  pe_conf_reader
  (
    .clk(clk),
    .conf_bus(conf_bus),
    .reset(reset),
    .conf_alu(conf_alu),
    .conf_const(pe_const),
    .conf_router(conf_router)
  );

  assign sel_alu_opcode = conf_alu[0:0];
  assign sel_mux_alu0 = conf_alu[2:1];
  assign sel_mux_alu1 = conf_alu[4:3];
  assign sel_elastic_pipeline0 = conf_alu[7:5];
  assign sel_elastic_pipeline1 = conf_alu[10:8];
  assign route_sel_in = conf_router[3:0];

endmodule



module pe_output_2_2_4_add_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] stream_out
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] in_reg1;
  wire [8-1:0] in_reg2;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [1-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;
  wire [4-1:0] route_sel_in;
  wire [3-1:0] route_sel_out;

  multiplexer_3
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline0)
  );


  multiplexer_3
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .en(en),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin0
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in0),
    .out(in_reg1)
  );


  reg_pipe
  #(
    .num_register(3),
    .width(8)
  )
  in_regin1
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(in1),
    .out(in_reg2)
  );


  route_2_3x3
  #(
    .width(8)
  )
  router
  (
    .sel_in(route_sel_in),
    .sel_out(route_sel_out),
    .in0(alu_out),
    .in1(in_reg1),
    .in2(in_reg2),
    .out0(out0),
    .out1(out1),
    .out2(stream_out)
  );

  wire [11-1:0] conf_alu;
  wire [7-1:0] conf_router;

  pe_conf_reader_alu_width_11_router_width_7
  #(
    .pe_id(id),
    .conf_bus_width(8)
  )
  pe_conf_reader
  (
    .clk(clk),
    .conf_bus(conf_bus),
    .reset(reset),
    .conf_alu(conf_alu),
    .conf_const(pe_const),
    .conf_router(conf_router)
  );

  assign sel_alu_opcode = conf_alu[0:0];
  assign sel_mux_alu0 = conf_alu[2:1];
  assign sel_mux_alu1 = conf_alu[4:3];
  assign sel_elastic_pipeline0 = conf_alu[7:5];
  assign sel_elastic_pipeline1 = conf_alu[10:8];
  assign route_sel_in = conf_router[3:0];
  assign route_sel_out = conf_router[6:4];

endmodule



module route_2_3x3 #
(
  parameter width = 16
)
(
  input [4-1:0] sel_in,
  input [3-1:0] sel_out,
  input [width-1:0] in0,
  input [width-1:0] in1,
  input [width-1:0] in2,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2
);

  wire [width-1:0] sin_sout0;
  wire [width-1:0] sin_sout1;

  switch_3_2
  #(
    .width(width)
  )
  switch_3_2
  (
    .sel(sel_in),
    .in0(in0),
    .in1(in1),
    .in2(in2),
    .out0(sin_sout0),
    .out1(sin_sout1)
  );


  switch_2_3
  #(
    .width(width)
  )
  switch_2_3
  (
    .sel(sel_out),
    .in0(sin_sout0),
    .in1(sin_sout1),
    .out0(out0),
    .out1(out1),
    .out2(out2)
  );


endmodule



module switch_2_3 #
(
  parameter width = 16
)
(
  input [3-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2
);


  multiplexer_2
  #(
    .width(width)
  )
  mux0
  (
    .in0(in0),
    .in1(in1),
    .sel(sel[0:0]),
    .out(out0)
  );


  multiplexer_2
  #(
    .width(width)
  )
  mux1
  (
    .in0(in0),
    .in1(in1),
    .sel(sel[1:1]),
    .out(out1)
  );


  multiplexer_2
  #(
    .width(width)
  )
  mux2
  (
    .in0(in0),
    .in1(in1),
    .sel(sel[2:2]),
    .out(out2)
  );


endmodule



module multiplexer_2 #
(
  parameter width = 8
)
(
  input [1-1:0] sel,
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);

  wire [width-1:0] aux [0:2-1];
  assign aux[0] = in0;
  assign aux[1] = in1;
  assign out = aux[sel];

endmodule



module pe_conf_reader_alu_width_11_router_width_7 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [11-1:0] conf_alu,
  output reg [8-1:0] conf_const,
  output reg [7-1:0] conf_router
);

  reg [17-1:0] conf_reg;
  reg [17-1:0] conf_reg0;
  reg [17-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[9:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[9:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[9:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[9:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[2:0]) begin
        case(conf_reg[5:3])
          3'b1: begin
            conf_alu <= conf_reg[16:6];
          end
          3'b10: begin
            conf_const <= conf_reg[13:6];
          end
          3'b11: begin
            conf_router <= conf_reg[12:6];
          end
          3'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
            conf_router <= 0;
          end
        endcase
      end 
    end 
  end


  initial begin
    reset = 0;
    conf_alu = 0;
    conf_const = 0;
    conf_router = 0;
    conf_reg = 0;
    conf_reg0 = 0;
    conf_reg1 = 0;
    flag = 0;
    conf_valid = 0;
  end


endmodule

