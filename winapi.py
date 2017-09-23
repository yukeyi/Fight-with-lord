#
# _*_ coding:UTF-8 _*_
import win32api
import win32con
import win32gui
from ctypes import *
import time


def mouse_click(x, y, offset):
    if not x is None and not y is None:
        mouse_move(x + offset[0], y + offset[1])
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)
    # mouse_move(0, 0)


def mouse_rclick(x, y, offset):
    if not x is None and not y is None:
        mouse_move(x + offset[0], y + offset[1])
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.05)
    # mouse_move(0, 0)


def mouse_dclick(x, y, offset):
    if not x is None and not y is None:
        mouse_move(x + offset[0], y + offset[1])
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)


def mouse_move(x, y):
    # print(x, y)
    windll.user32.SetCursorPos(x, y)


class RECT(Structure):
    _fields_ = [('left', c_int), ('top', c_int), ('right', c_int), ('bottom', c_int)]


def getrect():
    rect = RECT()
    HWND = win32gui.FindWindow(None, "斗地主角色版")
    windll.user32.GetWindowRect(HWND, byref(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)

# mouse_dclick(44,44)
