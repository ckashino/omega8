module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/ram.fst");
    $dumpvars(0, ram);
end
endmodule
