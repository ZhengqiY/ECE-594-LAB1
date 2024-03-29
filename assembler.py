registers = ['$zero','$ra','$sp','$gp','$tp','$t0','$t1','$t2','$s0','$s1','$a0','$a1','$a2','$a3','$a4','$a5',
'$a6','$a7','$s2','$s3','$s4','$s5','$s6','$s7','$s8','$s9','$s10','$s11','$t3','$t4','$t5','$t6']


def get_commands_and_func_dict(verilog_filename):
    verilog_file = open(verilog_filename, "r")

    commands = [line.strip('\n:') for line in verilog_file]
    commands = [line.replace('\t', ' ') for line in commands]
    commands = [line.replace(',', ' ') for line in commands]
    commands = [line.replace('(', ' ') for line in commands]
    commands = [line.replace(')', ' ') for line in commands]
    commands = list(filter(lambda a: a != '' and a != ' ', commands ))
    verilog_file.close()

    new_commands = []
    for line in commands:
        hash_position = line.find("#")
        if hash_position != -1:
            line = line[:hash_position]
        if hash_position != 0 and hash_position != 1:
            new_commands.append(line)

    new_commands = [line.split() for line in new_commands]
    
    func_dict = {}
    final_commands = new_commands
    for command in new_commands:
        if len(command) == 1:
            func_ind = final_commands.index(command)
            final_commands.pop(func_ind)
            func_dict[command[0]] = func_ind
    
    return final_commands, func_dict


def twos_compliment(bin_str):
    #flip the bits
    bin_str = '0' + bin_str
    bin_str = bin_str.replace('1', '2')
    bin_str = bin_str.replace('0', '1')
    bin_str = bin_str.replace('2', '0')

    value = int(bin_str, 2)
    value += 1
    bin_str = bin(value)
    bin_str = bin_str[2:]

    return bin_str    # Done

def conv_2_bin(bin_len, value):
    bin_str = bin(value)
    sign = bin_str[0]
    if sign == '0':
        bin_str = bin_str[2:]
        appender = '0'
    if sign == '-':
        bin_str = bin_str[3:]
        bin_str = twos_compliment(bin_str)
        appender = '1'

    while(len(bin_str) < bin_len):
        bin_str = appender + bin_str
    
    if(len(bin_str) > bin_len):
        print("Warning: Binary length of value is longer than allowed. Hex might be wrong")

    return bin_str


def conv_2_hex(bin_value):
    hex_str = hex(int(bin_value, 2))
    hex_str = hex_str[2:]
    while(len(hex_str) < 8):
        hex_str = '0' + hex_str

    return hex_str


def get_immediate_for_jumps(function, line_index):
    function_line = func_dict[function]
    immediate = (function_line - line_index) * 4
    return immediate

def add_call(command, line_index):    
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    rs2 = conv_2_bin(5, registers.index(command[3]))

    call_str = '0000000' + rs2 + rs1 + '000' + rd + '0110011'    
    call_str = conv_2_hex(call_str)
    return call_str

def div_call(command, line_index):
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    rs2 = conv_2_bin(5, registers.index(command[3]))

    call_str = '0000001' + rs2 + rs1 + '100' + rd + '0110011'
    call_str = conv_2_hex(call_str)
    return call_str

def mul_call(command, line_index):
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    rs2 = conv_2_bin(5, registers.index(command[3]))

    call_str = '0000001' + rs2 + rs1 + '000' + rd + '0110011'
    call_str = conv_2_hex(call_str)
    return call_str

def addi_call(command, line_index):
    imm = conv_2_bin(12, int(command[3]))
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    
    call_str = imm + rs1 + '000' + rd + '0010011'
    call_str = conv_2_hex(call_str)
    return call_str

def ori_call(command, line_index):
    imm = conv_2_bin(12, int(command[3]))
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    
    call_str = imm + rs1 + '110' + rd + '0010011'
    call_str = conv_2_hex(call_str)
    return call_str

def andi_call(command, line_index):
    imm = conv_2_bin(12, int(command[3]))
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    
    call_str = imm + rs1 + '111' + rd + '0010011'
    call_str = conv_2_hex(call_str)
    return call_str

