#include "solve.h"
#include <iostream>
#include <cstring>
#include <bitset>
#include <unordered_map>
#include "sha256.h"

uint8_t s1[256] = { 160, 184, 19, 185, 104, 20, 68, 18, 25, 24, 27, 137, 29, 28, 23, 17, 1, 222, 41, 55, 22, 4, 7, 113, 57, 101, 127, 10, 13, 190, 253, 218, 94, 205, 51, 77, 208, 73, 176, 189, 9, 213, 59, 60, 106, 196, 63, 62, 142, 180, 227, 34, 90, 203, 98, 89, 37, 198, 40, 42, 88, 125, 133, 46, 81, 39, 83, 186, 85, 84, 224, 86, 245, 45, 91, 177, 93, 35, 95, 118, 56, 240, 67, 66, 69, 92, 71, 70, 249, 193, 75, 74, 182, 241, 79, 78, 146, 116, 30, 172, 50, 61, 119, 114, 121, 120, 111, 122, 199, 147, 129, 126, 97, 15, 99, 5, 169, 100, 48, 102, 105, 21, 212, 31, 109, 108, 159, 130, 123, 144, 12, 6, 140, 252, 151, 150, 250, 152, 155, 154, 157, 195, 117, 158, 82, 202, 87, 80, 47, 225, 135, 134, 112, 136, 149, 3, 141, 231, 143, 33, 173, 107, 179, 178, 181, 156, 183, 233, 16, 167, 188, 11, 54, 187, 65, 216, 161, 220, 214, 200, 165, 164, 103, 166, 26, 168, 171, 131, 248, 49, 110, 174, 209, 53, 139, 210, 243, 223, 215, 115, 207, 191, 219, 14, 221, 163, 2, 0, 201, 192, 32, 194, 197, 38, 44, 43, 72, 138, 36, 128, 175, 204, 217, 206, 76, 64, 8, 242, 132, 244, 247, 246, 52, 162, 239, 153, 96, 148, 255, 254, 58, 145, 124, 226, 229, 228, 211, 230, 251, 232, 235, 234, 237, 236, 170, 238 };

uint8_t s2[256] = { 17, 74, 19, 0, 140, 20, 23, 60, 47, 178, 27, 232, 122, 229, 31, 145, 163, 57, 3, 154, 242, 225, 125, 217, 9, 8, 11, 10, 13, 50, 233, 71, 49, 43, 51, 12, 237, 134, 26, 176, 18, 36, 59, 58, 197, 2, 205, 139, 33, 136, 87, 48, 37, 171, 39, 180, 254, 212, 85, 42, 64, 44, 162, 46, 203, 66, 83, 82, 34, 251, 159, 172, 89, 248, 91, 117, 179, 92, 52, 228, 65, 204, 177, 1, 250, 200, 14, 70, 146, 221, 75, 16, 77, 76, 79, 78, 113, 112, 99, 114, 115, 214, 116, 5, 121, 105, 35, 29, 100, 124, 127, 126, 97, 206, 156, 95, 101, 211, 103, 102, 120, 104, 107, 106, 182, 108, 111, 110, 173, 72, 147, 130, 53, 148, 151, 150, 153, 152, 158, 22, 157, 90, 218, 155, 129, 128, 131, 73, 216, 142, 185, 227, 137, 32, 24, 210, 141, 25, 143, 238, 165, 186, 93, 160, 94, 38, 183, 109, 69, 184, 187, 84, 189, 188, 191, 61, 161, 55, 220, 235, 135, 7, 243, 167, 169, 231, 56, 170, 15, 86, 175, 40, 209, 208, 21, 138, 213, 149, 194, 240, 6, 30, 219, 123, 199, 195, 67, 249, 193, 192, 168, 190, 54, 215, 144, 198, 96, 68, 252, 223, 62, 28, 207, 81, 241, 45, 166, 118, 245, 244, 247, 246, 222, 88, 196, 202, 253, 230, 255, 236, 4, 224, 174, 226, 98, 181, 80, 201, 133, 63, 119, 234, 164, 41, 239, 132 };

uint32_t cvt2u32(uint8_t* in)
{
	uint32_t out = 0;
	for (int i = 0; i < 4; i++)
	{
		out |= ((uint32_t)in[3 - i]) << (i * 8);
	}
	return out;
}

void cvt2u8(uint32_t in, uint8_t* arr)
{
	for (int i = 0; i < 4; i++)
	{
		arr[3 - i] = (in >> (i * 8)) & 0xff;
	}
}

