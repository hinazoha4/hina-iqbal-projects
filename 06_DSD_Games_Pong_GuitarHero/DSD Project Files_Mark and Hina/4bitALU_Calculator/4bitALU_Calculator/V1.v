module calculator (
    input  [9:0] SW,     // Switches
    output [7:0] LEDR    // LEDs for result
);

    wire [3:0] A = SW[3:0];     // Operand A
    wire [3:0] B = SW[7:4];     // Operand B
    wire [1:0] op = SW[9:8];    // Operation select

    reg [7:0] result;

    always @(*) begin
        case (op)
            2'b00: result = A + B;     // Addition
            2'b01: result = A - B;     // Subtraction
            2'b10: result = A & B;     // Bitwise AND
            2'b11: result = A | B;     // Bitwise OR
            default: result = 8'b00000000;
        endcase
    end

    assign LEDR = result;

endmodule