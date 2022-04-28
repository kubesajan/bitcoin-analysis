import os, itertools
gathered_keys = set()
num_keys = os.path.getsize("keys_set") // 16
f = open("keys_set", "rb")
g = open("found_low_hw_direct", "w")
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

counter = 0
X = 0*G
for i in range(1,5):
	for bits in itertools.combinations(range(256), i):
		counter = counter + 1
		X = 0*G
		bitstr = ['0'] * 256
		for bit in bits:
			X = X + hwvalues[bit]
			bitstr[bit] = '1'
		temp = bytes.fromhex(Integer((X).xy()[0]).hex()[:32])
		if temp in gathered_keys:
			bitstr = ''.join(bitstr)
			g.write(str(int(bitstr,2)) + "\n")
		if (counter % 100000) == 0:
			print(counter)
g.close()
