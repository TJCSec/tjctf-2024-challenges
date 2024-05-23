#include <vector>

Word invS_f(Word in)
{
	return (invSbox[in >> 8] << 8) | invSbox[in & 0xff];
}


Word invP_f(Word in)
{
	int r = 3;

	//std::cout << "in " << in << "\n";

	Word out2 = 0;
	out2 |= in << r;
	out2 |= in >> (16 - r);
	//std::cout << "out2 " << out2 << "\n";
	out2 ^= out2 >> 8;

	Word out = 0;
	out |= (out2 >> 8) & 0xff;
	out |= (out2 & 0xff) << 8;
	//std::cout << "out " << out << "\n";
	return out;
}

RKey smashKey(Key in, int phase)
{
	RKey r;
		switch (phase % 255)
	{

		case 0:
			r = getMask<167>(in);

		case 1:
			r = getMask<97>(in);

		case 2:
			r = getMask<125>(in);

		case 3:
			r = getMask<68>(in);

		case 4:
			r = getMask<20>(in);

		case 5:
			r = getMask<46>(in);

		case 6:
			r = getMask<104>(in);

		case 7:
			r = getMask<242>(in);

		case 8:
			r = getMask<222>(in);

		case 9:
			r = getMask<172>(in);

		case 10:
			r = getMask<203>(in);

		case 11:
			r = getMask<103>(in);

		case 12:
			r = getMask<16>(in);

		case 13:
			r = getMask<22>(in);

		case 14:
			r = getMask<80>(in);

		case 15:
			r = getMask<200>(in);

		case 16:
			r = getMask<60>(in);

		case 17:
			r = getMask<91>(in);

		case 18:
			r = getMask<234>(in);

		case 19:
			r = getMask<141>(in);

		case 20:
			r = getMask<155>(in);

		case 21:
			r = getMask<162>(in);

		case 22:
			r = getMask<72>(in);

		case 23:
			r = getMask<44>(in);

		case 24:
			r = getMask<12>(in);

		case 25:
			r = getMask<95>(in);

		case 26:
			r = getMask<7>(in);

		case 27:
			r = getMask<151>(in);

		case 28:
			r = getMask<197>(in);

		case 29:
			r = getMask<195>(in);

		case 30:
			r = getMask<188>(in);

		case 31:
			r = getMask<61>(in);

		case 32:
			r = getMask<251>(in);

		case 33:
			r = getMask<51>(in);

		case 34:
			r = getMask<179>(in);

		case 35:
			r = getMask<239>(in);

		case 36:
			r = getMask<156>(in);

		case 37:
			r = getMask<10>(in);

		case 38:
			r = getMask<178>(in);

		case 39:
			r = getMask<122>(in);

		case 40:
			r = getMask<193>(in);

		case 41:
			r = getMask<173>(in);

		case 42:
			r = getMask<44>(in);

		case 43:
			r = getMask<216>(in);

		case 44:
			r = getMask<129>(in);

		case 45:
			r = getMask<4>(in);

		case 46:
			r = getMask<207>(in);

		case 47:
			r = getMask<171>(in);

		case 48:
			r = getMask<128>(in);

		case 49:
			r = getMask<44>(in);

		case 50:
			r = getMask<213>(in);

		case 51:
			r = getMask<28>(in);

		case 52:
			r = getMask<21>(in);

		case 53:
			r = getMask<91>(in);

		case 54:
			r = getMask<197>(in);

		case 55:
			r = getMask<171>(in);

		case 56:
			r = getMask<208>(in);

		case 57:
			r = getMask<246>(in);

		case 58:
			r = getMask<10>(in);

		case 59:
			r = getMask<84>(in);

		case 60:
			r = getMask<5>(in);

		case 61:
			r = getMask<153>(in);

		case 62:
			r = getMask<43>(in);

		case 63:
			r = getMask<28>(in);

		case 64:
			r = getMask<44>(in);

		case 65:
			r = getMask<24>(in);

		case 66:
			r = getMask<20>(in);

		case 67:
			r = getMask<136>(in);

		case 68:
			r = getMask<30>(in);

		case 69:
			r = getMask<137>(in);

		case 70:
			r = getMask<141>(in);

		case 71:
			r = getMask<172>(in);

		case 72:
			r = getMask<38>(in);

		case 73:
			r = getMask<8>(in);

		case 74:
			r = getMask<171>(in);

		case 75:
			r = getMask<46>(in);

		case 76:
			r = getMask<113>(in);

		case 77:
			r = getMask<19>(in);

		case 78:
			r = getMask<25>(in);

		case 79:
			r = getMask<248>(in);

		case 80:
			r = getMask<230>(in);

		case 81:
			r = getMask<181>(in);

		case 82:
			r = getMask<223>(in);

		case 83:
			r = getMask<218>(in);

		case 84:
			r = getMask<168>(in);

		case 85:
			r = getMask<30>(in);

		case 86:
			r = getMask<18>(in);

		case 87:
			r = getMask<51>(in);

		case 88:
			r = getMask<149>(in);

		case 89:
			r = getMask<187>(in);

		case 90:
			r = getMask<228>(in);

		case 91:
			r = getMask<101>(in);

		case 92:
			r = getMask<232>(in);

		case 93:
			r = getMask<249>(in);

		case 94:
			r = getMask<38>(in);

		case 95:
			r = getMask<237>(in);

		case 96:
			r = getMask<53>(in);

		case 97:
			r = getMask<52>(in);

		case 98:
			r = getMask<173>(in);

		case 99:
			r = getMask<135>(in);

		case 100:
			r = getMask<240>(in);

		case 101:
			r = getMask<37>(in);

		case 102:
			r = getMask<212>(in);

		case 103:
			r = getMask<12>(in);

		case 104:
			r = getMask<230>(in);

		case 105:
			r = getMask<97>(in);

		case 106:
			r = getMask<22>(in);

		case 107:
			r = getMask<3>(in);

		case 108:
			r = getMask<164>(in);

		case 109:
			r = getMask<181>(in);

		case 110:
			r = getMask<53>(in);

		case 111:
			r = getMask<154>(in);

		case 112:
			r = getMask<118>(in);

		case 113:
			r = getMask<179>(in);

		case 114:
			r = getMask<39>(in);

		case 115:
			r = getMask<104>(in);

		case 116:
			r = getMask<100>(in);

		case 117:
			r = getMask<9>(in);

		case 118:
			r = getMask<72>(in);

		case 119:
			r = getMask<71>(in);

		case 120:
			r = getMask<81>(in);

		case 121:
			r = getMask<22>(in);

		case 122:
			r = getMask<134>(in);

		case 123:
			r = getMask<4>(in);

		case 124:
			r = getMask<87>(in);

		case 125:
			r = getMask<38>(in);

		case 126:
			r = getMask<8>(in);

		case 127:
			r = getMask<129>(in);

		case 128:
			r = getMask<100>(in);

		case 129:
			r = getMask<135>(in);

		case 130:
			r = getMask<225>(in);

		case 131:
			r = getMask<206>(in);

		case 132:
			r = getMask<132>(in);

		case 133:
			r = getMask<194>(in);

		case 134:
			r = getMask<30>(in);

		case 135:
			r = getMask<86>(in);

		case 136:
			r = getMask<167>(in);

		case 137:
			r = getMask<179>(in);

		case 138:
			r = getMask<79>(in);

		case 139:
			r = getMask<224>(in);

		case 140:
			r = getMask<96>(in);

		case 141:
			r = getMask<246>(in);

		case 142:
			r = getMask<64>(in);

		case 143:
			r = getMask<152>(in);

		case 144:
			r = getMask<156>(in);

		case 145:
			r = getMask<56>(in);

		case 146:
			r = getMask<162>(in);

		case 147:
			r = getMask<88>(in);

		case 148:
			r = getMask<94>(in);

		case 149:
			r = getMask<21>(in);

		case 150:
			r = getMask<225>(in);

		case 151:
			r = getMask<60>(in);

		case 152:
			r = getMask<125>(in);

		case 153:
			r = getMask<138>(in);

		case 154:
			r = getMask<74>(in);

		case 155:
			r = getMask<60>(in);

		case 156:
			r = getMask<52>(in);

		case 157:
			r = getMask<168>(in);

		case 158:
			r = getMask<251>(in);

		case 159:
			r = getMask<57>(in);

		case 160:
			r = getMask<160>(in);

		case 161:
			r = getMask<230>(in);

		case 162:
			r = getMask<48>(in);

		case 163:
			r = getMask<157>(in);

		case 164:
			r = getMask<226>(in);

		case 165:
			r = getMask<167>(in);

		case 166:
			r = getMask<11>(in);

		case 167:
			r = getMask<211>(in);

		case 168:
			r = getMask<64>(in);

		case 169:
			r = getMask<50>(in);

		case 170:
			r = getMask<4>(in);

		case 171:
			r = getMask<193>(in);

		case 172:
			r = getMask<231>(in);

		case 173:
			r = getMask<27>(in);

		case 174:
			r = getMask<3>(in);

		case 175:
			r = getMask<208>(in);

		case 176:
			r = getMask<13>(in);

		case 177:
			r = getMask<211>(in);

		case 178:
			r = getMask<51>(in);

		case 179:
			r = getMask<193>(in);

		case 180:
			r = getMask<140>(in);

		case 181:
			r = getMask<94>(in);

		case 182:
			r = getMask<168>(in);

		case 183:
			r = getMask<243>(in);

		case 184:
			r = getMask<84>(in);

		case 185:
			r = getMask<128>(in);

		case 186:
			r = getMask<180>(in);

		case 187:
			r = getMask<32>(in);

		case 188:
			r = getMask<30>(in);

		case 189:
			r = getMask<145>(in);

		case 190:
			r = getMask<173>(in);

		case 191:
			r = getMask<91>(in);

		case 192:
			r = getMask<188>(in);

		case 193:
			r = getMask<243>(in);

		case 194:
			r = getMask<112>(in);

		case 195:
			r = getMask<130>(in);

		case 196:
			r = getMask<47>(in);

		case 197:
			r = getMask<110>(in);

		case 198:
			r = getMask<20>(in);

		case 199:
			r = getMask<227>(in);

		case 200:
			r = getMask<201>(in);

		case 201:
			r = getMask<0>(in);

		case 202:
			r = getMask<117>(in);

		case 203:
			r = getMask<125>(in);

		case 204:
			r = getMask<153>(in);

		case 205:
			r = getMask<30>(in);

		case 206:
			r = getMask<118>(in);

		case 207:
			r = getMask<111>(in);

		case 208:
			r = getMask<69>(in);

		case 209:
			r = getMask<235>(in);

		case 210:
			r = getMask<107>(in);

		case 211:
			r = getMask<187>(in);

		case 212:
			r = getMask<206>(in);

		case 213:
			r = getMask<240>(in);

		case 214:
			r = getMask<54>(in);

		case 215:
			r = getMask<147>(in);

		case 216:
			r = getMask<108>(in);

		case 217:
			r = getMask<122>(in);

		case 218:
			r = getMask<32>(in);

		case 219:
			r = getMask<101>(in);

		case 220:
			r = getMask<39>(in);

		case 221:
			r = getMask<186>(in);

		case 222:
			r = getMask<139>(in);

		case 223:
			r = getMask<29>(in);

		case 224:
			r = getMask<43>(in);

		case 225:
			r = getMask<227>(in);

		case 226:
			r = getMask<40>(in);

		case 227:
			r = getMask<187>(in);

		case 228:
			r = getMask<86>(in);

		case 229:
			r = getMask<167>(in);

		case 230:
			r = getMask<220>(in);

		case 231:
			r = getMask<27>(in);

		case 232:
			r = getMask<199>(in);

		case 233:
			r = getMask<0>(in);

		case 234:
			r = getMask<108>(in);

		case 235:
			r = getMask<196>(in);

		case 236:
			r = getMask<58>(in);

		case 237:
			r = getMask<193>(in);

		case 238:
			r = getMask<17>(in);

		case 239:
			r = getMask<154>(in);

		case 240:
			r = getMask<237>(in);

		case 241:
			r = getMask<33>(in);

		case 242:
			r = getMask<126>(in);

		case 243:
			r = getMask<193>(in);

		case 244:
			r = getMask<246>(in);

		case 245:
			r = getMask<132>(in);

		case 246:
			r = getMask<96>(in);

		case 247:
			r = getMask<138>(in);

		case 248:
			r = getMask<73>(in);

		case 249:
			r = getMask<44>(in);

		case 250:
			r = getMask<88>(in);

		case 251:
			r = getMask<8>(in);

		case 252:
			r = getMask<58>(in);

		case 253:
			r = getMask<226>(in);

		case 254:
			r = getMask<149>(in);

		case 255:
			r = getMask<143>(in);
	}

	return r;
}

