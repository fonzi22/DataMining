from collections import defaultdict

class PrefixSpan:
    def __init__(self, min_support):
        self.min_support = min_support
        self._frequent_sequences = {}
        
    def _find_frequent_items(self, sequences):
        """Tìm các item xuất hiện với tần suất >= min_support"""
        items = defaultdict(int)
        for sequence in sequences:
            # Lấy unique items trong mỗi sequence để đếm support
            unique_items = set(item for itemset in sequence for item in itemset)
            for item in unique_items:
                items[item] += 1
        return {item: count for item, count in items.items() 
                if count >= self.min_support}
    
    def _project_database(self, sequences, prefix):
        """Tạo projected database cho một prefix"""
        projected = []
        for sequence in sequences:
            # Tìm vị trí của prefix trong sequence
            i = 0
            for item in prefix:
                found = False
                while i < len(sequence):
                    if item in sequence[i]:
                        found = True
                        i += 1
                        break
                    i += 1
                if not found:
                    break
            else:
                # Nếu tìm thấy prefix, thêm phần còn lại vào projected database
                if i < len(sequence):
                    projected.append(sequence[i:])
        return projected
    
    def mine_sequential_patterns(self, sequences):
        """Khai thác các mẫu tuần tự"""
        self._frequent_sequences = {}
        
        # Tìm các item phổ biến đầu tiên
        frequent_items = self._find_frequent_items(sequences)
        
        # Với mỗi item phổ biến, tạo prefix và đệ quy
        for item, support in frequent_items.items():
            prefix = [(item,)]
            self._frequent_sequences[tuple(prefix)] = support
            self._mine_rec(prefix, sequences, support)
            
        return self._frequent_sequences
    
    def _mine_rec(self, prefix, sequences, prefix_support):
        """Đệ quy khai thác các mẫu với prefix cho trước"""
        # Project database với prefix hiện tại
        projected = self._project_database(sequences, prefix[-1])
        if not projected:
            return
        
        # Tìm các item phổ biến trong projected database
        frequent_items = self._find_frequent_items(projected)
        
        # Với mỗi item phổ biến, mở rộng prefix
        for item, support in frequent_items.items():
            new_prefix = prefix + [(item,)]
            self._frequent_sequences[tuple(new_prefix)] = support
            self._mine_rec(new_prefix, projected, support)
