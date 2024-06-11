
'''
작성자: 김민식

프로그램 이름: Space Invaders

사용 방법:
- 이동
	- 방향 키를 사용하여 플레이어를 좌우로 움직입니다.
  		- 왼쪽 화살표 키: 플레이어를 왼쪽으로 이동
  		- 오른쪽 화살표 키: 플레이어를 오른쪽으로 이동
- 공격
	- 스페이스바를 눌러 미사일을 발사합니다.
  		- 미사일은 적을 맞추기 위해 사용됩니다.
- 재시작
	- 게임이 종료되면 'r' 키를 눌러 게임을 재시작 할 수 있습니다.
- 창 닫기
	- 'ESC' 키를 눌러 창을 닫을 수 있습니다.
- 치트 키
	- 게임 중 'c' 키를 눌러 적 인베이더를 제거할 수 있습니다.

게임 진행:
- 'space_invaders.py' 파일을 실행시키면 게임이 시작됩니다.
- 적들이 생성되며 적들은 좌우로 움직이며 점점 아래로 내려옵니다.
	- 적이 아래로 한 칸 내려올 때마다 이동속도가 증가합니다.
- 플레이어를 이동하고 미사일을 발사해 적을 처치할 수 있습니다.
	- 적을 처치하면 종류별로 정해진 점수를 얻을 수 있습니다. (문어-10점, 게-20점, 오징어-30점)
	- UFO가 15초마다 생성됩니다. UFO를 처치하면 50~300점 사이의 랜덤 점수를 받습니다.
- 적도 랜덤으로 미사일을 발사합니다.
	- 적이 발사한 미사일에 맞으면 생명이 줄어듭니다.
- 적이 초록색 선에 도달하기 전에 모두 처치하면 스테이지가 클리어됩니다.
	- 스테이지가 클리어되면 다음 스테이지로 넘어가며 적과 생명이 재생성됩니다. 
	- 스테이지가 넘어갈 때마다 적의 이동속도 증가 폭이 커집니다.
- 스테이지는 게임이 종료될 때까지 반복됩니다.

게임 종료:
- 플레이어는 생명이 세 개로 시작하고, 플레이어 생명이 0이 되면 게임이 종료됩니다.
- 적이 초록색 선까지 도달하면 게임이 종료됩니다.
- 게임 종료 시, 최고점수가 'highscore.txt' 파일에 저장되고 다음 실행 시 해당 텍스트 파일에 적힌 최고점수를 로드합니다.

주의 사항:
- MAC OS 환경에서 실행하면 소리 재생 시 프레임이 멈추는 오류가 존재합니다.
	- w.playSound()가 사용된 네 줄의 코드를 주석처리하고 실행시키면 정상 플레이 가능합니다.
 _____ ______   ___   _____  _____   _____  _   _  _   _   ___  ______  _____ ______  _____ 
/  ___|| ___ \ / _ \ /  __ \|  ___| |_   _|| \ | || | | | / _ \ |  _  \|  ___|| ___ \/  ___|
\ `--. | |_/ // /_\ \| /  \/| |__     | |  |  \| || | | |/ /_\ \| | | || |__  | |_/ /\ `--. 
 `--. \|  __/ |  _  || |    |  __|    | |  | . ` || | | ||  _  || | | ||  __| |    /  `--. |
/\__/ /| |    | | | || \__/\| |___   _| |_ | |\  |\ \_/ /| | | || |/ / | |___ | |\ \ /\__/ /
\____/ \_|    \_| |_/ \____/\____/   \___/ \_| \_/ \___/ \_| |_/|___/  \____/ \_| \_|\____/ 
<Chung-Ang University Computer Science and Engineering OSS Python Programming Term Project>
'''

import gui_core as gui
import random

screen_width = 600
screen_height = 800
x_offset = 60
y_offset = 80
score = 0
gameClearTime = 0
timeMod = 0.9

w = gui.Window("Space Invaders", screen_width, screen_height)

def read_highscore():
    try:
        with open('highscore.txt', 'r') as file:
            content = file.read().strip()
            if content == "":
                return 0
            if content.isdigit():
                highscore = int(content)
                return highscore
            else:
                raise ValueError(f"Error: File 'highscore.txt' does not contain a valid integer. Content: '{content}'")
    except FileNotFoundError:
        print(f"Error: File 'highscore.txt' not found.")
    except ValueError as ve:
        return 0

def write_new_highscore(highscore):
    with open('highscore.txt', 'w') as file:
        file.write(str(highscore))

def setGameOver():
	w.newRectangle(x_offset + 4, y_offset * 2, screen_width - (x_offset * 2) - 8, screen_height - (y_offset * 3.5))
	w.newImage(screen_width / 2 - 80, screen_height / 3 - 40, 'game_over.png', 161, 23)
	w.newText(screen_width / 2 - 5, screen_height - 280, 200, 'Press \'ESC\' to quit.', 'white')
	w.newText(screen_width / 2 - 5, screen_height - 250, 200, 'Press \'R\' to restart.', 'white')
	if score > w.data.highscore:
		w.newImage(screen_width / 2 - 136, screen_height / 3, 'new_high.png', 273, 23)
		w.setText(w.data.hstNum, str(score).zfill(4))
		write_new_highscore(score)
	w.data.isGameOver = True

def trashCan():
	for obj in w.data.objs:
		w.deleteObject(obj[1])
		w.data.objs.remove(obj)