Word r4(Word in, Key kin)
{

	RKey k0 = smashKey(kin, 0);
	RKey k1 = smashKey(kin, 0);
	RKey k2 = smashKey(kin, 0);
	RKey k3 = smashKey(kin, 0);
 
	kin ^= k0;
	kin ^= ((Key)k0) << 32;
	kin |= 0xff << 24;
	kin |= 0xffULL << (24 + 32);

	Key k = kin;

	k0 = k & 0xffffffff;
	k0 ^= 1162466901;
	k0 ^= k0 >> 16;
	k0 *= 3726821653;

	k1 = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
	k1 ^= 3811777446;
	k1 = (k1 * 1240568533);

	k2 = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
	k2 ^= 3915669785;
	k2 = (k2 * 1247778533);

	k3 = ((k >> 32) & 0xffffffff) ^ (k & 0xffffffff);
	k3 ^= 3140176925;
	k3 = (k3 * 1934965865);	

	//std::cout << "Round keys: " << ((k0 & 0xffff) ^ ((k0 >> 16) & 0xffff)) << " " << k0 << " " << k1 << " " << k2 << " " << k3 << "\n";

	Word out = r(in, k0);
	out = r(out, k1);
	out = r(out, k2);
	out = r(out, k3);
	return out;
}

void kinfo(Key kin)
{

	RKey k0 = smashKey(kin, 0);
	RKey k1 = smashKey(kin, 0);
	RKey k2 = smashKey(kin, 0);
	RKey k3 = smashKey(kin, 0);

	kin ^= k0;
	kin ^= ((Key)k0) << 32;
	kin |= 0xff << 24;
	kin |= 0xffULL << (24 + 32);

	Key k = kin;

	k0 = k & 0xffffffff;
	k0 ^= 1162466901;
	k0 ^= k0 >> 16;
	k0 *= 3726821653;

	std::cout << "k0x: " << ((k0 & 0xffff) ^ ((k0 >> 16) & 0xffff)) << "\n";

	std::cout << "lxr: " << (((k >> 32) & 0xffffffff) ^ (k & 0xffffffff)) << "\n";
}

