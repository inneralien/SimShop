/*
    Minimum required tasks for SimShop.
*/
`timescale 1ns / 100ps
`ifndef D
  `define D #1
`endif

module test_util;

`include "test_util.vh"

task report_error;
input [8*128:1] s;
begin
    $display("<%0t> ERROR: %0s", $time, s);
end
endtask // report_error


task simulation_finish;
begin
    $finish;
end
endtask

endmodule // test_util

