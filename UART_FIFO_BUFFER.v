module UART_FIFO_BUFFER (
    input        clk,
    input        reset,
    input        write_req,      
    input  [7:0] write_data,
    input        read_req,       
    output [7:0] read_data,
    output       lowword
);

    reg [7:0] buffer [0:15];   
    reg [3:0] read_pointer = 0;          
    reg [3:0] write_pointer = 0;          
    reg [4:0] count = 0;         

    always @(posedge clk) begin
        if (reset) begin
            write_pointer <= 0;
            count <= 0;
        end else if (write_req & (count < 4'hF)) begin
            buffer[write_pointer] <= write_data;
            write_pointer <= write_pointer + 1;
            count <= count + 1;
        end
    end

    always @(posedge clk) begin
        if (reset) begin
            read_pointer <= 0;
        end else if (read_req) begin
            read_pointer <= read_pointer + 1;
            count <= count - 1;
        end
    end

    assign read_data = buffer[read_pointer];
    assign lowword = ~(read_pointer < write_pointer)


endmodule
