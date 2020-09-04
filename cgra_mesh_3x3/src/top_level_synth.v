module top_level_synth
(
  input clk,
  input rst,
  output out
);

  reg [8-1+1-1:0] conf_bus;
  reg [8-1+1-1:0] in_stream0;
  reg [8-1+1-1:0] in_stream3;
  reg [8-1+1-1:0] in_stream6;
  wire [8-1+1-1:0] cgra_out_stream2;
  wire [8-1+1-1:0] cgra_out_stream5;
  wire [8-1+1-1:0] cgra_out_stream8;
  wire [8-1+1-1:0] data;

  cgra
  cgra
  (
    .clk(clk),
    .conf_bus(conf_bus),
    .in_stream0(in_stream0),
    .in_stream3(in_stream3),
    .in_stream6(in_stream6),
    .out_stream2(cgra_out_stream2),
    .out_stream5(cgra_out_stream5),
    .out_stream8(cgra_out_stream8)
  );


  always @(posedge clk) begin
    if(rst) begin
      conf_bus <= 0;
      in_stream0 <= 0;
      in_stream3 <= 0;
      in_stream6 <= 0;
    end else begin
      conf_bus <= conf_bus + 1;
      in_stream0 <= in_stream0 + 1;
      in_stream3 <= in_stream3 + 1;
      in_stream6 <= in_stream6 + 1;
    end
  end

  assign data = cgra_out_stream2|cgra_out_stream5|cgra_out_stream8;
  assign out = ^data;

  initial begin
    conf_bus = 0;
    in_stream0 = 0;
    in_stream3 = 0;
    in_stream6 = 0;
  end

endmodule