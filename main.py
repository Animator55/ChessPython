import tkinter as tk

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess in Tkinter")
        
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        
        self.selected = None  # Initialize the selected attribute here
        self.turn = 1
        
        self.draw_board()
        self.pieces = self.load_pieces()
        self.board = self.initialize_board()
        self.draw_pieces()
        
        self.canvas.bind("<Button-1>", self.select_piece)
    
    def draw_board(self):
        colors = ["#DDB88C", "#A66D4F"]  # Shades of brown
        for row in range(8):
            for col in range(8):
                # If the square is the selected one, change its color
                if self.selected == (row, col):
                    color = "#44DD00"  # Highlight color
                else:
                    color = colors[(row + col) % 2]
                
                x0, y0 = col * 50, row * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
    
    def load_pieces(self):
        return {
            "P": "♙", "p": "♟", "T": "♖", "t": "♜",
            "C": "♘", "c": "♞", "A": "♗", "a": "♝",
            "Q": "♕", "q": "♛", "R": "♔", "r": "♚"
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
    
    def draw_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    x, y = col * 50 + 25, row * 50 + 25
                    self.canvas.create_text(x, y, text=self.pieces[piece], font=("Arial", 24), tags="piece")

    
    def select_piece(self, event):
        col, row = event.x // 50, event.y // 50
        if self.selected is None:
            if self.board[row][col]:
                pieceColor = "white" if self.board[row][col].lower() == self.board[row][col] else "black"
                if (self.turn == 0 and pieceColor == "white") or (self.turn == 1 and pieceColor == "black"):
                    self.selected = (row, col)
        else:
            selected_row, selected_col = self.selected
            piece = self.board[selected_row][selected_col] # original selected
            pieceColor = "white" if piece.lower() == piece else "black"
            otherPieceColor = "white" if self.board[row][col].lower() == self.board[row][col] else "black"
            if(self.board[row][col] == "") or (pieceColor != otherPieceColor):
                self.board[row][col] = piece
                self.board[selected_row][selected_col] = ""
                self.selected = None
                self.turn = 1 if self.turn == 0 else 0
            else:
                if row == selected_row and col == selected_col: 
                    self.selected = None
                else: 
                    self.selected = (row, col)
        self.draw_board()  # Redraw the board after selection/move
        self.draw_pieces()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()