template<bool mod_s1>
void make_sbox(uint8_t* k)
{
	uint8_t* target;
	if (mod_s1){
		target = s1;
}
	else {
		target = s2;
	}

	uint8_t temp[256] = { 17, 16, 19, 18, 21, 20, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 49, 48, 51, 50, 53, 52, 55, 54, 57, 56, 59, 58, 61, 60, 63, 62, 33, 32, 35, 34, 37, 36, 39, 38, 41, 40, 43, 42, 45, 44, 47, 46, 81, 80, 83, 82, 85, 84, 87, 86, 89, 88, 91, 90, 93, 92, 95, 94, 65, 64, 67, 66, 69, 68, 71, 70, 73, 72, 75, 74, 77, 76, 79, 78, 113, 112, 115, 114, 117, 116, 119, 118, 121, 120, 123, 122, 125, 124, 127, 126, 97, 96, 99, 98, 101, 100, 103, 102, 105, 104, 107, 106, 109, 108, 111, 110, 145, 144, 147, 146, 149, 148, 151, 150, 153, 152, 155, 154, 157, 156, 159, 158, 129, 128, 131, 130, 133, 132, 135, 134, 137, 136, 139, 138, 141, 140, 143, 142, 177, 176, 179, 178, 181, 180, 183, 182, 185, 184, 187, 186, 189, 188, 191, 190, 161, 160, 163, 162, 165, 164, 167, 166, 169, 168, 171, 170, 173, 172, 175, 174, 209, 208, 211, 210, 213, 212, 215, 214, 217, 216, 219, 218, 221, 220, 223, 222, 193, 192, 195, 194, 197, 196, 199, 198, 201, 200, 203, 202, 205, 204, 207, 206, 241, 240, 243, 242, 245, 244, 247, 246, 249, 248, 251, 250, 253, 252, 255, 254, 225, 224, 227, 226, 229, 228, 231, 230, 233, 232, 235, 234, 237, 236, 239, 238 };

	uint8_t swappers[256];

	for (int i = 0; i < 8; i++)
	{
		SHA256 hasher;
		if (i == 0)
		{
			hasher.update(k, 4);
			auto arr = hasher.digest();
			memcpy(swappers, &arr[0], 32);
			continue;
		}

		hasher.update(&swappers[(i - 1) * 32], 32);
		auto arr = hasher.digest();
		memcpy(&swappers[i * 32], &arr[0], 32);
	}



	for (int i = 0; i < 256; i += 2)
	{
		std::swap(temp[swappers[i]], temp[swappers[i + 1]]);
	}
	//for (int i = 0; i < 256; i++)
	//{
	//	std::cout << (int)temp[i] << "\n";
	//}

	std::memcpy(target, temp, 256);
}

uint32_t r_1(uint32_t r)
{
	uint8_t out[4];

	uint8_t in[4];

	cvt2u8(r, in);

	std::memcpy(out, in, 4);
	for (int i = 0; i < 4; i++)
	{
		out[i] = s1[in[i]];
	}

	for (int i = 1; i < 4; i++)
	{
		out[i] ^= out[i - 1];
	}

	return cvt2u32(out);
}

uint32_t r2(uint32_t r)
{
	uint8_t out[4];

	uint8_t in[4];

	cvt2u8(r, in);

	std::memcpy(out, in, 4);
	for (int i = 0; i < 4; i++)
	{
		out[i] = s2[in[i]];
	}
	for (int i = 2; i >= 0; i--)
	{
		out[i] ^= out[i + 1];
	}
	return cvt2u32(out);
}

uint32_t rrot(uint32_t w, int sh)
{
	sh %= 32;
	return (w << (32 - sh)) | (w >> sh);
}

uint32_t lrot(uint32_t w, int sh)
{
	sh %= 32;
	return (w >> (32 - sh)) | (w << sh);
}

uint32_t r345(uint32_t word, uint32_t k, int rnum) {
	
	word ^= rrot(word, -463 + 439 * rnum + -144 * rnum * rnum + 20 * rnum * rnum * rnum - rnum * rnum * rnum * rnum) ^ lrot(word, 63 + -43 * rnum + 12 * rnum * rnum + -rnum * rnum * rnum);
	
	word = (4124669716 + word * k);
	word = word * word * word;
	
	word ^= word << 5;
	word ^= word << 5;

	word ^= rrot(word, -463 + 439 * rnum + -144 * rnum * rnum + 20 * rnum * rnum * rnum  - rnum * rnum * rnum * rnum) ^ lrot(word, 63 + -43 * rnum + 12 * rnum * rnum + -rnum * rnum * rnum);

	return rrot(word, -504 + 418 * rnum - 499 * rnum * rnum + -511 * rnum * rnum * rnum + 98 * rnum * rnum * rnum * rnum);
}

