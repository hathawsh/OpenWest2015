"""
Convert a 320x240 ASCII PPM to a list of drawing commands for the OpenWest
2015 conference badge add-on kit.  This is just a quick hack to get my
badge to show a static image of my choice.

Steps:

1. In the GIMP, create a simple 320x240 image with a white background and
   minimal colors.  The more complex the image, the more likely we'll run
   out of program space.

2. Export the image as an ASCII PPM file named image.ppm.

3. Run this program and copy its output into the drawing portion of
   drawrects.spin.

4. Use PropellerIDE to build the binary.  The binary output file will appear
   in the same directory as drawrects.spin.

   http://developer.parallax.com/projects/propelleride/

5. Copy the binary output file to the MicroSD card as run.bin, install the
   card and turn on your badge.
"""


lines = open('image.ppm').readlines()[4:]
colors = []
for i in range(0, len(lines), 3):
    tup = lines[i:i + 3]
    if len(tup) == 3:
        r, g, b = tup
        r = int(r)
        g = int(g)
        b = int(b)
        color = ((r & 0xf8) << 8) | ((g & 0xfc) << 3) | ((b & 0xf8) >> 3)
        colors.append(color)


def print_rect(c, x0, x1, y):
    if c != 0xffff:
        print('disp.SetColours($%x, $ffff)' % c)
        print('disp.DrawRect(%d, %d, %d, %d)' % (x0, y, x1, y))


for y in range(240):
    old_c = None
    x0 = None
    for x in xrange(320):
        c = colors[320 * (239 - y) + (319 - x)]
        if c != old_c:
            if x0 is not None:
                print_rect(old_c, x0, x - 1, y)
            x0 = x
            old_c = c
    if x0 is not None:
        print_rect(old_c, x0, 319, y)
