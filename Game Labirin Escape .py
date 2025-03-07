import turtle
import time
import random

# Setup screen
window = turtle.Screen()
window.bgcolor("salmon")
window.title("A Maze Game")
window.setup(1300, 700)

# Global Variables
start_position_x = 0
start_position_y = 0
end_position_x = 0
end_position_y = 0
solver_in_progress = False

# Classes for different elements
class GamePlayer(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.speed(0)

class Wall(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)

class PathMarker(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)

class BacktrackMarker(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.setheading(270)
        self.penup()
        self.speed(0)

class SolutionMarker(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(0)

import turtle
import time
import random

# Konfigurasi layar utama
window = turtle.Screen()
window.bgcolor("salmon")  # Warna latar belakang
window.title("A Maze Game")  # Judul game
window.setup(1300, 700)  # Ukuran layar

# Variabel global
start_position_x = 0  # Posisi awal pemain (koordinat x)
start_position_y = 0  # Posisi awal pemain (koordinat y)
end_position_x = 0  # Posisi akhir/labirin keluar (koordinat x)
end_position_y = 0  # Posisi akhir/labirin keluar (koordinat y)
solver_in_progress = False  # Status apakah solver algoritma sedang berjalan

# Kelas untuk berbagai elemen dalam permainan
class GamePlayer(turtle.Turtle):  
    def __init__(self):
        super().__init__()
        self.shape("circle")  # Bentuk karakter pemain
        self.color("white")  # Warna karakter pemain
        self.penup()  # Nonaktifkan jejak pena
        self.speed(0)  # Kecepatan pergerakan pemain

class Wall(turtle.Turtle):  
    def __init__(self):
        super().__init__()
        self.shape("square")  # Bentuk dinding
        self.color("blue")  # Warna dinding
        self.penup()
        self.speed(0)

class PathMarker(turtle.Turtle):  
    def __init__(self):
        super().__init__()
        self.shape("square")  # Bentuk penanda jalur
        self.color("green")  # Warna penanda jalur
        self.penup()
        self.speed(0)

class BacktrackMarker(turtle.Turtle):  
    def __init__(self):
        super().__init__()
        self.shape("square")  # Bentuk penanda backtracking
        self.color("red")  # Warna backtracking
        self.setheading(270)
        self.penup()
        self.speed(0)

class SolutionMarker(turtle.Turtle):  
    def __init__(self):
        super().__init__()
        self.shape("square")  # Bentuk penanda solusi
        self.color("yellow")  # Warna penanda solusi
        self.penup()
        self.speed(0)

# Fungsi untuk menghasilkan labirin besar dan lebih kompleks
def generate_maze(rows, cols):
    class MazeCell:
        def __init__(self, x, y):
            self.x, self.y = x, y  # Koordinat sel labirin
            self.visited = False  # Status apakah sel sudah dikunjungi
            self.walls = [True, True, True, True]  # Dinding: Atas, Kanan, Bawah, Kiri

    # Fungsi untuk menghapus dinding antara dua sel
    def remove_walls(current_cell, next_cell):
        dx = current_cell.x - next_cell.x
        dy = current_cell.y - next_cell.y
        if dx == 1:  # Tetangga berada di kiri
            current_cell.walls[3] = False
            next_cell.walls[1] = False
        elif dx == -1:  # Tetangga berada di kanan
            current_cell.walls[1] = False
            next_cell.walls[3] = False
        elif dy == 1:  # Tetangga berada di atas
            current_cell.walls[0] = False
            next_cell.walls[2] = False
        elif dy == -1:  # Tetangga berada di bawah
            current_cell.walls[2] = False
            next_cell.walls[0] = False

    # Membuat grid labirin
    grid = [[MazeCell(x, y) for x in range(cols)] for y in range(rows)]
    stack = []  # Tumpukan untuk proses backtracking
    current_cell = grid[0][0]  # Mulai dari sel pertama
    current_cell.visited = True

    # Algoritma untuk membentuk labirin menggunakan DFS
    while True:
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current_cell.x + dx, current_cell.y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not grid[ny][nx].visited:
                neighbors.append(grid[ny][nx])

        if neighbors:
            next_cell = random.choice(neighbors)  # Pilih tetangga secara acak
            remove_walls(current_cell, next_cell)  # Hapus dinding antara sel

            # Tambahkan jalur lebih panjang dengan probabilitas 70%
            if len(neighbors) > 1 and random.random() < 0.7:
                stack.append(current_cell)

            current_cell = next_cell  # Pindah ke sel berikutnya
            current_cell.visited = True
        elif stack:
            current_cell = stack.pop()  # Backtracking ke sel sebelumnya
        else:
            break

    # Konversi grid menjadi format 2D untuk tampilan
    maze_grid = [["+" for _ in range(cols * 2 + 1)] for _ in range(rows * 2 + 1)]
    for y in range(rows):
        for x in range(cols):
            cx, cy = x * 2 + 1, y * 2 + 1
            maze_grid[cy][cx] = " "
            if not grid[y][x].walls[1]:  # Kanan
                maze_grid[cy][cx + 1] = " "
            if not grid[y][x].walls[2]:  # Bawah
                maze_grid[cy + 1][cx] = " "

    # Tambahkan jalur tambahan untuk variasi
    for y in range(1, len(maze_grid) - 1, 2):
        for x in range(1, len(maze_grid[y]) - 1, 2):
            if random.random() < 0.2:  # 20% kemungkinan membuka jalur baru
                maze_grid[y][x] = " "

    # Tetapkan posisi mulai ('s') dan keluar ('e')
    maze_grid[1][1] = "s"
    maze_grid[rows * 2 - 1][cols * 2 - 1] = "e"

    # Hapus dinding pertama di bawah posisi 's'
    maze_grid[2][1] = " "

    return ["".join(row) for row in maze_grid]



# Menghasilkan labirin baru
maze = generate_maze(17, 25)
print("\n".join(maze))  # Mencetak labirin dalam format teks ke konsol

# Fungsi untuk mengatur dan menampilkan labirin pada layar menggunakan Turtle Graphics
def setup_maze(grid):
    global start_position_x, start_position_y, end_position_x, end_position_y
    path.clear()  # Menghapus jalur lama
    walls.clear()  # Menghapus daftar dinding lama
    for y in range(len(grid)):  # Iterasi melalui setiap baris grid
        for x in range(len(grid[y])):  # Iterasi melalui setiap kolom di baris
            character = grid[y][x]
            screen_x = -588 + (x * 24)  # Mengonversi koordinat grid ke posisi layar (x)
            screen_y = 288 - (y * 24)   # Mengonversi koordinat grid ke posisi layar (y)

            if character == "+":  # Jika karakter adalah dinding
                wall.goto(screen_x, screen_y)
                wall.stamp()
                walls.append((screen_x, screen_y))
            elif character == " ":  # Jika karakter adalah jalur
                path.append((screen_x, screen_y))
            elif character == "e":  # Jika karakter adalah titik akhir
                backtrack_marker.goto(screen_x, screen_y)
                backtrack_marker.stamp()
                end_position_x, end_position_y = screen_x, screen_y
                path.append((screen_x, screen_y))
            elif character == "s":  # Jika karakter adalah titik awal
                start_position_x, start_position_y = screen_x, screen_y
                player.goto(start_position_x, start_position_y)
                path_marker.goto(screen_x, screen_y)
                path_marker.stamp()
                path.append((screen_x, screen_y))


def restart_game():
    """Restart the game by generating a new maze and resetting all elements."""
    global walls, path, visited, frontier, solution, start_position_x, start_position_y, end_position_x, end_position_y, solver_in_progress

    # Clear all visual elements
    wall.clearstamps()
    backtrack_marker.clearstamps()
    path_marker.clearstamps()
    solution_marker.clearstamps()
    player.goto(0, 0)  # Reset player position to default

    # Reset data structures
    walls = []
    path = []
    visited = []
    frontier = []
    solution = {}
    solver_in_progress = False  # Reset solver state

    # Generate a new maze and set it up
    new_maze = generate_maze(12, 20)  # Generate a new maze with the same size
    setup_maze(new_maze)  # Setup the new maze

    # Print a message
    print("Game restarted with a new maze!")






# Fungsi untuk mencari solusi labirin menggunakan metode pencarian jalur
def search(x, y):
    global solver_in_progress
    
    if solver_in_progress:  # Jika solver sudah berjalan, hentikan eksekusi baru
        return
    
    solver_in_progress = True
    frontier.append((x, y))  # Mulai dari posisi awal
    solution[x, y] = x, y  # Menyimpan jalur dari posisi awal

    while len(frontier) > 0:  # Selama masih ada titik dalam frontier
        time.sleep(0.05)  # Menambahkan jeda untuk menampilkan proses pencarian
        current = frontier.pop()  # Ambil titik terakhir dari frontier
        current_x, current_y = current
        
        # Jika titik saat ini adalah titik akhir
        if (current_x, current_y) == (end_position_x, end_position_y):
            solution_marker.goto(current_x, current_y)
            solution_marker.stamp()
            print("Labirin selesai!")
            break
        
        # Tandai jalur yang sedang dijelajahi
        backtrack_marker.goto(current_x, current_y)
        backtrack_marker.stamp()

        # Mengeksplorasi semua arah yang mungkin
        directions = [
            (current_x - 24, current_y),  # Kiri
            (current_x, current_y - 24),  # Bawah
            (current_x + 24, current_y),  # Kanan
            (current_x, current_y + 24)   # Atas
        ]

        explored = False  # Flag untuk melacak apakah ada langkah yang valid

        for next_x, next_y in directions:
            if (next_x, next_y) in path and (next_x, next_y) not in visited:
                explored = True
                frontier.append((next_x, next_y))  # Tambahkan ke frontier
                solution[next_x, next_y] = current  # Simpan jalur
                visited.append((next_x, next_y))

        # Jika tidak ada jalur yang ditemukan (jalan buntu), tandai dengan warna biru
        if not explored:
            wall.goto(current_x, current_y)
            wall.stamp()
            visited.append((current_x, current_y))
        
        # Tandai langkah yang dikunjungi
        solution_marker.goto(current_x, current_y)
        solution_marker.stamp()

    print("Pencarian selesai!")

# Fungsi untuk melacak kembali jalur solusi dari titik akhir ke titik awal
def backtrack(x, y):                       
    path_marker.goto(x, y)  # Mulai dari titik akhir
    path_marker.stamp()
    while (x, y) != (start_position_x, start_position_y):  # Sampai mencapai titik awal
        path_marker.goto(solution[x, y])        
        path_marker.stamp()                     
        x, y = solution[x, y]  # Pindah ke titik sebelumnya

# Fungsi untuk memulai pencarian solusi
def start_solver():
    global solver_in_progress
    
    if not solver_in_progress:
        start_position_x, start_position_y = player.xcor(), player.ycor()
        search(start_position_x, start_position_y)
        backtrack(end_position_x, end_position_y)

# Fungsi untuk menggerakkan pemain ke arah yang berbeda
def move_up():
    current_x, current_y = player.xcor(), player.ycor()
    if can_move(current_x, current_y + 24):  # Periksa jika bisa bergerak ke atas
        player.goto(current_x, current_y + 24)
        check_exit()

def move_down():
    current_x, current_y = player.xcor(), player.ycor()
    if can_move(current_x, current_y - 24):  # Periksa jika bisa bergerak ke bawah
        player.goto(current_x, current_y - 24)
        check_exit()

def move_left():
    current_x, current_y = player.xcor(), player.ycor()
    if can_move(current_x - 24, current_y):  # Periksa jika bisa bergerak ke kiri
        player.goto(current_x - 24, current_y)
        check_exit()

def move_right():
    current_x, current_y = player.xcor(), player.ycor()
    if can_move(current_x + 24, current_y):  # Periksa jika bisa bergerak ke kanan
        player.goto(current_x + 24, current_y)
        check_exit()

# Periksa apakah pemain berada di titik keluar
def can_move(x, y):
    return (x, y) in path and (x, y) not in walls

# Fungsi untuk memeriksa apakah pemain sudah mencapai titik akhir
def check_exit():
    if (player.xcor(), player.ycor()) == (end_position_x, end_position_y):
        print("Selamat! Anda telah menyelesaikan labirin.")
        window.bye()

# Inisialisasi elemen game
wall = Wall()
backtrack_marker = BacktrackMarker()
path_marker = PathMarker()
solution_marker = SolutionMarker()
player = GamePlayer()
walls, path, visited, frontier, solution = [], [], [], [], {}

# Menyiapkan labirin dengan ukuran yang lebih besar dan menantang
setup_maze(generate_maze(12, 20))  # Menggunakan labirin 12x20

# Menghubungkan tombol keyboard dengan fungsi gerakan
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")
window.onkey(start_solver, 's')
# Bind the restart function to the "R" key
window.onkey(restart_game, "r")


window.listen()
window.exitonclick()
