

module cgra
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in_stream0,
  input [8-1:0] in_stream3,
  input [8-1:0] in_stream6,
  output [8-1:0] out_stream2,
  output [8-1:0] out_stream5,
  output [8-1:0] out_stream8
);

  wire [8-1:0] pe0_to_pe1;
  wire [8-1:0] pe0_to_pe3;
  wire [8-1:0] pe1_to_pe0;
  wire [8-1:0] pe1_to_pe2;
  wire [8-1:0] pe1_to_pe4;
  wire [8-1:0] pe2_to_pe1;
  wire [8-1:0] pe2_to_pe5;
  wire [8-1:0] pe3_to_pe0;
  wire [8-1:0] pe3_to_pe4;
  wire [8-1:0] pe3_to_pe6;
  wire [8-1:0] pe4_to_pe1;
  wire [8-1:0] pe4_to_pe3;
  wire [8-1:0] pe4_to_pe5;
  wire [8-1:0] pe4_to_pe7;
  wire [8-1:0] pe5_to_pe2;
  wire [8-1:0] pe5_to_pe4;
  wire [8-1:0] pe5_to_pe8;
  wire [8-1:0] pe6_to_pe3;
  wire [8-1:0] pe6_to_pe7;
  wire [8-1:0] pe7_to_pe4;
  wire [8-1:0] pe7_to_pe6;
  wire [8-1:0] pe7_to_pe8;
  wire [8-1:0] pe8_to_pe5;
  wire [8-1:0] pe8_to_pe7;
  wire [8-1:0] conf_bus_reg_in [0:9-1];
  wire [8-1:0] conf_bus_reg_out [0:9-1];

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


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_4
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[4]),
    .out(conf_bus_reg_out[4])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_5
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[5]),
    .out(conf_bus_reg_out[5])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_6
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[6]),
    .out(conf_bus_reg_out[6])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_7
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[7]),
    .out(conf_bus_reg_out[7])
  );


  reg_pipe
  #(
    .num_register(1),
    .width(8)
  )
  reg_pipe_conf_8
  (
    .clk(clk),
    .rst(1'b0),
    .en(1'b1),
    .in(conf_bus_reg_in[8]),
    .out(conf_bus_reg_out[8])
  );


  pe_input_2_0_0_add_mul_sub
  #(
    .id(1)
  )
  pe_0
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[0]),
    .stream_in(in_stream0),
    .in0(pe1_to_pe0),
    .in1(pe3_to_pe0),
    .out0(pe0_to_pe1),
    .out1(pe0_to_pe3)
  );


  pe_basic_3_0_0_add_mul_sub
  #(
    .id(2)
  )
  pe_1
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[1]),
    .in0(pe0_to_pe1),
    .in1(pe2_to_pe1),
    .in2(pe4_to_pe1),
    .out0(pe1_to_pe0),
    .out1(pe1_to_pe2),
    .out2(pe1_to_pe4)
  );


  pe_output_2_0_0_add_mul_sub
  #(
    .id(3)
  )
  pe_2
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[2]),
    .stream_out(out_stream2),
    .in0(pe1_to_pe2),
    .in1(pe5_to_pe2),
    .out0(pe2_to_pe1),
    .out1(pe2_to_pe5)
  );


  pe_input_3_0_0_add_mul_sub
  #(
    .id(4)
  )
  pe_3
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[3]),
    .stream_in(in_stream3),
    .in0(pe0_to_pe3),
    .in1(pe4_to_pe3),
    .in2(pe6_to_pe3),
    .out0(pe3_to_pe0),
    .out1(pe3_to_pe4),
    .out2(pe3_to_pe6)
  );


  pe_basic_4_0_0_add_mul_sub
  #(
    .id(5)
  )
  pe_4
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[4]),
    .in0(pe1_to_pe4),
    .in1(pe3_to_pe4),
    .in2(pe5_to_pe4),
    .in3(pe7_to_pe4),
    .out0(pe4_to_pe1),
    .out1(pe4_to_pe3),
    .out2(pe4_to_pe5),
    .out3(pe4_to_pe7)
  );


  pe_output_3_0_0_add_mul_sub
  #(
    .id(6)
  )
  pe_5
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[5]),
    .stream_out(out_stream5),
    .in0(pe2_to_pe5),
    .in1(pe4_to_pe5),
    .in2(pe8_to_pe5),
    .out0(pe5_to_pe2),
    .out1(pe5_to_pe4),
    .out2(pe5_to_pe8)
  );


  pe_input_2_0_0_add_mul_sub
  #(
    .id(7)
  )
  pe_6
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[6]),
    .stream_in(in_stream6),
    .in0(pe3_to_pe6),
    .in1(pe7_to_pe6),
    .out0(pe6_to_pe3),
    .out1(pe6_to_pe7)
  );


  pe_basic_3_0_0_add_mul_sub
  #(
    .id(8)
  )
  pe_7
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[7]),
    .in0(pe4_to_pe7),
    .in1(pe6_to_pe7),
    .in2(pe8_to_pe7),
    .out0(pe7_to_pe4),
    .out1(pe7_to_pe6),
    .out2(pe7_to_pe8)
  );


  pe_output_2_0_0_add_mul_sub
  #(
    .id(9)
  )
  pe_8
  (
    .clk(clk),
    .conf_bus(conf_bus_reg_out[8]),
    .stream_out(out_stream8),
    .in0(pe5_to_pe8),
    .in1(pe7_to_pe8),
    .out0(pe8_to_pe5),
    .out1(pe8_to_pe7)
  );

  assign conf_bus_reg_in[0] = conf_bus;
  assign conf_bus_reg_in[3] = conf_bus_reg_out[0];
  assign conf_bus_reg_in[6] = conf_bus_reg_out[3];
  assign conf_bus_reg_in[1] = conf_bus_reg_out[0];
  assign conf_bus_reg_in[2] = conf_bus_reg_out[1];
  assign conf_bus_reg_in[4] = conf_bus_reg_out[3];
  assign conf_bus_reg_in[5] = conf_bus_reg_out[4];
  assign conf_bus_reg_in[7] = conf_bus_reg_out[6];
  assign conf_bus_reg_in[8] = conf_bus_reg_out[7];

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



