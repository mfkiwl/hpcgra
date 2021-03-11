

module kernel_top #
(
  parameter C_S_AXI_CONTROL_ADDR_WIDTH = 12,
  parameter C_S_AXI_CONTROL_DATA_WIDTH = 32,
  parameter C_M_AXI_ADDR_WIDTH = 64,
  parameter C_M_AXI_DATA_WIDTH = 512
)
(
  input ap_clk,
  input ap_rst_n,
  input s_axi_control_awvalid,
  output s_axi_control_awready,
  input [C_S_AXI_CONTROL_ADDR_WIDTH-1:0] s_axi_control_awaddr,
  input s_axi_control_wvalid,
  output s_axi_control_wready,
  input [C_S_AXI_CONTROL_DATA_WIDTH-1:0] s_axi_control_wdata,
  input [C_S_AXI_CONTROL_DATA_WIDTH/8-1:0] s_axi_control_wstrb,
  input s_axi_control_arvalid,
  output s_axi_control_arready,
  input [C_S_AXI_CONTROL_ADDR_WIDTH-1:0] s_axi_control_araddr,
  output s_axi_control_rvalid,
  input s_axi_control_rready,
  output [C_S_AXI_CONTROL_DATA_WIDTH-1:0] s_axi_control_rdata,
  output [2-1:0] s_axi_control_rresp,
  output s_axi_control_bvalid,
  input s_axi_control_bready,
  output [2-1:0] s_axi_control_bresp,
  output interrupt,
  output m00_axi_awvalid,
  input m00_axi_awready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m00_axi_awaddr,
  output [8-1:0] m00_axi_awlen,
  output m00_axi_wvalid,
  input m00_axi_wready,
  output [C_M_AXI_DATA_WIDTH-1:0] m00_axi_wdata,
  output [C_M_AXI_DATA_WIDTH/8-1:0] m00_axi_wstrb,
  output m00_axi_wlast,
  input m00_axi_bvalid,
  output m00_axi_bready,
  output m00_axi_arvalid,
  input m00_axi_arready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m00_axi_araddr,
  output [8-1:0] m00_axi_arlen,
  input m00_axi_rvalid,
  output m00_axi_rready,
  input [C_M_AXI_DATA_WIDTH-1:0] m00_axi_rdata,
  input m00_axi_rlast,
  output m01_axi_awvalid,
  input m01_axi_awready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m01_axi_awaddr,
  output [8-1:0] m01_axi_awlen,
  output m01_axi_wvalid,
  input m01_axi_wready,
  output [C_M_AXI_DATA_WIDTH-1:0] m01_axi_wdata,
  output [C_M_AXI_DATA_WIDTH/8-1:0] m01_axi_wstrb,
  output m01_axi_wlast,
  input m01_axi_bvalid,
  output m01_axi_bready,
  output m01_axi_arvalid,
  input m01_axi_arready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m01_axi_araddr,
  output [8-1:0] m01_axi_arlen,
  input m01_axi_rvalid,
  output m01_axi_rready,
  input [C_M_AXI_DATA_WIDTH-1:0] m01_axi_rdata,
  input m01_axi_rlast
);

  (* DONT_TOUCH = "yes" *)
  reg areset;
  wire ap_start;
  wire ap_idle;
  wire ap_done;
  wire ap_ready;
  wire [32-1:0] in_s0;
  wire [32-1:0] in_s1;
  wire [32-1:0] out_s0;
  wire [32-1:0] out_s1;
  wire [64-1:0] in0;
  wire [64-1:0] out0;
  wire [64-1:0] in1;
  wire [64-1:0] out1;

  always @(posedge ap_clk) begin
    areset <= ~ap_rst_n;
  end


  control_s_axi_2
  #(
    .C_S_AXI_ADDR_WIDTH(C_S_AXI_CONTROL_ADDR_WIDTH),
    .C_S_AXI_DATA_WIDTH(C_S_AXI_CONTROL_DATA_WIDTH)
  )
  control_s_axi_inst
  (
    .aclk(ap_clk),
    .areset(areset),
    .aclk_en(1'b1),
    .awvalid(s_axi_control_awvalid),
    .awready(s_axi_control_awready),
    .awaddr(s_axi_control_awaddr),
    .wvalid(s_axi_control_wvalid),
    .wready(s_axi_control_wready),
    .wdata(s_axi_control_wdata),
    .wstrb(s_axi_control_wstrb),
    .arvalid(s_axi_control_arvalid),
    .arready(s_axi_control_arready),
    .araddr(s_axi_control_araddr),
    .rvalid(s_axi_control_rvalid),
    .rready(s_axi_control_rready),
    .rdata(s_axi_control_rdata),
    .rresp(s_axi_control_rresp),
    .bvalid(s_axi_control_bvalid),
    .bready(s_axi_control_bready),
    .bresp(s_axi_control_bresp),
    .interrupt(interrupt),
    .ap_start(ap_start),
    .ap_done(ap_done),
    .ap_ready(ap_ready),
    .ap_idle(ap_idle),
    .in_s0(in_s0),
    .in_s1(in_s1),
    .out_s0(out_s0),
    .out_s1(out_s1),
    .in0(in0),
    .out0(out0),
    .in1(in1),
    .out1(out1)
  );


  app_top
  #(
    .C_M_AXI_ADDR_WIDTH(C_M_AXI_ADDR_WIDTH),
    .C_M_AXI_DATA_WIDTH(C_M_AXI_DATA_WIDTH)
  )
  app_inst
  (
    .ap_clk(ap_clk),
    .ap_rst_n(ap_rst_n),
    .ap_start(ap_start),
    .ap_done(ap_done),
    .ap_idle(ap_idle),
    .ap_ready(ap_ready),
    .in_s0(in_s0),
    .in_s1(in_s1),
    .out_s0(out_s0),
    .out_s1(out_s1),
    .in0(in0),
    .out0(out0),
    .in1(in1),
    .out1(out1),
    .m00_axi_awvalid(m00_axi_awvalid),
    .m00_axi_awready(m00_axi_awready),
    .m00_axi_awaddr(m00_axi_awaddr),
    .m00_axi_awlen(m00_axi_awlen),
    .m00_axi_wvalid(m00_axi_wvalid),
    .m00_axi_wready(m00_axi_wready),
    .m00_axi_wdata(m00_axi_wdata),
    .m00_axi_wstrb(m00_axi_wstrb),
    .m00_axi_wlast(m00_axi_wlast),
    .m00_axi_bvalid(m00_axi_bvalid),
    .m00_axi_bready(m00_axi_bready),
    .m00_axi_arvalid(m00_axi_arvalid),
    .m00_axi_arready(m00_axi_arready),
    .m00_axi_araddr(m00_axi_araddr),
    .m00_axi_arlen(m00_axi_arlen),
    .m00_axi_rvalid(m00_axi_rvalid),
    .m00_axi_rready(m00_axi_rready),
    .m00_axi_rdata(m00_axi_rdata),
    .m00_axi_rlast(m00_axi_rlast),
    .m01_axi_awvalid(m01_axi_awvalid),
    .m01_axi_awready(m01_axi_awready),
    .m01_axi_awaddr(m01_axi_awaddr),
    .m01_axi_awlen(m01_axi_awlen),
    .m01_axi_wvalid(m01_axi_wvalid),
    .m01_axi_wready(m01_axi_wready),
    .m01_axi_wdata(m01_axi_wdata),
    .m01_axi_wstrb(m01_axi_wstrb),
    .m01_axi_wlast(m01_axi_wlast),
    .m01_axi_bvalid(m01_axi_bvalid),
    .m01_axi_bready(m01_axi_bready),
    .m01_axi_arvalid(m01_axi_arvalid),
    .m01_axi_arready(m01_axi_arready),
    .m01_axi_araddr(m01_axi_araddr),
    .m01_axi_arlen(m01_axi_arlen),
    .m01_axi_rvalid(m01_axi_rvalid),
    .m01_axi_rready(m01_axi_rready),
    .m01_axi_rdata(m01_axi_rdata),
    .m01_axi_rlast(m01_axi_rlast)
  );


  initial begin
    areset = 1'b1;
  end


endmodule



