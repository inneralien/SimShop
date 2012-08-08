`timescale 1 ns / 10 ps
module tb();

// Active high chip reset (Needed by SimShop - TODO: will be removed later)
task chip_reset(input integer N);
begin
    $display("<%0t> %m Reset chip", $time);
end
endtask

//=============================================================================
// Declare signals to be driven from the testbench as 'reg' type
//=============================================================================
reg in0, in1;

//=============================================================================
// Declare module interconnect wires or the compiler will complain about
// implicit definitions.
//=============================================================================
wire and_out, nand_out;
wire or_out, nor_out;

//=============================================================================
// Instantiate the and_nand module
//=============================================================================
and_nand and_nand_instance(
   .in0         (in0),      // I
   .in1         (in1),      // I
   .and_out     (and_out),  // O
   .nand_out    (nand_out)  // O
);

//=============================================================================
// Instantiate the or_nor module
//=============================================================================
or_nor or_nor_instance(
   .in0         (in0),      // I
   .in1         (in1),      // I
   .or_out      (or_out),   // O
   .nor_out     (nor_out)   // O
);

//=============================================================================
// This is where the actual simulation starts.
// The input signals are driven from the testbench here.
// Signals must be declared as 'reg' type for them to be
// driven this way.
//=============================================================================
task run_sim;
begin
    $display("--------||---------|----------|--------|--------");
    $display("in1 in0 || and_out | nand_out | or_out | nor_out");
    $display("--------||---------|----------|--------|--------");
    in1 = 1'b0;
    in0 = 1'b0;
    #5; // Let 5 simulation time steps pass
    $display(" %b   %b  ||    %b    |     %b    |   %b    |    %b",
        in1, in0, and_out, nand_out, or_out, nor_out);
    in1 = 1'b0;
    in0 = 1'b1;
    #5; // Let 5 simulation time steps pass
    $display(" %b   %b  ||    %b    |     %b    |   %b    |    %b",
        in1, in0, and_out, nand_out, or_out, nor_out);
    in1 = 1'b1;
    in0 = 1'b0;
    #5; // Let 5 simulation time steps pass
    $display(" %b   %b  ||    %b    |     %b    |   %b    |    %b",
        in1, in0, and_out, nand_out, or_out, nor_out);
    in1 = 1'b1;
    in0 = 1'b1;
    #5; // Let 5 simulation time steps pass
    $display(" %b   %b  ||    %b    |     %b    |   %b    |    %b",
        in1, in0, and_out, nand_out, or_out, nor_out);
    $finish;
end
endtask

task dummy1;
begin
    $display("Dummy task 1 begin");
    #5;
    $display("Dummy task 1 end");
end
endtask

task dummy2;
begin
    $display("Dummy task 2 begin");
    #5;
    $display("Dummy task 2 end");
end
endtask

endmodule
