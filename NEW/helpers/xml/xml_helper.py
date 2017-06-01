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