module control_s_axi_2 #
(
  parameter C_S_AXI_ADDR_WIDTH = 7,
  parameter C_S_AXI_DATA_WIDTH = 32
)
(
  input aclk,
  input areset,
  input aclk_en,
  input [C_S_AXI_ADDR_WIDTH-1:0] awaddr,
  input awvalid,
  output awready,
  input [C_S_AXI_DATA_WIDTH-1:0] wdata,
  input [C_S_AXI_DATA_WIDTH/8-1:0] wstrb,
  input wvalid,
  output wready,
  output [2-1:0] bresp,
  output bvalid,
  input bready,
  input [C_S_AXI_ADDR_WIDTH-1:0] araddr,
  input arvalid,
  output arready,
  output [C_S_AXI_DATA_WIDTH-1:0] rdata,
  output [2-1:0] rresp,
  output rvalid,
  input rready,
  output interrupt,
  output ap_start,
  input ap_done,
  input ap_ready,
  input ap_idle,
  output [32-1:0] in_s0,
  output [32-1:0] in_s1,
  output [32-1:0] out_s0,
  output [32-1:0] out_s1,
  output [64-1:0] in0,
  output [64-1:0] in1,
  output [64-1:0] out0,
  output [64-1:0] out1
);

  localparam ADDR_AP_CTRL = 7'h0;
  localparam ADDR_GIE = 7'h4;
  localparam ADDR_IER = 7'h8;
  localparam ADDR_ISR = 7'hc;
  localparam ADDR_IN_S0_DATA_0 = 7'h10;
  localparam ADDR_IN_S0_CTRL = 7'h14;
  localparam ADDR_IN_S1_DATA_0 = 7'h18;
  localparam ADDR_IN_S1_CTRL = 7'h1c;
  localparam ADDR_OUT_S0_DATA_0 = 7'h20;
  localparam ADDR_OUT_S0_CTRL = 7'h24;
  localparam ADDR_OUT_S1_DATA_0 = 7'h28;
  localparam ADDR_OUT_S1_CTRL = 7'h2c;
  localparam ADDR_IN0_DATA_0 = 7'h30;
  localparam ADDR_IN0_DATA_1 = 7'h34;
  localparam ADDR_IN0_CTRL = 7'h38;
  localparam ADDR_OUT0_DATA_0 = 7'h3c;
  localparam ADDR_OUT0_DATA_1 = 7'h40;
  localparam ADDR_OUT0_CTRL = 7'h44;
  localparam ADDR_IN1_DATA_0 = 7'h48;
  localparam ADDR_IN1_DATA_1 = 7'h4c;
  localparam ADDR_IN1_CTRL = 7'h50;
  localparam ADDR_OUT1_DATA_0 = 7'h54;
  localparam ADDR_OUT1_DATA_1 = 7'h58;
  localparam ADDR_OUT1_CTRL = 7'h5c;
  localparam WRIDLE = 2'd0;
  localparam WRDATA = 2'd1;
  localparam WRRESP = 2'd2;
  localparam WRRESET = 2'd3;
  localparam RDIDLE = 2'd0;
  localparam RDDATA = 2'd1;
  localparam RDRESET = 2'd2;
  localparam ADDR_BITS = 7;
  reg [2-1:0] wstate;
  reg [2-1:0] wnext;
  reg [ADDR_BITS-1:0] waddr;
  wire [32-1:0] wmask;
  wire aw_hs;
  wire w_hs;
  reg [2-1:0] rstate;
  reg [2-1:0] rnext;
  reg [32-1:0] rrdata;
  wire ar_hs;
  wire [ADDR_BITS-1:0] raddr;
  reg int_ap_idle;
  reg int_ap_ready;
  reg int_ap_done;
  reg int_ap_start;
  reg int_auto_restart;
  reg int_gie;
  reg [2-1:0] int_ier;
  reg [2-1:0] int_isr;
  reg [32-1:0] int_in_s0;
  reg [32-1:0] int_in_s1;
  reg [32-1:0] int_out_s0;
  reg [32-1:0] int_out_s1;
  reg [64-1:0] int_in0;
  reg [64-1:0] int_out0;
  reg [64-1:0] int_in1;
  reg [64-1:0] int_out1;
  assign awready = wstate == WRIDLE;
  assign wready = wstate == WRDATA;
  assign bresp = 2'b0;
  assign bvalid = wstate == WRRESP;
  assign wmask = { { 8{ wstrb[3] } }, { 8{ wstrb[2] } }, { 8{ wstrb[1] } }, { 8{ wstrb[0] } } };
  assign aw_hs = awvalid & awready;
  assign w_hs = wvalid & wready;

  always @(posedge aclk) begin
    if(areset) begin
      wstate <= WRRESET;
    end else begin
      if(aclk_en) begin
        wstate <= wnext;
      end 
    end
  end


  always @(*) begin
    case(wstate)
      WRIDLE: begin
        if(awvalid) begin
          wnext <= WRDATA;
        end else begin
          wnext <= WRIDLE;
        end
      end
      WRDATA: begin
        if(wvalid) begin
          wnext <= WRRESP;
        end else begin
          wnext <= WRDATA;
        end
      end
      WRRESP: begin
        if(bready) begin
          wnext <= WRIDLE;
        end else begin
          wnext <= WRRESP;
        end
      end
      default: begin
        wnext <= WRIDLE;
      end
    endcase
  end


  always @(posedge aclk) begin
    if(aclk_en) begin
      if(aw_hs) begin
        waddr <= awaddr[ADDR_BITS-1:0];
      end 
    end 
  end

  assign arready = rstate == RDIDLE;
  assign rdata = rrdata;
  assign rresp = 2'b0;
  assign rvalid = rstate == RDDATA;
  assign ar_hs = arvalid & arready;
  assign raddr = araddr[ADDR_BITS-1:0];

  always @(posedge aclk) begin
    if(areset) begin
      rstate <= RDRESET;
    end else begin
      if(aclk_en) begin
        rstate <= rnext;
      end 
    end
  end


  always @(*) begin
    case(rstate)
      RDIDLE: begin
        if(arvalid) begin
          rnext <= RDDATA;
        end else begin
          rnext <= RDIDLE;
        end
      end
      RDDATA: begin
        if(rready & rvalid) begin
          rnext <= RDIDLE;
        end else begin
          rnext <= RDDATA;
        end
      end
      default: begin
        rnext <= RDIDLE;
      end
    endcase
  end


  always @(posedge aclk) begin
    if(aclk_en) begin
      if(ar_hs) begin
        rrdata <= 1'b0;
        case(raddr)
          ADDR_AP_CTRL: begin
            rrdata[0] <= int_ap_start;
            rrdata[1] <= int_ap_done;
            rrdata[2] <= int_ap_idle;
            rrdata[3] <= int_ap_ready;
            rrdata[7] <= int_auto_restart;
          end
          ADDR_GIE: begin
            rrdata <= int_gie;
          end
          ADDR_IER: begin
            rrdata <= int_ier;
          end
          ADDR_ISR: begin
            rrdata <= int_isr;
          end
          ADDR_IN_S0_DATA_0: begin
            rrdata <= int_in_s0[31:0];
          end
          ADDR_IN_S1_DATA_0: begin
            rrdata <= int_in_s1[31:0];
          end
          ADDR_OUT_S0_DATA_0: begin
            rrdata <= int_out_s0[31:0];
          end
          ADDR_OUT_S1_DATA_0: begin
            rrdata <= int_out_s1[31:0];
          end
          ADDR_IN0_DATA_0: begin
            rrdata <= int_in0[31:0];
          end
          ADDR_IN0_DATA_1: begin
            rrdata <= int_in0[63:32];
          end
          ADDR_IN1_DATA_0: begin
            rrdata <= int_in1[31:0];
          end
          ADDR_IN1_DATA_1: begin
            rrdata <= int_in1[63:32];
          end
          ADDR_OUT0_DATA_0: begin
            rrdata <= int_out0[31:0];
          end
          ADDR_OUT0_DATA_1: begin
            rrdata <= int_out0[63:32];
          end
          ADDR_OUT1_DATA_0: begin
            rrdata <= int_out1[31:0];
          end
          ADDR_OUT1_DATA_1: begin
            rrdata <= int_out1[63:32];
          end
        endcase
      end 
    end 
  end

  assign interrupt = int_gie & |int_isr;
  assign ap_start = int_ap_start;
  assign in_s0 = int_in_s0;
  assign in_s1 = int_in_s1;
  assign out_s0 = int_out_s0;
  assign out_s1 = int_out_s1;
  assign in0 = int_in0;
  assign out0 = int_out0;
  assign in1 = int_in1;
  assign out1 = int_out1;

  always @(posedge aclk) begin
    if(areset) begin
      int_ap_start <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_AP_CTRL) && wstrb[0] && wdata[0]) begin
          int_ap_start <= 1'b1;
        end else if(ap_ready) begin
          int_ap_start <= int_auto_restart;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_ap_done <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(ap_done) begin
          int_ap_done <= 1'b1;
        end else if(ar_hs && (raddr == ADDR_AP_CTRL)) begin
          int_ap_done <= 1'b0;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_ap_idle <= 1'b1;
    end else begin
      if(aclk_en) begin
        int_ap_idle <= ap_idle;
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_ap_ready <= 1'b0;
    end else begin
      if(aclk_en) begin
        int_ap_ready <= ap_ready;
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_auto_restart <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_AP_CTRL) && wstrb[0]) begin
          int_auto_restart <= wdata[7];
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_gie <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_GIE) && wstrb[0]) begin
          int_gie <= wdata[0];
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_ier <= 2'b0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IER) && wstrb[0]) begin
          int_ier <= wdata[1:0];
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_isr[0] <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(int_ier[0] & ap_done) begin
          int_isr[0] <= 1'b1;
        end else if(w_hs && (waddr == ADDR_ISR) && wstrb[0]) begin
          int_isr[0] <= int_isr[0] ^ wdata[0];
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_isr[1] <= 1'b0;
    end else begin
      if(aclk_en) begin
        if(int_ier[1] & ap_ready) begin
          int_isr[1] <= 1'b1;
        end else if(w_hs && (waddr == ADDR_ISR) && wstrb[0]) begin
          int_isr[1] <= int_isr[1] ^ wdata[1];
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in_s0[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN_S0_DATA_0)) begin
          int_in_s0[31:0] <= wdata[31:0] & wmask | int_in_s0[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in_s1[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN_S1_DATA_0)) begin
          int_in_s1[31:0] <= wdata[31:0] & wmask | int_in_s1[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out_s0[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT_S0_DATA_0)) begin
          int_out_s0[31:0] <= wdata[31:0] & wmask | int_out_s0[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out_s1[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT_S1_DATA_0)) begin
          int_out_s1[31:0] <= wdata[31:0] & wmask | int_out_s1[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in0[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN0_DATA_0)) begin
          int_in0[31:0] <= wdata[31:0] & wmask | int_in0[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in0[63:32] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN0_DATA_1)) begin
          int_in0[63:32] <= wdata[31:0] & wmask | int_in0[63:32] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out0[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT0_DATA_0)) begin
          int_out0[31:0] <= wdata[31:0] & wmask | int_out0[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out0[63:32] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT0_DATA_1)) begin
          int_out0[63:32] <= wdata[31:0] & wmask | int_out0[63:32] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in1[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN1_DATA_0)) begin
          int_in1[31:0] <= wdata[31:0] & wmask | int_in1[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_in1[63:32] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_IN1_DATA_1)) begin
          int_in1[63:32] <= wdata[31:0] & wmask | int_in1[63:32] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out1[31:0] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT1_DATA_0)) begin
          int_out1[31:0] <= wdata[31:0] & wmask | int_out1[31:0] & ~wmask;
        end 
      end 
    end
  end


  always @(posedge aclk) begin
    if(areset) begin
      int_out1[63:32] <= 32'd0;
    end else begin
      if(aclk_en) begin
        if(w_hs && (waddr == ADDR_OUT1_DATA_1)) begin
          int_out1[63:32] <= wdata[31:0] & wmask | int_out1[63:32] & ~wmask;
        end 
      end 
    end
  end


  initial begin
    wstate = WRRESET;
    wnext = 0;
    waddr = 0;
    rstate = RDRESET;
    rnext = 0;
    rrdata = 0;
    int_ap_idle = 1'b1;
    int_ap_ready = 0;
    int_ap_done = 0;
    int_ap_start = 0;
    int_auto_restart = 0;
    int_gie = 0;
    int_ier = 0;
    int_isr = 0;
    int_in_s0 = 0;
    int_in_s1 = 0;
    int_out_s0 = 0;
    int_out_s1 = 0;
    int_in0 = 0;
    int_out0 = 0;
    int_in1 = 0;
    int_out1 = 0;
  end


