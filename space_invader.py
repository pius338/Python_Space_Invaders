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
	w.data.width_image = 24
	w.data.squid_filenames = ['squid_0.png', 'squid_1.png']
	w.data.crab_filenames = ['crab_0.png', 'crab_1.png']
	w.data.octopus_filenames = ['octopus_0.png', 'octopus_1.png']
	
	w.data.key_quit = 'Escape'

	w.data.objs = []
	w.data.bg = w.newRectangle(0, 0, 480, 640)
	w.data.squid = w.newImage(0, 0, 'squid_0.png',  w.data.width_image,  w.data.width_image)


def update(timestamp):
	global prevTimestamp
	if w.keys[w.data.key_quit]:
		w.stop()
		return
	if(prevTimestamp + 1 <= timestamp):
		print(timestamp)
		prevTimestamp = timestamp

w.initialize = initialize
w.update = update

w.start()