Word r_i(Word in, RKey kin)
{
	Word smeck = invS_f(invP_f(in));
	RKey k = kin;
	smeck ^= (k & 0xffff) ^ ((k >> 16) & 0xffff);
	return smeck;
}

Word invSP(Word in)
{
	return invS_f(invP_f(in));
}

Word lowK(Word in, Word out, RKey lxr)
{
	RKey magic = 196558397; //mod inverse of 3726821653 (mod 1 << 32)

	RKey k1 = lxr;
	k1 ^= 3811777446;
	k1 = (k1 * 1240568533);

	RKey k2 = lxr;
	k2 ^= 3915669785;
	k2 = (k2 * 1247778533);

	RKey k3 = lxr;
	k3 ^= 3140176925;
	k3 = (k3 * 1934965865);

	Word s3 = r_i(out, k3);
	Word s2 = r_i(s3, k2);
	Word s1 = r_i(s2, k1);
	Word r1 = invSP(s1);
	//r1 = in ^ (k0 & 0xffff) ^ (k0 >> 16)
	return (in ^ r1);
}

Word r4_lxr(Word in, Word k0x, RKey lxr)
{
	RKey k0 = k0x;

	RKey k1 = lxr;
	k1 ^= 3811777446;
	k1 = (k1 * 1240568533);

	RKey k2 = lxr;
	k2 ^= 3915669785;
	k2 = (k2 * 1247778533);

	RKey k3 = lxr;
	k3 ^= 3140176925;
	k3 = (k3 * 1934965865);

	Word out = r(in, k0);
	out = r(out, k1);
	out = r(out, k2);
	out = r(out, k3);
	return out;
}