endmodule



module app_top #
(
  parameter C_M_AXI_ADDR_WIDTH = 64,
  parameter C_M_AXI_DATA_WIDTH = 512
)
(
  input ap_clk,
  input ap_rst_n,
  output m00_axi_awvalid,
  input m00_axi_awready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m00_axi_awaddr,
  output [8-1:0] m00_axi_awlen,
  output m00_axi_wvalid,
  input m00_axi_wready,
  output [C_M_AXI_DATA_WIDTH-1:0] m00_axi_wdata,
  output [C_M_AXI_DATA_WIDTH/8-1:0] m00_axi_wstrb,
  output m00_axi_wlast,
  input m00_axi_bvalid,
  output m00_axi_bready,
  output m00_axi_arvalid,
  input m00_axi_arready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m00_axi_araddr,
  output [8-1:0] m00_axi_arlen,
  input m00_axi_rvalid,
  output m00_axi_rready,
  input [C_M_AXI_DATA_WIDTH-1:0] m00_axi_rdata,
  input m00_axi_rlast,
  output m01_axi_awvalid,
  input m01_axi_awready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m01_axi_awaddr,
  output [8-1:0] m01_axi_awlen,
  output m01_axi_wvalid,
  input m01_axi_wready,
  output [C_M_AXI_DATA_WIDTH-1:0] m01_axi_wdata,
  output [C_M_AXI_DATA_WIDTH/8-1:0] m01_axi_wstrb,
  output m01_axi_wlast,
  input m01_axi_bvalid,
  output m01_axi_bready,
  output m01_axi_arvalid,
  input m01_axi_arready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m01_axi_araddr,
  output [8-1:0] m01_axi_arlen,
  input m01_axi_rvalid,
  output m01_axi_rready,
  input [C_M_AXI_DATA_WIDTH-1:0] m01_axi_rdata,
  input m01_axi_rlast,
  input ap_start,
  output ap_idle,
  output ap_done,
  output ap_ready,
  input [32-1:0] in_s0,
  input [32-1:0] in_s1,
  input [32-1:0] out_s0,
  input [32-1:0] out_s1,
  input [64-1:0] in0,
  input [64-1:0] out0,
  input [64-1:0] in1,
  input [64-1:0] out1
);

  localparam LP_NUM_EXAMPLES = 2;
  localparam LP_LENGTH_WIDTH = 32;
  localparam LP_DW_BYTES = C_M_AXI_DATA_WIDTH / 8;
  localparam LP_AXI_BURST_LEN = (4096 / LP_DW_BYTES < 256)? 4096 / LP_DW_BYTES : 256;
  localparam LP_LOG_BURST_LEN = $clog2(LP_AXI_BURST_LEN);
  localparam LP_BRAM_DEPTH = 512;
  localparam LP_RD_MAX_OUTSTANDING = LP_BRAM_DEPTH / LP_AXI_BURST_LEN;
  localparam LP_WR_MAX_OUTSTANDING = 32;
  (* KEEP = "yes" *)
  reg reset;
  reg ap_idle_r;
  reg ap_done_r;
  wire [LP_NUM_EXAMPLES-1:0] rd_ctrl_done;
  wire [LP_NUM_EXAMPLES-1:0] wr_ctrl_done;
  reg [LP_NUM_EXAMPLES-1:0] acc_user_done_rd_data;
  reg [LP_NUM_EXAMPLES-1:0] acc_user_done_wr_data;
  wire [LP_NUM_EXAMPLES-1:0] acc_user_request_read;
  wire [LP_NUM_EXAMPLES-1:0] acc_user_read_data_valid;
  wire [C_M_AXI_DATA_WIDTH*LP_NUM_EXAMPLES-1:0] acc_user_read_data;
  wire [LP_NUM_EXAMPLES-1:0] acc_user_available_write;
  wire [LP_NUM_EXAMPLES-1:0] acc_user_request_write;
  wire [C_M_AXI_DATA_WIDTH*LP_NUM_EXAMPLES-1:0] acc_user_write_data;
  wire acc_user_done;
  wire rd_tvalid0;
  wire rd_tready0;
  wire rd_tlast0;
  wire [C_M_AXI_DATA_WIDTH-1:0] rd_tdata0;
  wire rd_tvalid1;
  wire rd_tready1;
  wire rd_tlast1;
  wire [C_M_AXI_DATA_WIDTH-1:0] rd_tdata1;
  wire wr_tvalid0;
  wire wr_tready0;
  wire [C_M_AXI_DATA_WIDTH-1:0] wr_tdata0;
  wire wr_tvalid1;
  wire wr_tready1;
  wire [C_M_AXI_DATA_WIDTH-1:0] wr_tdata1;
  reg [2-1:0] fsm_reset;
  reg areset;
  reg ap_start_pulse;
  localparam FSM_STATE_START = 2'b0;
  localparam FSM_STATE_RESET = 2'b1;
  localparam FSM_STATE_RUNNING = 2'b10;

  always @(posedge ap_clk) begin
    reset <= ~ap_rst_n;
  end


  always @(posedge ap_clk) begin
    if(reset) begin
      areset <= 1'b0;
      fsm_reset <= FSM_STATE_START;
      ap_start_pulse <= 1'b0;
    end else begin
      areset <= 1'b0;
      ap_start_pulse <= 1'b0;
      case(fsm_reset)
        FSM_STATE_START: begin
          if(ap_start) begin
            areset <= 1'b1;
            fsm_reset <= FSM_STATE_RESET;
          end 
        end
        FSM_STATE_RESET: begin
          ap_start_pulse <= 1'b1;
          fsm_reset <= FSM_STATE_RUNNING;
        end
        FSM_STATE_RUNNING: begin
          if(~ap_start) begin
            fsm_reset <= FSM_STATE_START;
          end 
        end
      endcase
    end
  end


  always @(posedge ap_clk) begin
    if(areset) begin
      ap_idle_r <= 1'b1;
    end else begin
      ap_idle_r <= (ap_done)? 1'b1 : 
                   (ap_start_pulse)? 1'b0 : ap_idle;
    end
  end

  assign ap_idle = ap_idle_r;

  always @(posedge ap_clk) begin
    if(areset) begin
      ap_done_r <= 1'b0;
    end else begin
      ap_done_r <= (ap_done)? 1'b0 : ap_done_r | acc_user_done;
    end
  end

  assign ap_done = ap_done_r;
  assign ap_ready = ap_done;
  integer i;

  always @(posedge ap_clk) begin
    if(areset) begin
      acc_user_done_rd_data <= { LP_NUM_EXAMPLES{ 1'b0 } };
      acc_user_done_wr_data <= { LP_NUM_EXAMPLES{ 1'b0 } };
    end else begin
      for(i=0; i<LP_NUM_EXAMPLES; i=i+1) begin
        acc_user_done_rd_data[i] <= (rd_ctrl_done[i])? 1'b1 : acc_user_done_rd_data[i];
        acc_user_done_wr_data[i] <= (wr_ctrl_done[i])? 1'b1 : acc_user_done_wr_data[i];
      end
    end
  end

  assign rd_tready0 = acc_user_request_read[0];
  assign rd_tready1 = acc_user_request_read[1];
  assign acc_user_read_data_valid = {rd_tvalid1,rd_tvalid0};
  assign acc_user_read_data = {rd_tdata1,rd_tdata0};

  assign acc_user_available_write = {wr_tready1,wr_tready0};
  assign wr_tvalid0 = acc_user_request_write[0];
  assign wr_tdata0 = acc_user_write_data[1*C_M_AXI_DATA_WIDTH-1:0*C_M_AXI_DATA_WIDTH];
  assign wr_tvalid1 = acc_user_request_write[1];
  assign wr_tdata1 = acc_user_write_data[2*C_M_AXI_DATA_WIDTH-1:1*C_M_AXI_DATA_WIDTH];

  axi_reader_wrapper
  #(
    .C_M_AXI_ADDR_WIDTH(C_M_AXI_ADDR_WIDTH),
    .C_M_AXI_DATA_WIDTH(C_M_AXI_DATA_WIDTH),
    .C_XFER_SIZE_WIDTH(32),
    .C_MAX_OUTSTANDING(LP_RD_MAX_OUTSTANDING),
    .C_INCLUDE_DATA_FIFO(1)
  )
  axi_reader_0
  (
    .aclk(ap_clk),
    .areset(areset),
    .ctrl_start(ap_start_pulse),
    .ctrl_done(rd_ctrl_done[0]),
    .ctrl_addr_offset(in0),
    .ctrl_xfer_size_in_bytes(in_s0),
    .m_axi_arvalid(m00_axi_arvalid),
    .m_axi_arready(m00_axi_arready),
    .m_axi_araddr(m00_axi_araddr),
    .m_axi_arlen(m00_axi_arlen),
    .m_axi_rvalid(m00_axi_rvalid),
    .m_axi_rready(m00_axi_rready),
    .m_axi_rdata(m00_axi_rdata),
    .m_axi_rlast(m00_axi_rlast),
    .m_axis_aclk(ap_clk),
    .m_axis_areset(areset),
    .m_axis_tvalid(rd_tvalid0),
    .m_axis_tready(rd_tready0),
    .m_axis_tlast(rd_tlast0),
    .m_axis_tdata(rd_tdata0)
  );


  axi_reader_wrapper
  #(
    .C_M_AXI_ADDR_WIDTH(C_M_AXI_ADDR_WIDTH),
    .C_M_AXI_DATA_WIDTH(C_M_AXI_DATA_WIDTH),
    .C_XFER_SIZE_WIDTH(32),
    .C_MAX_OUTSTANDING(LP_RD_MAX_OUTSTANDING),
    .C_INCLUDE_DATA_FIFO(1)
  )
  axi_reader_1
  (
    .aclk(ap_clk),
    .areset(areset),
    .ctrl_start(ap_start_pulse),
    .ctrl_done(rd_ctrl_done[1]),
    .ctrl_addr_offset(in1),
    .ctrl_xfer_size_in_bytes(in_s1),
    .m_axi_arvalid(m01_axi_arvalid),
    .m_axi_arready(m01_axi_arready),
    .m_axi_araddr(m01_axi_araddr),
    .m_axi_arlen(m01_axi_arlen),
    .m_axi_rvalid(m01_axi_rvalid),
    .m_axi_rready(m01_axi_rready),
    .m_axi_rdata(m01_axi_rdata),
    .m_axi_rlast(m01_axi_rlast),
    .m_axis_aclk(ap_clk),
    .m_axis_areset(areset),
    .m_axis_tvalid(rd_tvalid1),
    .m_axis_tready(rd_tready1),
    .m_axis_tlast(rd_tlast1),
    .m_axis_tdata(rd_tdata1)
  );


  axi_writer_wrapper
  #(
    .C_M_AXI_ADDR_WIDTH(C_M_AXI_ADDR_WIDTH),
    .C_M_AXI_DATA_WIDTH(C_M_AXI_DATA_WIDTH),
    .C_XFER_SIZE_WIDTH(32),
    .C_MAX_OUTSTANDING(LP_WR_MAX_OUTSTANDING),
    .C_INCLUDE_DATA_FIFO(1)
  )
  axi_writer_0
  (
    .aclk(ap_clk),
    .areset(areset),
    .ctrl_start(ap_start_pulse),
    .ctrl_done(wr_ctrl_done[0]),
    .ctrl_addr_offset(out0),
    .ctrl_xfer_size_in_bytes(out_s0),
    .m_axi_awvalid(m00_axi_awvalid),
    .m_axi_awready(m00_axi_awready),
    .m_axi_awaddr(m00_axi_awaddr),
    .m_axi_awlen(m00_axi_awlen),
    .m_axi_wvalid(m00_axi_wvalid),
    .m_axi_wready(m00_axi_wready),
    .m_axi_wdata(m00_axi_wdata),
    .m_axi_wstrb(m00_axi_wstrb),
    .m_axi_wlast(m00_axi_wlast),
    .m_axi_bvalid(m00_axi_bvalid),
    .m_axi_bready(m00_axi_bready),
    .s_axis_aclk(ap_clk),
    .s_axis_areset(areset),
    .s_axis_tvalid(wr_tvalid0),
    .s_axis_tready(wr_tready0),
    .s_axis_tdata(wr_tdata0)
  );


  axi_writer_wrapper
  #(
    .C_M_AXI_ADDR_WIDTH(C_M_AXI_ADDR_WIDTH),
    .C_M_AXI_DATA_WIDTH(C_M_AXI_DATA_WIDTH),
    .C_XFER_SIZE_WIDTH(32),
    .C_MAX_OUTSTANDING(LP_WR_MAX_OUTSTANDING),
    .C_INCLUDE_DATA_FIFO(1)
  )
  axi_writer_1
  (
    .aclk(ap_clk),
    .areset(areset),
    .ctrl_start(ap_start_pulse),
    .ctrl_done(wr_ctrl_done[1]),
    .ctrl_addr_offset(out1),
    .ctrl_xfer_size_in_bytes(out_s1),
    .m_axi_awvalid(m01_axi_awvalid),
    .m_axi_awready(m01_axi_awready),
    .m_axi_awaddr(m01_axi_awaddr),
    .m_axi_awlen(m01_axi_awlen),
    .m_axi_wvalid(m01_axi_wvalid),
    .m_axi_wready(m01_axi_wready),
    .m_axi_wdata(m01_axi_wdata),
    .m_axi_wstrb(m01_axi_wstrb),
    .m_axi_wlast(m01_axi_wlast),
    .m_axi_bvalid(m01_axi_bvalid),
    .m_axi_bready(m01_axi_bready),
    .s_axis_aclk(ap_clk),
    .s_axis_areset(areset),
    .s_axis_tvalid(wr_tvalid1),
    .s_axis_tready(wr_tready1),
    .s_axis_tdata(wr_tdata1)
  );


  cgra_acc
  #(
    .INTERFACE_DATA_WIDTH(C_M_AXI_DATA_WIDTH)
  )
  cgra_acc
  (
    .clk(ap_clk),
    .rst(areset),
    .start(ap_start_pulse),
    .acc_user_done_rd_data(acc_user_done_rd_data),
    .acc_user_done_wr_data(acc_user_done_wr_data),
    .acc_user_request_read(acc_user_request_read),
    .acc_user_read_data_valid(acc_user_read_data_valid),
    .acc_user_read_data(acc_user_read_data),
    .acc_user_available_write(acc_user_available_write),
    .acc_user_request_write(acc_user_request_write),
    .acc_user_write_data(acc_user_write_data),
    .acc_user_done(acc_user_done)
  );


  initial begin
    reset = 1'b1;
    ap_idle_r = 1'b1;
    ap_done_r = 0;
    acc_user_done_rd_data = 0;
    acc_user_done_wr_data = 0;
    fsm_reset = FSM_STATE_START;
    areset = 1'b1;
    ap_start_pulse = 0;
  end


