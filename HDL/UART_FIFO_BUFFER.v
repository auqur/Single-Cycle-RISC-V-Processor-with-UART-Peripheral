module UART_FIFO_BUFFER (
    input        UART_CLK,
    input        BUTTON_CLK,
    input        reset,
    input        write_req,      
    input  [7:0] write_data,
    input        read_req,       
    output [7:0] read_data,
    output       lowword
);

    reg [7:0] buffer [0:15];        // 16-byte buffer
    reg [3:0] read_pointer = 0;     // Read pointer for the buffer        
    reg [3:0] write_pointer = 0;    // Write pointer for the buffer            

    // Write operation on UART_CLK
    always @(posedge UART_CLK) begin
        if (reset) begin
            write_pointer <= 0;
        end 
        else if (write_req) begin
            buffer[write_pointer] <= write_data;    // Store data in the buffer when write request is high
            write_pointer <= write_pointer + 1;     // Increment write pointer  
        end
    end
    
    // Read operation on BUTTON_CLK
    always @(posedge BUTTON_CLK) begin
        if (reset) begin
            read_pointer <= 0;
        end else if (read_req) begin
            read_pointer <= read_pointer + 1;       // Increment read pointer
        end
    end

    assign read_data = buffer[read_pointer];
    assign lowword = ~(read _pointer < write_pointer);

endmodule
