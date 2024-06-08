'''
gui 모듈을 사용하기 위한 기본 구조를 미리 적어 둔 파일입니다.

- 여러분은 이 아래에 있는, 함수 initialize()와 update()에 대한
  함수 정의 내용물을 구성함으로써 프로그램을 구성해야 해요

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui

w = gui.Window("Space Invador", 480, 640)

def initialize(timestamp):
	w.data.bg = w.newRectangle(0, 0, 480, 640)

	w.data.width_image = [16, 22, 24]
	w.data.height_image = [16, 16, 16]
	w.data.filenames = [['squid_0.png', 'squid_1.png'], ['crab_0.png', 'crab_1.png'], ['octopus_0.png', 'octopus_1.png']]
	w.data.invader_interval_h = 36
	w.data.invader_interval_v = 42
	w.data.invaders = []

	w.data.missile_width = 6
	w.data.missile_height = 14
	w.data.missilefiles = ['missile_1.png', 'missile_2.png', 'missile_3.png', 'missile_4.png']
	w.data.missiles = []

	w.data.key_quit = 'Escape'
	w.data.key_left = 'Left'
	w.data.key_right = 'Right'
	w.data.key_space = 'space'

	player_x = 240
	player_y = 600
	playerNumber= w.newImage(player_x, player_y, 'player.png', 26, 16)
	w.data.player = [playerNumber, player_x, player_y]

	for i in range(5):
		for j in range(11):
			fileNameIdx = 2 if i == 0 or i == 1 else 1 if i == 2 or i == 3 else 0 #Invader 종류 설정
			dx = 0 if fileNameIdx == 2 else 1 if fileNameIdx == 1 else 4 #너비 보정
			pos_x = 368 - (w.data.invader_interval_h * j) + dx
			pos_y = 332 - (w.data.invader_interval_v * i)
			number = w.newImage(pos_x, pos_y, w.data.filenames[fileNameIdx][0],  w.data.width_image[fileNameIdx],  w.data.height_image[fileNameIdx])
			w.data.invaders.append([
				number,
				fileNameIdx,
				0,
				pos_x,
				pos_y,
                timestamp + (i / 20),
				0,
				1,
				1
			])


def update(timestamp):
	p = w.data.player
	if w.keys[w.data.key_quit]:
		w.stop()
		return
	
	if w.keys[w.data.key_left]:
		p[1] -= 3
		w.moveObject(p[0], p[1], p[2])
		
	if w.keys[w.data.key_right]:
		p[1] += 3
		w.moveObject(p[0], p[1], p[2])

	if w.keys[w.data.key_space]:
		if len(w.data.missiles) == 0 or w.data.missiles[-1][4] + 1 < timestamp:
			mNum = w.newImage(p[1], p[2], w.data.missilefiles[0], w.data.missile_width, w.data.missile_height)
			w.data.missiles.append([mNum, p[1], p[2], 0, timestamp, timestamp])

	for missile in w.data.missiles:
		'''
		missile[0]: number
		missile[1]: pos_x
		missile[2]: pos_y
		missile[3]: animationIdx
		missile[4]: moveTimestamp
		missile[5]: animationTimestamp
		'''
		missile[2] -= 4
		missile[3] = (missile[3] + 1) % 4
		w.moveObject(missile[0], missile[1], missile[2])
		if missile[5] + 0.1 < timestamp:
			w.setImage(missile[0], w.data.missilefiles[missile[3]], w.data.missile_width, w.data.missile_height)
			missile[5] = timestamp

	for invader in w.data.invaders:
		'''
        invader[0]: number
        invader[1]: fileNameIdx
        invader[2]: animationIdx
        invader[3]: pos_x
        invader[4]: pos_y
        invader[5]: timestamp
        invader[6]: moveCnt
        invader[7]: moveDir
		invader[8]: timeMod
        '''
		if invader[5] <= timestamp:
			invader[1] %= 3
			invader[2] = (invader[2] + 1) % 2
			invader[3] += 8 * invader[7]
			w.moveObject(invader[0], invader[3], invader[4])
			w.setImage(invader[0], w.data.filenames[invader[1]][invader[2]], w.data.width_image[invader[1]], w.data.height_image[invader[1]])
			invader[5] = timestamp + invader[8]
			invader[6] += 1
			if invader[6] >= 10:
				invader[3] += 8 * invader[7]
				invader[4] += w.data.invader_interval_v / 3
				invader[7] *= -1
				invader[6] = -1
				invader[8] = max(0.1, invader[8] * 0.9)

w.initialize = initialize
w.update = update

w.start()
