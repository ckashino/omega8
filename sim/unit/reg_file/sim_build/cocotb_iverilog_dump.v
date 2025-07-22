module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/reg_file.fst");
    $dumpvars(0, reg_file);
end
endmodule
