import pygame

def main ():
	pygame.init ()
	screen = pygame.display.set_mode ((512, 512))
	pygame.display.set_caption ("The Program")

	screen.fill ((255, 30, 200))

	s = pygame.Surface([64,64], pygame.SRCALPHA, 32)

	#s = pygame.Surface ((64, 64))
	#s.fill ((10, 10, 200, 0))
	r = s.get_rect (center=(512*4/8, 512*4/8), top=22,left=33)
	screen.blit (s, r)
	pygame.display.update ()
	print (r.topleft)


	running = True
	while running:
		dirty_rect = []
		event = pygame.event.wait ()
		print (event)
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEMOTION:
			u = r.union (r.move (event.pos))
			r.center = event.pos
			screen.fill ((255, 30, 200))
			screen.blit (s, r)
			dirty_rect.append (u)
		pygame.display.update (dirty_rect)


main ()