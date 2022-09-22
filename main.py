import wx

import laborer


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Booker', size=(800, 600))
        laborer_model = laborer.ListModel()

        tab = wx.Notebook(self)
        laborer_list = laborer.ListView(tab, laborer_model)
        tab.InsertPage(0, page=laborer_list, text='Home')


def main():
    app = wx.App()
    booker = MainFrame()
    booker.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
