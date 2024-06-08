'''
gui 모듈을 사용하기 위한 기본 구조를 미리 적어 둔 파일입니다.

- 여러분은 이 아래에 있는, 함수 initialize()와 update()에 대한
  함수 정의 내용물을 구성함으로써 프로그램을 구성해야 해요

- 중간중간 F5를 눌러 interactive를 켜 둔 다음 진행하면
  IDLE이 함수 호출식 적을 때마다 적당한 툴팁을 읽어 보여줄 거예요
'''

import gui_core as gui

w = gui.Window("Space Invador", 480, 640)
prevTimestamp = 0

def initialize(timestamp):
	w.data.width_image = [16, 22, 24]
	w.data.height_image = [16, 16, 16]
	w.data.filenames = [['squid_0.png', 'squid_1.png'], ['crab_0.png', 'crab_1.png'], ['octopus_0.png', 'octopus_1.png']]
	
	w.data.key_quit = 'Escape'

	w.data.objs = []
	w.data.moveCnt = 0
	w.data.bg = w.newRectangle(0, 0, 480, 640)

	w.data.invader_interval_h = 36
	w.data.invader_interval_v = 42

	for i in range(5):
		for j in range(11):
			fileNameIdx = 2 if i == 0 or i == 1 else 1 if i == 2 or i == 3 else 0 #Invader 종류 설정
			dx = 0 if fileNameIdx == 2 else 1 if fileNameIdx == 1 else 4 #너비 보정
			pos_x = 368 - (w.data.invader_interval_h * j) + dx
			pos_y = 332 - (w.data.invader_interval_v * i)
			number = w.newImage(pos_x, pos_y, w.data.filenames[fileNameIdx][0],  w.data.width_image[fileNameIdx],  w.data.height_image[fileNameIdx])
			w.data.objs.append([
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
	global prevTimestamp
	if w.keys[w.data.key_quit]:
		w.stop()
		return
	for obj in w.data.objs:
		'''
        obj[0]: number
        obj[1]: fileNameIdx
        obj[2]: animationIdx
        obj[3]: pos_x
        obj[4]: pos_y
        obj[5]: timestamp
        obj[6]: moveCnt
        obj[7]: moveDir
		obj[8]: timeMod
        '''
		if obj[5] <= timestamp:
			obj[1] %= 3
			obj[2] = (obj[2] + 1) % 2
			obj[3] += 8 * obj[7]
			w.moveObject(obj[0], obj[3], obj[4])
			w.setImage(obj[0], w.data.filenames[obj[1]][obj[2]], w.data.width_image[obj[1]], w.data.height_image[obj[1]])
			obj[5] = timestamp + obj[8]
			obj[6] += 1
			if obj[6] >= 10:
				obj[3] += 8 * obj[7]
				obj[4] += w.data.invader_interval_v / 2
				obj[7] *= -1
				obj[6] = -1
				obj[8] = max(0.1, obj[8] * 0.9)
		prevTimestamp = timestamp

w.initialize = initialize
w.update = update

w.start()
