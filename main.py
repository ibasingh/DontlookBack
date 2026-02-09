# empty
#!/usr/bin/env python3
import sys


def prompt_choice(prompt, choices):
	"""Tampilkan prompt dan kembalikan pilihan valid (1..n)."""
	while True:
		print()
		print(prompt)
		for i, c in enumerate(choices, 1):
			print(f"  {i}. {c}")
		choice = input("Pilih angka: ").strip()
		if choice.isdigit() and 1 <= int(choice) <= len(choices):
			return int(choice)
		print("Pilihan tidak dikenal. Coba lagi.")


def ending_escape(state):
	print('\n--- ENDING: Kabur ---')
	print('Kamu berhasil meninggalkan rumah itu sebelum malam turun sepenuhnya.')
	print('Lampu kota di kejauhan terlihat seperti janji bahwa hidup akan berlanjut.')


def ending_vanished(state):
	print('\n--- ENDING: Menghilang ---')
	print('Saat kamu menoleh, ada sesuatu di belakangmu. Sebelum kamu sempat berteriak, semuanya menjadi gelap.')
	print('Tidak ada jejakmu. Hanya barang-barangmu yang tersisa.')


def ending_truth(state):
	print('\n--- ENDING: Kebenaran ---')
	print('Kamu menemukan lembaran-lembaran lama dan foto yang menjelaskan apa yang terjadi di rumah ini.')
	print('Kebenaran itu pahit: tragedi dalam keluarga, rasa bersalah, dan sebuah aturan sederhana: jangan menoleh ke belakang.')


def ending_sacrifice(state):
	print('\n--- ENDING: Pengorbanan ---')
	print('Untuk menyelamatkan orang lain, kamu memilih tinggal. Dunia luar selamat, tetapi kamu tetap di sana.')


def ending_loop(state):
	print('\n--- ENDING: Lingkaran Waktu ---')
	print('Kamu kembali di awal. Seolah rumah menuntut agar aturan itu dilanggar berkali-kali.')


def scene_intro(state):
	print('DontlookBack - Jangan Menoleh ke Belakang')
	print('\nMalam turun ketika kamu kembali ke kampung halaman setelah bertahun-tahun berada di kota.')
	print('Rumah keluarga lama menunggu—penuh barang-barang dan kenangan yang samar.')
	print('Tetangga berkata ada suara-suara aneh, dan seseorang meninggalkan catatan kasar: "JANGAN MENEOLEH KE BELAKANG."')

	c = prompt_choice('Apa yang akan kamu lakukan pertama?', [
		'Masuk ke rumah dan memeriksa ruang tamu.',
		'Mengelilingi rumah di luar dulu, periksa jendela dan pintu.',
		'Kembali ke mobil dan pulang.'
	])

	if c == 1:
		scene_living_room(state)
	elif c == 2:
		scene_outside(state)
	else:
		print('\nKamu memutuskan pulang. Kadang ketakutan itu wajar, tetapi rasa ingin tahu tetap menggigit.')
		ending_escape(state)


def scene_outside(state):
	print('\nDi luar, udara dingin dan ada jejak kaki di tanah basah.')
	c = prompt_choice('Mau lanjut?', [
		'Masuk lewat pintu belakang yang sedikit terbuka.',
		'Periksa jendela samping, lihat ke dalam.',
		'Tunggu sebentar, ada suara—menoleh ke belakang untuk melihat.'
	])
	if c == 1:
		state['found_flashlight'] = True
		print('\nPintu belakang ternyata hampir terbuka. Ada senter tua di lantai dapur.')
		scene_kitchen(state)
	elif c == 2:
		print('\nDari jendela, kamu melihat meja yang berantakan dan foto keluarga yang jatuh.')
		scene_living_room(state)
	else:
		state['looked_back'] += 1
		print('\nKamu menoleh. Hanya kegelapan dan pohon yang menari. Tapi sesuatu terasa berbeda.')
		scene_living_room(state)


def scene_living_room(state):
	print('\nRuang tamu berdebu. Jam dinding berhenti pada waktu yang aneh.')
	c = prompt_choice('Apa yang ingin kamu periksa?', [
		'Periksa foto keluarga di rak.',
		'Naik ke lantai atas untuk memeriksa kamar.',
		'Pergi ke dapur.'
	])
	if c == 1:
		state['found_photos'] = True
		print('\nFoto-foto itu menunjukkan orang yang kamu kenal, tetapi ada salah satu yang tampak diubah—sosok di belakang tampak kabur.')
		scene_whisper(state)
	elif c == 2:
		scene_upstairs(state)
	else:
		scene_kitchen(state)


def scene_whisper(state):
	print('\nSaat kamu memperhatikan foto itu, ruangan terasa lebih dingin. Ada bisikan lembut dari arah loteng.')
	c = prompt_choice('Bisikan itu memunculkan perasaan aneh. Apa yang kamu lakukan?', [
		'Ikuti suara dan naik ke lantai atas.',
		'Abaikan, tetap tenang dan periksa dapur.',
		'Menoleh cepat mencari sumber bisikan.'
	])
	if c == 1:
		scene_upstairs(state)
	elif c == 2:
		scene_kitchen(state)
	else:
		state['looked_back'] += 1
		state['sanity'] -= 1
		print('\nKamu menoleh. Hanya bayangan di sudut, tapi hatimu berdebar.')
		if state['sanity'] <= 0:
			ending_loop(state)
		else:
			scene_attic(state)