module pe_input_2_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  output [8-1:0] out0,
  output [8-1:0] out1,
  input [8-1:0] stream_in
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

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

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
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

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_3x2
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1)
  );

  wire [6-1:0] conf_alu;

  pe_conf_reader_alu_width_6_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[3:2];
  assign sel_mux_alu1 = conf_alu[5:4];

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



module elastic_pipeline_0 #
(
  parameter width = 8
)
(
  input [width-1:0] in,
  output [width-1:0] out
);

  assign out = in;

endmodule



module alu_2_add_mul_sub #
(
  parameter width = 8
)
(
  input clk,
  input [2-1:0] opcode,
  input [width-1:0] in0,
  input [width-1:0] in1,
  output [width-1:0] out
);

  reg [width-1:0] in0_reg;
  reg [width-1:0] in1_reg;
  reg [width-1:0] reg_results [0:3-1];
  reg [width-1:0] add_temp;
  reg [width-1:0] mul_temp;
  reg [width-1:0] sub_temp;

  always @(posedge clk) begin
    in0_reg <= in0;
    in1_reg <= in1;
    add_temp <= in0_reg + in1_reg;
    reg_results[0] <= add_temp;
    mul_temp <= in0_reg * in1_reg;
    reg_results[1] <= mul_temp;
    sub_temp <= in0_reg - in1_reg;
    reg_results[2] <= sub_temp;
  end

  assign out = reg_results[opcode];
  integer i_initial;

  initial begin
    in0_reg = 0;
    in1_reg = 0;
    for(i_initial=0; i_initial<3; i_initial=i_initial+1) begin
      reg_results[i_initial] = 0;
    end
    add_temp = 0;
    mul_temp = 0;
    sub_temp = 0;
  end


endmodule



module route_0_3x2 #
(
  parameter width = 16
)
(
  input [width-1:0] in0,
  output [width-1:0] out0,
  output [width-1:0] out1
);

  assign out0 = in0;
  assign out1 = in0;

endmodule



module pe_conf_reader_alu_width_6_router_width_0 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [6-1:0] conf_alu,
  output reg [8-1:0] conf_const
);

  reg [15-1:0] conf_reg;
  reg [15-1:0] conf_reg0;
  reg [15-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[7:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[7:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[7:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[7:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[4:0]) begin
        case(conf_reg[6:5])
          2'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
          end
          2'b1: begin
            conf_alu <= conf_reg[12:7];
          end
          2'b10: begin
            conf_const <= conf_reg[14:7];
          end
        endcase
      end 
    end 
  end


  initial begin
    reset = 0;
    conf_alu = 0;
    conf_const = 0;
    conf_reg = 0;
    conf_reg0 = 0;
    conf_reg1 = 0;
    flag = 0;
    conf_valid = 0;
  end


endmodule



module pe_basic_3_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  input [8-1:0] in2,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] out2
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
  );


  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_4x3
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(out2)
  );

  wire [6-1:0] conf_alu;

  pe_conf_reader_alu_width_6_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[3:2];
  assign sel_mux_alu1 = conf_alu[5:4];

endmodule



module route_0_4x3 #
(
  parameter width = 16
)
(
  input [width-1:0] in0,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2
);

  assign out0 = in0;
  assign out1 = in0;
  assign out2 = in0;

endmodule



module pe_output_2_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] stream_out
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

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

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
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

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_3x3
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(stream_out)
  );

  wire [6-1:0] conf_alu;

  pe_conf_reader_alu_width_6_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[3:2];
  assign sel_mux_alu1 = conf_alu[5:4];

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



