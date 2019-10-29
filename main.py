# ((((x)=(y))=(((z)>((-(x))+(-(y))))>(-(z))))=((x)+(-(y))))

class Expression:
    def __init__(self, left, right, repr):
        self._left = left
        self._right = right
        self._repr = repr
    def left(self, atoms_values):
        return self._left.value(atoms_values)
    def right(self, atoms_values):
        return self._right.value(atoms_values)
    def value(self, atoms_values):
        pass

class Negative(Expression):
    def value(self, atoms_values):
        return not self.right(atoms_values)

class Conjunction(Expression):
    def value(self, atoms_values):
        return self.left(atoms_values) and self.right(atoms_values)

class Disjunction(Expression):
    def value(self, atoms_values):
        return self.left(atoms_values) or self.right(atoms_values)

class Implication(Expression):
    def value(self, atoms_values):
        return not self.left(atoms_values) or self.right(atoms_values)

class Equivalence(Expression):
    def value(self, atoms_values):
        return self.left(atoms_values) == self.right(atoms_values)
        
class T(Expression):
    def value(self, atoms_values):
        return True

class F(Expression):
    def value(self, atoms_values):
        return False

class NonePrimitive(Expression):
    def __init__(self):
        self._left = None
        self._right = None
    def value(self, atoms_values):
        return None

class Atom(Expression):
    def __init__(self, left, right, repr, letter):
        super().__init__(left, right, repr)
        self._letter = letter
    def value(self, atoms_values):
        return atoms_values[self._letter]
        
        
def str_to_expression_recurse(s):
    # print('Рекурсія', s)
    
    # перевір мінус
    # врахуй дужки
    # врахуй представлення
    
    # print("ВХІД:", s)
    
    operators = {'-': Negative, '*': Conjunction, '+': Disjunction, '>': Implication, '=': Equivalence}
    primitives = {'0': F, '1': T}
    if len(s) >= 4:
        inset = 0
        for i, c in enumerate(s):
            if c == '(':
                inset += 1
            elif c == ')':
                inset -= 1
            elif (inset == 1) and c in operators:
                a = s[1:i]
                op = c
                b = s[i+1:-1]
        try:
            return operators[op](str_to_expression_recurse(a), str_to_expression_recurse(b), s[1:-1])
        except KeyError:
            raise Exception('Містить недопустимі оператори')
    elif s:
        try:
            return primitives[s](NonePrimitive(), NonePrimitive(), s[1])
        except KeyError:
            return Atom(NonePrimitive(), NonePrimitive(), s[1], s[1])
    else:
        return NonePrimitive();

def str_to_expression(s):
    return str_to_expression_recurse(s)
    
def print_full_table(expression, expression_atoms):
    print(''.join(expression_atoms))
    
    for i in range(2 ** len(expression_atoms)):
        prepare_bin = bin(i)[2:].rjust(len(expression_atoms), '0')
        prepare_dict = {}
        for j in range(len(expression_atoms)):
            prepare_dict[expression_atoms[j]] = bool(int(prepare_bin[j]))
        
        print(prepare_bin, expression.value(prepare_dict))
    
def main():
    print('''---------- ІНСТРУКЦІЯ ----------

Ця програма будує таблицю істинності для введеного виразу. Атоми і їх кількість визначаються автоматично.

Вводьте вираз без пробілів, усі висловлювання загортайте в дужки.
Наприклад: ((((x)=(y))=(((z)>((-(x))+(-(y))))>(-(z))))=((x)+(-(y))))

Оператори:
    -       заперечення
    *       кон\'юнкція
    +       диз\'юнкція
    >       імплікація
    =       еквівалентність

--------------------------------
    ''')
    entered_expression = input('Введіть вираз: ')
    
    expression_atoms = set()
    for i in entered_expression:
        if i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            expression_atoms.add(i)
    expression_atoms = sorted(list(expression_atoms))
    
    try:
        expression = str_to_expression(entered_expression)
        print_full_table(expression, expression_atoms)
    except:
        print('Неправильно введений вираз')

if __name__ == '__main__':
    main()