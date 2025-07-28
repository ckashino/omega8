module iverilog_dump();
initial begin
    $dumpfile("instr_mem.fst");
    $dumpvars(0, instr_mem);
end
endmodule
