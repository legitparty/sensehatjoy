#!/usr/bin/env python

class HSBColor:
	def __init__(self, h = 0.0, s = 0.0, b = 0.0):
		self.h = h
		self.s = s
		self.b = b

	def rgb(self):
		normal_h = (float(self.h) * 3.0) % 3.0
		hr  = 1.0 - (min(1.0, abs(normal_h      )))
		hg  = 1.0 - (min(1.0, abs(normal_h - 1.0)))
		hb  = 1.0 - (min(1.0, abs(normal_h - 2.0)))
		hr2 = 1.0 - (min(1.0, abs(normal_h - 3.0)))
		hr += hr2
		r = self.b - (self.s * self.b) * (1.0 - hr)
		g = self.b - (self.s * self.b) * (1.0 - hg)
		b = self.b - (self.s * self.b) * (1.0 - hb)
		return int(r * 255), int(g * 255), int(b * 255)

	def copy(self):
		return HSBColor(self.h, self.s, self.b)

class HSBDisplay:
	def __init__(self, width = 8, height = 8, image = None):
		self.width = width
		self.height = height
		if image is None:
			self.image = [[HSBColor() for x in range(self.width)] for y in range(self.height)]
		else:
			self.image = image
		

	def rgb(self):
		return [
			[x.rgb() for x in y]
			for y
			in self.image
		]

	def get_pixel(self, x, y):
		return self.image[y][x]

	def set_pixel(self, x, y, hsb):
		pixel = self.get_pixel(x, y)
		pixel.h = hsb.h
		pixel.s = hsb.s
		pixel.b = hsb.b

	def draw(self, hat):
		pixels = []
		for row in self.rgb():
			pixels.extend(row)

		hat.set_pixels(pixels)

	def copy(self):
		image = [[hsb.copy() for hsb in range(self.width)] for y in range(self.height)]
		return HSBDisplay(self.width, self.height, image)

class HatPen:
	def __init__(self):
		from sense_hat import SenseHat
		self.hat = SenseHat()
		self.hat.clear()
		self.cursor_pos = (0, 0)
		self.cursor_color = HSBColor()
		self.display = HSBDisplay()

	def apply(self):
		x, y = self.cursor_pos
		self.display.set_pixel(x, y, self.cursor_color)

	def draw(self):
		self.display.draw(self.hat)

	def draw_cursor(self):
		x, y = self.cursor_pos
		self.hat.set_pixel(x, y, self.cursor_color.rgb())

class HatJoy(HatPen):
	pass

	

def main():
	from sys import stdout
	from sense_hat.stick import SenseStick
	j = SenseStick()
	hsb = [
		1.0,
		1.0,
		1.0,
	]
	hsb_labels = ["hue", "saturation", "brightness"]

	c_cursor = 0
	c_color = 1
	c_drawing = 2
	c_labels = ["cursor", "color", "drawing"]

	c = 0
	i = 0
	x = 0
	y = 0

	o = HatPen()
	o.cursor_color = HSBColor(hsb[0], hsb[1], hsb[2])
	o.cursor_pos = (x, y)

	while True:
		stdout.write("\r")
		stdout.flush()
		print "-" * 40
		print "In %s command mode." %   c_labels[c%3]
		if c_labels[c%3] == "color":
			print "HSBColor(h=%.2f, s=%.2f, b=%.2f)." % (hsb[0], hsb[1], hsb[2])
			print "%s to %.2f" % (hsb_labels[i%3], hsb[i%3])
		print "Cursor at pos: %i, %i" % (x, y)
		o.draw()
		if c_labels[c%3] in ["cursor", "color"]:
			o.draw_cursor()
		e = j.wait_for_event()

		if e.action == "pressed":# or e.action == "held":
			if e.direction == "middle":
				c += 1
				continue
			elif e.direction == "up":
				if c_labels[c%3] == "color":
					hsb[i%3] = max(0.0, min(1.0, hsb[i%3] + 0.01))
					o.cursor_color = HSBColor(hsb[0], hsb[1], hsb[2])
				else:
					y = max(0, min(7, y - 1))
					o.cursor_pos = (x, y)
			elif e.direction == "down":
				if c_labels[c%3] == "color":
					hsb[i%3] = max(0.0, min(1.0, hsb[i%3] - 0.01))
					o.cursor_color = HSBColor(hsb[0], hsb[1], hsb[2])
				else:
					y = max(0, min(7, y + 1))
					o.cursor_pos = (x, y)
			elif e.direction == "left":
				if c_labels[c%3] == "color":
					i -= 1
					o.cursor_color = HSBColor(hsb[0], hsb[1], hsb[2])
				else:
					x = max(0, min(7, x - 1))
					o.cursor_pos = (x, y)
			elif e.direction == "right":
				if c_labels[c%3] == "color":
					i += 1
					o.cursor_color = HSBColor(hsb[0], hsb[1], hsb[2])
				else:
					x = max(0, min(7, x + 1))
					o.cursor_pos = (x, y)

			if c_labels[c%3] == "drawing":
				o.apply()


	


if __name__ == '__main__':
	main()