template<bool printy>
uint64_t encrypt(uint64_t in, uint32_t k0, uint32_t k1)
{
	uint32_t l = in >> 32;
	uint32_t r = (in) & 0xffffffff;
	if (printy)
		std::cout << "R0: " << l << " " << r << "\n";


	/*#round 1
	l ^= r1(r, m_sbox_1)
	l, r = swap(l,r)

	print("r1:",bin(l), bin(r))

	#round 2
	l ^= r2(r, m_sbox_2)
	l, r = swap(l,r)

	#print("r2:",bin(l), bin(r))
	#print("3", hex(l), hex(r))
	#round 3
	l ^= r34(r, k1)
	l, r = swap(l,r)

	#print("4", hex(l), hex(r))

	#print("r3:",bin(l), bin(r))

	#round 4
	l ^= r34(r, k2)
	r ^= l
	*/
	l ^= r2(r);
	std::swap(r, l);

	if (printy)
		std::cout << "R1: " << l << " " << r << "\n";

	l ^= r_1(r);
	std::swap(r, l);

	if (printy)
		std::cout << "R2: " << l << " " << r << "\n";

	l ^= r345(r, k0, 3);
	std::swap(r, l);
	if (printy)
		std::cout << "R3: " << l << " " << r << "\n";

	l ^= r345(r, k1, 4);
	std::swap(r, l);
	if (printy)
		std::cout << "R4: " << l << " " << r << "\n";

	l ^= r345(r, k1 ^ k0, 5);
	std::swap(r, l);
	if (printy)
		std::cout << "R5: " << l << " " << r << "\n";

	l ^= r345(r, k0, 6);
	std::swap(r, l);
	if (printy)
		std::cout << "R6: " << l << " " << r << "\n";

	l ^= r345(r, k1, 7);
	r ^= l;
	if (printy)
		std::cout << "R7: " << l << " " << r << "\n";

	return ((uint64_t)l << 32) | r;
}

void encryptp(uint64_t p0, uint64_t p1, uint32_t k0, uint32_t k1)
{
	uint32_t l0 = p0 >> 32;
	uint32_t r0 = (p0) & 0xffffffff;

	uint32_t l1 = p1 >> 32;
	uint32_t r1 = (p1) & 0xffffffff;

	uint32_t dl = 0;
	uint32_t dr = 0;

	dl = l0 ^ l1;
	dr = r0 ^ r1;

	std::cout << "R0 p0: " << l0 << " " << r0 << "\n";
	std::cout << "R0 p1: " << l1 << " " << r1 << "\n";
	std::cout << "R0 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";


	/*#round 1
	l ^= r1(r, m_sbox_1)
	l, r = swap(l,r)

	print("r1:",bin(l), bin(r))

	#round 2
	l ^= r2(r, m_sbox_2)
	l, r = swap(l,r)

	#print("r2:",bin(l), bin(r))
	#print("3", hex(l), hex(r))
	#round 3
	l ^= r34(r, k1)
	l, r = swap(l,r)

	#print("4", hex(l), hex(r))

	#print("r3:",bin(l), bin(r))

	#round 4
	l ^= r34(r, k2)
	r ^= l
	*/
	l0 ^= r2(r0);
	std::swap(r0, l0);

	l1 ^= r2(r1);
	std::swap(r1, l1);

	dl = l0 ^ l1;
	dr = r0 ^ r1;

	std::cout << "R1 p0: " << l0 << " " << r0 << "\n";
	std::cout << "R1 p1: " << l1 << " " << r1 << "\n";
	std::cout << "R1 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";

	l0 ^= r_1(r0);
	std::swap(r0, l0);

	l1 ^= r_1(r1);
	std::swap(r1, l1);

	dl = l0 ^ l1;
	dr = r0 ^ r1;

	std::cout << "R2 p0: " << l0 << " " << r0 << "\n";
	std::cout << "R2 p1: " << l1 << " " << r1 << "\n";
	std::cout << "R2 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";

	
	l0 ^= r345(r0, k0, 3);
	std::swap(r0, l0);

	l1 ^= r345(r1, k0, 3);
	std::swap(r1, l1);

	dl = l0 ^ l1;
	dr = r0 ^ r1;

	std::cout << "R3 p0: " << l0 << " " << r0 << "\n";
	std::cout << "R3 p1: " << l1 << " " << r1 << "\n";
	std::cout << "R3 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";


	l0 ^= r345(r0, k1, 4);

	l1 ^= r345(r1, k1, 4);

	r0 ^= l0;
	r1 ^= l1;

	dl = l0 ^ l1;
	dr = r0 ^ r1;

	std::cout << "R4 p0: " << l0 << " " << r0 << "\n";
	std::cout << "R4 p1: " << l1 << " " << r1 << "\n";
	std::cout << "R4 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";
}

