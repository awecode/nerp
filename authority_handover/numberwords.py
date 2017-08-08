# -*- coding: utf-8 -*-
number_map = (
    "सुन्य", "एक", "दुइ", "तिन", "चार", "पाँच", "छ", "सात", "आठ", "नौ",
    "दश", "एघार", "बाह्र", "तेह्र", "चौध", "पन्ध्र", "सोह्र", "सत्र", "अठार", "उन्नाइस",
    "बिस", "एक्काइस", "बाइस", "तेइस", "चौबिस", "पच्चिस", "छब्बिस", "सत्ताइस", "अठ्ठाइस", "उनान्तिस",
    "तिस", "एकतिस", "बत्तिस", "तेत्तिस", "चौतिस", "पैतिस", "छत्तिस", "सैतिस", "अठतिस", "उनान्चालिस",
    "चालिस", "एकचालिस", "बयालिस", "त्रिचालिस", "चवालिस", "पैतालिस", "छयालिस", "सत्चालिस", "अठ्चालिस", "उनन्चास",
    "पचास", "एकाउन्न", "बाउन्न", "त्रिपन्न", "चौवन्न", "पचपन्न", "छपन्न", "सन्ताउन्न", "अन्ठाउन्न", "उनन्साठी",
    "साठी", "एकसठ्ठी", "बैसठ्ठी", "त्रिसठ्ठी", "चौसठ्ठी", "पैंसठ्ठी", "छैसठ्ठी", "सत्सठ्ठी", "अठ्सठ्ठी",
    "उनान्सत्तरी",
    "सत्तरी", "एकहत्तर", "बहत्तर", "त्रिहत्तर", "चौरहत्तर", "पचहत्तर", "छयत्तर", "सतहत्तर", "अठहत्तर", "उनासी",
    "असी", "एकासी", "बयासी", "त्रियासी", "चौरासी", "पचासी", "छयासी", "सतासी", "अठासी", "उनान्नब्बे",
    "नब्बे", "एकान्नब्बे", "बयान्नब्बे", "त्रियान्नब्बे", "चौरान्नब्बे", "पन्चान्नब्बे", "छ्यान्नब्बे",
    "सन्तान्नब्बे", "अन्ठान्नब्बे", "उनान्सय"
)

levels = (
    "सय",
    "हजार",
    "लाख",
    "करोड",
    "अर्ब",
    "खर्ब"
)


# two digit
def get_lte_two_digit_word(number):
    if int(number):
        return number_map[int(number)]
    else:
        return ''


# three digit
def get_three_digit_words(number):
    number_str = str(number)
    word = ''
    if int(number_str[0:1]):
        word += "%s सय " % number_map[int(number_str[0:1])]
    word += get_lte_two_digit_word(int(number_str[1:3]))

    return word


def is_valid(number):
    if isinstance(number, int):
        return True
    else:
        return False


def subtract_string(strg, del_position):
    strg = list(strg)
    del strg[del_position[0]:del_position[1]:del_position[2]]
    return "".join(strg)


def get_word(num_str):
    words = []
    counter = 0
    while num_str:
        if not counter:
            words.append(get_three_digit_words(num_str[0:3][::-1]))
            num_str = subtract_string(num_str, (0, 3, 1))
        else:
            if get_lte_two_digit_word(num_str[0:2][::-1]):
                words.append(get_lte_two_digit_word(num_str[0:2][::-1]) + " " + levels[counter])
            num_str = subtract_string(num_str, (0, 2, 1))
        counter += 1
    return " ".join(words[::-1])


def number_to_words(number):
    kharba_list = []
    if is_valid(number):
        number_str = str(number)
        while number_str:
            kharba_list.append(get_word(number_str[-1:-12:-1]))
            number_str = subtract_string(number_str, (-1, -12, -1))
    else:
        raise ValueError('Invalid Value')
    return " खर्ब ".join(kharba_list[::-1]) + " रुपैया"
