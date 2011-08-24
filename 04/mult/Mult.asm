@i
M=1 // i=1
@R2
M=0 // R2=0
(LOOP)
    @i
    D=M // D=i
    @R0
    D=D-M // i=i-R0
    @END
    D;JGT // if i>R0 jump to the end of the loop (END)
    @R1 
    D=M // D=R1
    @R2
    M=M+D // sum=sum+R1
    @i
    M=M+1 //i=i+1
    @LOOP
    0;JMP // jump to the beginning of the loop
(END)
    @END
    0;JMP // Infinite loop
