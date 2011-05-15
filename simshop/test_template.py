# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

test_template = """
`timescale $timescale
//`include "testlib.vh"

module auto_test();
  // Setup simulation dumping or not
    initial begin : setup
        $$display("");
        $$display("<%0t> Dump file set to $dumpfile.", $$time);
        $$dumpfile("$dumpfile");
        if ($$test$$plusargs("DUMPON")) begin
            $$display("<%0t> Dumping started.", $$time);
            $dumpvars
        end
        else
        $$display("<%0t> Dumping has been turned OFF. Nothing will be dumped.", $$time);

        $$display("");
        #0;
        $reset
        runsim;
        $finish
    end

    task runsim;
    begin
        fork : auto_tests
        begin : auto_tests_run
            $$display("<%0t> Starting Auto Tests", $$time);
            $tasks
            disable auto_tests;
        end
        begin
            #$timeout;   // Timeout
            $timeout_error
            $$display("<%0t> Timeout.", $$time);
            disable auto_tests_run;
            disable auto_tests;
        end
        join
    end
    endtask
endmodule"""
