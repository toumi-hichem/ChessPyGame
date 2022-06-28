import pygame
import sys

#TODO
#make self.select_square update a lot of rects at the same time by overloading argument

class Piece:
	def __init__ (self, piece, player, image=None, square_height=64, square_width=64, empty=False):
		self.piece = piece 		#['p', 'b', 'kn', r', 'q', 'k']
		self.player = player    #b o w
		if empty:
			self.image = pygame.Surface([64,64], pygame.SRCALPHA, 32)
		else:
			self.image = pygame.image.load(image)
	def is_valid_move (self, pick_up, put_down):
		pass

	def get_valid_moves (self, current_pos):
		pass
	def get_type (self):
		return self.piece

class Board:
	def __init__ (self, height, width, image, screen):
		self.screen = screen
		self.pieces_on_screen = {}
		self.height = height
		self.square_height = height/8
		self.width = width
		self.square_width = width/8
		self.image = pygame.image.load (image).convert()
		self.pieces = self.make_pieces()
		self.selected_img = pygame.image.load ("selected_img.jpg").convert ()
		self.selected_img.set_alpha (100)
		self.init_pos ()
		self.current_board_pos = self.pieces

		pygame.display.update ()


	def get_pieces (self):
		return self.pieces_on_screen
	def make_pieces (self):
		w_pawn		= Piece ('p', 'w', 'pawn_w.png')
		w_knight	= Piece ('kn', 'w', 'knight_w.png')
		w_bishop	= Piece ('b', 'w', 'bishop_w.png')
		w_rook		= Piece ('r', 'w', 'rook_w.png')
		w_queen		= Piece ('q', 'w', 'queen_w.png')
		w_king 		= Piece ('k', 'w', 'king_w.png')

		b_pawn		= Piece ('p', 'b', 'pawn_b.png')
		b_knight	= Piece ('kn', 'b', 'knight_b.png')
		b_bishop	= Piece ('b', 'b', 'bishop_b.png')
		b_rook		= Piece ('r', 'b', 'rook_b.png')
		b_queen		= Piece ('q', 'b', 'queen_b.png')
		b_king 		= Piece ('k', 'b', 'king_b.png')
		empty 		= Piece ('None', 'None', empty=True)
		self.empty = empty

		return {(0, 0):b_rook, (1, 0):b_knight, (2, 0):b_bishop, (3, 0):b_queen, (4, 0):b_king, (5, 0):b_bishop, (6, 0):b_knight, (7, 0):b_rook,
				(0, 1):b_pawn, (1, 1):b_pawn, (2, 1):b_pawn, (3, 1):b_pawn, (4, 1):b_pawn, (5, 1):b_pawn, (6, 1):b_pawn, (7, 1):b_pawn, 
				(0, 2):empty, (1, 2):empty, (2, 2):empty, (3, 2):empty, (4, 2):empty, (5, 2):empty, (6, 2):empty, (7, 2):empty, 
				(0, 3):empty, (1, 3):empty, (2, 3):empty, (3, 3):empty, (4, 3):empty, (5, 3):empty, (6, 3):empty, (7, 3):empty, 
				(0, 4):empty, (1, 4):empty, (2, 4):empty, (3, 4):empty, (4, 4):empty, (5, 4):empty, (6, 4):empty, (7, 4):empty, 
				(0, 5):empty, (1, 5):empty, (2, 5):empty, (3, 5):empty, (4, 5):empty, (5, 5):empty, (6, 5):empty, (7, 5):empty,
				(0, 6):w_pawn, (1, 6):w_pawn, (2, 6):w_pawn, (3, 6):w_pawn, (4, 6):w_pawn, (5, 6):w_pawn, (6, 6):w_pawn, (7, 6):w_pawn, 
				(0, 7):w_rook, (1, 7):w_knight, (2, 7):w_bishop, (3, 7):w_queen, (4, 7):w_king, (5, 7):w_bishop, (6, 7):w_knight, (7, 7):w_rook,
				}
	def init_pos (self):
		#Place the corresponding piece

		self.screen.blit (self.image, (0, 0))
		self.selected_rect_by_mouse = pygame.Rect ((64, 64), (64, 64))
		self.screen.blit (self.selected_img,  self.selected_rect_by_mouse, area=pygame.Rect (7*64, 7*64, 64, 64))
		for x in range (8):
			for y in range (8):
				p = self.pieces [(x, y)]
				if p != None:
					self.pieces_on_screen[(x, y)] = self.screen.blit (p.image, (x*64, y*64, 64, 64))
				else:
					r = pygame.Surface((64, 64))
					r.set_alpha (0)
					r.fill ((0, 0, 155))
					self.pieces_on_screen[(x, y)] = self.screen.blit (r, (x*64, y*64, 64, 64))
	def move (self, selected_pos, pos):

		self.screen.blit (self.image, self.pieces_on_screen [pos], area=pygame.Rect(0 if sum(pos)%2==0 else 64, 0, 64, 64)) #blit the background on the clicked location
		self.screen.blit (self.image, self.pieces_on_screen [selected_pos], area=pygame.Rect(0 if sum(selected_pos)%2==0 else 64, 0, 64, 64)) #blit the background on the selected location
		self.screen.blit (self.current_board_pos [selected_pos].image, self.pieces_on_screen [pos]) #blit the piece from the selected location to the clicked one
		pygame.display.update (self.pieces_on_screen[pos].union (self.pieces_on_screen [selected_pos])) #update the whole process

		#updating the internal memory of the object
		print ("the two objs: ", pos, selected_pos)
		self.current_board_pos [pos] = self.current_board_pos [selected_pos]
		self.current_board_pos [selected_pos] = self.empty

	def mouse_selected_square (self, coordinates):
		coordinate = (coordinates[0]*64, coordinates[1]*64)	#to convert them from position values to pixel values. There s plays a role, hope you don't get confused!!
		if coordinate == self.selected_rect_by_mouse.topleft:
			#No need to repdate if the square is already selected
			return None
		self.deselect_square (self.selected_rect_by_mouse.topleft, cor_in_px=True)
		self.select_square (coordinate, cor_in_px=True)
		self.selected_rect_by_mouse = pygame.Rect (coordinate, (64, 64))
	def update_rect (self, rects):
		for r in rects:
			self.screen.update (r)
	def select_square (self, coordinate, cor_in_px=False):
		'''Takes a coordinates and selects the corresponding square'''
		if cor_in_px:
			coordinate_in_px = coordinate
			coordinate_in_car = (coordinate[0]/64, coordinate[1]/64)
		else:
			coordinate_in_px = (coordinate[0]*64, coordinate[1]*64)
			coordinate_in_car = coordinate

		self.screen.blit (self.image, pygame.Rect (coordinate_in_px, (64, 64)), area=pygame.Rect(coordinate_in_px, (64, 64))) #bliting the background

		#blit selected img
		self.screen.blit (self.selected_img,  pygame.Rect (coordinate_in_px, (64, 64)), area=pygame.Rect ((0, 0), (64, 64)))

		self.screen.blit (self.current_board_pos [coordinate_in_car].image, pygame.Rect (coordinate_in_px, (64, 64))) #bliting the piece
		
		pygame.display.update (pygame.Rect (coordinate_in_px, (64, 64))) #updating the dirty square

	def deselect_square (self, coordinate, cor_in_px=False):
		if cor_in_px:
			coordinate_in_px = coordinate
			coordinate_in_car = (coordinate[0]/64, coordinate[1]/64)
		else:
			coordinate_in_px = (coordinate[0]*64, coordinate[1]*64)
			coordinate_in_car = coordinate

		self.screen.blit (self.image, pygame.Rect (coordinate_in_px, (64, 64)), area=pygame.Rect(coordinate_in_px, (64, 64))) #bliting the background

		self.screen.blit (self.current_board_pos [coordinate_in_car].image, pygame.Rect (coordinate_in_px, (64, 64))) #bliting the piece
		
		pygame.display.update (pygame.Rect (coordinate_in_px, (64, 64))) #updating the dirty square
	def is_inside_the_board (self, coordinate):
		if coordinate [0] <= 7 and coordinate [1] <= 7 and coordinate [0] >= 0 and coordinate [1] >= 0:
			return True 
		else:
			return False 
	
	def get_possible_moves (self, coordinate):
		if coordinate [0] >= 9 or coordinate [1] >= 9: #making sure that we're using board coordinates, not pixel count
			coordinate = (coordinate[0]/64, coordinate[1]/64)

		#finds possible plays but not accounting for other pieces

		piece_type = self.current_board_pos[coordinate].get_type () # is one of these ['p', 'b', 'kn', r', 'q', 'k']
		possible_plays = []

		if piece_type == 'p':		#pawn
			possible_plays.append ((coordinate [0]	  , coordinate [1] - 1))
			possible_plays.append ((coordinate [0] + 1, coordinate [1] - 1))
			possible_plays.append ((coordinate [0] - 1, coordinate [1] - 1))
		elif piece_type == 'b':	#bishop
			temp = []
			i, j = coordinate
			while coordinate [0] >= 0 and coordinate [1] >= 0:	#go to top left 	//-1 -1
				temp.append ((i - 1, j - 1))
			i, j = coordinate
			while coordinate [0] <= 7 and coordinate [1] >= 0:	#go to top right 	//+1 -1
				temp.append ((i + 1, j - 1))
			i, j = coordinate
			while coordinate [0] <= 7 and coordinate [1] <= 7:	#go to bottom right //+1 +1
				temp.append ((i + 1, j + 1))
			i, j = coordinate
			while coordinate [0] <= 0 and coordinate [1] <= 7:	#go to bottom left  //-1 +1
				temp.append ((i - 1, j + 1))
			for t in temp:
				if is_inside_the_board (t):
					possible_plays.append (t)
			del t

		elif piece_type == 'kn':	#knight
			temp = []
			temp.append ((coordinate [0] + 2, coordinate[1] + 1))
			temp.append ((coordinate [0] + 2, coordinate[1] - 1))

			temp.append ((coordinate [0] - 2, coordinate[1] + 1))
			temp.append ((coordinate [0] - 2, coordinate[1] - 1))

			temp.append ((coordinate [0] + 1, coordinate[1] + 2))
			temp.append ((coordinate [0] - 1, coordinate[1] + 2))

			temp.append ((coordinate [0] + 1, coordinate[1] - 2))
			temp.append ((coordinate [0] - 1, coordinate[1] - 2))

			for t in temp:
				if self.is_inside_the_board (t):
					possible_plays.append (t)
			del t

		elif piece_type == 'r':	#rook
			for x in range (7):
				if x == coordinate [0]:
					continue 
				possible_plays.append( (x, coordinate [1]))
			for y in range (7):
				if y == coordinate [1]:
					continue 
				possible_plays.append ((coordinate [0], y))

		elif piece_type == 'q':	#queen
			#rook moves
			temp = []
			for x in range (7):
				if x == coordinate [0]:
					continue 
				temp.append ((x, coordinate [1]))
			for y in range (7):
				if y == coordinate [1]:
					continue 
				temp.append ((coordinate [0], y))

			#bishop juice
			i, j = coordinate
			while coordinate [0] >= 0 and coordinate [1] >= 0:	#go to top left 	//-1 -1
				temp.append ((i - 1, j - 1))
			i, j = coordinate
			while coordinate [0] <= 7 and coordinate [1] >= 0:	#go to top right 	//+1 -1
				temp.append ((i + 1, j - 1))
			i, j = coordinate
			while coordinate [0] <= 7 and coordinate [1] <= 7:	#go to bottom right //+1 +1
				temp.append ((i + 1, j + 1))
			i, j = coordinate
			while coordinate [0] <= 0 and coordinate [1] <= 7:	#go to bottom left  //-1 +1
				temp.append ((i - 1, j + 1))
			for t in temp:
				if is_inside_the_board (t):
					possible_plays.append (t)
			del t

		elif piece_type == 'k':	#king
			temp = []
			temp.append ((coordinate [0] + 1, coordinate[1] + 1))
			temp.append ((coordinate [0] + 1, coordinate[1] + 0))
			temp.append ((coordinate [0] + 1, coordinate[1] - 1))
			temp.append ((coordinate [0] + 0, coordinate[1] - 1))
			temp.append ((coordinate [0] - 1, coordinate[1] - 1))
			temp.append ((coordinate [0] - 1, coordinate[1] + 0))
			temp.append ((coordinate [0] - 1, coordinate[1] + 1))
			temp.append ((coordinate [0] - 0, coordinate[1] + 1))

			for t in temp:
				if is_inside_the_board (t):
					possible_plays.append (t)
		
		return possible_plays


def init ():
	running = True
	pygame.init()
	b, screen = set_board ()
	
	selected_pos = None
	while running:
		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and selected_pos == None:
			pieces_rect = b.get_pieces ()
			for position in pieces_rect:
				if pieces_rect [position].collidepoint (event.pos):
					for to in b.get_possible_moves(position):
						b.select_square (to)
					selected_pos = position
					break
			continue 

		if event.type == pygame.MOUSEBUTTONDOWN and selected_pos != None:
			pieces_rect = b.get_pieces ()
			for position in pieces_rect:
				if pieces_rect [position].collidepoint (event.pos):
					b.move (selected_pos, position)
					selected_pos = None
					break
			continue
		if event.type == pygame.MOUSEMOTION:
			pieces_rect = b.get_pieces ()
			for pos in pieces_rect:
				if pieces_rect [pos].collidepoint (event.pos):
					b.mouse_selected_square (pos)
					break
				continue



def set_board ():
	pygame.display.set_caption ("Chess")
	screen = pygame.display.set_mode ((512, 512))

	return (Board (512, 512, "board.png", screen), screen)

if __name__ == "__main__":
	init ()