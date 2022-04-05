import win32clipboard as wcb
import time

class ClipboardMonitor():
    # 获取剪贴板内容
    def GetText(self):
        # 剪贴板每打开一次就要关闭，否则其他进程无法访问剪切板
        # 内容是文字时
        try:
            wcb.OpenClipboard()
            text = wcb.GetClipboardData(wcb.CF_UNICODETEXT)
            return [True, text]
        # 内容是图片时，进入异常
        except:
            return [False, ""]
        finally:
            wcb.CloseClipboard()

    # 处理剪贴板内容
    def ProcessText(self, txt):
        # 按行分割内容
        txt = txt.splitlines()
        # 用空格拼接每行
        txt = ' '.join(txt)
        # 将长度大于1的空格转为1个空格
        txt = ' '.join(txt.split())
        # 处理行末的-
        txt = txt.replace('- ','')
        # 放入剪贴板,写入前必须先清空，得到剪切板占有权
        wcb.OpenClipboard()
        wcb.EmptyClipboard()
        wcb.SetClipboardData(wcb.CF_UNICODETEXT, txt)
        wcb.CloseClipboard()

    def Monitor(self):
        _, lastText = self.GetText()
        while True:
            flag, newText = self.GetText()
            if(flag):
                # 剪贴板内容发生变化
                if newText != lastText:
                    # 处理内容
                    self.ProcessText(newText)
                    lastText = newText
                # 延迟1秒
            time.sleep(1)

if __name__ == '__main__':
    clipBoard = ClipboardMonitor()
    clipBoard.Monitor()