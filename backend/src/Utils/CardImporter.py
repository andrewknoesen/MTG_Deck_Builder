from pprint import pprint
class CardImporter:
    def __init__(self) -> None:
        pass
    
    def split_string_to_list(self, s: str) -> list[str]:
        return [line.strip() for line in s.split('\n') if line.strip().lower() != 'deck' and line.strip().lower() != 'sideboard' and line != '\n']
    
    def read_text_file(self, path: str) -> list[str]:
        with open(path) as f:
            s: list[str] = f.readlines()
            
        return [line.strip() for line in s if line.strip().lower() != 'deck' and line.strip().lower() != 'sideboard' and line != '\n']
    
    def import_mtgo(self, string: str| None = None, path: str| None = None ) -> list[dict]|None:        
        if string is None and path is None:
            return None
        if isinstance(string, str) and isinstance(path, str):
            return None
        
        if path is not None: 
            lines = self.read_text_file(path)
            
        if string is not None:
            lines = self.split_string_to_list(string)
            
        deck_list = []
        d = dict({})
        
        for line in lines:
            l = line.split(' ', 1)
            
            if l[1] not in d.keys():
                d[l[1]] = int(l[0])
            else:
                d[l[1]] += int(l[0])
            
            
        for k,v in d.items():
            deck_list.append({
                'name': k,
                'qty': v
            })    
        
        return deck_list
    
    
def main():
    ci = CardImporter()
    ci.import_mtgo(path = './import_test.txt')
    
    
    
if __name__ == "__main__":
    main()