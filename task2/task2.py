from trie import Trie


class Homework(Trie): 
    def __init__(self):
        # Композиція: Два незалежних Trie
        self.forward_trie = Trie() # Для префіксів 
        self.reversed_trie = Trie() # Для суфіксів

    def _find_node(self, trie_instance: Trie, key: str):
        """Знаходить кінцевий вузол для заданого ключа або повертає None."""
        current = trie_instance.root
        for char in key:
            if char not in current.children:
                return None
            current = current.children[char]
        return current

    def _count_words_in_subtree(self, node) -> int:
        """Рекурсивно рахує кількість слів, починаючи з даного вузла."""
        count = 0
        
        # Якщо вузол є кінцем слова, рахуємо його (word is stored in .value)
        if node.value is not None:
            count += 1
            
        # Рекурсивно перевіряємо всіх нащадків
        for child_node in node.children.values():
            count += self._count_words_in_subtree(child_node)
            
        return count

    def put(self, key, value=None):
        # 1. Вставляємо в пряме дерево
        self.forward_trie.put(key, value)
        # 2. Вставляємо в обернене дерево
        self.reversed_trie.put(key[::-1], value)

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str) or not prefix:
             raise TypeError(f"Illegal argument for has_prefix: prefix = {prefix} must be a non-empty string")

        node = self._find_node(self.forward_trie, prefix)
        return node is not None

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str) or not pattern:
            return 0

        reversed_pattern = pattern[::-1]

        current_node = self._find_node(self.reversed_trie, reversed_pattern)
        
        if current_node is None:
            return 0 

        return self._count_words_in_subtree(current_node)


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
