class CompileException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LinkException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FunctionNode:
    def __init__(self, parent, element):
        self.parent = parent
        self.element = element

        self.leftchild = None
        self.rightchild = None
    
    def is_complete(self):
        return 'primitive' not in self.element or self.element['primitive'] != '`' or (self.leftchild is not None and self.leftchild.is_complete() and self.rightchild is not None and self.rightchild.is_complete())
    
    def get_vars(self):
        if 'primitive' in self.element and self.element['primitive'] == '`':
            return self.leftchild.get_vars() | self.rightchild.get_vars()
        elif 'variable' in self.element:
            return {self.element['variable']}
        else:
            return set()

    def is_pure(self, var = None):
        if 'impure_function' in self.element:
            return False
        
        if 'primitive' in self.element and self.element['primitive'] == '`':
            appl1 = self.leftchild
            if 'primitive' in appl1.element and appl1.element['primitive'] == '`':
                appl2 = appl1.leftchild
                if 'primitive' in appl2.element:
                    # ``k
                    if appl2.element['primitive'] == 'k':
                        return False
                    elif appl2.element['primitive'] == '`':
                        appl3 = appl2.leftchild
                        if 'primitive' in appl3.element and appl3.element['primitive'] == '`':
                            appl4 = appl3.leftchild
                            # ```s
                            if 'primitive' in appl4.element and appl4.element['primitive'] == 's':
                                return False

        if var is not None and 'variable' in self.element and self.element['variable'] == var:
            return False

        return (self.leftchild is None or self.leftchild.is_pure(var)) and (self.rightchild is None or self.rightchild.is_pure(var))

    def _propagate_variable(self, parent, var):
        if 'variable' in self.element and self.element['variable'] == var:
            return FunctionNode(parent, {'primitive': 'i'})
        elif not self.is_pure(var) and 'primitive' in self.element and self.element['primitive'] == '`':
            appl1 = FunctionNode(parent, {'primitive': '`'})
            appl2 = FunctionNode(appl1, {'primitive': '`'})
            s = FunctionNode(appl2, {'primitive': 's'})

            appl1.leftchild = appl2
            appl1.rightchild = self.rightchild._propagate_variable(appl1, var)

            appl2.leftchild = s
            appl2.rightchild = self.leftchild._propagate_variable(appl2, var)

            return appl1
        else:
            appl = FunctionNode(parent, {'primitive': '`'})
            k = FunctionNode(appl, {'primitive': 'k'})
            self.parent = appl

            appl.leftchild = k
            appl.rightchild = self

            return appl
    
    def propagate_variable(self, var):
        assert(self.parent is None)
        return self._propagate_variable(self.parent, var)

    def dependencies(self):
        if 'primitive' in self.element and self.element['primitive'] == '`':
            return self.leftchild.dependencies() | self.rightchild.dependencies()
        elif 'impure_function' in self.element:
            return {self.element['impure_function']}
        elif 'pure_function' in self.element:
            return {self.element['pure_function']}
        else:
            return set()
    
    def _replace_function_call_with_node(self, fname, node, copy = False):
        result = self.copy() if copy else self
        if 'primitive' in self.element and self.element['primitive'] == '`':
            result.leftchild = self.leftchild._replace_function_call_with_node(fname, node)
            result.rightchild = self.rightchild._replace_function_call_with_node(fname, node)
        elif 'impure_function' in self.element and self.element['impure_function'] == fname:
            if copy:
                result = node.copy()
                result.parent = self.parent
                return result
            else:
                return node
        elif 'pure_function' in self.element and self.element['pure_function'] == fname:
            if copy:
                result = node.copy()
                result.parent = self.parent
                return result
            else:
                return node
        return result

    """
    def eliminate_recursion(self, fname):
        var = 'f'

        recursive_call = FunctionNode(None, {'primitive': '`'})
        recursive_call.leftchild = FunctionNode(recursive_call, {'variable': var})
        recursive_call.rightchild = FunctionNode(recursive_call, {'variable': var})

        non_recursive = self._replace_function_call_with_node(fname, recursive_call, copy=True).propagate_variable(var)

        appl = FunctionNode(self.parent, {'primitive': '`'})
        appl.leftchild = appl.rightchild = non_recursive
        non_recursive.parent = appl

        return appl
    """
    
    def eliminate_recursion(self, fname):
        var = 'f'

        var_node = FunctionNode(None, {'variable': var})

        non_recursive = self._replace_function_call_with_node(fname, var_node, copy=True).propagate_variable(var)

        appl = FunctionNode(self.parent, {'primitive': '`'})
        appl.rightchild = non_recursive
        self.parent = appl
        
        appl.leftchild = FunctionNode(appl, {'pure_function': 'Y'})

        return appl

    def replace_function(self, fname, node):
        return self._replace_function_call_with_node(fname, node)
    
    def to_unlambda(self):
        if 'primitive' in self.element:
            if self.element['primitive'] == '`':
                return '`' + self.leftchild.to_unlambda() + self.rightchild.to_unlambda()
            else:
                return self.element['primitive']
        elif 'variable' in self.element:
            return '$' + self.element['variable']
        elif 'impure_function' in self.element:
            return '[' + self.element['impure_function'] + ']'
        elif 'pure_function' in self.element:
            return '<' + self.element['pure_function'] + '>'
        else:
            raise RuntimeError(f"Unexpected element {self.element}")

    def copy(self, parent=None):
        result = FunctionNode(parent, self.element.copy())
        if self.leftchild is not None:
            result.leftchild = self.leftchild.copy(parent = result)
        if self.rightchild is not None:
            result.rightchild = self.rightchild.copy(parent = result)
        return result

    @staticmethod
    def build(name, body):
        def find_next_unfilled(tree):
            if tree is not None and 'primitive' in tree.element and tree.element['primitive'] == '`':
                if tree.leftchild is None:
                    return tree
                else:
                    left_leaf = find_next_unfilled(tree.leftchild)
                    if left_leaf is not None:
                        return left_leaf
                if tree.rightchild is None:
                    return tree
                else:
                    right_leaf = find_next_unfilled(tree.rightchild)
                    if right_leaf is not None:
                        return right_leaf
            # All other cases
            return None

        if not body:
            raise CompileException(f"Function '{name}' has an empty body")
        
        root_node = FunctionNode(None, body[0])
        body = body[1:]
        while body:
            appl = find_next_unfilled(root_node)
            if appl is None:
                raise CompileException(f"Function '{name}' has insufficient function application operators")
            next_node = FunctionNode(appl, body[0])
            if appl.leftchild is None:
                appl.leftchild = next_node
            elif appl.rightchild is None:
                appl.rightchild = next_node
            else:
                raise RuntimeError("Tried to add child to filled node!")

            body = body[1:]

        return root_node