endmodule



module axi_reader_wrapper #
(
  parameter C_M_AXI_ADDR_WIDTH = 64,
  parameter C_M_AXI_DATA_WIDTH = 512,
  parameter C_XFER_SIZE_WIDTH = 64,
  parameter C_MAX_OUTSTANDING = 16,
  parameter C_INCLUDE_DATA_FIFO = 1
)
(
  input aclk,
  input areset,
  input ctrl_start,
  output ctrl_done,
  input [C_M_AXI_ADDR_WIDTH-1:0] ctrl_addr_offset,
  input [C_XFER_SIZE_WIDTH-1:0] ctrl_xfer_size_in_bytes,
  output m_axi_arvalid,
  input m_axi_arready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m_axi_araddr,
  output [8-1:0] m_axi_arlen,
  input m_axi_rvalid,
  output m_axi_rready,
  input [C_M_AXI_DATA_WIDTH-1:0] m_axi_rdata,
  input m_axi_rlast,
  input m_axis_aclk,
  input m_axis_areset,
  output m_axis_tvalid,
  input m_axis_tready,
  output [C_M_AXI_DATA_WIDTH-1:0] m_axis_tdata,
  output m_axis_tlast
);

  axi_reader #(
            .C_M_AXI_ADDR_WIDTH  ( C_M_AXI_ADDR_WIDTH  ) ,
            .C_M_AXI_DATA_WIDTH  ( C_M_AXI_DATA_WIDTH  ) ,
            .C_XFER_SIZE_WIDTH   ( C_XFER_SIZE_WIDTH   ) ,
            .C_MAX_OUTSTANDING   ( C_MAX_OUTSTANDING   ) ,
            .C_INCLUDE_DATA_FIFO ( C_INCLUDE_DATA_FIFO )
          )
          inst_axi_reader (
            .aclk                    ( aclk                   ) ,
            .areset                  ( areset                 ) ,
            .ctrl_start              ( ctrl_start             ) ,
            .ctrl_done               ( ctrl_done              ) ,
            .ctrl_addr_offset        ( ctrl_addr_offset       ) ,
            .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes) ,
            .m_axi_arvalid           ( m_axi_arvalid          ) ,
            .m_axi_arready           ( m_axi_arready          ) ,
            .m_axi_araddr            ( m_axi_araddr           ) ,
            .m_axi_arlen             ( m_axi_arlen            ) ,
            .m_axi_rvalid            ( m_axi_rvalid           ) ,
            .m_axi_rready            ( m_axi_rready           ) ,
            .m_axi_rdata             ( m_axi_rdata            ) ,
            .m_axi_rlast             ( m_axi_rlast            ) ,
            .m_axis_aclk             ( m_axis_aclk            ) ,
            .m_axis_areset           ( m_axis_areset          ) ,
            .m_axis_tvalid           ( m_axis_tvalid          ) ,
            .m_axis_tready           ( m_axis_tready          ) ,
            .m_axis_tlast            ( m_axis_tlast           ) ,
            .m_axis_tdata            ( m_axis_tdata           )
          );