template<bool printy>
std::vector<uint32_t> attack_last_round(uint64_t c0, uint64_t c1)
{
	std::vector<uint32_t> k1s;

	uint32_t l0 = c0 >> 32;
	uint32_t r0 = (c0) & 0xffffffff;

	uint32_t l1 = c1 >> 32;
	uint32_t r1 = (c1) & 0xffffffff;
	if (printy)
	{
		std::cout << "R7 LR0: " << l0 << " " << r0 << "\n";
		std::cout << "R7 LR1: " << l1 << " " << r1 << "\n";
	}
	r0 ^= l0;
	r1 ^= l1;

	uint32_t dl = l0 ^ l1;
	uint32_t dr = r0 ^ r1;
	if (printy) {

		std::cout << "R7 Del: " << std::bitset<32>(dl) << " " << std::bitset<32>(dr) << "\n";
	}

	for (uint32_t k1 = 0; k1 < 0xffffffff; k1++)
	{
		uint32_t round_delta = r345(r1, k1, 7) ^ r345(r0, k1, 7);
		uint32_t prop_in_diff = round_delta ^ dl;
		if (prop_in_diff == 0x80000000)
		{
			if (printy)
				std::cout << k1 << "\n";
			k1s.push_back(k1);
		}
	}

	return k1s;

}

int comp(const std::pair<uint32_t, int>* a, const std::pair<uint32_t, int>* b)
{
	return a->second < b->second;
}

int comp2(const void* a, const void* b)
{
	return comp((std::pair<uint32_t, int>*) a, (std::pair<uint32_t, int>*) b);
}

std::vector<uint32_t> k1_from_last_round(std::vector<uint64_t> c0, std::vector<uint64_t> c1)
{
	std::unordered_map<uint32_t, int> tried;
	for (int i = 0; i < c0.size(); i++)
	{
		std::vector<uint32_t> k1s = attack_last_round<false>(c0[i], c1[i]);
		std::cout << "Tried " << i + 1 << " pairs, found " << k1s.size() << " new potential keys...               \n"<<std::flush;
		for (auto& k1 : k1s)
		{
			if (tried.find(k1) != tried.end())
			{
				tried[k1] ++;
			}
			tried.insert({ k1, 0 });
		}
	}
	int max_score = 0;
	uint32_t best = 0xdeadbeef;
	
	std::vector<std::pair<uint32_t, int>> k0s;

	for (std::unordered_map<uint32_t, int>::iterator itr = tried.begin(); itr != tried.end(); itr++)
	{
		if (itr->second != 0)
			k0s.push_back({ itr->first, itr->second });
	}

	std::qsort(&k0s[0], k0s.size(), sizeof(std::pair<uint32_t, int>), comp2);

	for (auto& a : k0s)
	{
		std::cout << a.first << " " << a.second << "\n";
	}

	std::vector<uint32_t> out;
	for (int i = 0; i < k0s.size(); i++)
	{
		out.push_back(k0s[i].first);
	}

	return out;
}

int main()
{
	std::cout << "Hello world!!\n";

	//std::cout << options.size() << "\n";
	//
	//
	//for (int i = 0; i < p0s.size(); i++)
	//{
	//	if (c0s[i] != encrypt<false>(p0s[i], k0, k1))
	//	{
	//		std::cout << "issue!\n";
	//	}
	//}

	
	//std::vector<uint32_t> k1_guesses = { 577202280, 2724685928, 1650944104, 3798427752 };
	auto k1_guesses = k1_from_last_round(c0s, c1s);
	for (auto k1_guess : k1_guesses)
	{
		uint8_t k1_guess_u8[4];
		cvt2u8(k1_guess, k1_guess_u8);
		make_sbox<false>(k1_guess_u8);
		//sbox2 now correct, we bruteforce sbox1 and k0 now

		for (uint32_t k0_guess = 0x0; k0_guess < (1<<24); k0_guess++)
		{

			if (k0_guess % 1000000 == 0)
			{
				std::cout << k0_guess << "\n";
			}

			uint8_t k0_guess_u8[4];
			cvt2u8(k0_guess, k0_guess_u8);
			make_sbox<true>(k0_guess_u8);
			if (encrypt<false>(p0s[0], k0_guess, k1_guess) == c0s[0])
			{
				bool solved = true;
				for (int j = 0; j < 5; j++)
				{
					if (encrypt<false>(p0s[j], k0_guess, k1_guess) != c0s[j])
						solved = false;
				}
				if (solved)
				{
					uint64_t ans = (((uint64_t)k0_guess) << 32) | (uint64_t)k1_guess;
					std::cout << "========================================\n"<< ans << "========================================\n";
				}
			}
		}
	}

	return 0;
}