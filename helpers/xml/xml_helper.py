class XmlHelper:

    def get_header(self, name, fields={}, indentation=0):
        string = "<"+name

        if fields != {}:
            string += " " + " ".join([str(k)+"="+str(v) for k,v in fields.items()])

        string += ">"

        return self.add_indentation(string, indentation)

    def get_footer(self, name, indentation=0):
        return self.add_indentation("</"+name+">", indentation)

    def add_indentation(self, string, indentation):
        indentation = '\t' * indentation
        return indentation + string

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