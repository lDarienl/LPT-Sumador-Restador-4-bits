def NAND(a, b):
    if a == 0 and b == 0: return 1
    if a == 0 and b == 1: return 1
    if a == 1 and b == 0: return 1
    if a == 1 and b == 1: return 0

def NOT(a):
    return NAND(a, a)

def AND(a, b):
    return NOT(NAND(a, b))

def OR(a, b):
    return NAND(NAND(a, a), NAND(b, b))

def XOR(a, b):
    return AND(OR(a, b), NOT(AND(a, b)))

def half_adder(a, b):
    carry = AND(a, b)
    sum = XOR(a, b)
    return (carry, sum)

def full_adder(a, b, carry_in):
    carry1, sum1 = half_adder(a, b)
    carry2, sum2 = half_adder(carry_in, sum1)
    carry_out = OR(carry1, carry2)
    return (carry_out, sum2)

def add4bits(x, y):
    carry3, sum3 = full_adder(x[3], y[3], 0)
    carry2, sum2 = full_adder(x[2], y[2], carry3)
    carry1, sum1 = full_adder(x[1], y[1], carry2)
    carry0, sum0 = full_adder(x[0], y[0], carry1)
    return (carry0, sum0, sum1, sum2, sum3)

def cadena_a_bits(cadena):
    return [int(c) for c in cadena.strip()]

def validar_4bits(cadena, nombre):
    c = cadena.strip()
    if len(c) != 4:
        print(f"Error: '{nombre}' debe tener exactamente 4 bits (se ingresaron {len(c)}). Ejemplo válido: 1100")
        return False
    if not all(b in '01' for b in c):
        print(f"Error: '{nombre}' solo puede contener 0 y 1. Se ingresó: {cadena}")
        return False
    return True

x_str = input("Ingrese el primer numero en binario (ej: 1100): ")
y_str = input("Ingrese el segundo numero en binario (ej: 0011): ")

if not validar_4bits(x_str, "Primer número"):
    exit(1)
if not validar_4bits(y_str, "Segundo número"):
    exit(1)

x = cadena_a_bits(x_str)
y = cadena_a_bits(y_str)
carry0, sum0, sum1, sum2, sum3 = add4bits(x, y)

if carry0 == 1:
    print("Error: La suma supera los 4 bits (hay acarreo de salida). Ejemplo: 1111 + 0001 = 10000 no cabe en 4 bits.")
    exit(1)

print(f"La suma de {x_str} y {y_str} es {sum0}{sum1}{sum2}{sum3}")
