/*
  Copyright (C) 2011 RTLCores LLC.
  http://rtlcores.com

  Creation Date : 16-Mar-2010
  Support Email : support@rtlcores.com
  Support Forum : http://rtlcores.com/forum

  Descripton
    Simple combinational AND/NAND logic example

  ================================
  Truth Table for 'and' and 'nand'
  ================================
  in1 in0 || and_out | nand_out
  --------||---------|---------
   0   0  ||    0    |     1
   0   1  ||    0    |     1
   1   0  ||    0    |     1
   1   1  ||    1    |     0
*/

`timescale 1 ns / 10 ps

module and_nand (
    input  wire in0,
    input  wire in1,
    output wire and_out,
    output wire nand_out
);

assign and_out = in0 & in1;

assign nand_out = ~(in0 & in1);

endmodule
