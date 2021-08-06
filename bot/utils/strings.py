from attrify import Attrify as R
import ujson
import glob

string = R(ujson.load(open(glob.glob('bot/utils/*.json')[0], encoding='utf8')))