def scene_kitchen(state):
	print('\nDapur dingin. Bau logam sedikit terasa. Di meja ada sebuah surat yang sobek.')
	c = prompt_choice('Mau baca surat itu?', ['Baca surat.', 'Jangan baca, kamu merasa diawasi.'])
	if c == 1:
		state['read_note'] = True
		print('\nSurat itu menyinggung tentang kesalahan lama dan sebuah larangan: "Jika kau mendengar, jangan pernah menoleh."')
		scene_whisper(state)
	else:
		print('\nKamu menutup pintu lemari, tetapi terdengar bisik-bisik samar dari loteng.')
		scene_whisper(state)


def scene_upstairs(state):
	print('\nLantai atas berknak. Pintu kamar tertutup, dan ada bekas sepatu yang menuju ke koridor.')
	c = prompt_choice('Langkahmu?', ['Ikuti bekas sepatu.', 'Masuk ke kamar utama.', 'Menoleh ke belakang untuk memastikan koridor kosong.'])
	if c == 1:
		print('\nBekas sepatu berakhir di depan sebuah pintu kecil yang terkunci.')
		state['found_locked'] = True
		scene_attic(state)
	elif c == 2:
		print('\nKamar utama berantakan. Di bawah tempat tidur ada kunci tua.')
		state['found_key'] = True
		scene_attic(state)
	else:
		state['looked_back'] += 1
		print('\nKamu menoleh. Ada bayangan yang bergerak cepat lalu lenyap.')
		state['sanity'] -= 1
		scene_attic(state)


def scene_attic(state):
	print('\nLoteng lembab. Ada pintu kecil yang mungkin menuju ruang bawah tanah atau gudang.')
	c = prompt_choice('Apa yang dilakukan?', ['Buka pintu kecil itu.', 'Pergi turun dan keluarkan mobil dari garasi.', 'Menoleh sekali lagi (meskipun kamu tahu larangan).'])
	if c == 1:
		if state.get('found_key'):
			print('\nKunci cocok. Di balik pintu ada ruang kecil dengan benda-benda lama dan sebuah kotak kayu.')
			state['opened_box'] = True
			scene_box(state)
		else:
			print('\nPintunya terkunci, tapi ada goresan di sekelilingnya—seperti seseorang mencoba melarikan diri.')
			scene_box(state)
	elif c == 2:
		print('\nKamu turun dan menyalakan mobil. Rasa takut mendorongmu untuk pergi.')
		if state['looked_back'] >= 1:
			ending_vanished(state)
		else:
			ending_escape(state)
	else:
		state['looked_back'] += 1
		print('\nKali ini, sesuatu berbisik namamu. Suara itu tidak manusiawi.')
		state['sanity'] -= 2
		if state['sanity'] <= 0:
			ending_loop(state)
		else:
			scene_box(state)


def scene_box(state):
	print('\nDi dalam kotak ada foto, kunci, dan sebuah cermin kecil yang retak.')
	c = prompt_choice('Kamu mengambil...', ['Foto dan kunci.', 'Cermin kecil.', 'Meninggalkan kotak dan turun.'])
	if c == 1:
		state['found_photos'] = True
		state['found_key'] = True
		print('\nFoto-foto itu menegaskan hubunganmu dengan rumah ini—bahkan ada catatan di balik salah satunya: "Maaf."')
	elif c == 2:
		state['took_mirror'] = True
		print('\nCermin retak memantulkan sesuatu yang sepertinya bukan kamu.')
		state['sanity'] -= 1
	else:
		print('\nKamu turun dengan perasaan campur aduk.')

	decide_final(state)


def decide_final(state):
	print('\nMalam semakin larut. Waktu untuk membuat keputusan terakhir.')
	c = prompt_choice('Pilihan akhir?', ['Keluar dan jangan menoleh sama sekali.', 'Menoleh sekali, cari jawaban.', 'Tinggal dan hadapi apa pun di rumah.'])
	if c == 1:
		if state['looked_back'] == 0 and state['sanity'] >= 2:
			ending_escape(state)
		else:
			ending_vanished(state)
	elif c == 2:
		if state.get('took_mirror') or state.get('read_note'):
			ending_truth(state)
		else:
			ending_vanished(state)
	else:
		if state.get('found_photos') and state.get('found_key'):
			ending_sacrifice(state)
		else:
			ending_loop(state)


def main():
	state = {
		'sanity': 3,
		'looked_back': 0,
		'found_flashlight': False,
		'found_photos': False,
		'found_key': False,
		'read_note': False,
		'took_mirror': False,
	}

	try:
		scene_intro(state)
	except (KeyboardInterrupt, EOFError):
		print('\nPermainan dihentikan. Sampai jumpa.')
		sys.exit(0)


if __name__ == '__main__':
	main()

