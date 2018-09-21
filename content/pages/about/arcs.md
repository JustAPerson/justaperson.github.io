Title: ARCS
Slug: about/arcs

This is the earliest code I wrote that I can still find. Judging by one of the
timestamps, I was around 13 at the time. I also happened to have an interest in
cryptography then. My dad had given me a copy of Bruce Schneier's _Applied
Cryptography_. I tried reading the AES and SHA2 specs. SHA2 I came close to
implementing correctly, but I couldn't wrap my head around the math of AES's
sbox.

It took another two years before I managed a [correct SHA256
implementation][luacrypt] (minus [one _tiny_ edge case][fix]).

Below you will find something vaguely inspired by SHA256 and AES256. Marvel in
the horrible security implications of a fixed-format-non-random initial vector
paired with CBC mode. Also find amusement in implementing bitwise operators as
functions over strings since Lua 5.1 does not have native bit operators.

[luacrypt]: https://github.com/JustAPerson/LuaCrypt/blob/master/sha2.lua
[fix]: https://github.com/JustAPerson/LuaCrypt/commit/a1a80d21c600aaa8164a31fd8c85f8b32453f7e7

```lua
--[[

the Advanced Roblox CryptoSystem, or ARCS, is being designed to bring better security to roblox games, such as private servers.
While still in its infancy, hopefully one day, ARCS will become a suitable means of data encryption.

ARCS currently supplies 2 features.

A secure Hash function,
And secure encryption algorithm.


The secure Hash algorithm (A SHA256 variant), can be called with the Hash() function.
It has 1 input, which is the text to be hashed.

print(ARCS.Hash("Some Random Data"))
-->28551017D06B84BD97742D373E60D4CF6D1D863E3817A7CB7058B824204194A6


ARCS also includes the ARCS Cipher, is a (hopefully) secure encryption algorithm.
The cipher has 3 inputs, the text to be encrypted, the key to use, and the number of rounds (optional)
You can use ARCS.CipherEN to encrypt, and ARCS.CipherDE to decrypt

print(ARCS.CipherEN("HOLY SHNAPPLE","WHAT 9000!?!?!?"))
-->36FF255D11705BDF5939208F7C25BE54B20992B45265ACE387551AE4798D5D5F

print(ARCS.CipherDE("36FF255D11705BDF5E12208C7C25BE5493BE8F2C200F55FC26CD2C3EE4D49D6E","WHAT 9000!?!?!?"))
-->HOLY SHNAPPLE	08/16/10 13:53:42 0016

(The number of rounds is -not- required when decrypting, even if the string has been encrypted with more than 16)

the decryption function will return two strings, the decrypted text, and the decrypted header.
The header is a 16 character string of text included at the begining of the cipher text.
The header includes the time and date of when the encryption was started for that string, and 
the number of rounds it was encrypted with.

Currently, the ARCS cipher is a variable strength cipher, in the sense, that you can use more rounds in the encryption.
The main portion of the encryption consits of a function that systematically encrypts the text.
When you encrypt something, its encrypted in stages, each stage is a round. Each round is just the main portion of the cipher,
but it is repeated over and over again to offer more security. There is a mininum of 16 rounds, and a maximum of 9999.

It should also be noted that the header string is always encrypted with 16 rounds, which is strong enough to protect the inocous data
held within it.

The ARCS Cipher currently is not exactly how I would like it to be, so there will most likely be several updates in the comming days,
to improve security, and efficiency.

Please check back every once in a while to ensure that you are using the most up-to-date version of ARCS.

]])--

ARCS = {}
ARCS.Name = "ARCS - Advanced Roblox CryptoSystem"

function XOR(in1, in2)
    final = ""
    for i=1,#in1 do
        x1 = in1:sub(i,i)
        x2 = in2:sub(i,i)
        if x1 == x2 then
            final = final .. "0"
        else
            final = final .. "1"
        end
    end
    return final
end

function AND(in1, in2)
    final = ""
    for u=1,#in1/8 do
        x1 = in1:sub(u*8-7,u*8)
        x2 = in2:sub(u*8-7,u*8)
        local out = ""
        for i=1,8 do
            i1 = x1:sub(i,i)
            i2 = x1:sub(i,i)
            if i1 == i2 then
                out = out .. "1"
            elseif i1 ~= i2 then
                out = out .. "0"
            end
        end
        final = final .. out
    end
    return final
end

function NOT(in1)
    final = ""
    for u=1,#in1/8 do
        x1 = in1:sub(u*8-7,u*8)
        local out = ""
        for i=1,8 do
            i1 = x1:sub(i,i)
            i2 = x1:sub(i,i)
            if i1 == "1" then
                out = out .. "0"
            else
                out = out .. "1"
            end
        end
        final = final .. out
    end
    return final
end

function OR(in1,in2)
    local out = ""
    for i=1,8 do
        i1 = in1:sub(i,i)
        i2 = in2:sub(i,i)
        if i1 == "1" or i2 == "1" then
            out = out  .. "1"
        else
            out = out .. "0"
        end
    end
    return out
end

function LeftShift(x,n)
    y=#x
    x = x:sub(n+1,32)
    x = x .. string.rep("0",32-#x)
    return x
end

function RightShift(x,n)
    y=#x
    x = x:sub(1,n)
    x = string.rep("0",32-n) .. x
    return x
end

function RightRotate(x,n)
    return x:sub(n+1,#x) .. x:sub(1,n)
end


function moduloAdd(txt1,txt2,x)
    if not x then x = 32 end
    txt1 = bToDec(txt1)
    txt2 = bToDec(txt2)
    txt = (txt1 + txt2) % 2^x
    final = nToBin(txt,x)
    return final
end

function columTran(txt)
    local tmp = {}
    for i=1,16 do
        tmp[i] = txt:sub(i*8-7,i*8)
    end
    local final = ""
    local x,y  = -3,1
    repeat
        x = (x + 4)
        if x > 16 then
            y = y + 1
            x = y
        end
        final = final .. tmp[x]
    until x == 16
    return final
end

function shiftRow(txt,way)
    if not way then
        local tmp = {}
        for i=1,4 do
            tmp[i] = txt:sub(i*32-31,i*32)
        end
        tmp[2] = RightRotate(tmp[2],8)
        tmp[3] = RightRotate(tmp[3],16)
        tmp[4] = RightRotate(tmp[4],24)
        return table.concat(tmp)
    elseif way then
        local tmp = {}
        for i=1,4 do
            tmp[i] = txt:sub(i*32-31,i*32)
        end
        tmp[2] = RightRotate(tmp[2],24)
        tmp[3] = RightRotate(tmp[3],16)
        tmp[4] = RightRotate(tmp[4],8)
        return table.concat(tmp)
    end
end

function cToHex(text)
    final = ''
    for i=1,#text do
        work = string.format("%X",text:sub(i,i):byte())
        if #work == 1 then
            work = "0"..work
        end
        final = final .. work
    end
    return final
end

function hToBin(char)
    local final = ""
    for i=1,#char/2 do
        local fix = 0
        fix = tonumber(char:sub(i*2-1,i*2),16)
        final = final .. nToBin(fix)
    end
    return final
end

function nToBin(Decimal,x)
    if x == nil then x = 8 end
    local BinaryRep = ""
    local Number = Decimal
    while Number > 0 do
        BinaryRep = BinaryRep .. Number % 2
        Number = math.floor(Number / 2)
    end
    return Decimal == 1 and ("0"):rep(x-1) .. "1" or ("0"):rep(x - BinaryRep:len()) .. BinaryRep:reverse()
end

function nToHex(num)
    return string.format("%X",num)
end

function bToHex(txt)
    rfinal = ""
    for u=1,#txt/8 do
        bin = tostring(txt:sub(u*8-7,u*8))
        local final = ""
        for i=1,8,4 do
            local fix = bin:sub(i,i+3)
            local subtotal = 0
            local o = 0
            for u=4,1,-1 do
                local fx = fix:sub(u,u)
                if fx == "1" then
                    subtotal = subtotal + 2^(o)
                end
                o = o +1
            end
            if subtotal > 9 then
                subtotal = string.char(subtotal+55)
            end
            final = final .. subtotal
        end
        rfinal = rfinal .. final
    end
    return rfinal
end

function hToDec(text)
    return tonumber(text,16)
end

function bToDec(text)
    return tonumber(text,2)
end

function hToChar(text)
    final = ""
    for i=1,#text/2 do
        work = text:sub(i*2-1,i*2)
        work = hToDec(work)
        work = string.char(work)
        final = final .. work
    end
    return final
end

function bToChar(text)
    final = ""
    for i=1,#text/8 do
        work = text:sub(i*8-7,i*8)
        final = final .. string.char(tonumber(work,2))
    end
    return final
end

function cToBin(text)
    final = ""
    for i=1,#text do
        final = final .. nToBin(text:sub(i,i):byte())
    end
    return final
end

function sMod(num,base)
    if num == base then
        return 1
    else
        return num % base
    end
end


function XinY(num,base)
    local x = 0
    while num >= base do
        num = num - base
        x=x+1
    end
    return x
end

function nextInt(num,base)
    y = XinY(num,base) + 1
    return base*y - num
end


Blocks={}
HVal = {}
Blocks[0] = {}
Constants = {}
Constants[0] = "01000010100010100010111110011000"
Constants[1] = "01110001001101110100010010010001"
Constants[2] = "10110101110000001111101111001111"
Constants[3] = "11101001101101011101101110100101"
Constants[4] = "00111001010101101100001001011011"
Constants[5] = "01011001111100010001000111110001"
Constants[6] = "10010010001111111000001010100100"
Constants[7] = "10101011000111000101111011010101"
Constants[8] = "11011000000001111010101010011000"
Constants[9] = "00010010100000110101101100000001"
Constants[10] = "00100100001100011000010110111110"
Constants[11] = "01010101000011000111110111000011"
Constants[12] = "01110010101111100101110101110100"
Constants[13] = "10000000110111101011000111111110"
Constants[14] = "10011011110111000000011010100111"
Constants[15] = "11000001100110111111000101110100"
Constants[16] = "11100100100110110110100111000001"
Constants[17] = "11101111101111100100011110000110"
Constants[18] = "00001111110000011001110111000110"
Constants[19] = "00100100000011001010000111001100"
Constants[20] = "00101101111010010010110001101111"
Constants[21] = "01001010011101001000010010101010"
Constants[22] = "01011100101100001010100111011100"
Constants[23] = "01110110111110011000100011011010"
Constants[24] = "10011000001111100101000101010010"
Constants[25] = "10101000001100011100011001101101"
Constants[26] = "10110000000000110010011111001000"
Constants[27] = "10111111010110010111111111000111"
Constants[28] = "11000110111000000000101111110011"
Constants[29] = "11010101101001111001000101000111"
Constants[30] = "00000110110010100110001101010001"
Constants[31] = "00010100001010010010100101100111"
Constants[32] = "00100111101101110000101010000101"
Constants[33] = "00101110000110110010000100111000"
Constants[34] = "01001101001011000110110111111100"
Constants[35] = "01010011001110000000110100010011"
Constants[36] = "01100101000010100111001101010100"
Constants[37] = "01110110011010100000101010111011"
Constants[38] = "10000001110000101100100100101110"
Constants[39] = "10010010011100100010110010000101"
Constants[40] = "10100010101111111110100010100001"
Constants[41] = "10101000000110100110011001001011"
Constants[42] = "11000010010010111000101101110000"
Constants[43] = "11000111011011000101000110100011"
Constants[44] = "11010001100100101110100000011001"
Constants[45] = "11010110100110010000011000100100"
Constants[46] = "11110100000011100011010110000101"
Constants[47] = "00010000011010101010000001110000"
Constants[48] = "00011001101001001100000100010110"
Constants[49] = "00011110001101110110110000001000"
Constants[50] = "00100111010010000111011101001100"
Constants[51] = "00110100101100001011110010110101"
Constants[52] = "00111001000111000000110010110011"
Constants[53] = "01001110110110001010101001001010"
Constants[54] = "01011011100111001100101001001111"
Constants[55] = "01101000001011100110111111110011"
Constants[56] = "01110100100011111000001011101110"
Constants[57] = "01111000101001010110001101101111"
Constants[58] = "10000100110010000111100000010100"
Constants[59] = "10001100110001110000001000001000"
Constants[60] = "10010000101111101111111111111010"
Constants[61] = "10100100010100000110110011101011"
Constants[62] = "10111110111110011010001111110111"
Constants[63] = "11000110011100010111100011110010"

function miniReset()
    for i=0,7 do
        HVal[i] = Blocks[0][i]
    end
end

function largeReset()
    Blocks[0][0] = "01101010000010011110011001100111"
    Blocks[0][1] = "10111011011001111010111010000101"
    Blocks[0][2] = "00111100011011101111001101110010"
    Blocks[0][3] = "10100101010011111111010100111010"
    Blocks[0][4] = "01010001000011100101001001111111"
    Blocks[0][5] = "10011011000001010110100010001100"
    Blocks[0][6] = "00011111100000111101100110101011"
    Blocks[0][7] = "01011011111000001100110100011001"
end

largeReset()
for i=0,63 do Constants[i] = hToBin(Constants[i]) end

function ARCS.Hash(text)
    text = tostring(text)
    --String preprocessing
    local tmp = cToBin(text)
    tml = #tmp
    local nextI = nextInt(tml+65,512)
    tmp = tmp .. "1" .. string.rep("0",nextI)
    local append = nToBin(#text)
    append = string.rep("0",64-#append) .. append
    text = tmp .. append
    local nB = XinY(#text,512)
    largeReset()
    for i=1,nB do
        Blocks[i] = {}
        Blocks[i].String=text:sub(i*512-511,i*512)
    end
    --Block preprocessing
    for i=1,nB do
        work = Blocks[i].String
        for u=0,15 do
            Blocks[i][u] = Blocks[i].String:sub((u+1)*32-31,(u+1)*32)
        end
        for u=16,63 do
            s0 = XOR(RightRotate(Blocks[i][u-15],7),RightRotate(Blocks[i][u-15],18))
            s0 = XOR(s0,RightRotate(Blocks[i][u-15],3))
            s1 =  XOR(RightRotate(Blocks[i][u-2],17),RightRotate(Blocks[i][u-2],19))
            s1 = XOR(s1,RightRotate(Blocks[i][u-2],10))
            step1 = moduloAdd(Blocks[i][u-16],s0)
            step1 = moduloAdd(step1,Blocks[i][u-7])
            Blocks[i][u] = moduloAdd(step1,s1)
        end
    end
    --Getting to the actual hash now
    for i=1,nB do
        miniReset()
        for o=0,63 do
            local s0 = XOR(RightRotate(HVal[0],2),RightRotate(HVal[0],13))
            s0 = XOR(s0,RightRotate(HVal[0],22))
            local maj = XOR(AND(HVal[0],HVal[1]),AND(HVal[0],HVal[2]))
            maj = XOR(maj,AND(HVal[1],HVal[2]))
            local t2 = moduloAdd(s0,maj)
            local s1 = XOR(RightRotate(HVal[4],6),RightRotate(HVal[4],11))
            s1 = XOR(s1,RightRotate(HVal[4],25))
            local ch = XOR(AND(HVal[4],HVal[5]),AND(NOT(HVal[4]),HVal[6]))
            local t1 = moduloAdd(HVal[7],s1)
            t1 = moduloAdd(t1,ch)
            t1 = moduloAdd(t1,Constants[o])
            t1 = moduloAdd(t1,Blocks[i][o])
            HVal[7] = HVal[6]
            HVal[6] = HVal[5]
            HVal[5] = HVal[4]
            HVal[4] = moduloAdd(HVal[3],t1)
            HVal[3] = HVal[2]
            HVal[2] = HVal[1]
            HVal[1] = HVal[0]
            HVal[0] = moduloAdd(t1,t2)
        end
        for o=0,7 do
            Blocks[i][o] = moduloAdd(Blocks[i-1][o],HVal[o])
        end
    end
    FINAL = ""
    for i=0,7 do
        FINAL = FINAL .. bToHex(Blocks[nB][i])
    end
    return FINAL
end

HEX = {"0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"}
SHIFT = {23, 27, 33, 41, 51, 63, 77, 93, 111, 131, 153, 177, 203, 231, 261, 293, 327, 363, 401, 441, 483, 527, 573, 621, 671, 723, 777, 833, 891, 951, 1013, 1077, 1143, 1211, 1281, 1353, 1427, 1503, 1581, 1661, 1743, 1827, 1913, 2001, 2091, 2183, 2277, 2373, 2471, 2571, 2673, 2777, 2883, 2991, 3101, 3213, 3327, 3443, 3561, 3681, 3803, 3927, 4053, 4181, 4311, 4443, 4577, 4713, 4851, 4991, 5133, 5277, 5423, 5571, 5721, 5873, 6027, 6183, 6341, 6501, 6663, 6827, 6993, 7161, 7331, 7503, 7677, 7853, 8031, 8211, 8393, 8577, 8763, 8951, 9141, 9333, 9527, 9723, 9921, 10121, 10323, 10527, 10733, 10941, 11151, 11363, 11577, 11793, 12011, 12231, 12453, 12677, 12903, 13131, 13361, 13593, 13827, 14063, 14301, 14541, 14783, 15027, 15273, 15521, 15771, 16023, 16277, 16533, 16791, 17051, 17313, 17577, 17843, 18111, 18381, 18653, 18927, 19203, 19481, 19761, 20043, 20327, 20613, 20901, 21191, 21483, 21777, 22073, 22371, 22671, 22973, 23277, 23583, 23891, 24201, 24513, 24827, 25143, 25461, 25781, 26103, 26427, 26753, 27081, 27411, 27743, 28077, 28413, 28751, 29091, 29433, 29777, 30123, 30471, 30821, 31173, 31527, 31883, 32241, 32601, 32963, 33327, 33693, 34061, 34431, 34803, 35177, 35553, 35931, 36311, 36693, 37077, 37463, 37851, 38241, 38633, 39027, 39423, 39821, 40221, 40623, 41027, 41433, 41841, 42251, 42663, 43077, 43493, 43911, 44331, 44753, 45177, 45603, 46031, 46461, 46893, 47327, 47763, 48201, 48641, 49083, 49527, 49973, 50421, 50871, 51323, 51777, 52233, 52691, 53151, 53613, 54077, 54543, 55011, 55481, 55953, 56427, 56903, 57381, 57861, 58343, 58827, 59313, 59801, 60291, 60783, 61277, 61773, 62271, 62771, 63273, 63777, 64283, 64791, 65301, 65813}
function genSBox(seed)
    local Key = seed
    local SBox = {}
    for i=2,16 do
        work = seed:sub(i*16-15,i*16)
        fin = XOR(work:sub(1,8),work:sub(9,16))
    end
    local nx,ny = bToDec(fin:sub(5,8)),bToDec(fin:sub(1,4))
    of = SHIFT[bToDec(fin)%256+1]
    local tmp = {}
    local IBox=  {}
    for y=0,15 do
        tmp[y] = {}
        SBox[y] = {}
        for x=0,15 do
            SBox[y][x] =  nToBin((y*of+ny)%16,4)..nToBin((x*of+nx)%16,4)
            tmp[y][x] =  nToBin((y*of+ny)%16,4)..nToBin((x*of+nx)%16,4)
        end
    end
    for i=0,15 do
        for x=0,15 do
            tmp[x][i] = SBox[(x*(of*2+1)+1+i)%16][i]
        end
    end
    local SBox = {}
    local IBox = {}
    for i=0,15 do
        SBox[HEX[17+i]] = {}
        for x=0,15 do
            p1,p2,p3 = HEX[17+i],HEX[17+x],tmp[i][(x*of+1+i)%16]
            SBox[p1][p2] = p3
            if IBox[p3:sub(1,4)] == nil then
                IBox[p3:sub(1,4)] = {}
            end
            IBox[p3:sub(1,4)][p3:sub(5,8)] = p1 .. p2
        end
    end
    tmp = nil
    return SBox,IBox
end

function SubByte(txt,tab)
    final = ""
    for i=1,#txt/8 do
        p1,p2 = txt:sub(i*8-7,i*8-4),txt:sub(i*8-3,i*8)
        final = final .. tab[p1][p2]
    end
    return final
end


function ARCS.CipherEN(txt,key,rounds)
    Key = hToBin(ARCS.Hash(key)) 	-- Creates a stronger key
    if not rounds or rounds < 16 then	--makes sure you use proper round values
        rounds = 16
    end
    if rounds > 9999 then
        rounds = rounds % 9999 + 1
    end
    IV = os.date() 	-- Sets up the initial CBC (cipher block chaining) vector
    IV = string.gsub(string.gsub(IV:sub(1,8) .. IV:sub(10,17),"/",""),":","")
    IV = IV .. string.rep("0",16-(#IV+#tostring(rounds))) .. rounds
    ttxt = txt .. string.char(3) ..string.rep(string.char(1),nextInt(#txt+1,16))
    PTxt = cToBin(IV .. ttxt)	 -- translates everything into binary for INCREASED speed
    PTxt = XOR(PTxt:sub(1,128),Key:sub(1,128)) .. PTxt:sub(129,#PTxt)
    nB = XinY(#PTxt,128)
    local Blocks = {}
    Blocks[1] = PTxt:sub(1,128)
    for u=2,nB do 	 -- breaks message into 128 bit (16 character) blocks
        Blocks[u] = XOR(PTxt:sub(u*128-127,u*128),Blocks[u-1])
    end
    TEXT = hToBin(ARCS.Hash(bToChar(Key)))
    SBox = genSBox(Key)  	-- generating the key dependant S-Box
    KBox = genSBox(TEXT)	-- generating the secondary key dependant S-Box (used for key expansion)
    KEYS = {}
    KEYS[0] = Key
    for i=1,rounds+1 do
        tmp = XOR(KEYS[i-1],XOR(SubByte(KEYS[i-1],SBox),SubByte(KEYS[i-1],KBox))) 	-- Turns 1, 256bit key into the required number of 256 bit keys
        KEYS[i] = RightRotate(tmp,(i%64)+1)
    end
    TMP = Blocks[1]
    for u=1,2 do
    TMP = XOR(TMP,KEYS[0]:sub(u*128-127,u*128))
    end
    for u=1,2 do  			-- encrypts the header with 16 rounds, always, ALWAYS
        for i=1,16 do
            TMP = SubByte(TMP,SBox)
            TMP = shiftRow(TMP)
            TMP = XOR(TMP,KEYS[i]:sub(u*128-127,u*128))
        end
    end
    TMP = SubByte(TMP,SBox)
    TMP = shiftRow(TMP)
    for u=1,2 do
    TMP = XOR(TMP,KEYS[17]:sub(u*128-127,u*128))
    end
    Blocks[1] = TMP
    for Z=2,nB do
        TMP = Blocks[Z]
        for u=1,2 do
            TMP = XOR(TMP,KEYS[0]:sub(u*128-127,u*128))
        end
        for u=1,2 do
            for i=1,rounds do
                TMP = SubByte(TMP,SBox)
                TMP = shiftRow(TMP)
                TMP = XOR(TMP,KEYS[i]:sub(u*128-127,u*128))
                TMP = RightRotate(TMP,i%64+1)
            end
        end
        TMP = SubByte(TMP,SBox)
        TMP = shiftRow(TMP)
        for u=1,2 do
            TMP = XOR(TMP,KEYS[rounds+1]:sub(u*128-127,u*128))
        end
        TMP = RightRotate(TMP,(rounds+1)%64+1)
        Blocks[Z] = TMP
    end
    FINAL = ""
    for i=1,nB do
        FINAL = FINAL .. bToHex(Blocks[i])
    end
    return FINAL
end

function ARCS.CipherDE(txt,key,rounds)
    if not rounds or rounds < 16 then
        rounds = 16
    end
    if rounds > 9999 then
        rounds = rounds % 9999 + 1
    end
    Key = hToBin(ARCS.Hash(key))
    PTxt = hToBin(txt)
    nB = XinY(#PTxt,128)
    local Blocks = {}
    for u=1,nB do 	 -- breaks message into 128 bit (16 character) blocks
        Blocks[u] = PTxt:sub(u*128-127,u*128)
    end
    TEXT = hToBin(ARCS.Hash(bToChar(Key)))
    SBox,IBox = genSBox(Key)  	-- generating the key dependant S-Box
    KBox = genSBox(TEXT) 	-- generating the secondary key dependant S-Box (used for key expansion)
    KEYS = {}
    KEYS[0] = Key
    for i=1,rounds+1 do
        tmp = XOR(KEYS[i-1],XOR(SubByte(KEYS[i-1],SBox),SubByte(KEYS[i-1],KBox))) 	-- Turns 1, 256bit key into 98 256 bit keys
        KEYS[i] = RightRotate(tmp,(i%64)+1)
    end
    TMP = Blocks[1]
    for u=2,1,-1 do
    TMP = XOR(TMP,KEYS[17]:sub(u*128-127,u*128))
    end
    TMP = shiftRow(TMP,true)
    TMP = SubByte(TMP,IBox)
    for u=2,1,-1 do  			-- encrypts the header with 16 rounds, always, ALWAYS
        for i=16,1,-1 do
            TMP = XOR(TMP,KEYS[i]:sub(u*128-127,u*128))
            TMP = shiftRow(TMP,true)
            TMP = SubByte(TMP,IBox)
        end
    end
    for u=1,2 do
    TMP = XOR(TMP,KEYS[0]:sub(u*128-127,u*128))
    end
    FINAL = {}
    for i=1,nB do
        FINAL[i] = {}
    end
    FINAL[1] = TMP
    HEADER = bToChar(XOR(TMP,Key:sub(1,128)))
    nRnds = tonumber(HEADER:sub(#HEADER-3,#HEADER))
    if nRnds then
        if nRnds > rounds then
            for i=rounds,nRnds+1 do
                tmp = XOR(KEYS[i-1],XOR(SubByte(KEYS[i-1],SBox),SubByte(KEYS[i-1],KBox))) 	-- Turns 1, 256bit key into 98 256 bit keys
                KEYS[i] = RightRotate(tmp,(i%64)+1)
            end
        end
        rounds = nRnds
        for Z=2,nB do
            TMP = Blocks[Z]
            TMP = RightRotate(TMP,128-((rounds+1)%64+1))
            for u=2,1,-1 do
                TMP = XOR(TMP,KEYS[rounds+1]:sub(u*128-127,u*128))
            end
            TMP = shiftRow(TMP,true)
            TMP = SubByte(TMP,IBox)
            for u=2,1,-1 do
                for i=rounds,1,-1 do
                    TMP = RightRotate(TMP,128-(i%64+1))
                    TMP = XOR(TMP,KEYS[i]:sub(u*128-127,u*128))
                    TMP = shiftRow(TMP,true)
                    TMP = SubByte(TMP,IBox)
                end
            end
            for u=2,1,-1 do
                TMP = XOR(TMP,KEYS[0]:sub(u*128-127,u*128))
            end
            FINAL[Z] = TMP
        end
        FINALans = ""
        for u=2,nB do 	 -- breaks message into 128 bit (16 character) blocks
            work = bToChar(XOR(FINAL[u],FINAL[u-1]))
            found = work:find(string.char(3))
            if found then
                work = work:sub(1,found-1)
            end
            FINALans = FINALans .. work
        end
        HEADER = HEADER:sub(1,2) .. "/" .. HEADER:sub(3,4) .. "/" .. HEADER:sub(5,6) .. " ".. HEADER:sub(7,8) .. ":" .. HEADER:sub(9,10) .. ":" .. HEADER:sub(11,12) .. " " .. HEADER:sub(13,16)
        return FINALans,HEADER
    else
        return "Invalid Key or corrupted file"
    end
end
```