Word enc4(Word in, Key k)
{
	Word out = in;
	for (int i = 0; i < rounds / 4; i++)
	{
		out = r4(out, k);
	}
	return out;
}

Word enc4_lxr(Word in, Word k0x, RKey lxr)
{
	Word out = in;
	for (int i = 0; i < rounds / 4; i++)
	{
		out = r4_lxr(out, k0x, lxr);
	}
	return out;
}

void test_lxr()
{
	Key kin = key;
	kin ^= smashKey(kin, 0);
	kin ^= ((Key)smashKey(kin, 0)) << 32;
	kin |= 0xff << 24;
	kin |= 0xffULL << (24 + 32);

	RKey lxr = (kin >> 32) ^ (kin & 0xffffffff);

	Word m = rand();

	Word c = r4(m, key);

	std::cout << "m, c: " << m << " " << c << "\n";
	std::cout << lowK(m, c, lxr) << "\n";
	std::cout << "r4 with l xor r vs r4: " << r4_lxr(m, lowK(m, c, lxr), lxr) << " " << r4(m, key) << "\n";
}

bool verf(Word p, Word c, Word k0x, RKey lxr)
{
	return enc4_lxr(p, k0x, lxr) == c;
}

Word r4_lxr_i(Word in, Word k0x, RKey lxr)
{
	RKey k0 = k0x;

	RKey k1 = lxr;
	k1 ^= 3811777446;
	k1 = (k1 * 1240568533);

	RKey k2 = lxr;
	k2 ^= 3915669785;
	k2 = (k2 * 1247778533);

	RKey k3 = lxr;
	k3 ^= 3140176925;
	k3 = (k3 * 1934965865);

	Word out = r_i(in, k3);
	out = r_i(out, k2);
	out = r_i(out, k1);
	out = r_i(out, k0);
	return out;
}

