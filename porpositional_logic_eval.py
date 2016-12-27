import operator as op


class BinaryTree:
    def __init__(self, rootObj):
        self.key = rootObj
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self, newNode):
        if self.leftChild == None:
            t = BinaryTree(newNode)
            self.leftChild = t
            t.parent = self
        else:
            t = BinaryTree(newNode)
            t.parent = self
            t.leftChild = self.leftChild
            self.leftChild.parent = t
            self.leftChild = t

    def insertRight(self, newNode):
        if self.rightChild == None:
            t = BinaryTree(newNode)
            self.rightChild = t
            t.parent = self
        else:
            t = BinaryTree(newNode)
            t.parent = self
            t.rightChild = self.rightChild
            self.rightChild.parent = t
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def getParent(self):
        return self.parent

    def getRootVal(self):
        return self.key

    def setRootVal(self, obj):
        self.key = obj

    def setLeftChild(self, nodeObj):
        self.leftChild = nodeObj

    def setRightChild(self, nodeObj):
        self.rightChild = nodeObj

    def setParent(self, nodeObj):
        self.parent = nodeObj

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRoot(self):
        return


def inorder_traversal(tree):
    if tree:
        inorder_traversal(tree.getLeftChild())
        print(tree.getRootVal())
        inorder_traversal(tree.getRightChild())


implication = lambda x, y: op.or_(op.not_(x), y)


def build_parse_tree(exp):
    exp_list = exp.replace('(', ' ( ').replace(')', ' ) ').replace('~', ' ~ ').split()
    e_tree = BinaryTree('')
    current_tree = e_tree
    cnt = 0
    for token in exp_list:
        if token == '(':
            current_tree.insertLeft('')
            current_tree = current_tree.getLeftChild()
        elif token in ['||', '&&', '->']:
            if current_tree.getRootVal() == '~':
                current_tree.getParent().setRootVal(token)
                current_tree.insertRight('')
                current_tree = current_tree.getRightChild()
            else:
                current_tree.setRootVal(token)
                current_tree.insertRight('')
                current_tree = current_tree.getRightChild()
        elif token in ['1', '0']:
            current_tree.setRootVal(bool(int(token)))
            current_tree = current_tree.getParent()
            if current_tree.getRootVal() == '~':
                current_tree = current_tree.getParent()
        elif token == '~':
            current_tree.setRootVal('~')
            current_tree.insertLeft('')
            current_tree = current_tree.getLeftChild()
        elif token == ')':
            current_tree = current_tree.getParent()
        else:
            raise ValueError
        cnt += 1
    return e_tree


def evaluate_parse_tree(tree):
    opers = {'||': op.or_, '&&': op.and_, '~': op.not_, '->': implication}
    leftT = tree.getLeftChild()
    rightT = tree.getRightChild()
    if leftT and not rightT:
        fn = opers[tree.getRootVal()]
        return fn(evaluate_parse_tree(leftT))
    elif leftT and rightT:
        fn = opers[tree.getRootVal()]
        return fn(evaluate_parse_tree(leftT), evaluate_parse_tree(rightT))
    else:
        return tree.getRootVal()
