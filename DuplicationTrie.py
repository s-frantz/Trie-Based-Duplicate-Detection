class DuplicationTrie:
    """Duplicate Detection Using A Search Trie"""
    head = {
        #character1: {character 2a: {...}, character 2b: {...}}
    }
    duplicates = {
        #term: [oid1, oid2]
    }
    def Store(self, charString, oid):
        currentNode = self.head
        for char in charString:
            if char not in currentNode:
                currentNode[char] = {}
            currentNode = currentNode[char]
        if True in currentNode:
            duplicationRecord = currentNode[True]
            count = duplicationRecord[0] + 1
            if count == 2:
                firstInstanceOid = duplicationRecord[1]
                self.duplicates[charString] = [firstInstanceOid]
            currentNode[True] = [count]
            self.duplicates[charString].append(oid)
        else:
            currentNode[True] = [1, oid]

    def Report(self):
        import sys
        sys.path.append(r'\\ace-ra-fs1\data\GIS\_Dev\python\apyx')
        from apyx import JsonPrettyPrint
        JsonPrettyPrint(self.duplicates)
        return self.duplicates