# Sumador de 4 bits (diseño e implementación)

Diseño e implementación en Python de un **sumador de 4 bits**, usando **solo funciones AND, OR y NOT** (construidas a partir de NAND).

---

## Fuente y referencias

La explicación de **qué es un sumador de 4 bits**, cómo se construye a partir de sumadores completos (full adders) y cómo se representa la suma multi-bit está tomada del artículo:

**[Multi-bit addition – Programmer's Compendium (Destroy All Software)](https://www.destroyallsoftware.com/compendium/multi-bit-addition?share_key=34046b818d0eac60)**

En esa página se describe:

- Representación de números multi-bit como listas de 0s y 1s.
- Uso de **un full adder por bit** (en nuestro caso, cuatro).
- **Encadenamiento (cascada)** de full adders: el `carry_out` de cada uno es el `carry_in` del siguiente.
- El **sumador de 4 bits** como tipo **ripple adder**: el acarreo “ripple” de etapa en etapa.
- Diagramas del circuito: uno con bloques FULL (FULL1…FULL4) y otro con el detalle de puertas AND, OR y XOR (y medio sumadores).

Las imágenes que acompañan este README son las de esa página (sumador en cascada y detalle con puertas).

---

## Qué es un operador / sumador de 4 bits

- Opera sobre **dos números de 4 bits** en binario.
- Los representamos como **listas de 4 bits**: por ejemplo `[0, 0, 0, 1]` para el 1 y `[1, 0, 0, 1]` para el 9.
- El índice **0** es el bit más significativo (MSB) y el **3** el menos significativo (LSB); la suma se hace de derecha a izquierda (LSB primero), como en la suma por columnas.
- Se necesitan **cuatro full adders** en cascada: el acarreo de salida de uno es el acarreo de entrada del siguiente. El primer `carry_in` es 0; el último `carry_out` indica overflow si la suma no cabe en 4 bits.

---

## Qué se usó en el código

- **Solo AND, OR y NOT** (y por debajo, NAND).
- **NAND**: puerta base; con ella se definen NOT, AND y OR.
- **NOT**: `NAND(a, a)`.
- **AND**: `NOT(NAND(a, b))`.
- **OR**: `NAND(NAND(a,a), NAND(b,b))`.
- **XOR**: construido con AND, OR y NOT: `AND(OR(a,b), NOT(AND(a,b)))` (necesario para la suma bit a bit).
- **Half adder**: AND para el acarreo, XOR para la suma de dos bits.
- **Full adder**: dos half adders + OR para combinar los acarreos; entradas `(a, b, carry_in)`; salidas `(carry_out, sum)`.
- **add4bits**: cuatro llamadas a full adder en cascada, con índices `[3]` → `[0]` (LSB a MSB), igual que en la página.
- **Entrada/salida**: conversión de cadenas tipo `"1100"` a lista de bits, validación de 4 bits y detección de overflow (acarreo final).

---

## Por qué se usó así

- **NAND como base**: en la referencia todo se construye desde NAND; en el código AND, OR y NOT están implementados con NAND para mantener la misma idea (y XOR a partir de AND/OR/NOT).
- **Un full adder por bit**: para sumar 4 bits hacen falta 4 full adders; cada uno suma dos bits más el acarreo entrante y produce un bit de suma y un acarreo saliente.
- **Cascada de acarreos**: el `carry_out` de la etapa `i` se usa como `carry_in` de la etapa `i+1`, igual que en el artículo y en los diagramas (ripple adder).
- **Orden de índices**: `x[3], y[3]` son los LSB (primera columna); `x[0], y[0]` son los MSB (última columna), coherente con la representación `[MSB, ..., LSB]` de la página.
- **Validación y overflow**: se exige exactamente 4 bits por entrada y se comprueba el acarreo final; si hay acarreo, la suma no cabe en 4 bits (como 15+1=16) y se reporta error, igual que se explica en la referencia cuando el último carry se descarta.

---

## Cómo se usó (flujo del programa)

1. **Entrada**: el usuario escribe dos cadenas binarias de exactamente 4 bits (por ejemplo `1100` y `0011`).
2. **Validación**:  
   - Longitud distinta de 4 → error.  
   - Cualquier carácter que no sea `0` o `1` → error.
3. **Conversión**: cada cadena se convierte en lista de enteros con `cadena_a_bits` (p. ej. `"1100"` → `[1,1,0,0]`).
4. **Suma**: se llama `add4bits(x, y)`, que internamente hace:
   - `full_adder(x[3], y[3], 0)` → `sum3`, `carry3`
   - `full_adder(x[2], y[2], carry3)` → `sum2`, `carry2`
   - `full_adder(x[1], y[1], carry2)` → `sum1`, `carry1`
   - `full_adder(x[0], y[0], carry1)` → `sum0`, `carry0`
5. **Overflow**: si `carry0 == 1`, la suma no cabe en 4 bits y se muestra error.
6. **Salida**: si no hay overflow, se imprime el resultado como los cuatro bits de la suma (p. ej. `sum0 sum1 sum2 sum3`).

---

## Diagramas (referencia)

La página [Multi-bit addition](https://www.destroyallsoftware.com/compendium/multi-bit-addition?share_key=34046b818d0eac60) incluye dos imágenes que explican el circuito:

1. **Sumador en cascada**: cuatro bloques FULL (FULL1…FULL4), con `left[i]`, `right[i]`, acarreos encadenados y salidas `out1`…`out4`. El primer `carry_in` y el último `carry_out` no se usan (0 inicial y overflow descartado en 4 bits).
2. **Detalle con puertas**: mismo sumador de 4 bits desglosado en medio sumadores (XOR + AND) y full adders (dos medio sumadores + OR), mostrando que todo se construye con puertas lógicas y, en última instancia, con NAND.

Puedes ver ambas figuras directamente en el artículo enlazado. Coinciden con la implementación en `operado4bits.py`.

---

## Cómo ejecutar

```bash
python operado4bits.py
```

Se pedirán dos números en binario de 4 bits (por ejemplo `1100` y `0011`). El programa validará longitud y caracteres, realizará la suma con el sumador de 4 bits y mostrará el resultado o un mensaje de error si la entrada es inválida o hay overflow.

---

## Resumen de la tarea

- **Objetivo**: Diseñar e implementar en Python un sumador (y en extensión sumador-restador) de 4 bits.
- **Restricción**: Usar solo funciones **AND**, **OR** y **NOT** (en este proyecto construidas desde NAND y usadas para XOR, half adder, full adder y add4bits).
- **Referencia**: Conceptos y estructura del sumador de 4 bits según [Destroy All Software – Multi-bit addition](https://www.destroyallsoftware.com/compendium/multi-bit-addition?share_key=34046b818d0eac60).
