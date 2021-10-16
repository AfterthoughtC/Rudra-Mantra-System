# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:02:26 2020

@author: AfterthoughtC
"""

import pandas as pd
import re

""" How this shit works """
"""
1. Input your spell name
2. The script splits the spell at the splitter value to form a list of phrases
   called subspells. The default splitter value is " ".
3. Each subspell will then be split further into parts called bits. Having
   a '+' value between different letters will force the two letters to be
   together in the bit.
4. The script will then try to find component phrases found in the csv file by
   combining consecutive subspells together. If it can't find a component it
   returns a null value for that phrase
   
   Ex. Say a spell named "rin+ga sen+t"
       Converting it to subspells produces a list of two subspells; "rin+ga"
       and "sen+t"
       Converting "rin+ga" to bits produces ['r', 'i', 'ng', 'a'] as its list
       of bits. Notice how the plus in between the 'n' and 'g' creates the bit
       'ng' rather than an individual 'n' and 'g'
       Converting "sen+t" to bits produces ['s', 'e', 'nt'] as its list of bits.
"""

phrase_csv = 'phrases.csv'
# This should be the name or directory of the csv file containing your list of phrases
# The csv should contain at least one column with the name 'Phrase'\

splitter = ' '
# Value to signify that two bits must not be together

phrase_list = pd.read_csv(phrase_csv)
phrase_list.set_index('Phrase',inplace = True)


def _subspell_to_bits_(subspell): # Converts subspells to bits
    split_phrase = re.findall(r"[A-Za-z](?:\++[A-Za-z])*",subspell)
    split_phrase = [part.replace('+','') for part in split_phrase]
    return(split_phrase) # save


def spell_to_bits(spell): # Converts spells to subspells to bits
    split = [[]]
    space_split = spell.split(splitter)
    for subspell in space_split:
        if len(split[-1]) != 0:
            split.append([])
        split[-1].extend(_subspell_to_bits_(subspell))
    if len(split[-1]) == 0:
        split = split[:-1]
    return(split) # save


def bit_to_component(split_phrase): # Converts bits to components
    P = len(split_phrase)
    p = 0
    spell_component = []
    while p < P:
        x = P
        finding = True
        while finding:
            comp = ''.join(split_phrase[p:x])
            if comp in phrase_list.index:
                spell_component.append(comp)
                finding = False
            else:
                if p+1 == x:
                    spell_component.append(None)
                    finding = False
                else:
                    x -= 1
        p = x
    return(spell_component) # save


def spell_to_bit_to_component(spell): # Converts spells to subspells to bits then back to components
    all_bits = spell_to_bits(spell)
    components = []
    for bit_list in all_bits:
        components.append(bit_to_component(bit_list))
    return(components) # save
        



old_spell = 'aorong'
#old_spell = 'ao+rong'

print(old_spell)
print(spell_to_bits(old_spell))
print(spell_to_bit_to_component(old_spell))
