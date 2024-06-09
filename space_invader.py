import gui_core as gui
import random

screen_width = 600
screen_height = 800
x_offset = 60
y_offset = 80

w = gui.Window("Space Invador", screen_width, screen_height)

def setGameOver():
	w.newText(screen_width / 2 - 5, screen_height / 3 + 20, 100, 'GAME OVER', 'red')
	w.newText(screen_width / 2 - 5, screen_height - 300, 200, 'Press \'ESC\' to quit.', 'white')
	w.data.isGameOver = True

def setGameClear():
	w.newText(screen_width / 2 - 5, screen_height / 3 + 20, 100, '!!GAME CLEAR!!', 'green')
	w.newText(screen_width / 2 - 5, screen_height - 300, 200, 'Press \'ESC\' to quit.', 'white')
	w.data.isGameOver = True

def initialize(timestamp):
	w.data.objs = []

	w.data.isGameOver = False

	w.data.bg = w.newRectangle(x_offset, y_offset, screen_width - (x_offset * 2), screen_height - (y_offset * 2))
	w.data.game_over_line_y = screen_height - (y_offset * 1.5)

	w.data.score = 0
	sText = str(w.data.score).zfill(4)
	w.newText(screen_width / 2 - 5, y_offset * 1.5, 200, 'SCORE', 'white')
	stNum = w.newText(screen_width / 2 - 5, y_offset * 1.7, 200, sText, 'white')
	w.data.objs.append(['score_text', stNum])

	w.data.invader_width = [16, 22, 24]
	w.data.invader_height = [16, 16, 16]
	w.data.filenames = [['squid_0.png', 'squid_1.png'], ['crab_0.png', 'crab_1.png'], ['octopus_0.png', 'octopus_1.png']]
	w.data.invader_interval_h = 36
	w.data.invader_interval_v = 42
	w.data.invader_count = 0

	w.data.ufo_width = 48
	w.data.ufo_height = 21
	w.data.ufo_x = x_offset - w.data.ufo_width - 5
	w.data.ufo_y = y_offset * 2

	w.data.missile_width = 6
	w.data.missile_height = 14
	w.data.missilefiles = ['missile_1.png', 'missile_2.png', 'missile_3.png', 'missile_4.png']
	w.data.last_missile_time = 0

	w.data.invader_missile_width = 6
	w.data.invader_missile_height = 14
	w.data.invader_missilefiles = ['invader_missile_1.png', 'invader_missile_2.png', 'invader_missile_3.png', 'invader_missile_4.png']
	w.data.last_invader_missile_time = 0

	w.data.player_width = 26
	w.data.player_height = 16
	w.data.player_life = 3
	player_x = (screen_width / 2) - (w.data.player_width / 2)
	player_y = w.data.game_over_line_y - (w.data.player_height * 2.5)
	playerNumber = w.newImage(player_x, player_y, 'player.png', w.data.player_width, w.data.player_height)
	w.data.objs.append(['player', playerNumber, player_x, player_y, w.data.player_width, False, 0])

	tNum = w.newText(x_offset + 25, w.data.game_over_line_y + 20, 50, str(w.data.player_life), 'white')
	w.data.objs.append(['life_text', tNum])
	for i in range(w.data.player_life):
		life_x = i * (w.data.player_width * 1.5) + x_offset * 1.8
		life_y = w.data.game_over_line_y + 10
		hNum = w.newImage(life_x, life_y, 'player.png', w.data.player_width, w.data.player_height)
		w.data.objs.append(['life_gauge', hNum, life_x, life_y])

	for i in range(5):
		for j in range(11):
			fileNameIdx = 2 if i == 0 or i == 1 else 1 if i == 2 or i == 3 else 0
			dx = 0 if fileNameIdx == 2 else 1 if fileNameIdx == 1 else 4
			pos_x = 424 - (w.data.invader_interval_h * j) + dx
			pos_y = 382 - (w.data.invader_interval_v * i)
			number = w.newImage(pos_x, pos_y, w.data.filenames[fileNameIdx][0], w.data.invader_width[fileNameIdx], w.data.invader_height[fileNameIdx])
			w.data.objs.append([
				'invader', number, fileNameIdx, 0, pos_x, pos_y, timestamp + (i / 20) + (j / 50), 0, 1, 1, False, 0
			])

	ufoNum = w.newImage(w.data.ufo_x, w.data.ufo_y, 'ufo.png', w.data.ufo_width, w.data.ufo_height)
	w.data.objs.append(['ufo', ufoNum, w.data.ufo_x, w.data.ufo_y, timestamp, False, 0])
	w.newRectangle(x_offset, w.data.game_over_line_y, screen_width - (x_offset * 2), 3, 'green')