def slt_call(command, line_index):
    rd = conv_2_bin(5, registers.index(command[1]))
    rs1 = conv_2_bin(5, registers.index(command[2]))
    rs2 = conv_2_bin(5, registers.index(command[3]))

    call_str = '0000000' + rs2 + rs1 + '010' + rd + '0110011'
    call_str = conv_2_hex(call_str)
    return call_str

def bne_call(command, line_index):
    imm = get_immediate_for_jumps(command[3], line_index)
    imm = conv_2_bin(13, imm)
    rs1 = conv_2_bin(5, registers.index(command[1]))
    rs2 = conv_2_bin(5, registers.index(command[2]))

    call_str = imm[0] + imm[2:8] + rs2 + rs1 + '001' + imm[8:12] + imm[1] + '1100011'
    call_str = conv_2_hex(call_str)
    return call_str

def beq_call(command, line_index):
    imm = get_immediate_for_jumps(command[3], line_index)
    imm = conv_2_bin(13, imm)
    rs1 = conv_2_bin(5, registers.index(command[1]))
    rs2 = conv_2_bin(5, registers.index(command[2]))

    call_str = imm[0] + imm[2:8] + rs2 + rs1 + '000' + imm[8:12] + imm[1] + '1100011'
    call_str = conv_2_hex(call_str)
    return call_str

def blt_call(command, line_index):
    imm = get_immediate_for_jumps(command[3], line_index)
    imm = conv_2_bin(13, imm)
    rs1 = conv_2_bin(5, registers.index(command[1]))
    rs2 = conv_2_bin(5, registers.index(command[2]))

    call_str = imm[0] + imm[2:8] + rs2 + rs1 + '100' + imm[8:12] + imm[1] + '1100011'
    call_str = conv_2_hex(call_str)
    return call_str

def sw_call(command, line_index):
    rs2 = conv_2_bin(5, registers.index(command[1]))
    imm = conv_2_bin(12, int(command[2]))
    rs1 = conv_2_bin(5, registers.index(command[3]))
    
    call_str = imm[0:7] + rs2 + rs1 + '010' + imm[7:12] + '0100011'
    call_str = conv_2_hex(call_str)
    return call_str

def lw_call(command, line_index):
    rd = conv_2_bin(5, registers.index(command[1]))
    imm = conv_2_bin(12, int(command[2]))
    rs1 = conv_2_bin(5, registers.index(command[3]))

    call_str = imm + rs1 + '010' + rd + '0000011'
    call_str = conv_2_hex(call_str)
    return call_str

def jal_call(command, line_index):
    imm = get_immediate_for_jumps(command[2], line_index)
    imm = conv_2_bin(21, imm)
    rd = conv_2_bin(5, registers.index(command[1]))

    call_str = imm[0] + imm[10:20] + imm[9] + imm[1:9] + rd + '1101111'
    call_str = conv_2_hex(call_str)

    return call_str

def jr_call(command, line_index):
    rs1 = conv_2_bin(5, registers.index(command[1]))

    call_str = ('0' * 12) + rs1 + ('0' * 8) + '1100111'
    call_str = conv_2_hex(call_str)
    return call_str




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert Assembly Code to Machine Code')
    parser.add_argument("-f", "--filename", type=str, help="assembly filename")
    args = parser.parse_args()
    filename = args.filename

    commands, func_dict = get_commands_and_func_dict(filename)
    function_calls = {
        'div': div_call,
        'mul': mul_call,
        'add': add_call,
        'addi': addi_call,
        'ori': ori_call,
        'slt': slt_call,
        'bne': bne_call,
        'blt': blt_call,
        'sw': sw_call,
        'lw': lw_call,
        'jal': jal_call,
        'jr': jr_call,
        'beq': beq_call,
        'andi':andi_call,
    }

    machine_code = []
    for ind, command in enumerate(commands):
        call = function_calls[command[0]]
        call_code = call(command, ind)
        machine_code.append(call_code)


    machine_file = open('machinecode.txt', 'w')
    for line in machine_code:
        machine_file.write(line + '\n')

    machine_file.close()
