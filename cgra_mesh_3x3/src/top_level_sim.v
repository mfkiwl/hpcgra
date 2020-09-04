module top_level_sim
(

);

  reg rst;
  reg clk;
  reg [8-1+1-1:0] conf_bus;
  reg [8-1+1-1:0] in_stream0;
  reg [8-1+1-1:0] in_stream3;
  reg [8-1+1-1:0] in_stream6;
  wire [8-1+1-1:0] out_stream2;
  wire [8-1+1-1:0] out_stream5;
  wire [8-1+1-1:0] out_stream8;
  reg mem_conf_re;
  reg mem_conf_we;
  reg [20-1:0] mem_conf_addr;
  reg [8-1+1-1:0] mem_conf_din;
  wire [8-1+1-1:0] mem_conf_dout;

  memory
  #(
    .init_file("mem_file.txt"),
    .data_width(8 - 1 + 1),
    .addr_width(20)
  )
  mem_conf
  (
    .clk(clk),
    .we(mem_conf_we),
    .re(mem_conf_re),
    .raddr(mem_conf_addr),
    .waddr(mem_conf_addr),
    .din(mem_conf_din),
    .dout(mem_conf_dout)
  );


  cgra
  cgra
  (
    .clk(clk),
    .conf_bus(conf_bus),
    .in_stream0(in_stream0),
    .in_stream3(in_stream3),
    .in_stream6(in_stream6),
    .out_stream2(out_stream2),
    .out_stream5(out_stream5),
    .out_stream8(out_stream8)
  );


  initial begin
    rst = 1;
    clk = 0;
    conf_bus = 0;
    in_stream0 = 0;
    in_stream3 = 0;
    in_stream6 = 0;
    mem_conf_re = 0;
    mem_conf_we = 0;
    mem_conf_addr = 0;
    mem_conf_din = 0;
  end


  initial begin
    @(posedge clk);
    @(posedge clk);
    @(posedge clk);
    rst = 0;
    #1000000$finish();
  end

  always #5clk=~clk;

  always @(posedge clk) begin
    if(rst) begin
      in_stream0 <= 0;
      in_stream3 <= 0;
      in_stream6 <= 0;
      mem_conf_re <= 0;
      mem_conf_we <= 0;
      mem_conf_addr <= 0;
      mem_conf_din <= 0;
    end else begin
      mem_conf_re <= 0;
      conf_bus <= 0;
      if(mem_conf_addr < 2 ** 10 - 1) begin
        mem_conf_re <= 1;
        if(mem_conf_re) begin
          mem_conf_addr <= mem_conf_addr + 1;
          conf_bus <= mem_conf_dout;
        end 
      end else begin
        in_stream0 <= in_stream0 + 1;
        in_stream3 <= in_stream3 + 1;
        in_stream6 <= in_stream6 + 1;
      end
    end
  end

endmodule