def update(timestamp):
	if w.keys['Escape']:
		w.stop()
		return
	life_count = w.data.player_life
	for obj in w.data.objs:
		if obj[0] == 'life_text':
			w.setText(obj[1], str(w.data.player_life))

		elif obj[0] == 'life_gauge':
			if life_count <= 0:
				w.deleteObject(obj[1])
				w.data.objs.remove(obj)
			life_count -= 1
		elif obj[0] == 'score_text':
			t = str(w.data.score).zfill(4)
			w.setText(obj[1], t)

	if w.data.isGameOver == False:
		w.data.invader_count = 0
		for obj in w.data.objs:
			if obj[0] == 'player':
				if obj[5] and timestamp - obj[6] > 0.3:
					w.setImage(obj[1], 'player.png', w.data.player_width, w.data.player_height)
					w.data.player_life -= 1
					if w.data.player_life <= 0:
						w.deleteObject(obj[1])
						w.data.objs.remove(obj)
						setGameOver()
					obj[5] = False
				if obj[5] == False:
					if w.keys['Left']:
						if obj[2] > 8 + x_offset:
							obj[2] -= 3
						w.moveObject(obj[1], obj[2], obj[3])
					if w.keys['Right']:
						if obj[2] < screen_width - x_offset - w.data.player_width - 8:
							obj[2] += 3
						w.moveObject(obj[1], obj[2], obj[3])
					if w.keys['space'] and timestamp - w.data.last_missile_time > 0.5:
						mNum = w.newImage(obj[2], obj[3], w.data.missilefiles[0], w.data.missile_width, w.data.missile_height)
						w.data.objs.append(['missile', mNum, obj[2], obj[3], 0, timestamp])
						w.data.last_missile_time = timestamp
						w.playSound('shoot.wav')
				
					for missile in [m for m in w.data.objs if m[0] == 'invader_missile']:
						m_x = missile[2] + (w.data.invader_missile_width / 2)
						m_y = missile[3]
						if m_x > obj[2] and m_x < obj[2] + w.data.player_width and m_y > obj[3] and m_y < obj[3] + w.data.player_height:
							w.deleteObject(missile[1])
							w.data.objs.remove(missile)
							w.setImage(obj[1], 'player_die.png', 30, 16)
							obj[5] = True
							obj[6] = timestamp
							w.playSound('explosion.wav')
							break

			elif obj[0] == 'missile':
				'''
				missile[0]: objName
				missile[1]: number
				missile[2]: pos_x
				missile[3]: pos_y
				missile[4]: animationIdx
				missile[5]: moveTimestamp
				missile[6]: animationTimestamp
				'''
				obj[3] -= 4
				obj[4] = (obj[4] + 1) % 4
				w.moveObject(obj[1], obj[2], obj[3])
				if timestamp - obj[5] > 0.1:
					w.setImage(obj[1], w.data.missilefiles[obj[4]], w.data.missile_width, w.data.missile_height)
					obj[5] = timestamp

			elif obj[0] == 'ufo':
				'''
				ufo[0]: objName
				ufo[1]: number
				ufo[2]: pos_x
				ufo[3]: pos_y
				ufo[4]: resetTime
				ufo[5]: isDead
				ufo[6]: deadTime
				'''
				if obj[5] and timestamp - obj[6] > 0.3:	
					ufo_score = random.randint(50, 300)
					w.data.score += ufo_score
					obj[2] = w.data.ufo_x
					obj[4] = timestamp
					obj[5] = False

				if obj[5] == False and timestamp - obj[4] > 2:
					obj[2] += 4

				w.moveObject(obj[1], obj[2], obj[3])

				if obj[2] > screen_width:
					obj[2] = w.data.ufo_x
					obj[4] = timestamp
					obj[5] = False

				for missile in [m for m in w.data.objs if m[0] == 'missile']:
					m_x = missile[2] + (w.data.missile_width / 2)
					m_y = missile[3]
					if m_x > obj[2] and m_x < obj[2] + w.data.ufo_width and m_y > obj[3] and m_y < obj[3] + w.data.ufo_height:
						w.setImage(obj[1], 'invader_die.png', 52, 32)
						obj[5] = True
						obj[6] = timestamp
						w.playSound('invader_die.wav')
						w.deleteObject(missile[1])
						w.data.objs.remove(missile)
						break

			elif obj[0] == 'invader':
				'''
				invader[0]: objName
				invader[1]: number
				invader[2]: fileNameIdx
				invader[3]: animationIdx
				invader[4]: pos_x
				invader[5]: pos_y
				invader[6]: timestamp
				invader[7]: moveCnt
				invader[8]: moveDir
				invader[9]: timeMod
				invader[10]: isDead
				invader[11]: deadTime
				'''
				if w.keys['c']:
					w.deleteObject(obj[1])
					w.data.objs.remove(obj)
				
				if obj[10] and timestamp - obj[11] > 0.2:	
					w.data.score += 30 - (obj[2] * 10)
					w.playSound('invader_die.wav')
					w.deleteObject(obj[1])
					w.data.objs.remove(obj)

				if obj[5] + w.data.invader_height[obj[2]] >= w.data.game_over_line_y:
					setGameOver()

				for missile in [m for m in w.data.objs if m[0] == 'missile']:
					m_x = missile[2] + (w.data.missile_width / 2)
					m_y = missile[3]
					if m_x > obj[4] and m_x < obj[4] + w.data.invader_width[obj[2]] and m_y > obj[5] and m_y < obj[5] + w.data.invader_height[obj[2]]:
						w.setImage(obj[1], 'invader_die.png', 26, 16)
						obj[10] = True
						obj[11] = timestamp
						w.deleteObject(missile[1])
						w.data.objs.remove(missile)
						break

				if  random.random() < 0.0008 and timestamp - w.data.last_invader_missile_time > 0.5:
					mNum = w.newImage(obj[4], obj[5], w.data.invader_missilefiles[0], w.data.invader_missile_width, w.data.invader_missile_height)
					w.data.objs.append(['invader_missile', mNum, obj[4], obj[5], 0, timestamp])
					w.data.last_invader_missile_time = timestamp

				if obj[10] == False and obj[6] <= timestamp:
					obj[2] %= 3
					obj[3] = (obj[3] + 1) % 2
					obj[4] += 8 * obj[8]
					w.moveObject(obj[1], obj[4], obj[5])
					w.setImage(obj[1], w.data.filenames[obj[2]][obj[3]], w.data.invader_width[obj[2]], w.data.invader_height[obj[2]])
					obj[6] = timestamp + obj[9]
					obj[7] += 1
					# obj[9] = 0.01
					if obj[7] >= 11:
						obj[4] += 8 * obj[8]
						obj[5] += w.data.invader_interval_v / 3
						obj[8] *= -1
						obj[7] = -1
						obj[9] = max(0.1, obj[9] * 0.9)
				w.data.invader_count += 1
			elif obj[0] == 'invader_missile':
				obj[3] += 3
				obj[4] = (obj[4] + 1) % 4
				w.moveObject(obj[1], obj[2], obj[3])
				if timestamp - obj[5] > 0.1:
					w.setImage(obj[1], w.data.invader_missilefiles[obj[4]], w.data.invader_missile_width, w.data.invader_missile_height)
					obj[5] = timestamp
				if obj[3] > w.data.game_over_line_y - w.data.invader_missile_height:
					w.deleteObject(obj[1])
					w.data.objs.remove(obj)
		if w.data.invader_count == 0:
			setGameClear()
w.initialize = initialize
w.update = update

w.start()