endmodule



module axi_writer_wrapper #
(
  parameter C_M_AXI_ADDR_WIDTH = 64,
  parameter C_M_AXI_DATA_WIDTH = 512,
  parameter C_XFER_SIZE_WIDTH = 64,
  parameter C_MAX_OUTSTANDING = 32,
  parameter C_INCLUDE_DATA_FIFO = 1
)
(
  input aclk,
  input areset,
  input ctrl_start,
  output ctrl_done,
  input [C_M_AXI_ADDR_WIDTH-1:0] ctrl_addr_offset,
  input [C_XFER_SIZE_WIDTH-1:0] ctrl_xfer_size_in_bytes,
  output m_axi_awvalid,
  input m_axi_awready,
  output [C_M_AXI_ADDR_WIDTH-1:0] m_axi_awaddr,
  output [8-1:0] m_axi_awlen,
  output m_axi_wvalid,
  input m_axi_wready,
  output [C_M_AXI_DATA_WIDTH-1:0] m_axi_wdata,
  output [C_M_AXI_DATA_WIDTH/8-1:0] m_axi_wstrb,
  output m_axi_wlast,
  input m_axi_bvalid,
  output m_axi_bready,
  input s_axis_aclk,
  input s_axis_areset,
  input s_axis_tvalid,
  output s_axis_tready,
  input [C_M_AXI_DATA_WIDTH-1:0] s_axis_tdata
);

  axi_writer #(
            .C_M_AXI_ADDR_WIDTH  ( C_M_AXI_ADDR_WIDTH ) ,
            .C_M_AXI_DATA_WIDTH  ( C_M_AXI_DATA_WIDTH ) ,
            .C_XFER_SIZE_WIDTH   ( C_XFER_SIZE_WIDTH  ) ,
            .C_MAX_OUTSTANDING   ( C_MAX_OUTSTANDING  ) ,
            .C_INCLUDE_DATA_FIFO ( C_INCLUDE_DATA_FIFO)
          )
          inst_axi_writer (
            .aclk                    ( aclk                   ) ,
            .areset                  ( areset                 ) ,
            .ctrl_start              ( ctrl_start             ) ,
            .ctrl_done               ( ctrl_done              ) ,
            .ctrl_addr_offset        ( ctrl_addr_offset       ) ,
            .ctrl_xfer_size_in_bytes ( ctrl_xfer_size_in_bytes) ,
            .m_axi_awvalid           ( m_axi_awvalid) ,
            .m_axi_awready           ( m_axi_awready) ,
            .m_axi_awaddr            ( m_axi_awaddr ) ,
            .m_axi_awlen             ( m_axi_awlen  ) ,
            .m_axi_wvalid            ( m_axi_wvalid ) ,
            .m_axi_wready            ( m_axi_wready ) ,
            .m_axi_wdata             ( m_axi_wdata  ) ,
            .m_axi_wstrb             ( m_axi_wstrb  ) ,
            .m_axi_wlast             ( m_axi_wlast  ) ,
            .m_axi_bvalid            ( m_axi_bvalid ) ,
            .m_axi_bready            ( m_axi_bready ) ,
            .s_axis_aclk             ( s_axis_aclk  ) ,
            .s_axis_areset           ( s_axis_areset) ,
            .s_axis_tvalid           (s_axis_tvalid ) ,
            .s_axis_tready           (s_axis_tready ) ,
            .s_axis_tdata            (s_axis_tdata  )
          );

endmodule



module cgra_acc #
(
  parameter INTERFACE_DATA_WIDTH = 512
)
(
  input clk,
  input rst,
  input start,
  input [2-1:0] acc_user_done_rd_data,
  input [2-1:0] acc_user_done_wr_data,
  output [2-1:0] acc_user_request_read,
  input [2-1:0] acc_user_read_data_valid,
  input [INTERFACE_DATA_WIDTH*2-1:0] acc_user_read_data,
  input [2-1:0] acc_user_available_write,
  output [2-1:0] acc_user_request_write,
  output [INTERFACE_DATA_WIDTH*2-1:0] acc_user_write_data,
  output acc_user_done
);

  wire [2-1:0] request_read;
  wire conf_control_req_rd_data;
  wire en;
  wire [2-1:0] en_pop;
  wire [32-1:0] fifo_in_data;
  wire [2-1:0] available_pop;
  wire [2-1:0] en_push;
  wire [32-1:0] fifo_out_data;
  wire [2-1:0] available_push;
  wire [8-1:0] conf_out_bus;
  wire [2-1:0] read_fifo_mask;
  wire [2-1:0] write_fifo_mask;
  wire [32-1:0] write_fifo_ignore;
  wire [32-1:0] write_fifo_loop_ignore;
  wire conf_done;
  genvar genv;
  assign acc_user_request_read[1:1] = request_read[1:1];
  assign acc_user_request_read[0] = request_read[0] | conf_control_req_rd_data;

  generate for(genv=0; genv<2; genv=genv+1) begin : inst_fecth_data

    fecth_data
    #(
      .INPUT_DATA_WIDTH(INTERFACE_DATA_WIDTH),
      .OUTPUT_DATA_WIDTH(16)
    )
    fecth_data
    (
      .clk(clk),
      .rst(rst),
      .start(conf_done),
      .request_read(request_read[genv]),
      .data_valid(acc_user_read_data_valid[genv]),
      .read_data(acc_user_read_data[(genv+1)*INTERFACE_DATA_WIDTH-1:genv*INTERFACE_DATA_WIDTH]),
      .pop_data(en_pop[genv]),
      .available_pop(available_pop[genv]),
      .data_out(fifo_in_data[(genv+1)*16-1:genv*16])
    );

  end
  endgenerate


  generate for(genv=0; genv<2; genv=genv+1) begin : inst_dispath_data

    dispath_data
    #(
      .INPUT_DATA_WIDTH(16),
      .OUTPUT_DATA_WIDTH(INTERFACE_DATA_WIDTH)
    )
    dispath_data
    (
      .clk(clk),
      .rst(rst),
      .available_write(acc_user_available_write[genv]),
      .request_write(acc_user_request_write[genv]),
      .write_data(acc_user_write_data[(genv+1)*INTERFACE_DATA_WIDTH-1:genv*INTERFACE_DATA_WIDTH]),
      .push_data(en_push[genv]),
      .available_push(available_push[genv]),
      .data_in(fifo_out_data[(genv+1)*16-1:genv*16])
    );

  end
  endgenerate


  cgra0_control_conf
  control_conf
  (
    .clk(clk),
    .rst(rst),
    .start(start),
    .req_rd_data(conf_control_req_rd_data),
    .rd_data(acc_user_read_data[INTERFACE_DATA_WIDTH-1:0]),
    .rd_data_valid(acc_user_read_data_valid[0]),
    .conf_out_bus(conf_out_bus),
    .read_fifo_mask(read_fifo_mask),
    .write_fifo_mask(write_fifo_mask),
    .write_fifo_ignore(write_fifo_ignore),
    .write_fifo_loop_ignore(write_fifo_loop_ignore),
    .done(conf_done)
  );


  cgra0_control_exec
  control_exec
  (
    .clk(clk),
    .rst(rst),
    .start(conf_done),
    .read_fifo_mask(read_fifo_mask),
    .write_fifo_mask(write_fifo_mask),
    .write_fifo_ignore(write_fifo_ignore),
    .write_fifo_loop_ignore(write_fifo_loop_ignore),
    .available_pop(available_pop),
    .available_push(available_push),
    .read_fifo_done(acc_user_done_rd_data),
    .write_fifo_done(acc_user_done_wr_data),
    .en(en),
    .en_pop(en_pop),
    .en_push(en_push),
    .done(acc_user_done)
  );


  cgra
  cgra
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_out_bus),
    .in_stream0(fifo_in_data[15:0]),
    .in_stream2(fifo_in_data[31:16]),
    .out_stream1(fifo_out_data[15:0]),
    .out_stream3(fifo_out_data[31:16])
  );


endmodule



