test_template = """
$timescale
`timescale 1 ns / 10 ps


module test_top();
`include "testlib.vh"

/////////////////
// Start dumping
/////////////////
initial begin
    `ifdef NCV
	$$display("<%0t> Dump file set to ./results/ncv.trn.", $$time);
        $$recordfile("./log/ncv.trn");
    `endif
    `ifndef NCV
	$$display("<%0t> Dump file set to $dump.", $$time);
        $$dumpfile("$dump");
    `endif

    $$display("");
    if ($$test$$plusargs("DUMPON")) begin
	$$display("<%0t> Dumping started.", $$time);
        `ifdef NCV
//	    $$recordvars(0,tb);
	    $$recordvars(tb);
        `endif
        `ifndef NCV
	    $$dumpvars(8,tb);
	    $$dumpvars(4,test_common);
	    $$dumpvars;
        `endif
        end
    else
	$$display("<%0t> Dumping has been turned OFF. Nothing will be dumped.", $$time);
end


initial begin : main
    `reset_chip;
    if ($$test$$plusargs("check")) begin
        $$display("");
        $$display("#################################################");
        $$display("Running Check Tests.");
        $$display("#################################################");
        // list all tasks here
        test_common.reg_defaults;
        test_common.dlmp_test;
    end
   else if ($$test$$plusargs("regression")) begin
      $$display("");
      $$display("###################################");
      $$display("## Running regression test suite ##");
      $$display("###################################");
      test_common.reg_defaults;
      test_common.dlmp_test;
   end
   else begin
      if ( $$test$$plusargs("reg_defaults"))		begin test_common.reg_defaults; end
      if ( $$test$$plusargs("dlmp_test"))			begin test_common.dlmp_test; end
   end

   repeat(100) @(posedge tb.clk_16m);
   `simulation_finish;
end

endmodule"""
