

module testbench_sim
(

);

  localparam INTERFACE_DATA_WIDTH = 512;
  reg clk;
  reg rst;
  reg start;
  wire [2-1:0] rd_done;
  reg [1-1:0] wr_done;
  wire [2-1:0] rd_available;
  reg [1-1:0] wr_available;
  wire [2-1:0] rd_request;
  wire [2-1:0] rd_valid;
  wire [INTERFACE_DATA_WIDTH*2-1:0] rd_data;
  wire [1-1:0] wr_request;
  wire [INTERFACE_DATA_WIDTH*1-1:0] wr_data;
  wire acc_done;

  data_producer
  #(
    .file("/home/jeronimo/Documentos/GIT/hpcgra/simul_tests/Exemplos/example_cgra_2x2/loopback.bit"),
    .data_width(INTERFACE_DATA_WIDTH)
  )
  data_producer_0
  (
    .clk(clk),
    .rst(rst),
    .rd_request(rd_request[0]),
    .read_data_valid(rd_valid[0]),
    .rd_done(rd_done[0]),
    .read_data(rd_data[1*INTERFACE_DATA_WIDTH-1:0*INTERFACE_DATA_WIDTH])
  );


  data_producer
  #(
    .file("/home/jeronimo/Documentos/GIT/hpcgra/simul_tests/Exemplos/example_cgra_2x2/loopback.bit"),
    .data_width(INTERFACE_DATA_WIDTH)
  )
  data_producer_1
  (
    .clk(clk),
    .rst(rst),
    .rd_request(rd_request[1]),
    .read_data_valid(rd_valid[1]),
    .rd_done(rd_done[1]),
    .read_data(rd_data[2*INTERFACE_DATA_WIDTH-1:1*INTERFACE_DATA_WIDTH])
  );


  initial begin
    clk = 0;
    rst = 1;
    start = 0;
    wr_done = 0;
    wr_available = 1;
  end


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0);
  end


  initial begin
    @(posedge clk);
    @(posedge clk);
    @(posedge clk);
    rst = 0;
    start = 1;
    #10000;
    $finish;
  end

  always #5clk=~clk;

  always @(posedge clk) begin
    if(acc_done) begin
      $display("ACC DONE!");
      $finish;
    end 
  end


endmodule



module data_producer #
(
  parameter file = "file.txt",
  parameter data_width = 512
)
(
  input clk,
  input rst,
  input rd_request,
  output reg read_data_valid,
  output reg rd_done,
  output [data_width-1:0] read_data
);

  wire re;


  reg re_fsw;
  reg [3-1:0] data_counter;


  reg [2-1:0] fsm_produce_data;
  localparam fsm_init = 2'd0;
  localparam fsm_produce = 2'd1;
  localparam fsm_done = 2'd2;


  assign re = re_fsw | rd_request;

  always @(posedge clk) begin
    if(rst) begin
      data_counter <= 3'd0;
      read_data_valid <= 1'd0;
      rd_done <= 1'd0;
      fsm_produce_data <= fsm_init;
    end else begin
      case(fsm_produce_data)
        fsm_init: begin
          re_fsw <= 1'd1;
          fsm_produce_data <= fsm_produce;
        end
        fsm_produce: begin
          re_fsw <= 1'd0;
          read_data_valid <= 1'd1;
          if(rd_request) begin
            data_counter <= data_counter + 3'd1;
          end 
          if(data_counter == 3'd4) begin
            fsm_produce_data <= fsm_done;
          end 
        end
        fsm_done: begin
          read_data_valid <= 1'd0;
          rd_done <= 1'd1;
        end
      endcase
    end
  end


  memory
  #(
    .init_file(file),
    .data_width(data_width),
    .addr_width(3)
  )
  mem_rom
  (
    .clk(clk),
    .we(1'b0),
    .re(re),
    .raddr(data_counter),
    .waddr(data_counter),
    .din({ data_width{ 1'b0 } }),
    .dout(read_data)
  );


  initial begin
    read_data_valid = 0;
    rd_done = 0;
    re_fsw = 0;
    data_counter = 0;
    fsm_produce_data = 0;
  end


endmodule



module memory #
(
  parameter init_file = "mem_file.txt",
  parameter data_width = 32,
  parameter addr_width = 8
)
(
  input clk,
  input we,
  input re,
  input [addr_width-1:0] raddr,
  input [addr_width-1:0] waddr,
  input [data_width-1:0] din,
  output reg [data_width-1:0] dout
);

  (* ramstyle = "AUTO, no_rw_check" *) reg  [data_width-1:0] mem[0:2**addr_width-1];
  /*
  reg [data_width-1:0] mem [0:2**addr_width-1];
  */

  always @(posedge clk) begin
    if(we) begin
      mem[waddr] <= din;
    end 
    if(re) begin
      dout <= mem[raddr];
    end 
  end

  //synthesis translate_off
  integer i;

  initial begin
    dout = 0;
    for(i=0; i<2**addr_width; i=i+1) begin
      mem[i] = 0;
    end
    $readmemh(init_file, mem);
  end

  //synthesis translate_on

endmodule

