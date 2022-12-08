from typing import Literal


def part_1(dirs):
    return sum([d.size for d in dirs if d.size <= 100_000])


def part_2(root, dirs):
    file_system_space = 70_000_000
    required_space = 30_000_000
    occupied_space = root.size
    free_space = file_system_space - occupied_space
    lacking_space = required_space - free_space

    if lacking_space <= 0:
        return 0
    
    return min(map(lambda folder: folder.size, filter(lambda folder: folder.size >= lacking_space, dirs)))


def build_tree(file_name):
    root = Node('/', 'dir', None)
    dirs = [root]
    cwd = root
    discovering = False

    with open(file_name) as f:
        while line := f.readline().strip():
            if line.startswith('$ '):
                tokens = line[2:].split()
                if len(tokens) == 2 and tokens[0] == 'cd':
                    if discovering:
                        cwd.discovered = True
                        discovering = False
                    cwd = resolve_dir(tokens[1], cwd, root)
                elif tokens[0] == 'ls':
                    discovering = True
            else:
                name, kind, size = parse_item(line)
                cwd.add_child(name, kind, size)
                if kind == 'dir':
                    child = cwd.get_child(name, kind)
                    dirs.append(child)  
        
    if discovering:
        cwd.discovered = True

    root.calculate_size() 
    return root, dirs


def resolve_dir(to_wd, cwd, root):
    match to_wd:
        case '/':
            to_wd = root
        case '..':
            to_wd = cwd.parent
        case _:
            to_wd = cwd.get_child(to_wd, 'dir')
    return to_wd


def parse_item(description):
    tokens = description.split()
    name = tokens[1]
    kind = 'dir' if tokens[0] == 'dir' else 'file'
    size = -1 if kind == 'dir' else int(tokens[0])
    return name, kind, size


class Node:
    @staticmethod
    def _get_full_name(name, kind):
        return f'{kind}_{name}'

    def __init__(self, name: str, kind: Literal['dir', 'file'], parent, size: int =-1) -> None:
        if parent == None and name != '/':
            raise ValueError('Only root dit does not have parent directory')
        if kind != 'dir' and size == -1:
            raise ValueError('Files must contain size')
        self.name = name
        self.kind = kind
        self.parent = parent
        self.children = list()
        self.children_full_names = set()
        self.size = size
        self.discovered = False if kind == 'dir' else True
    
    def add_child(self, name, kind, size):
        child_full_name = Node._get_full_name(name, kind)
        if child_full_name not in self.children_full_names:
            self.children.append(Node(name, kind, self, size))
            self.children_full_names.add(name)
    
    def get_child(self, name, kind):
        for child in self.children:
            if child.name == name and child.kind == kind:
                return child
        raise ValueError('Child does not exist')

    def calculate_size(self):
        if self.kind == 'file':
            return
        if not self.discovered:
            raise AttributeError('Could not calculate size of undiscovered dir')

        acc = 0
        for child in self.children:
            if child.size < 0 :
                child.calculate_size()
            assert child.size >= 0
            acc += child.size
        self.size = acc

    def __repr__(self):
        parent = 'None' if self.parent is None else self.parent.name
        return f'Node({self.name}, {self.kind}, {parent}, size={self.size}, discovered={self.discovered})'
   

##############################
test_tree, test_dirs = build_tree('input_t.txt')
assert part_1(test_dirs) == 95437
assert part_2(test_tree, test_dirs) == 24933642
##############################


file_tree, dirs = build_tree('input.txt')

print(part_1(dirs))
print(part_2(file_tree, dirs))