Word dec4_lxr(Word in, Word k0x, RKey lxr)
{
	Word out = in;
	for (int i = 0; i < rounds / 4; i++)
	{
		out = r4_lxr_i(out, k0x, lxr);
	}
	return out;
}

std::vector<std::pair<Word, RKey>> get_k0x_lxrs(Word p0, Word p1, Word c0, Word c1)
{
	std::vector<std::pair<Word, RKey>> out;
	for (RKey lxr = 0; lxr < 1 << 24; lxr++)
	{
		Word k0x = lowK(p0, p1, lxr);
		if (r4_lxr(c0, k0x, lxr) == c1)
		{
			//maybe slid pair??
			if (verf(p0, c0, k0x, lxr))
				out.push_back({ k0x, lxr });
		}
	}
	return out;
}

void crack(std::vector<std::pair<Word, Word>> pairs)
{
	int ctr = 0;
	for (auto& pr1 : pairs)
	{
		for (auto& pr2 : pairs)
		{
			ctr++;

			Word p0 = pr1.first;
			Word p1 = pr2.first;
			Word c0 = pr1.second;
			Word c1 = pr2.second;
			auto fnd = get_k0x_lxrs(p0, p1, c0, c1);
			for (auto& i : fnd)
			{
				std::cout << i.first << " " << i.second << "\n";
				Word out[21];
				out[20] = 0;

				for (int ctr = 0; ctr < 40; ctr += 2)
				{
					out[ctr / 2] = dec4_lxr(*(Word*)&flag[ctr / 2], i.first, i.second);
				}

				std::cout << (char*)out << "\n";
			}

			std::cout << "\r" << ctr << " pairs tested....       ";
			
		}
	}
}


void all()
{
	kinfo(key);

	readflag();

	auto st = std::chrono::high_resolution_clock::now();

	std::vector<std::pair<Word, Word>> pairs;

	for (int i = 0; i < 18; i++)
	{
		Word p = getRand();
		Word c = oracle(p);
		pairs.push_back({ p, c });
	}

	Word p0 = getRand();
	Word p1 = r4(p0, key);
	Word c0 = oracle(p0);
	Word c1 = oracle(p1);

	pairs.push_back({ p0, c0 });
	pairs.push_back({ p1, c1 });

	for (int i = 0; i < 20; i++)
	{
		swap(pairs[getRand() % 20], pairs[getRand() % 20]);
	}

	std::cout << "OUTPUT.TXT STARTS HERE\n\n";

	for (auto& pair : pairs)
	{
		std::cout << "Plaintext, ciphertext: " << pair.first << " " << pair.second << "\n";
	}

	for (int i = 0; i < 20; i++)
	{
		std::cout << "Flag, ciphertext: " << flag[i] << "\n";
	}

	std::cout << "OUTPUT.TXT ENDS HERE\n\n";

	auto end = std::chrono::high_resolution_clock::now();

	std::cout << "Pair gen took " << std::chrono::duration_cast<std::chrono::microseconds>(end - st).count() << " us\n";

	st = std::chrono::high_resolution_clock::now();
	crack(pairs);
	end = std::chrono::high_resolution_clock::now();

	std::cout << "Crack took " << std::chrono::duration_cast<std::chrono::microseconds>(end - st).count() << " us\n";
}