class UnxCompiler:

    """
    Convert a string in UNX format to UnLambda
    """
    def compile(self, unx):
        import networkx as nx
        # TODO: Implement file inclusion
        # TODO: Implement <n> builtins

        self.function_trees = {}
        self.function_dependencies = {}

        # Stage 0: Flatten unx['definitions']
        unx_definitions = [f['function'] for f in unx['definitions']]

        # Stage 1: parse functions to tree format
        for function in unx_definitions:
            fname = function['name']['pure_function'] if 'pure_function' in function['name'] else function['name']['impure_function']
            function['tree'] = FunctionNode.build(fname, function['body'])
        
        # Stage 2: Validity checks
        for function in unx_definitions:
            fname = function['name']['pure_function'] if 'pure_function' in function['name'] else function['name']['impure_function']
            if not function['tree'].is_complete():
                raise CompileException(f"Function '{fname}' has an incomplete definition (you might have too many ` operators)")
            undeclared_vars = function['tree'].get_vars() - (set(function['variables']) if 'variables' in function else set())
            if undeclared_vars:
                raise CompileException(f"Function '{fname}' has undeclared variables {sorted(undeclared_vars)}")
            if 'pure_function' in function['name'] and not function['tree'].is_pure():
                raise CompileException(f"Function '{fname}' is declared as pure, but contains potential impurity")
        
        # Stage 3: Variable expansion
        for function in unx_definitions:
            if 'variables' not in function:
                continue
            for var in reversed(function['variables']):
                function['tree'] = function['tree'].propagate_variable(var)
        
        # Stage 4: Recursive function expansion
        for function in unx_definitions:
            fname = function['name']['pure_function'] if 'pure_function' in function['name'] else function['name']['impure_function']
            if fname in function['tree'].dependencies():
                function['tree'] = function['tree'].eliminate_recursion(fname)

        # Stage 5: Check for duplicate function names
        for function in unx_definitions:
            fname = function['name']['pure_function'] if 'pure_function' in function['name'] else function['name']['impure_function']
            if fname in self.function_trees:
                raise LinkException(f"Function '{fname}' is defined twice")
            self.function_trees[fname] = function['tree']
        
        # Stage 6: Build dependency graph
        dep_graph = nx.DiGraph()
        for fname, tree in self.function_trees.items():
            self.function_dependencies[fname] = tree.dependencies()
            dep_graph.add_edges_from(list((fname, dep) for dep in self.function_dependencies[fname]))
        
        # Stage 6.5: Insert <n>s. Note that these depend on <inc> and <m> being defined, with m < n
        if 'inc' in self.function_trees:
            declared_numbers = [int(x) for x in self.function_trees if x.isnumeric()]
            all_numbers = [int(x) for x in dep_graph if x.isnumeric()]
            if declared_numbers:
                base_number = min(declared_numbers)
                base_number_name = str(base_number)
                for num in set(all_numbers) - set(declared_numbers):
                    fname = str(num)
                    if num < base_number:
                        raise CompileException(f"Cannot insert <{num}>. Lowest declared number is {base_number}")
                    appls = [FunctionNode(None, {'primitive': '`'}) for _ in range(base_number, num)]
                    for i in range(len(appls) - 1):
                        appls[i + 1].parent = appls[i]
                        appls[i].rightchild = appls[i+1]
                    for appl in appls:
                        appl.leftchild = FunctionNode(appl, {'pure_function': 'inc'})
                    appls[-1].rightchild = FunctionNode(appls[-1], {'pure_function': base_number_name})
                    self.function_trees[fname] = appls[0]
                    self.function_dependencies[fname] = {'inc', base_number_name}

                    dep_graph.add_edges_from([(fname, 'inc'), (fname, base_number_name)])

        # Stage 7: Check dependency graph
        if not nx.is_directed_acyclic_graph(dep_graph):
            raise LinkException(f"There is a cyclic dependency '" + "' -> '".join(e[0] for e in nx.find_cycle(dep_graph)) + "'")
        undeclared_fns = set(dep_graph.nodes) - set(self.function_trees.keys())
        if undeclared_fns:
            raise LinkException(f"Functions {sorted(undeclared_fns)} are not declared")

        # Stage 8: Expand functions
        for fname in self.function_trees:
            for dep in self.function_dependencies[fname]:
                self.function_trees[fname] = self.function_trees[fname].replace_function(dep, self.function_trees[dep])
        
        # Stage 9: Check for main function
        if 'main' not in self.function_trees:
            raise LinkException(f"No main function found")

        # Stage 10: Flatten function tree to Unlambda
        result = self.function_trees['main'].to_unlambda()
        print(f"Compiled {len(self.function_trees)} functions to {len(result)} symbols")
        return result
    
    def compileFile(self, file):
        from . import UnxParser

        return self.compile(UnxParser().parseFile(file, parseAll=True).asDict())