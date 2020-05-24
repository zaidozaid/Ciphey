import string
import os
import sys
from loguru import logger

sys.path.append("..")
try:
    import mathsHelper as mh
except ModuleNotFoundError:
    import ciphey.mathsHelper as mh


class dictionaryChecker:
    """
    Class designed to confirm whether something is **language** based on how many words of **language** appears
    Call confirmlanguage(text, language)
    * text: the text you want to confirm
    * language: the language you want to confirm

    Find out what language it is by using chisquared.py, the highest chisquared score is the language
    languageThreshold = 45
    if a string is 45% **language** words, then it's confirmed to be english
    """

    def __init__(self):
        self.mh = mh.mathsHelper()
        self.languagePercentage = 0.0
        self.languageWordsCounter = 0.0
        self.languageThreshold = 55
        # this is hard coded because i dont want to use a library or rely on reading from files, as it's slow.
        # dictionary because lookup is O(1)
        self.top1000Words = {'able': None, 'about': None, 'above': None, 'act': None, 'add': None, 'afraid': None, 'after': None, 'again': None, 'against': None, 'age': None, 'ago': None, 'agree': None, 'air': None, 'all': None, 'allow': None, 'also': None, 'always': None, 'am': None, 'among': None, 'an': None, 'and': None, 'anger': None, 'animal': None, 'answer': None, 'any': None, 'appear': None, 'apple': None, 'are': None, 'area': None, 'arm': None, 'arrange': None, 'arrive': None, 'art': None, 'as': None, 'ask': None, 'at': None, 'atom': None, 'baby': None, 'back': None, 'bad': None, 'ball': None, 'band': None, 'bank': None, 'bar': None, 'base': None, 'basic': None, 'bat': None, 'be': None, 'bear': None, 'beat': None, 'beauty': None, 'bed': None, 'been': None, 'before': None, 'began': None, 'begin': None, 'behind': None, 'believe': None, 'bell': None, 'best': None, 'better': None, 'between': None, 'big': None, 'bird': None, 'bit': None, 'black': None, 'block': None, 'blood': None, 'blow': None, 'blue': None, 'board': None, 'boat': None, 'body': None, 'bone': None, 'book': None, 'born': None, 'both': None, 'bottom': None, 'bought': None, 'box': None, 'boy': None, 'branch': None, 'bread': None, 'break': None, 'bright': None, 'bring': None, 'broad': None, 'broke': None, 'brother': None, 'brought': None, 'brown': None, 'build': None, 'burn': None, 'busy': None, 'but': None, 'buy': None, 'by': None, 'call': None, 'came': None, 'camp': None, 'can': None, 'capital': None, 'captain': None, 'car': None, 'card': None, 'care': None, 'carry': None, 'case': None, 'cat': None, 'catch': None, 'caught': None, 'cause': None, 'cell': None, 'cent': None, 'center': None, 'century': None, 'certain': None, 'chair': None, 'chance': None, 'change': None, 'character': None, 'charge': None, 'chart': None, 'check': None, 'chick': None, 'chief': None, 'child': None, 'children': None, 'choose': None, 'chord': None, 'circle': None, 'city': None, 'claim': None, 'class': None, 'clean': None, 'clear': None, 'climb': None, 'clock': None, 'close': None, 'clothe': None, 'cloud': None, 'coast': None, 'coat': None, 'cold': None, 'collect': None, 'colony': None, 'color': None, 'column': None, 'come': None, 'common': None, 'company': None, 'compare': None, 'complete': None, 'condition': None, 'connect': None, 'consider': None, 'consonant': None, 'contain': None, 'continent': None, 'continue': None, 'control': None, 'cook': None, 'cool': None, 'copy': None, 'corn': None, 'corner': None, 'correct': None, 'cost': None, 'cotton': None, 'could': None, 'count': None, 'country': None, 'course': None, 'cover': None, 'cow': None, 'crease': None, 'create': None, 'crop': None, 'cross': None, 'crowd': None, 'cry': None, 'current': None, 'cut': None, 'dad': None, 'dance': None, 'danger': None, 'dark': None, 'day': None, 'dead': None, 'deal': None, 'dear': None, 'death': None, 'decide': None, 'decimal': None, 'deep': None, 'degree': None, 'depend': None, 'describe': None, 'desert': None, 'design': None, 'determine': None, 'develop': None, 'dictionary': None, 'did': None, 'die': None, 'differ': None, 'difficult': None, 'direct': None, 'discuss': None, 'distant': None, 'divide': None, 'division': None, 'do': None, 'doctor': None, 'does': None, 'dog': None, 'dollar': None, "don't": None, 'done': None, 'door': None, 'double': None, 'down': None, 'draw': None, 'dream': None, 'dress': None, 'drink': None, 'drive': None, 'drop': None, 'dry': None, 'duck': None, 'during': None, 'each': None, 'ear': None, 'early': None, 'earth': None, 'ease': None, 'east': None, 'eat': None, 'edge': None, 'effect': None, 'egg': None, 'eight': None, 'either': None, 'electric': None, 'element': None, 'else': None, 'end': None, 'enemy': None, 'energy': None, 'engine': None, 'enough': None, 'enter': None, 'equal': None, 'equate': None, 'especially': None, 'even': None, 'evening': None, 'event': None, 'ever': None, 'every': None, 'exact': None, 'example': None, 'except': None, 'excite': None, 'exercise': None, 'expect': None, 'experience': None, 'experiment': None, 'eye': None, 'face': None, 'fact': None, 'fair': None, 'fall': None, 'family': None, 'famous': None, 'far': None, 'farm': None, 'fast': None, 'fat': None, 'father': None, 'favor': None, 'fear': None, 'feed': None, 'feel': None, 'feet': None, 'fell': None, 'felt': None, 'few': None, 'field': None, 'fig': None, 'fight': None, 'figure': None, 'fill': None, 'final': None, 'find': None, 'fine': None, 'finger': None, 'finish': None, 'fire': None, 'first': None, 'fish': None, 'fit': None, 'five': None, 'flat': None, 'floor': None, 'flow': None, 'flower': None, 'fly': None, 'follow': None, 'food': None, 'foot': None, 'for': None, 'force': None, 'forest': None, 'form': None, 'forward': None, 'found': None, 'four': None, 'fraction': None, 'free': None, 'fresh': None, 'friend': None, 'from': None, 'front': None, 'fruit': None, 'full': None, 'fun': None, 'game': None, 'garden': None, 'gas': None, 'gather': None, 'gave': None, 'general': None, 'gentle': None, 'get': None, 'girl': None, 'give': None, 'glad': None, 'glass': None, 'go': None, 'gold': None, 'gone': None, 'good': None, 'got': None, 'govern': None, 'grand': None, 'grass': None, 'gray': None, 'great': None, 'green': None, 'grew': None, 'ground': None, 'group': None, 'grow': None, 'guess': None, 'guide': None, 'gun': None, 'had': None, 'hair': None, 'half': None, 'hand': None, 'happen': None, 'happy': None, 'hard': None, 'has': None, 'hat': None, 'have': None, 'he': None, 'head': None, 'hear': None, 'heard': None, 'heart': None, 'heat': None, 'heavy': None, 'held': None, 'help': None, 'her': None, 'here': None, 'high': None, 'hill': None, 'him': None, 'his': None, 'history': None, 'hit': None, 'hold': None, 'hole': None, 'home': None, 'hope': None, 'horse': None, 'hot': None, 'hour': None, 'house': None, 'how': None, 'huge': None, 'human': None, 'hundred': None, 'hunt': None, 'hurry': None, 'ice': None, 'idea': None, 'if': None, 'imagine': None, 'in': None, 'inch': None, 'include': None, 'indicate': None, 'industry': None, 'insect': None, 'instant': None, 'instrument': None, 'interest': None, 'invent': None, 'iron': None, 'is': None, 'island': None, 'it': None, 'job': None, 'join': None, 'joy': None, 'jump': None, 'just': None, 'keep': None, 'kept': None, 'key': None, 'kill': None, 'kind': None, 'king': None, 'knew': None, 'know': None, 'lady': None, 'lake': None, 'land': None, 'language': None, 'large': None, 'last': None, 'late': None, 'laugh': None, 'law': None, 'lay': None, 'lead': None, 'learn': None, 'least': None, 'leave': None, 'led': None, 'left': None, 'leg': None, 'length': None, 'less': None, 'let': None, 'letter': None, 'level': None, 'lie': None, 'life': None, 'lift': None, 'light': None, 'like': None, 'line': None, 'liquid': None, 'list': None, 'listen': None, 'little': None, 'live': None, 'locate': None, 'log': None, 'lone': None, 'long': None, 'look': None, 'lost': None, 'lot': None, 'loud': None, 'love': None, 'low': None, 'machine': None, 'made': None, 'magnet': None, 'main': None, 'major': None, 'make': None, 'man': None, 'many': None, 'map': None, 'mark': None, 'market': None, 'mass': None, 'master': None, 'match': None, 'material': None, 'matter': None, 'may': None, 'me': None, 'mean': None, 'meant': None, 'measure': None, 'meat': None, 'meet': None, 'melody': None, 'men': None, 'metal': None, 'method': None, 'middle': None, 'might': None, 'mile': None, 'milk': None, 'million': None, 'mind': None, 'mine': None, 'minute': None, 'miss': None, 'mix': None, 'modern': None, 'molecule': None, 'moment': None, 'money': None, 'month': None, 'moon': None, 'more': None, 'morning': None, 'most': None, 'mother': None, 'motion': None, 'mount': None, 'mountain': None, 'mouth': None, 'move': None, 'much': None, 'multiply': None, 'music': None, 'must': None, 'my': None, 'name': None, 'nation': None, 'natural': None, 'nature': None, 'near': None, 'necessary': None, 'neck': None, 'need': None, 'neighbor': None, 'never': None, 'new': None, 'next': None, 'night': None, 'nine': None, 'no': None, 'noise': None, 'noon': None, 'nor': None, 'north': None, 'nose': None, 'not': None, 'note': None, 'nothing': None, 'notice': None, 'noun': None, 'now': None, 'number': None, 'numeral': None, 'object': None, 'observe': None, 'occur': None, 'ocean': None, 'of': None, 'off': None, 'offer': None, 'office': None, 'often': None, 'oh': None, 'oil': None, 'old': None, 'on': None, 'once': None, 'one': None, 'only': None, 'open': None, 'operate': None, 'opposite': None, 'or': None, 'order': None, 'organ': None, 'original': None, 'other': None, 'our': None, 'out': None, 'over': None, 'own': None, 'oxygen': None, 'page': None, 'paint': None, 'pair': None, 'paper': None, 'paragraph': None, 'parent': None, 'part': None, 'particular': None, 'party': None, 'pass': None, 'past': None, 'path': None, 'pattern': None, 'pay': None, 'people': None, 'perhaps': None, 'period': None, 'person': None, 'phrase': None, 'pick': None, 'picture': None, 'piece': None, 'pitch': None, 'place': None, 'plain': None, 'plan': None, 'plane': None, 'planet': None, 'plant': None, 'play': None, 'please': None, 'plural': None, 'poem': None, 'point': None, 'poor': None, 'populate': None, 'port': None, 'pose': None, 'position': None, 'possible': None, 'post': None, 'pound': None, 'power': None, 'practice': None, 'prepare': None, 'present': None, 'press': None, 'pretty': None, 'print': None, 'probable': None, 'problem': None, 'process': None, 'produce': None, 'product': None, 'proper': None, 'property': None, 'protect': None, 'prove': None, 'provide': None, 'pull': None, 'push': None, 'put': None, 'quart': None, 'question': None, 'quick': None, 'quiet': None, 'quite': None, 'quotient': None, 'race': None, 'radio': None, 'rail': None, 'rain': None, 'raise': None, 'ran': None, 'range': None, 'rather': None, 'reach': None, 'read': None, 'ready': None, 'real': None, 'reason': None, 'receive': None, 'record': None, 'red': None, 'region': None, 'remember': None, 'repeat': None, 'reply': None, 'represent': None, 'require': None, 'rest': None, 'result': None, 'rich': None, 'ride': None, 'right': None, 'ring': None, 'rise': None, 'river': None, 'road': None, 'rock': None, 'roll': None, 'room': None, 'root': None, 'rope': None, 'rose': None, 'round': None, 'row': None, 'rub': None, 'rule': None, 'run': None, 'safe': None, 'said': None, 'sail': None, 'salt': None, 'same': None, 'sand': None, 'sat': None, 'save': None, 'saw': None, 'say': None, 'scale': None, 'school': None, 'science': None, 'score': None, 'sea': None, 'search': None, 'season': None, 'seat': None, 'second': None, 'section': None, 'see': None, 'seed': None, 'seem': None, 'segment': None, 'select': None, 'self': None, 'sell': None, 'send': None, 'sense': None, 'sent': None, 'sentence': None, 'separate': None, 'serve': None, 'set': None, 'settle': None, 'seven': None, 'several': None, 'shall': None, 'shape': None, 'share': None, 'sharp': None, 'she': None, 'sheet': None, 'shell': None, 'shine': None, 'ship': None, 'shoe': None, 'shop': None, 'shore': None, 'short': None, 'should': None, 'shoulder': None, 'shout': None, 'show': None, 'side': None, 'sight': None, 'sign': None, 'silent': None, 'silver': None, 'similar': None, 'simple': None, 'since': None, 'sing': None, 'single': None, 'sister': None, 'sit': None, 'six': None, 'size': None, 'skill': None, 'skin': None, 'sky': None, 'slave': None, 'sleep': None, 'slip': None, 'slow': None, 'small': None, 'smell': None, 'smile': None, 'snow': None, 'so': None, 'soft': None, 'soil': None, 'soldier': None, 'solution': None, 'solve': None, 'some': None, 'son': None, 'song': None, 'soon': None, 'sound': None, 'south': None, 'space': None, 'speak': None, 'special': None, 'speech': None, 'speed': None, 'spell': None, 'spend': None, 'spoke': None, 'spot': None, 'spread': None, 'spring': None, 'square': None, 'stand': None, 'star': None, 'start': None, 'state': None, 'station': None, 'stay': None, 'stead': None, 'steam': None, 'steel': None, 'step': None, 'stick': None, 'still': None, 'stone': None, 'stood': None, 'stop': None, 'store': None, 'story': None, 'straight': None, 'strange': None, 'stream': None, 'street': None, 'stretch': None, 'string': None, 'strong': None, 'student': None, 'study': None, 'subject': None, 'substance': None, 'subtract': None, 'success': None, 'such': None, 'sudden': None, 'suffix': None, 'sugar': None, 'suggest': None, 'suit': None, 'summer': None, 'sun': None, 'supply': None, 'support': None, 'sure': None, 'surface': None, 'surprise': None, 'swim': None, 'syllable': None, 'symbol': None, 'system': None, 'table': None, 'tail': None, 'take': None, 'talk': None, 'tall': None, 'teach': None, 'team': None, 'teeth': None, 'tell': None, 'temperature': None, 'ten': None, 'term': None, 'test': None, 'than': None, 'thank': None, 'that': None, 'the': None, 'their': None, 'them': None, 'then': None, 'there': None, 'these': None, 'they': None, 'thick': None, 'thin': None, 'thing': None, 'think': None, 'third': None, 'this': None, 'those': None, 'though': None, 'thought': None, 'thousand': None, 'three': None, 'through': None, 'throw': None, 'thus': None, 'tie': None, 'time': None, 'tiny': None, 'tire': None, 'to': None, 'together': None, 'told': None, 'tone': None, 'too': None, 'took': None, 'tool': None, 'top': None, 'total': None, 'touch': None, 'toward': None, 'town': None, 'track': None, 'trade': None, 'train': None, 'travel': None, 'tree': None, 'triangle': None, 'trip': None, 'trouble': None, 'truck': None, 'true': None, 'try': None, 'tube': None, 'turn': None, 'twenty': None, 'two': None, 'type': None, 'under': None, 'unit': None, 'until': None, 'up': None, 'us': None, 'use': None, 'usual': None, 'valley': None, 'value': None, 'vary': None, 'verb': None, 'very': None, 'view': None, 'village': None, 'visit': None, 'voice': None, 'vowel': None, 'wait': None, 'walk': None, 'wall': None, 'want': None, 'war': None, 'warm': None, 'was': None, 'wash': None, 'watch': None, 'water': None, 'wave': None, 'way': None, 'we': None, 'wear': None, 'weather': None, 'week': None, 'weight': None, 'well': None, 'went': None, 'were': None, 'west': None, 'what': None, 'wheel': None, 'when': None, 'where': None, 'whether': None, 'which': None, 'while': None, 'white': None, 'who': None, 'whole': None, 'whose': None, 'why': None, 'wide': None, 'wife': None, 'wild': None, 'will': None, 'win': None, 'wind': None, 'window': None, 'wing': None, 'winter': None, 'wire': None, 'wish': None, 'with': None, 'woman': None, 'women': None, "won't": None, 'wonder': None, 'wood': None, 'word': None, 'work': None, 'world': None, 'would': None, 'write': None, 'written': None, 'wrong': None, 'wrote': None, 'yard': None, 'year': None, 'yellow': None, 'yes': None, 'yet': None, 'you': None, 'young': None, 'your': None}

    def cleanText(self, text):
        # makes the text unique words and readable
        text = text.lower()
        text = self.mh.stripPuncuation(text)
        text = text.split(" ")
        text = list(set(text))
        return text

    def check1000Words(self, text):
        check = dict.fromkeys(self.top1000Words)
        text = self.cleanText(text)
        logger.debug(f"Check 1000 words text is {text}")
        # If any of the top 1000 words in the text appear
        # return true
        for word in text:
            logger.debug(f"Word in check1000 is {word}")
            # I was debating using any() here, but I think they're the
            # same speed so it doesn't really matter too much
            if word.lower() == text.lower():
                logger.debug(f"THEY're the SAME! {word} and {text}")
            if word in check:
                logger.debug(f"Check 1000 words returns True for word {word}")
                return True
            else:
                return False

    def checkDictionary(self, text, language):
        """Compares a word with 
        The dictionary is sorted and the text is sorted"""
        # reads through most common words / passwords
        # and calculates how much of that is in language
        text = self.cleanText(text)
        text.sort()
        # can dynamically use languages then
        language = str(language) + ".txt"

        # https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "English.txt")
        file = open(file_path, "r")
        f = file.readlines()
        file.close()
        f = [x.strip().lower() for x in f]
        # dictionary is "word\n" so I remove the "\n"

        # so this should loop until it gets to the point in the @staticmethod
        # that equals the word :)

        """
        for every single word in main dictionary
        if that word == text[0] then +1 to counter
        then +1 to text[0 + i]
        so say the dict is ordered
        we just loop through dict 
        and eventually we'll reach a point where word in dict = word in text
        at that point, we move to the next text point
        both text and dict are sorted
        so we only loop once, we can do this in O(n log n) time
        """
        counter = 0
        counter_percent = 0

        for dictLengthCounter, word in enumerate(f):
            # if there is more words counted than there is text
            # it is 100%, sometimes it goes over
            # so this stops that
            if counter >= len(text):
                break
            # if the dictionary word is contained in the text somewhere
            # counter + 1
            if word in text:
                counter = counter + 1
                counter_percent = counter_percent + 1
        self.languageWordsCounter = counter
        self.languagePercentage = self.mh.percentage(
            float(self.languageWordsCounter), float(len(text))
        )
        return counter

    def confirmlanguage(self, text, language):
        self.checkDictionary(text, language)
        if self.languagePercentage > self.languageThreshold:
            logger.debug(f"The language percentange {self.languagePercentage} is over the threshold {self.languageThreshold}")
            return True
        else:
            return False

