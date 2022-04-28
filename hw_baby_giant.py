import os, itertools
gathered_keys = set()
num_keys = os.path.getsize("keys_set") // 16
f = open("keys_set", "rb")
g = open("found_low_hw_baby_giant", "w")
for i in range (num_keys):
	gathered_keys.add(f.read(16))

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000007)
E = EllipticCurve(K, (a, b))
G = E(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
E.set_order(0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 * 0x1)

hwvalues = list()
for i in range(256):
	hwvalues.append((2**i)*G)
d_publics = list()
d_privates = list()
for bits in itertools.combinations(range(256), 3):
	d_public = 0*G
	bitstr = ['0'] * 256
	for bit in bits:
		d_public = d_public + hwvalues[bit]
		bitstr[bit] = '1'
	d_publics.append(d_public)
	bitstr = ''.join(bitstr)
	d_privates.append(int(bitstr,2))
counter = 0
X = 0*G
for i in range(len(d_publics)):
	for j in range(len(d_publics)):
		counter = counter + 1
		X = d_publics[i] + d_publics[j]
		temp = bytes.fromhex(Integer((X).xy()[0]).hex()[:32])
		if temp in gathered_keys:
			private = d_privates[i] + d_privates[j]
			g.write(str(private) + "\n")
		if (counter % 100000) == 0:
			print(counter)
g.close()
