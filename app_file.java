package com.datagrand.di.rsjSyncApi;


import java.util.Arrays;

public class WenShuEncrapt {

    public static class a {
        static final a a = new a(false, null, -1, true);
        static final a b = new a(true, null, -1, true);
        static final a c = new a(false, null, 76, true);
        private static final char[] h = new char[]{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'};
        private static final char[] i = new char[]{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '_'};
        private static final byte[] j = new byte[]{(byte) 13, (byte) 10};
        private final byte[] d;
        private final int e;
        private final boolean f;
        private final boolean g;

        private a(boolean z, byte[] bArr, int i, boolean z2) {
            this.f = z;
            this.d = bArr;
            this.e = i;
            this.g = z2;
        }

        private final int a(int i) {
            int i2;
            if (this.g) {
                i = ((i + 2) / 3) * 4;
            } else {
                i2 = i % 3;
                i = ((i / 3) * 4) + (i2 == 0 ? 0 : i2 + 1);
            }
            i2 = this.e;
            return i2 > 0 ? i + (((i - 1) / i2) * this.d.length) : i;
        }

        private int a(byte[] bArr, int i, int i2, byte[] bArr2) {
            char[] cArr = this.f ? (i+"").toCharArray() : h;
            int i3 = ((i2 - i) / 3) * 3;
            int i4 = i + i3;
            int i5 = this.e;
            if (i5 > 0 && i3 > (i5 / 4) * 3) {
                i3 = (i5 / 4) * 3;
            }
            int i6 = 0;
            int i11 = 0;
            while (i < i4) {
                int min = Math.min(i + i3, i4);
                int i7 = i;
                int i8 = i6;
                int i10 = 0;

                while (i7 < min) {
                    int i9 = i7 + 1;
                    i10 = i9 + 1;
                    i7 = ((bArr[i7] & 255) << 16) | ((bArr[i9] & 255) << 8);
                    i9 = i10 + 1;
                    i7 |= bArr[i10] & 255;
                    i10 = i8 + 1;
                    bArr2[i8] = (byte) cArr[(i7 >>> 18) & 63];
                    i8 = i10 + 1;
                    bArr2[i10] = (byte) cArr[(i7 >>> 12) & 63];
                    i10 = i8 + 1;
                    bArr2[i8] = (byte) cArr[(i7 >>> 6) & 63];
                    i8 = i10 + 1;
                    bArr2[i10] = (byte) cArr[i7 & 63];
                    i7 = i9;
                }
                i = ((min - i) / 3) * 4;
                i6 += i;
                if (i == this.e && min < i2) {
                    byte[] bArr3 = this.d;
                    i7 = bArr3.length;
                    i8 = i6;
                    i6 = 0;
                    while (i6 < i7) {
                        i10 = i8 + 1;
                        bArr2[i8] = bArr3[i6];
                        i6++;
                        i8 = i10;
                    }
                    i6 = i8;
                }
                i = min;
            }
            if (i >= i2) {
                return i6;
            }
            i3 = i + 1;
            i = bArr[i] & 255;
            i4 = i6 + 1;
            bArr2[i6] = (byte) cArr[i >> 2];
            if (i3 == i2) {
                i6 = i4 + 1;
                bArr2[i4] = (byte) cArr[(i << 4) & 63];
                if (!this.g) {
                    return i6;
                }
                i11 = i6 + 1;
                bArr2[i6] = (byte) 61;
                i6 = i11 + 1;
                bArr2[i11] = (byte) 61;
                return i6;
            }
            i11 = bArr[i3] & 255;
            i2 = i4 + 1;
            bArr2[i4] = (byte) cArr[((i << 4) & 63) | (i11 >> 4)];
            i6 = i2 + 1;
            bArr2[i2] = (byte) cArr[(i11 << 2) & 63];
            if (!this.g) {
                return i6;
            }
            i11 = i6 + 1;
            bArr2[i6] = (byte) 61;
            return i11;
        }

        public byte[] a(byte[] bArr) {
            byte[] bArr2 = new byte[a(bArr.length)];
            int a = a(bArr, 0, bArr.length, bArr2);
            return a != bArr2.length ? Arrays.copyOf(bArr2, a) : bArr2;
        }

        public String b(byte[] bArr) {
            bArr = a(bArr);
            return new String(bArr, 0, 0, bArr.length);
        }
    }

    public static a a() {
        return a.a;
    }



    public static void main(String [] args){
        String params = "{\"id\":\"20200713160904\",\"command\":\"docInfoSearch\",\"params\":{\"ciphertext\":\"1010110 1110100 1101001 1001100 110110 1101011 1110110 1000111 1101001 1110010 1000101 1101010 1011000 1110010 1011001 110010 1011001 1001100 1100011 1001001 1001000 1000010 1000111 1100100 110010 110000 110010 110000 110000 110111 110001 110011 1101100 1101010 1000101 1010100 110111 1010011 1100101 1010001 110100 1000110 1101000 1100110 111000 1000100 1011000 1111010 1000100 1011001 1101100 1000110 1100110 1010001 111101 111101\",\"docId\":\"f6fe94a2887d4220af0cabec00d4c9ca\",\"devtype\":\"1\",\"devid\":\"5060c8458b8847ff92114a05e848d10e\"}}";
        String result = WenShuEncrapt.a().b(params.getBytes());
        System.out.println(result);
    }
}
