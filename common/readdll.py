# coding=utf-8
# author:ss

from ctypes import *

objdll = cdll.LoadLibrary(r"D:\envr\double-teacher\sunvote\SunVoteSDK_x64.dll")
objdll.VoteStart(40, "1,2,3,4,5,6,7")

