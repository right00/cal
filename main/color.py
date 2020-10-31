

class Colors():
    colors = ["black","gray","silver","blue","navy","aqua","teal","lime","green",
            "yellowgreen","yellow","olive","orange","red","maroon","fuchsia","purple"]
    def get_color(self):
        return self.colors

    def get_color_num(self,color):
        return self.colors.index(color)
    
    def get_len(self):
        return len(self.colors)
