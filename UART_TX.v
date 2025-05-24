module UART_TX (
    input        clk,         
    input        reset,       
    input        tx_start,    
    input  [7:0] tx_data,     
    input  [15:0] clk_per_bit,
    output reg   tx,          
    output reg   tx_busy     
);

    reg [3:0] bit_index;     
    reg [15:0] clk_count;     
    reg [9:0] shift_reg;      

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            tx <= 1'b1;        // Idle state is HIGH
            tx_busy <= 0;
            clk_count <= 0;
            bit_index <= 0;
            shift_reg <= 10'b1111111111;
        end else begin
            if (tx_start && !tx_busy) begin
                // Load transmit frame: start bit (0), 8 data bits, stop bit (1)
                shift_reg <= {1'b1, tx_data, 1'b0};
                tx_busy <= 1;
                bit_index <= 0;
                clk_count <= 0;
            end else if (tx_busy) begin
                if (clk_count < clk_per_bit - 1) begin
                    clk_count <= clk_count + 1;
                end else begin
                    clk_count <= 0;
                    tx <= shift_reg[bit_index];
                    bit_index <= bit_index + 1;

                    if (bit_index == 9) begin
                        tx_busy <= 0;
                        tx <= 1'b1; // Return to idle
                    end
                end
            end
        end
    end

endmodule
