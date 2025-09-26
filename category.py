class Category:
    def __init__(self, name, items):
        self.name = name
        self.items = items  

    def binary_search(self, target, key='name'):
        low, high = 0, len(self.items) - 1
        while low <= high:
            mid = (low + high) // 2

            if key == "name":
                mid_val = self.items[mid].name
            elif key == "price":
                mid_val = self.items[mid].price
            elif key == "brand":
                mid_val = self.items[mid].brand
            elif key == "model_year":
                mid_val = self.items[mid].model_year
            else:
                return None

            if mid_val == target:
                return self.items[mid]
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def bubble_sort(self, ascending=True, key='price'):
        n = len(self.items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if key == "name":
                    val1, val2 = self.items[j].name, self.items[j + 1].name
                elif key == "price":
                    val1, val2 = self.items[j].price, self.items[j + 1].price
                elif key == "brand":
                    val1, val2 = self.items[j].brand, self.items[j + 1].brand
                elif key == "model_year":
                    val1, val2 = self.items[j].model_year, self.items[j + 1].model_year
                else:
                    continue

                if (val1 > val2 and ascending) or (val1 < val2 and not ascending):
                    self.items[j], self.items[j + 1] = self.items[j + 1], self.items[j]

    def add_item(self, item):
        self.items.append(item)
        return True

    def update_item(self, old_name, new_item):
        for i, itm in enumerate(self.items):
            if itm.name == old_name:
                self.items[i] = new_item
                return True
        return False

    def delete_item(self, item_name):
        for i, itm in enumerate(self.items):
            if itm.name == item_name:
                self.items.pop(i)
                return True
        return False