def initialize(timestamp):
	w.data.objs = []

	w.data.isGameOver = False
	w.data.isClear = False

	w.data.bg = w.newRectangle(x_offset - 4, y_offset, screen_width - (x_offset * 2) + 8, screen_height - (y_offset * 2))
	w.data.game_over_line_y = screen_height - (y_offset * 1.5)
	w.newText(screen_width - (x_offset * 3) + 10, screen_height - (y_offset * 1.25), 200, 'CAU CSE OSS Python Minsik Kim', 'green')

	w.data.highscore = read_highscore()
	sText = str(score).zfill(4)
	hsText = str(w.data.highscore).zfill(4)
	w.newText(x_offset * 2.3 - 10, y_offset * 1.5, 200, 'SCORE', 'white')
	w.data.stNum = w.newText(x_offset * 2.3 - 10, y_offset * 1.7, 200, sText, 'white')
	w.newText(screen_width - x_offset * 2.3 + 10, y_offset * 1.5, 200, 'HI-SCORE', 'white')
	w.data.hstNum = w.newText(screen_width - x_offset * 2.3 + 10, y_offset * 1.7, 200, hsText, 'white')
	
	w.data.invader_width = [16, 22, 24]
	w.data.invader_height = [16, 16, 16]
	w.data.filenames = [['squid_0.png', 'squid_1.png'], ['crab_0.png', 'crab_1.png'], ['octopus_0.png', 'octopus_1.png']]
	w.data.invader_interval_h = 36
	w.data.invader_interval_v = 42
	w.data.invader_count = 0

	w.data.ufo_width = 49
	w.data.ufo_height = 22
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

	w.data.player_width = 27
	w.data.player_height = 17
	w.data.player_life = 3
	player_x = (screen_width / 2) - (w.data.player_width / 2)
	player_y = w.data.game_over_line_y - (w.data.player_height * 2.5)
	playerNumber = w.newImage(player_x, player_y, 'player.png', w.data.player_width, w.data.player_height)
	w.data.objs.append(['player', playerNumber, player_x, player_y, w.data.player_width, False, 0])

	w.data.ltNum = w.newText(x_offset + 25, w.data.game_over_line_y + 20, 50, str(w.data.player_life), 'white')
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
	w.newImage(0, 0, 'frame.png', screen_width, screen_height)

def update(timestamp):
	global score
	global gameClearTime
	global timeMod

	if w.keys['Escape']:
		w.stop()
		return
	if w.data.isGameOver and w.keys['r']:
		score = 0
		gameClearTime = 0
		timeMod = 0.9
		trashCan()
		initialize(timestamp)
	life_count = w.data.player_life
	w.setText(w.data.ltNum, str(w.data.player_life))
	w.setText(w.data.stNum, str(score).zfill(4))
	for obj in w.data.objs:
		if obj[0] == 'life_gauge':
			if life_count <= 0:
				w.deleteObject(obj[1])
				w.data.objs.remove(obj)
			life_count -= 1

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
						w.data.objs.append(['missile', mNum, obj[2] + (w.data.player_width / 2) - (w.data.missile_width / 2), obj[3], 0, timestamp])
						w.data.last_missile_time = timestamp
						w.playSound('shoot.wav')
				
					for missile in [m for m in w.data.objs if m[0] == 'invader_missile']:
						m_x = missile[2] + (w.data.invader_missile_width / 2)
						m_y = missile[3]
						if m_x > obj[2] and m_x < obj[2] + w.data.player_width and m_y > obj[3] and m_y < obj[3] + w.data.player_height:
							w.deleteObject(missile[1])
							w.data.objs.remove(missile)
							w.setImage(obj[1], 'player_die.png', 31, 17)
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
				if obj[3] < y_offset * 2:
					w.deleteObject(obj[1])
					w.data.objs.remove(obj)

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
					score += ufo_score
					obj[2] = w.data.ufo_x
					obj[4] = timestamp
					w.setImage(obj[1], 'ufo.png', w.data.ufo_width, w.data.ufo_height)
					obj[5] = False

				if obj[5] == False and timestamp - obj[4] > 15:
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
						w.setImage(obj[1], 'ufo_die.png', 53, 33)
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
					score += 30 - (obj[2] * 10)
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

				if  random.random() < 0.001 and timestamp - w.data.last_invader_missile_time > 0.5:
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
					if obj[7] >= 11:
						obj[4] += 8 * obj[8]
						obj[5] += w.data.invader_interval_v / 3
						obj[8] *= -1
						obj[7] = -1
						obj[9] = max(0.05, obj[9] * timeMod)
				w.data.invader_count += 1
			elif obj[0] == 'invader_missile':
				obj[3] += 4
				obj[4] = (obj[4] + 1) % 4
				w.moveObject(obj[1], obj[2], obj[3])
				if timestamp - obj[5] > 0.1:
					w.setImage(obj[1], w.data.invader_missilefiles[obj[4]], w.data.invader_missile_width, w.data.invader_missile_height)
					obj[5] = timestamp
				if obj[3] > w.data.game_over_line_y - w.data.invader_missile_height:
					w.deleteObject(obj[1])
					w.data.objs.remove(obj)
		if w.data.isClear == False and w.data.invader_count == 0:
			w.data.isClear = True
			gameClearTime = timestamp
		if w.data.isClear == True and timestamp - gameClearTime > 1:
			timeMod -= 0.1
			trashCan()
			initialize(timestamp)
w.initialize = initialize
w.update = update

w.start()
