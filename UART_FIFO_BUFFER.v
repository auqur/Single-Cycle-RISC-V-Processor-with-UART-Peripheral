module UART_FIFO_BUFFER (
    input        clk,
    input        reset,
    input        write_en,      
    input  [7:0] write_data,
    input        read_en,       
    output [7:0] read_data,
    output       empty,
    output       full
);

    reg [7:0] buffer [0:15];   
    reg [3:0] read_pointer = 0;          
    reg [3:0] write_pointer = 0;          
    reg [4:0] count = 0;         

    always @(posedge clk) begin
        if (reset) begin
            write_pointer <= 0;
            count <= 0;
        end else if (write_en && !full) begin
            buffer[write_pointer] <= write_data;
            write_pointer <= write_pointer + 1;
            count <= count + 1;
        end
    end

    always @(posedge clk) begin
        if (reset) begin
            read_pointer <= 0;
        end else if (read_en && !empty) begin
            read_pointer <= read_pointer + 1;
            count <= count - 1;
        end
    end

    assign read_data = buffer[read_pointer];
    assign empty = (count == 0);
    assign full  = (count == 16);

endmodule
