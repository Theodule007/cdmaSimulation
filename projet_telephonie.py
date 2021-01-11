#! /usr/bin/env python3

import random

#On entre le message a envoyer
message1 = 'text pour un test'
message2 = 'un autre texte pour un autre test'
B = 0.2

#On defini la matrice de Walsh ligne par ligne pour une capacite maximale de 8 utilisateurs
walsh1 = [1,1,1,1,1,1,1,1]
walsh2 = [1,-1,1,-1,1,-1,1,-1]
walsh3 = [1,1,-1,-1,1,1,-1,-1]
walsh4 = [1,-1,-1,1,1,-1,-1,1]
walsh5 = [1,1,1,1,-1,-1,-1,-1]
walsh6 = [1,-1,1,-1,-1,1,-1,1]
walsh7 = [1,1,-1,-1,-1,-1,1,1]
walsh8 = [1,-1,-1,1,-1,1,1,-1]


#On definit une fonction pour convertir le message texte en un train binaire
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

#On definit une fonction pour convertir le train binaire en message texte
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

#On definit une fonction pour generer un signal aleatoire (bruit)
#Pour le multiplexage, on fait en sorte que le bruit soit de la meme longueur que le message
def bruit_gen(length):
    bruit = []
    for i in range(length):
        bruit.append(B*random.randint(-1,1))
    return bruit

def bruit_nul(length):
    nobruit = []
    for i in range(length):
        nobruit.append(0)
    return nobruit

#On definit une fonction pour standardiser le train binaire pour avoir 1 et -1 au lieu de 1 et 0
def standard(train_bin):
    bin_list = []
    for bit in train_bin:
        if (bit=='1'):
            bin_list.append(1)
        elif(bit=='0'):
            bin_list.append(-1)
    return bin_list

#On definit une fonction qui fait en sorte que les vecteurs messages soient de meme longueur pour le multiplexage
#On aura 0 comme absence de bit dans le message le plus court
def equ_message(message1, message2):
    mes1 = []
    mes1.extend(message1)
    mes2 = []
    mes2.extend(message2)
    if (len(message1)>len(message2)):
        nbr = len(message1)-len(message2)
        for i in range(nbr):
            mes2.append(0)
    elif(len(message2)>len(message1)):
        nbr = len(message2)-len(message1)
        for i in range(nbr):
            mes1.append(0)
    return mes1, mes2


#On definit une fonction pour adapter le xor au standard 1 et -1
def xor(a,b):
    if(a==0 or b==0):
        return 0
    elif(a==b):
        return -1
    else:
        return 1

#On definit une fonction qui etale chaque bit du message sur 8 bits
def extend_message(train_bin_standard):
    extended_bit_list = []
    for bit in train_bin_standard:
        for i in range(8):
            extended_bit_list.append(bit)
    return extended_bit_list

#On definit une fonction qui fait un XOR  avec une ligne de la matrice de Walsh (a chaque utilisateur une ligne differente)
def coded_message(bit_message, code = walsh2):
    message_canal = []
    for i in range(len(bit_message)):
        message_canal.append(xor(int(bit_message[i]),int(code[i%8])))
    return message_canal

#On definit une fonction qui fait une representation standard en terme de voltage en mettant les bits 1 a -1 volts et les bits 0 a 1 volt
def volt_representation(message_code):
    representation_volt = []
    for elem in message_code:
        if (elem == 1):
            representation_volt.append(-1)
        else:
            representation_volt.append(1)
    return representation_volt
        
#On fait le multiplexage du message canal et du bruit s'il y a un seul utilisateur
def multiplex_1user(message1, noise):
    traffic = []
    for i in range(len(message1)):
        traffic.append(message1[i]+noise[i])
    return traffic

#On fait le multiplexage du message canal et du bruit s'il y a 2 utilisateurs
def multiplex_2users(message1, message2, noise):
    traffic = []
    for i in range(len(message1)):
        traffic.append(message1[i] + message2[i] +noise[i])
    return traffic

#On decode le texte en faisant trafic*code de walsh
def decode(trafic, code = walsh2):
    message_dec = []
    for i in range(len(trafic)):
        message_dec.append(round(trafic[i]*code[i%8]))
    return message_dec

#On definit une fonction pour restituer le message dans sa taille d'origine. On choisit un bit chaque 8 bits
def mesRec(message_dec):
    texte_standard = []
    for i in range(0,len(message_dec),8):
        sum = 0
        for j in range(i,i+7,1):
            sum+= message_dec[j]
        texte_standard.append(round(sum/8))
    return texte_standard

#On definit une fonction qui va transformer le train binaire recu et traite en train binaire convertible en lettres pour 
#restituer le message
def textelisible(texte_standard):
    txt = ''
    for elem in texte_standard:
        if (elem==1):
            txt += '1'
        elif(elem== -1):
            txt += '0'
    return txt

# print(message1)
# print(message2)

# binaire1 = text_to_bits(message1)
# print(binaire1)
# binaire2 = text_to_bits(message2)
# print(binaire2)

# stand_binaire1 = standard(binaire1)
# print(stand_binaire1)
# stand_binaire2 = standard(binaire2)
# print(stand_binaire2)

# stand_bin1, stand_bin2 = equ_message(stand_binaire1, stand_binaire2)
# print(stand_bin1)
# print(stand_bin2)

# ext_bin1 = extend_message(stand_bin1)
# print(ext_bin1)
# ext_bin2 = extend_message(stand_bin2)
# print(ext_bin2)

# code1 = coded_message(ext_bin1,walsh2)
# print("code1 : ", code1)
# code2 = coded_message(ext_bin2,walsh3)
# print("code2 : ", code2)

# volt1 = volt_representation(code1)
# print(volt1)
# volt2 = volt_representation(code2)
# print(volt2)

# bruit = bruit_gen(len(ext_bin1))
# print(bruit)

# phys = multiplex_2users(volt1, volt2, bruit)
# print(phys)

# mes_end1 = decode(phys,walsh2)
# print("\n")
# print("mes_end1",mes_end1)
# mes_end2 = decode(phys,walsh3)
# print("mes_end2",mes_end2)
# print("\n")

# bin_rec1 = mesRec(mes_end1)
# print(bin_rec1)
# bin_rec2 = mesRec(mes_end2)
# print(bin_rec2)

# bin_traite1 = textelisible(bin_rec1)
# print(bin_traite1)
# bin_traite2 = textelisible(bin_rec2)
# print(bin_traite2)

# texte1 = text_from_bits(bin_traite1)
# print(texte1)
# texte2 = text_from_bits(bin_traite2)
# print(texte2)