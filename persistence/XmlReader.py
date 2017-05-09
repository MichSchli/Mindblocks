class XmlReader:

    # Temporary
    def pop_symbol(self, lines, expect_value=False, start_index=0):
        scanner = start_index
        if expect_value:
            while lines[scanner] != "<":
                scanner += 1
            symbol = lines[start_index:scanner].strip()
            return symbol, [], scanner
        else:
            while lines[scanner] != ">":
                scanner += 1
            scanner += 1
            symbol = lines[start_index:scanner].strip()

        parts = symbol[1:-1].split(' ')

        name = parts[0]
        attributes = dict([tuple(att.split("=")) for att in parts[1:]])

        return name, attributes, scanner