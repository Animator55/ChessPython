import tkinter as tk

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess in Tkinter")
        
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        
        self.selected = None  
        self.turn = 0
        
        self.draw_board()
        self.pieces = self.load_pieces()
        self.board = self.initialize_board()
        self.draw_pieces()
        
        self.canvas.bind("<Button-1>", self.select_piece)
    
    def draw_board(self):
        colors = ["#DDB88C", "#A66D4F"]  
        for row in range(8):
            for col in range(8):
                
                piece = ""
                boolean = False
                if self.selected :
                    piece = self.board[self.selected[0]][self.selected[1]]
                    boolean = True if self.is_legal_move(piece, self.selected[0],self.selected[1], row, col) else False
                if self.selected == (row, col):
                    color = "#44DD00"  
                else:
                    color = colors[(row + col) % 2]
                
                if boolean: 
                    color = "#d11" if (self.get_color(piece) != self.get_color(self.board[row][col]) 
                        and self.board[row][col] != "") else "#d60"
                
                x0, y0 = col * 50, row * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
    
    def load_pieces(self):
        return {
            "P": "♟", "p": "♟", "T": "♜", "t": "♜",
            "C": "♞", "c": "♞", "A": "♝", "a": "♝",
            "Q": "♛", "q": "♛", "R": "♚", "r": "♚"
        }
    
    def initialize_board(self):
        return [
            ["T", "C", "A", "Q", "R", "A", "C", "T"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["t", "c", "a", "q", "r", "a", "c", "t"]
        ]
    def is_legal_move(self, piece, start_row, start_col, end_row, end_col):
        moves = {
        "p": [[-1, 0], [-1, -1], [-1, 1], [-2, 0]],  
        "P": [[1, 0], [1, -1], [1, 1], [2, 0]],  
            "t": [[i, 0] for i in range(1, 8)] + [[-i, 0] for i in range(1, 8)] +
                [[0, i] for i in range(1, 8)] + [[0, -i] for i in range(1, 8)],  
            "T": [[i, 0] for i in range(1, 8)] + [[-i, 0] for i in range(1, 8)] +
                [[0, i] for i in range(1, 8)] + [[0, -i] for i in range(1, 8)],  
            "c": [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]],  
            "C": [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]],  
            "a": [[i, i] for i in range(1, 8)] + [[-i, -i] for i in range(1, 8)] +
                [[i, -i] for i in range(1, 8)] + [[-i, i] for i in range(1, 8)],  
            "A": [[i, i] for i in range(1, 8)] + [[-i, -i] for i in range(1, 8)] +
                [[i, -i] for i in range(1, 8)] + [[-i, i] for i in range(1, 8)],  
            "q": [[i, 0] for i in range(1, 8)] + [[-i, 0] for i in range(1, 8)] +
                [[0, i] for i in range(1, 8)] + [[0, -i] for i in range(1, 8)] +
                [[i, i] for i in range(1, 8)] + [[-i, -i] for i in range(1, 8)] +
                [[i, -i] for i in range(1, 8)] + [[-i, i] for i in range(1, 8)],  
            "Q": [[i, 0] for i in range(1, 8)] + [[-i, 0] for i in range(1, 8)] +
                [[0, i] for i in range(1, 8)] + [[0, -i] for i in range(1, 8)] +
                [[i, i] for i in range(1, 8)] + [[-i, -i] for i in range(1, 8)] +
                [[i, -i] for i in range(1, 8)] + [[-i, i] for i in range(1, 8)],  
            "r": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]],  
            "R": [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]  
        }

        
        delta_row = end_row - start_row
        delta_col = end_col - start_col

        if [delta_row, delta_col] not in moves.get(piece, []):
            return False  

        
        destination_piece = self.board[end_row][end_col]
        if piece.lower() == "p":
            if delta_col != 0 and (not destination_piece or piece.isupper() == destination_piece.isupper()):
                return False  
            if delta_col == 0 and destination_piece:
                return False  
            if abs(delta_row) == 2:  
                initial_row = 1 if piece == "P" else 6
                if start_row != initial_row or self.board[start_row + delta_row // 2][start_col]:
                    return False  


        
        if piece.lower() in "taq":  
            step_row = 1 if delta_row > 0 else -1 if delta_row < 0 else 0
            step_col = 1 if delta_col > 0 else -1 if delta_col < 0 else 0

            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if self.board[current_row][current_col]:  
                    return False  
                current_row += step_row
                current_col += step_col

        if destination_piece and (piece.isupper() == destination_piece.isupper()):
            return False  

        return True  



    def draw_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    x, y = col * 50 + 25, row * 50 + 25
                    color = "#f3f3f3" if self.get_color(piece) == "white" else "#000"
                    self.canvas.create_text(x, y, text=self.pieces[piece], fill=color, font=("Arial", 24), tags="piece")

    def get_color(self, piece): 
        if piece == "": return ""
        return "white" if piece.lower() == piece else "black"

    def draw_drop_places(self):
        self.canvas.delete("piece")
        selected_row, selected_col = self.selected
        piece = self.board[selected_row][selected_col]

        for row in range(8):
            for col in range(8):
                if (self.is_legal_move(piece, selected_row, selected_col, row, col)) :
                    x, y = col * 50 + 25, row * 50 + 25
                    self.canvas.create_text(x, y, text="", font=("Arial", 24), tags="place")


    
    def select_piece(self, event):
        col, row = event.x // 50, event.y // 50
        if self.selected is None:
            if self.board[row][col]:
                pieceColor = self.get_color(self.board[row][col])
                if (self.turn == 0 and pieceColor == "white") or (self.turn == 1 and pieceColor == "black"):
                    self.selected = (row, col)
        else:
            selected_row, selected_col = self.selected
            piece = self.board[selected_row][selected_col] 
            
            pieceColor = self.get_color(piece)
            if(self.is_legal_move(piece, selected_row, selected_col, row, col)):
                self.board[row][col] = piece
                self.board[selected_row][selected_col] = ""
                self.selected = None
                self.turn = 1 if self.turn == 0 else 0
            else:
                self.selected = None
        self.draw_board()  
        self.draw_pieces()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()