module fecth_data #
(
  parameter INPUT_DATA_WIDTH = 512,
  parameter OUTPUT_DATA_WIDTH = 16
)
(
  input clk,
  input start,
  input rst,
  output reg request_read,
  input data_valid,
  input [INPUT_DATA_WIDTH-1:0] read_data,
  input pop_data,
  output reg available_pop,
  output [OUTPUT_DATA_WIDTH-1:0] data_out
);

  localparam NUM = INPUT_DATA_WIDTH / OUTPUT_DATA_WIDTH;
  reg [2-1:0] fsm_read;
  reg [2-1:0] fsm_control;
  reg [INPUT_DATA_WIDTH-1:0] data;
  reg [INPUT_DATA_WIDTH-1:0] buffer;
  reg [NUM-1:0] count;
  reg has_buffer;
  reg buffer_read;
  reg en;

  assign data_out = data[OUTPUT_DATA_WIDTH-1:0];

  always @(posedge clk) begin
    if(rst) begin
      en <= 1'b0;
    end else begin
      en <= (en)? en : start;
    end
  end


  always @(posedge clk) begin
    if(rst) begin
      fsm_read <= 0;
      request_read <= 0;
      has_buffer <= 0;
    end else begin
      request_read <= 0;
      case(fsm_read)
        0: begin
          if(en & data_valid) begin
            buffer <= read_data;
            request_read <= 1;
            has_buffer <= 1;
            fsm_read <= 1;
          end 
        end
        1: begin
          if(buffer_read) begin
            has_buffer <= 0;
            fsm_read <= 0;
          end 
        end
      endcase
    end
  end


  always @(posedge clk) begin
    if(rst) begin
      fsm_control <= 0;
      available_pop <= 0;
      count <= 0;
      buffer_read <= 0;
    end else begin
      buffer_read <= 0;
      case(fsm_control)
        0: begin
          if(has_buffer) begin
            data <= buffer;
            count <= 1;
            buffer_read <= 1;
            available_pop <= 1;
            fsm_control <= 1;
          end 
        end
        1: begin
          if(pop_data & ~count[NUM - 1]) begin
            count <= count << 1;
            data <= data[511:OUTPUT_DATA_WIDTH];
          end 
          if(pop_data & count[NUM - 1] & has_buffer) begin
            count <= 1;
            data <= buffer;
            buffer_read <= 1;
          end 
          if(count[NUM - 1] & pop_data & ~has_buffer) begin
            count <= count << 1;
            data <= data[511:OUTPUT_DATA_WIDTH];
            available_pop <= 0;
            fsm_control <= 0;
          end 
        end
      endcase
    end
  end


  initial begin
    request_read = 0;
    available_pop = 0;
    fsm_read = 0;
    fsm_control = 0;
    data = 0;
    buffer = 0;
    count = 0;
    has_buffer = 0;
    buffer_read = 0;
    en = 0;
  end


endmodule



