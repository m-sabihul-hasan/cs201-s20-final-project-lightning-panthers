
# BufferTree node
class BufferTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []
        self.buffer=[]


class BufferTree:
    def __init__(self, t):
        self.root = BufferTreeNode(True)
        self.t = t
        self.nodeswithbuffer = dict()

    # Insert a key
    def insert(self, k):
        root = self.root
        if len(root.keys) == (4 * self.t) - 1:
            temp = BufferTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    # Insert non full
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (4 * self.t) - 1:
                self.split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    # Split the child
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BufferTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (4 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 4 * t]
            y.child = y.child[0: t]

    # Delete a node
    def delete(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k[0] > x.keys[i][0]:
            i += 1
        if x.leaf:
            if i < len(x.keys) and x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        if i < len(x.keys) and x.keys[i][0] == k[0]:
            return self.delete_internal_node(x, k, i)
        elif len(x.child[i].keys) >= t:
            self.delete(x.child[i], k)
        else:
            if i != 0 and i + 2 < len(x.child):
                if len(x.child[i - 1].keys) >= t:
                    self.delete_sibling(x, i, i - 1)
                elif len(x.child[i + 1].keys) >= t:
                    self.delete_sibling(x, i, i + 1)
                else:
                    self.delete_merge(x, i, i + 1)
            elif i == 0:
                if len(x.child[i + 1].keys) >= t:
                    self.delete_sibling(x, i, i + 1)
                else:
                    self.delete_merge(x, i, i + 1)
            elif i + 1 == len(x.child):
                if len(x.child[i - 1].keys) >= t:
                    self.delete_sibling(x, i, i - 1)
                else:
                    self.delete_merge(x, i, i - 1)
            self.delete(x.child[i-1], k)

    # Delete internal node
    def delete_internal_node(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
                return
            return

        if len(x.child[i].keys) >= t:
            x.keys[i] = self.delete_predecessor(x.child[i])
            return
        elif len(x.child[i + 1].keys) >= t:
            x.keys[i] = self.delete_successor(x.child[i + 1])
            return
        else:
            self.delete_merge(x, i, i + 1)
            self.delete_internal_node(x.child[i], k, self.t - 1)

    # Delete the predecessor
    def delete_predecessor(self, x):
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.child[n].keys) >= self.t:
            self.delete_sibling(x, n + 1, n)
        else:
            self.delete_merge(x, n, n + 1)
        self.delete_predecessor(x.child[n])

    # Delete the successor
    def delete_successor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.child[1].keys) >= self.t:
            self.delete_sibling(x, 0, 1)
        else:
            self.delete_merge(x, 0, 1)
        self.delete_successor(x.child[0])

    # Delete resolution
    def delete_merge(self, x, i, j):
        cnode = x.child[i]

        if j > i:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            new = cnode
            x.keys.pop(i)
            x.child.pop(j)
        else:
            lsnode = x.child[j]
            lsnode.keys.append(x.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[i])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            new = lsnode
            x.keys.pop(j)
            x.child.pop(i)

        if x == self.root and len(x.keys) == 0:
            self.root = new

    # Delete the sibling
    def delete_sibling(self, x, i, j):
        cnode = x.child[i]
        if i < j:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            x.keys[i] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = x.child[j]
            cnode.keys.insert(0, x.keys[i - 1])
            x.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())

    # Print the tree
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=" : ")
        for i in x.keys:
            print(i[0], end=", ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)
    
    def inorder(self,x, topr):
        if not x.leaf:
            for i in range(len(x.child)):
                self.inorder(x.child[i], topr)
                if i < len(x.keys):
                    topr.append(x.keys[i][0])#, end=", ")
        else:
            for k in x.keys:
                topr.append(k[0])#, end=", ")

    def bufferempty(self, x):
        if x.child != []:
            for i in x.buffer:
                for j in range(len(x.keys)):
                    if i[0] < x.keys[j][0]:
                        x.child[j].buffer.append(i)
                        
                        for k in self.nodeswithbuffer:
                            if x in self.nodeswithbuffer[k]:
                                if k+1 in self.nodeswithbuffer:
                                    self.nodeswithbuffer[k+1].add(x.child[j])
                                    break
                                else:
                                    self.nodeswithbuffer[k+1] = {x.child[j]}
                                    break
                                

                    elif j == len(x.keys) - 1:
                        x.child[j+1].buffer.append(i)
                        for k in self.nodeswithbuffer:
                            if x in self.nodeswithbuffer[k]:
                                if k+1 in self.nodeswithbuffer:
                                    self.nodeswithbuffer[k+1].add(x.child[j+1])
                                    break
                                else:
                                    self.nodeswithbuffer[k+1] = {x.child[j+1]}
                                    break
            x.buffer = []
        else:
            while x.buffer != []:
                a = x.buffer.pop(0)
                if a[1] == "i":
                    self.insert((a[0],))
                elif a[1] == "d":
                    self.delete(self.root, (a[0],))
                
                

    def bufferinsert(self, b):
        b = [b]
        x = self.root
        self.nodeswithbuffer[0] = {x}
        for i in b:
            if len(x.buffer) == 3:
                self.bufferempty(x)
                x=self.root
            x.buffer.append(i)
    
    def emptyallbuffers(self):
        while not self.checkifbufferempty():
            for i in self.nodeswithbuffer.copy():
                for j in self.nodeswithbuffer[i].copy():
                    self.bufferempty(j)
                    self.nodeswithbuffer[i].remove(j)

    def checkifbufferempty(self):
        for i in self.nodeswithbuffer:
            for j in self.nodeswithbuffer[i]:
                if j.buffer != []:
                    return False
        return True

    def search(self, b, x):
        if (b,) in x.keys or (b,"i") in x.buffer or (b,"d") in x.buffer:
                return True
        if x.child != []:
            for i in range(len(x.keys)):
                if b < x.keys[i][0]:
                    return self.search(b, x.child[i])
                elif i == len(x.keys) - 1:
                    return self.search(b, x.child[i+1])
        return False

def main():
    B = BufferTree(2)

    #for i in range(10):
    #    B.insert((i, 2 * i))

    a = [8, 9, 10, 11, 15, 16, 17, 18, 20, 23,24, 1, 7, 5, 3, 6, 2, 4, 14, 12, 13]
    for i in a:
        B.bufferinsert((i, "i"))

    #print(B.search(4.5,B.root))
    B.emptyallbuffers()
    #B.print_tree(B.root)
    topr = []
    B.inorder(B.root, topr)
    print(topr)

#main()