module route_0_3x3 #
(
  parameter width = 16
)
(
  input [width-1:0] in0,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2
);

  assign out0 = in0;
  assign out1 = in0;
  assign out2 = in0;

endmodule



module pe_input_3_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  input [8-1:0] in2,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] out2,
  input [8-1:0] stream_in
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [3-1:0] sel_mux_alu0;
  wire [3-1:0] sel_mux_alu1;

  multiplexer_5
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
    .in4(in2),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
  );


  multiplexer_5
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
    .in4(in2),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_4x3
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(out2)
  );

  wire [8-1:0] conf_alu;

  pe_conf_reader_alu_width_8_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[4:2];
  assign sel_mux_alu1 = conf_alu[7:5];

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



module pe_conf_reader_alu_width_8_router_width_0 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [8-1:0] conf_alu,
  output reg [8-1:0] conf_const
);

  reg [15-1:0] conf_reg;
  reg [15-1:0] conf_reg0;
  reg [15-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[7:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[7:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[7:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[7:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[4:0]) begin
        case(conf_reg[6:5])
          2'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
          end
          2'b1: begin
            conf_alu <= conf_reg[14:7];
          end
          2'b10: begin
            conf_const <= conf_reg[14:7];
          end
        endcase
      end 
    end 
  end


  initial begin
    reset = 0;
    conf_alu = 0;
    conf_const = 0;
    conf_reg = 0;
    conf_reg0 = 0;
    conf_reg1 = 0;
    flag = 0;
    conf_valid = 0;
  end


endmodule



module pe_basic_4_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  input [8-1:0] in2,
  input [8-1:0] in3,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] out2,
  output [8-1:0] out3
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [3-1:0] sel_mux_alu0;
  wire [3-1:0] sel_mux_alu1;

  multiplexer_5
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .in4(in3),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
  );


  multiplexer_5
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .in4(in3),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_5x4
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(out2),
    .out3(out3)
  );

  wire [8-1:0] conf_alu;

  pe_conf_reader_alu_width_8_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[4:2];
  assign sel_mux_alu1 = conf_alu[7:5];

endmodule



module route_0_5x4 #
(
  parameter width = 16
)
(
  input [width-1:0] in0,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2,
  output [width-1:0] out3
);

  assign out0 = in0;
  assign out1 = in0;
  assign out2 = in0;
  assign out3 = in0;

endmodule



module pe_output_3_0_0_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input [8-1:0] conf_bus,
  input [8-1:0] in0,
  input [8-1:0] in1,
  input [8-1:0] in2,
  output [8-1:0] out0,
  output [8-1:0] out1,
  output [8-1:0] out2,
  output [8-1:0] stream_out
);

  wire reset;
  wire [8-1:0] pe_const;
  wire [8-1:0] alu_in0;
  wire [8-1:0] alu_in1;
  wire [8-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .out(alu_in0)
  );

  wire [8-1:0] elastic_pipeline_to_alu0;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0)
  );


  multiplexer_4
  #(
    .width(8)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .in3(in2),
    .out(alu_in1)
  );

  wire [8-1:0] elastic_pipeline_to_alu1;

  elastic_pipeline_0
  #(
    .width(8)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1)
  );


  alu_2_add_mul_sub
  #(
    .width(8)
  )
  alu
  (
    .clk(clk),
    .opcode(sel_alu_opcode),
    .in0(elastic_pipeline_to_alu0),
    .in1(elastic_pipeline_to_alu1),
    .out(alu_out)
  );


  route_0_4x4
  #(
    .width(8)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(out2),
    .out3(stream_out)
  );

  wire [6-1:0] conf_alu;

  pe_conf_reader_alu_width_6_router_width_0
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
    .conf_const(pe_const)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[3:2];
  assign sel_mux_alu1 = conf_alu[5:4];

endmodule



module route_0_4x4 #
(
  parameter width = 16
)
(
  input [width-1:0] in0,
  output [width-1:0] out0,
  output [width-1:0] out1,
  output [width-1:0] out2,
  output [width-1:0] out3
);

  assign out0 = in0;
  assign out1 = in0;
  assign out2 = in0;
  assign out3 = in0;

endmodule