module dispath_data #
(
  parameter INPUT_DATA_WIDTH = 16,
  parameter OUTPUT_DATA_WIDTH = 512
)
(
  input clk,
  input rst,
  input available_write,
  output reg request_write,
  output reg [OUTPUT_DATA_WIDTH-1:0] write_data,
  input push_data,
  output reg available_push,
  input [INPUT_DATA_WIDTH-1:0] data_in
);

  localparam NUM = OUTPUT_DATA_WIDTH / INPUT_DATA_WIDTH;

  reg [2-1:0] fsm_control;
  reg [OUTPUT_DATA_WIDTH-1:0] buffer1;
  reg [OUTPUT_DATA_WIDTH-1:0] buffer2;
  reg [NUM-1:0] count1;
  reg [NUM-1:0] count2;
  reg request_write1;
  reg request_write2;
  reg request_write11;
  reg request_write22;

  always @(posedge clk) begin
    if(rst) begin
      request_write <= 0;
      request_write11 <= 0;
      request_write22 <= 0;
    end else begin
      request_write11 <= request_write1;
      request_write22 <= request_write2;
      request_write <= request_write11 | request_write22;
      if(request_write11) begin
        write_data <= buffer1;
      end else if(request_write22) begin
        write_data <= buffer2;
      end 
    end
  end


  always @(posedge clk) begin
    if(rst) begin
      available_push <= 1;
      fsm_control <= 0;
      count1 <= 1;
      count2 <= 1;
      request_write1 <= 0;
      request_write2 <= 0;
    end else begin
      request_write1 <= 0;
      request_write2 <= 0;
      case(fsm_control)
        0: begin
          if(push_data) begin
            buffer1 <= { data_in, { OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH{ 1'b0 } } } | (buffer1 >> INPUT_DATA_WIDTH);
            count1 <= count1 << 1;
          end 
          if(count1[NUM - 1] & push_data) begin
            fsm_control <= 1;
          end 
        end
        1: begin
          if(available_write) begin
            count1 <= 1;
            request_write1 <= 1;
            available_push <= 1;
          end 
          if(available_write & available_push) begin
            fsm_control <= 2;
          end 
          if(available_write & ~available_push) begin
            fsm_control <= 3;
          end 
          if(push_data) begin
            buffer2 <= { data_in, { OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH{ 1'b0 } } } | (buffer2 >> INPUT_DATA_WIDTH);
            count2 <= count2 << 1;
          end 
          if(count2[NUM - 2] & push_data & ~available_write) begin
            available_push <= 0;
          end 
        end
        2: begin
          if(push_data) begin
            buffer2 <= { data_in, { OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH{ 1'b0 } } } | (buffer2 >> INPUT_DATA_WIDTH);
            count2 <= count2 << 1;
          end 
          if(count2[NUM - 1] & push_data) begin
            fsm_control <= 3;
          end 
        end
        3: begin
          if(available_write) begin
            request_write2 <= 1;
            available_push <= 1;
            count2 <= 1;
          end 
          if(available_write & available_push) begin
            fsm_control <= 0;
          end 
          if(available_write & ~available_push) begin
            fsm_control <= 1;
          end 
          if(push_data) begin
            buffer1 <= { data_in, { OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH{ 1'b0 } } } | (buffer1 >> INPUT_DATA_WIDTH);
            count1 <= count1 << 1;
          end 
          if(count1[NUM - 2] & push_data & ~available_write) begin
            available_push <= 0;
          end 
        end
      endcase
    end
  end


  initial begin
    request_write = 0;
    write_data = 0;
    available_push = 0;
    fsm_control = 0;
    buffer1 = 0;
    buffer2 = 0;
    count1 = 0;
    count2 = 0;
    request_write1 = 0;
    request_write2 = 0;
    request_write11 = 0;
    request_write22 = 0;
  end


endmodule



module cgra0_control_conf #
(
  parameter CONF_DATA_IN_WIDTH = 512,
  parameter CONF_DATA_OUT_WIDTH = 8
)
(
  input clk,
  input rst,
  input start,
  output req_rd_data,
  input [CONF_DATA_IN_WIDTH-1:0] rd_data,
  input rd_data_valid,
  output reg [CONF_DATA_OUT_WIDTH-1:0] conf_out_bus,
  output reg [2-1:0] read_fifo_mask,
  output reg [2-1:0] write_fifo_mask,
  output reg [32-1:0] write_fifo_ignore,
  output reg [32-1:0] write_fifo_loop_ignore,
  output reg done
);

  localparam CONF_SIZE = CONF_DATA_IN_WIDTH / CONF_DATA_OUT_WIDTH;
  localparam FSM_INIT_CTRL_IDLE = 0;
  localparam FSM_INIT_CTRL_INIT = 1;
  localparam FSM_INIT_CTRL_INIT2 = 2;
  localparam FSM_INIT_CTRL_INIT3 = 3;
  localparam FSM_SEND_INIT_CONF_PE = 4;
  localparam FSM_INIT_CTRL_REQ_DATA = 5;
  localparam FSM_WAIT_ALL_CONF_FINISH = 6;
  localparam FSM_INIT_CONF_DONE = 7;

  reg [4-1:0] fsm_conf_ctrl;
  reg [4-1:0] fsm_conf_ctrl_next;
  reg conf_req_data;
  reg [CONF_DATA_IN_WIDTH-1:0] conf_cl;
  reg [32-1:0] qtd_conf;
  reg [CONF_DATA_OUT_WIDTH-1:0] conf_data;
  reg send_conf;
  reg [32-1:0] conf_counter;
  reg [10-1:0] conf_counter_cl;
  reg [3-1:0] wait_counter;

  assign req_rd_data = conf_req_data;

  always @(posedge clk) begin
    if(rst) begin
      fsm_conf_ctrl <= FSM_INIT_CTRL_IDLE;
      fsm_conf_ctrl_next <= FSM_INIT_CTRL_IDLE;
      conf_req_data <= 0;
      send_conf <= 0;
      conf_counter <= 0;
      conf_counter_cl <= CONF_SIZE;
      done <= 0;
      read_fifo_mask <= 0;
      write_fifo_mask <= 0;
      wait_counter <= 0;
    end else begin
      conf_req_data <= 0;
      send_conf <= 0;
      done <= 0;
      case(fsm_conf_ctrl)
        FSM_INIT_CTRL_IDLE: begin
          if(start) begin
            fsm_conf_ctrl <= FSM_INIT_CTRL_REQ_DATA;
            fsm_conf_ctrl_next <= FSM_INIT_CTRL_INIT;
          end 
        end
        FSM_INIT_CTRL_INIT: begin
          qtd_conf <= conf_cl[17:0];
          read_fifo_mask <= conf_cl[33:32];
          write_fifo_mask <= conf_cl[97:96];
          fsm_conf_ctrl <= FSM_INIT_CTRL_REQ_DATA;
          fsm_conf_ctrl_next <= FSM_INIT_CTRL_INIT2;
        end
        FSM_INIT_CTRL_INIT2: begin
          write_fifo_ignore <= conf_cl[31:0];
          fsm_conf_ctrl <= FSM_INIT_CTRL_REQ_DATA;
          fsm_conf_ctrl_next <= FSM_INIT_CTRL_INIT3;
        end
        FSM_INIT_CTRL_INIT3: begin
          write_fifo_loop_ignore <= conf_cl[31:0];
          fsm_conf_ctrl <= FSM_SEND_INIT_CONF_PE;
        end
        FSM_SEND_INIT_CONF_PE: begin
          if(conf_counter >= qtd_conf) begin
            fsm_conf_ctrl <= FSM_WAIT_ALL_CONF_FINISH;
          end else if(conf_counter_cl < CONF_SIZE) begin
            conf_data <= conf_cl[CONF_DATA_OUT_WIDTH-1:0];
            conf_cl <= conf_cl[CONF_DATA_IN_WIDTH-1:CONF_DATA_OUT_WIDTH];
            send_conf <= 1;
            conf_counter <= conf_counter + 1;
            conf_counter_cl <= conf_counter_cl + 1;
          end else begin
            conf_counter_cl <= 10'd0;
            fsm_conf_ctrl <= FSM_INIT_CTRL_REQ_DATA;
            fsm_conf_ctrl_next <= FSM_SEND_INIT_CONF_PE;
          end
        end
        FSM_INIT_CTRL_REQ_DATA: begin
          if(rd_data_valid) begin
            conf_cl <= rd_data;
            conf_req_data <= 1;
            fsm_conf_ctrl <= fsm_conf_ctrl_next;
          end 
        end
        FSM_WAIT_ALL_CONF_FINISH: begin
          wait_counter <= wait_counter + 1;
          if(wait_counter > 4) begin
            fsm_conf_ctrl <= FSM_INIT_CONF_DONE;
            done <= 1;
          end 
        end
        FSM_INIT_CONF_DONE: begin
          if(~start) begin
            fsm_conf_ctrl <= FSM_INIT_CTRL_IDLE;
          end 
        end
      endcase
    end
  end


  always @(posedge clk) begin
    if(rst) begin
      conf_out_bus <= 0;
    end else begin
      if(send_conf) begin
        conf_out_bus <= conf_data;
      end else begin
        conf_out_bus <= 0;
      end
    end
  end


  initial begin
    conf_out_bus = 0;
    read_fifo_mask = 0;
    write_fifo_mask = 0;
    write_fifo_ignore = 0;
    write_fifo_loop_ignore = 0;
    done = 0;
    fsm_conf_ctrl = FSM_INIT_CTRL_IDLE;
    fsm_conf_ctrl_next = FSM_INIT_CTRL_IDLE;
    conf_req_data = 0;
    conf_cl = 0;
    qtd_conf = 0;
    conf_data = 0;
    send_conf = 0;
    conf_counter = 0;
    conf_counter_cl = CONF_SIZE;
    wait_counter = 0;
  end


endmodule



module cgra0_control_exec
(
  input clk,
  input rst,
  input start,
  input [2-1:0] read_fifo_mask,
  input [2-1:0] write_fifo_mask,
  input [32-1:0] write_fifo_ignore,
  input [32-1:0] write_fifo_loop_ignore,
  input [2-1:0] available_pop,
  input [2-1:0] available_push,
  input [2-1:0] read_fifo_done,
  input [2-1:0] write_fifo_done,
  output en,
  output [2-1:0] en_pop,
  output [2-1:0] en_push,
  output done
);

  localparam FSM_IDLE = 0;
  localparam FSM_PROCESS = 1;
  localparam FSM_DONE = 2;

  reg [2-1:0] fsm_state;
  reg [2-1:0] read_fifo_mask_r;
  reg [2-1:0] write_fifo_mask_r;
  reg [32-1:0] write_fifo_ignore_r;
  reg [32-1:0] write_fifo_loop_ignore_r;
  reg [2-1:0] available_pop_masked;
  reg [2-1:0] available_push_masked;
  reg [2-1:0] read_fifo_done_masked;
  reg [2-1:0] write_fifo_done_masked;
  reg en_r;
  reg [2-1:0] en_pop_r;
  reg [2-1:0] en_push_r;
  reg done_r;
  reg [2-1:0] read_fifo_done_r;
  reg [2-1:0] write_fifo_done_r;
  wire [2-1:0] ignore_counter_out;
  reg [2-1:0] en_counter;
  reg start_r;
  reg flag_initial;

  assign en = en_r;
  assign en_pop = en_pop_r;
  assign en_push = ignore_counter_out & en_push_r;
  assign done = done_r;

  always @(posedge clk) begin
    if(rst) begin
      start_r <= 1'b0;
    end else begin
      start_r <= (start_r)? start_r : start;
    end
  end


  always @(posedge clk) begin
    read_fifo_mask_r <= read_fifo_mask;
    write_fifo_mask_r <= write_fifo_mask;
    write_fifo_ignore_r <= write_fifo_ignore;
    write_fifo_loop_ignore_r <= write_fifo_loop_ignore;
    read_fifo_done_r <= read_fifo_done;
    write_fifo_done_r <= write_fifo_done;
  end


  always @(posedge clk) begin
    if(rst) begin
      available_pop_masked <= { 2{ 1'b0 } };
      available_push_masked <= { 2{ 1'b0 } };
      read_fifo_done_masked <= { 2{ 1'b0 } };
      write_fifo_done_masked <= { 2{ 1'b0 } };
    end else begin
      if(start_r) begin
        available_pop_masked <= available_pop | ~read_fifo_mask_r;
        available_push_masked <= available_push | ~write_fifo_mask_r;
        write_fifo_done_masked <= write_fifo_done_r | ~write_fifo_mask_r;
        read_fifo_done_masked <= read_fifo_done_r | ~read_fifo_mask_r;
      end else begin
        available_pop_masked <= { 2{ 1'b0 } };
        available_push_masked <= { 2{ 1'b0 } };
        read_fifo_done_masked <= { 2{ 1'b0 } };
        write_fifo_done_masked <= { 2{ 1'b0 } };
      end
    end
  end


  always @(posedge clk) begin
    if(rst) begin
      fsm_state <= FSM_IDLE;
      done_r <= 1'b0;
      en_r <= 1'b0;
      en_pop_r <= { 2{ 1'b0 } };
      en_push_r <= { 2{ 1'b0 } };
      en_counter <= { 2{ 1'b0 } };
      flag_initial <= 1'b0;
    end else begin
      en_r <= 1'b0;
      en_counter <= { 2{ 1'b0 } };
      en_pop_r <= { 2{ 1'b0 } };
      en_push_r <= { 2{ 1'b0 } };
      done_r <= 1'b0;
      case(fsm_state)
        FSM_IDLE: begin
          if(start) begin
            fsm_state <= FSM_PROCESS;
          end 
        end
        FSM_PROCESS: begin
          if(&available_push_masked && &available_pop_masked) begin
            en_r <= 1'b1;
            en_counter <= { 2{ 1'b1 } };
            en_pop_r <= { 2{ 1'b1 } };
            en_push_r <= { 2{ 1'b1 } };
            flag_initial <= 1'b1;
          end else if(&write_fifo_done_masked) begin
            fsm_state <= FSM_DONE;
            done_r <= 1'b1;
          end else if(&available_push_masked && flag_initial && &read_fifo_done_masked) begin
            en_r <= 1'b1;
            en_push_r <= { 2{ 1'b1 } };
            en_counter <= { 2{ 1'b1 } };
          end 
        end
        FSM_DONE: begin
          if(~start) begin
            fsm_state <= FSM_IDLE;
          end 
        end
      endcase
    end
  end

  genvar j;

  generate for(j=0; j<2; j=j+1) begin : genfor_ignore

    ignore_counter
    #(
      .width(16)
    )
    ignore_counter
    (
      .clk(clk),
      .rst(rst),
      .start(en_counter[j]),
      .limit(write_fifo_ignore[(j+1)*16-1:j*16]),
      .loop_limit(write_fifo_loop_ignore[(j+1)*16-1:j*16]),
      .out(ignore_counter_out[j])
    );

  end
  endgenerate


  initial begin
    fsm_state = FSM_IDLE;
    read_fifo_mask_r = 0;
    write_fifo_mask_r = 0;
    write_fifo_ignore_r = 0;
    write_fifo_loop_ignore_r = 0;
    available_pop_masked = 0;
    available_push_masked = 0;
    read_fifo_done_masked = 0;
    write_fifo_done_masked = 0;
    en_r = 0;
    en_pop_r = 0;
    en_push_r = 0;
    done_r = 0;
    read_fifo_done_r = 0;
    write_fifo_done_r = 0;
    en_counter = 0;
    start_r = 0;
    flag_initial = 0;
  end


endmodule



module ignore_counter #
(
  parameter width = 32
)
(
  input clk,
  input rst,
  input start,
  input [width-1:0] limit,
  input [width-1:0] loop_limit,
  output reg out
);

  reg [width-1:0] count;
  reg fsm;

  always @(posedge clk) begin
    if(rst) begin
      count <= 1;
      out <= 0;
      fsm <= 0;
    end else begin
      out <= 0;
      if(start) begin
        case(fsm)
          0: begin
            if(count == limit) begin
              out <= 1;
              count <= 1;
              fsm <= 1;
            end else begin
              count <= count + 1;
            end
          end
          1: begin
            if(count == loop_limit) begin
              out <= 1;
              count <= 1;
            end else begin
              count <= count + 1;
            end
          end
        endcase
      end 
    end
  end


  initial begin
    out = 0;
    count = 0;
    fsm = 0;
  end


endmodule



module cgra
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [16-1:0] in_stream0,
  input [16-1:0] in_stream2,
  output [16-1:0] out_stream1,
  output [16-1:0] out_stream3
);

  wire [16-1:0] pe0_to_pe1;
  wire [16-1:0] pe0_to_pe2;
  wire [16-1:0] pe1_to_pe0;
  wire [16-1:0] pe1_to_pe3;
  wire [16-1:0] pe2_to_pe0;
  wire [16-1:0] pe2_to_pe3;
  wire [16-1:0] pe3_to_pe1;
  wire [16-1:0] pe3_to_pe2;
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


  pe_input_2_0_4_acc_add_mul_sub
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


  pe_output_2_0_4_add_mul_sub
  #(
    .id(2)
  )
  pe_1
  (
    .clk(clk),
    .en(en),
    .conf_bus(conf_bus_reg_out[1]),
    .stream_out(out_stream1),
    .in0(pe0_to_pe1),
    .in1(pe3_to_pe1),
    .out0(pe1_to_pe0),
    .out1(pe1_to_pe3)
  );


  pe_input_2_0_4_add_mul_sub
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


  pe_output_2_0_4_add_mul_sub
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



module pe_input_2_0_4_acc_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [16-1:0] in0,
  input [16-1:0] in1,
  output [16-1:0] out0,
  output [16-1:0] out1,
  input [16-1:0] stream_in
);

  wire reset;
  wire [16-1:0] acc_wire;
  wire acc_rst;
  wire [16-1:0] conf_acc;
  wire [16-1:0] pe_const;
  wire [16-1:0] alu_in0;
  wire [16-1:0] alu_in1;
  wire [16-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [3-1:0] sel_mux_alu0;
  wire [3-1:0] sel_mux_alu1;

  multiplexer_5
  #(
    .width(16)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(stream_in),
    .in1(acc_wire),
    .in2(pe_const),
    .in3(in0),
    .in4(in1),
    .out(alu_in0)
  );

  wire [16-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(16)
  )
  elastic_pipeline0
  (
    .in(alu_in0),
    .out(elastic_pipeline_to_alu0),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline0)
  );


  multiplexer_5
  #(
    .width(16)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(stream_in),
    .in1(acc_wire),
    .in2(pe_const),
    .in3(in0),
    .in4(in1),
    .out(alu_in1)
  );

  wire [16-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(16)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_mul_sub
  #(
    .width(16)
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
    .num_register(1),
    .width(16)
  )
  acc_reg
  (
    .clk(clk),
    .rst(acc_rst),
    .en(en),
    .in(alu_out),
    .out(acc_wire)
  );


  acc_reset
  #(
    .width(16)
  )
  acc_reset_inst
  (
    .clk(clk),
    .rst(reset),
    .start(en),
    .limit(conf_acc),
    .out(acc_rst)
  );


  route_0_3x2
  #(
    .width(16)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1)
  );

  wire [14-1:0] conf_alu;

  pe_conf_reader_acc_alu_width_14_router_width_0
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
    .conf_acc(conf_acc)
  );

  assign sel_alu_opcode = conf_alu[1:0];
  assign sel_mux_alu0 = conf_alu[4:2];
  assign sel_mux_alu1 = conf_alu[7:5];
  assign sel_elastic_pipeline0 = conf_alu[10:8];
  assign sel_elastic_pipeline1 = conf_alu[13:11];

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



module alu_2_add_mul_sub #
(
  parameter width = 8
)
(
  input clk,
  input en,
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
      mul_temp <= in0_reg * in1_reg;
      reg_results[1] <= mul_temp;
    end 
    if(en) begin
      sub_temp <= in0_reg - in1_reg;
      reg_results[2] <= sub_temp;
    end 
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



module acc_reset #
(
  parameter width = 32
)
(
  input clk,
  input rst,
  input start,
  input [width-1:0] limit,
  output reg out
);

  reg [width-1:0] count;

  always @(posedge clk) begin
    if(rst) begin
      count <= 1;
      out <= 0;
    end else begin
      out <= 0;
      if(start) begin
        if(count == limit) begin
          out <= 1;
          count <= 1;
        end else begin
          count <= count + 1;
        end
      end 
    end
  end


  initial begin
    out = 0;
    count = 0;
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



module pe_conf_reader_acc_alu_width_14_router_width_0 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [14-1:0] conf_alu,
  output reg [16-1:0] conf_const,
  output reg [16-1:0] conf_acc
);

  reg [22-1:0] conf_reg;
  reg [22-1:0] conf_reg0;
  reg [22-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[14:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[14:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[14:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[14:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[2:0]) begin
        case(conf_reg[5:3])
          3'b1: begin
            conf_alu <= conf_reg[19:6];
          end
          3'b10: begin
            conf_const <= conf_reg[21:6];
          end
          3'b100: begin
            conf_acc <= conf_reg[21:6];
          end
          3'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
            conf_acc <= 0;
          end
        endcase
      end 
    end 
  end


  initial begin
    reset = 0;
    conf_alu = 0;
    conf_const = 0;
    conf_acc = 0;
    conf_reg = 0;
    conf_reg0 = 0;
    conf_reg1 = 0;
    flag = 0;
    conf_valid = 0;
  end


endmodule



module pe_output_2_0_4_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [16-1:0] in0,
  input [16-1:0] in1,
  output [16-1:0] out0,
  output [16-1:0] out1,
  output [16-1:0] stream_out
);

  wire reset;
  wire [16-1:0] pe_const;
  wire [16-1:0] alu_in0;
  wire [16-1:0] alu_in1;
  wire [16-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

  multiplexer_3
  #(
    .width(16)
  )
  mux_alu_in0
  (
    .sel(sel_mux_alu0),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in0)
  );

  wire [16-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(16)
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
    .width(16)
  )
  mux_alu_in1
  (
    .sel(sel_mux_alu1),
    .in0(pe_const),
    .in1(in0),
    .in2(in1),
    .out(alu_in1)
  );

  wire [16-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(16)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_mul_sub
  #(
    .width(16)
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


  route_0_3x3
  #(
    .width(16)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1),
    .out2(stream_out)
  );

  wire [12-1:0] conf_alu;

  pe_conf_reader_alu_width_12_router_width_0
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
  assign sel_elastic_pipeline0 = conf_alu[8:6];
  assign sel_elastic_pipeline1 = conf_alu[11:9];

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



module pe_conf_reader_alu_width_12_router_width_0 #
(
  parameter pe_id = 0,
  parameter conf_bus_width = 8
)
(
  input clk,
  input [conf_bus_width-1:0] conf_bus,
  output reg reset,
  output reg [12-1:0] conf_alu,
  output reg [16-1:0] conf_const
);

  reg [22-1:0] conf_reg;
  reg [22-1:0] conf_reg0;
  reg [22-1:0] conf_reg1;
  reg flag;
  reg conf_valid;

  always @(posedge clk) begin
    conf_valid <= conf_bus[0];
    flag <= (conf_bus[0])? ~flag : flag;
    if(flag) begin
      conf_reg1 <= 0;
      conf_reg0 <= { conf_reg0[14:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg0[14:0], conf_bus[conf_bus_width-1:1] };
    end else begin
      conf_reg0 <= 0;
      conf_reg1 <= { conf_reg1[14:0], conf_bus[conf_bus_width-1:1] };
      conf_reg <= { conf_reg1[14:0], conf_bus[conf_bus_width-1:1] };
    end
  end


  always @(posedge clk) begin
    reset <= 1'b0;
    if(conf_valid) begin
      if(pe_id == conf_reg[2:0]) begin
        case(conf_reg[5:3])
          3'b1: begin
            conf_alu <= conf_reg[17:6];
          end
          3'b10: begin
            conf_const <= conf_reg[21:6];
          end
          3'b0: begin
            reset <= 1'b1;
            conf_alu <= 0;
            conf_const <= 0;
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



module pe_input_2_0_4_add_mul_sub #
(
  parameter id = 0
)
(
  input clk,
  input en,
  input [8-1:0] conf_bus,
  input [16-1:0] in0,
  input [16-1:0] in1,
  output [16-1:0] out0,
  output [16-1:0] out1,
  input [16-1:0] stream_in
);

  wire reset;
  wire [16-1:0] pe_const;
  wire [16-1:0] alu_in0;
  wire [16-1:0] alu_in1;
  wire [16-1:0] alu_out;
  wire [2-1:0] sel_alu_opcode;
  wire [2-1:0] sel_mux_alu0;
  wire [2-1:0] sel_mux_alu1;

  multiplexer_4
  #(
    .width(16)
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

  wire [16-1:0] elastic_pipeline_to_alu0;
  wire [3-1:0] sel_elastic_pipeline0;

  elastic_pipeline_4
  #(
    .width(16)
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
    .width(16)
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

  wire [16-1:0] elastic_pipeline_to_alu1;
  wire [3-1:0] sel_elastic_pipeline1;

  elastic_pipeline_4
  #(
    .width(16)
  )
  elastic_pipeline1
  (
    .in(alu_in1),
    .out(elastic_pipeline_to_alu1),
    .clk(clk),
    .en(en),
    .latency(sel_elastic_pipeline1)
  );


  alu_2_add_mul_sub
  #(
    .width(16)
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


  route_0_3x2
  #(
    .width(16)
  )
  router
  (
    .in0(alu_out),
    .out0(out0),
    .out1(out1)
  );

  wire [12-1:0] conf_alu;

  pe_conf_reader_alu_width_12_router_width_0
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
  assign sel_elastic_pipeline0 = conf_alu[8:6];
  assign sel_elastic_pipeline1 = conf_alu[11:9];

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

