from gpiozero import Button, InputDevice
button = Button(24)

while True:
	if button.is_pressed:
		print("On")
	else:
		print("off")

