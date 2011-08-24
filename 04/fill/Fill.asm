(BEGIN)
@i
M=0 // i=0
@KBD
D=M
@LOOP-CLR
D;JEQ // clear the screen since a key isn't pressed
@LOOP-BLK
D;JNE // blacken the screen since a key is pressed

(LOOP-BLK)
    @i
    D=M // D=i
    @8191
    D=D-A
    @END-BLK
    D;JGT
    @i
    D=M // D=i
    @16384
    A=A+D
    M=-1
    @i
    M=M+1 // i++
    @LOOP-BLK
    0;JMP
(END-BLK)
@BEGIN
0;JMP

(LOOP-CLR)
    @i
    D=M // D=i
    @8191
    D=D-A
    @END-CLR
    D;JGT
    @i
    D=M // D=i
    @16384 // first SCREEN memory bit
    A=A+D
    M=0 // turn the pixel white
    @i
    M=M+1 // i++
    @LOOP-CLR
    0;JMP
(END-CLR)
@BEGIN
0;JMP
