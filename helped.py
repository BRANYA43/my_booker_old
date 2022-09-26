from abc import ABC, abstractmethod

import wx

import config as cfg
import Language.en as lang


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class MyPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class InterfaceListModel:
    def __init__(self):
        """Инициализирует словарь объектов, список имён"""
        self.object_dict: dict[str: object] = {}
        self.name_list: list[str] = []

    def get_object(self, select: str) -> object:
        """Возвращает выбранный объект"""
        return self.object_dict.get(select, 'None')

    def check_object(self, select: str, my_object):
        """В конце функ. edit. Проверяет имя объекта с именем выбранного объекта,
        при не соответствии удаляет старый объект и добавляет новый
        """
        if select != my_object.__str__():
            del self.object_dict[select]
            index = self.name_list.index(select)
            self.name_list[index] = my_object.__str__()
            self.object_dict.setdefault(my_object.__str__(), my_object)

    def add(self, my_object):
        """Добавляет объект к словарю [имя объекта: объект] и к списку [имя объекта].
        Имя объекта = __str__()
        """
        self.object_dict.setdefault(my_object.__str__(), my_object)
        self.name_list.append(my_object.__str__())

    def edit(self, select: str, **kwargs):
        """Изменяет атрибуты выбранного объекта значениями wx виджетов"""
        _object = self.get_object(select)
        for attr, wx_widget in kwargs.items():
            _object.__dict__[attr] = wx_widget.GetValue()
        self.check_object(select, _object)

    def delete(self, select: str):
        """Удаляет выбранный объект из словаря и списка"""
        del self.object_dict[select]
        self.name_list.remove(select)

    def set(self, select: str, **kwargs):
        """Устанавливает значения wx виджетов атрибутами выбранного объекта"""
        _object = self.get_object(select)
        for attr, wx_widget in kwargs.items():
            wx_widget.SetValue(str(_object.__dict__[attr]))


class InterfaceListView(MyPanel):
    def __init__(self, parent, model: InterfaceListModel, title: str):
        super().__init__(parent)
        self.parent = parent
        self.model = model
        self.select = None
        self.editing = False

        st_title = wx.StaticText(self, label=title)
        self.list_box = wx.ListBox(self, size=(210, 270), choices=self.model.name_list)
        self.btn_info = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['info'])
        self.btn_add = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['add'])
        self.btn_edit = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['edit'])
        self.btn_del = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['del'])
        self.check_list_is_none()

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(st_title, flag=wx.ALIGN_CENTRE | wx.TOP | wx.BOTTOM, border=10)
        main_box.Add(self.list_box, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_info, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_add, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_edit, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_del, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)

        self.SetSizer(main_box)

        self.Bind(wx.EVT_BUTTON, self.on_info, self.btn_info)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.on_del, self.btn_del)
        self.Bind(wx.EVT_BUTTON, self.on_edit, self.btn_edit)
        self.Bind(wx.EVT_LISTBOX, self.on_select)

    def on_select(self, event):
        self.select = self.model.name_list[self.list_box.GetSelection()]

    def on_info(self, info_view):
        my_object = self.model.get_object(self.select)
        info_view(self.parent, my_object).ShowModal()

    def on_add(self, dialog_view):
        self.editing = False
        dialog_view(self.parent, self.model, self.select, self.editing).ShowModal()
        self.list_box.SetItems(self.model.name_list)
        self.check_list_is_none()

    def on_edit(self, dialog_view, **kwargs):
        self.model.set(self.select, **kwargs)
        dialog_view.ShowModal()
        self.list_box.SetItems(self.model.name_list)

    def on_del(self, event):
        self.model.delete(self.select)
        self.select = None
        self.list_box.SetItems(self.model.name_list)
        self.check_list_is_none()

    def check_list_is_none(self):
        if len(self.model.name_list) == 1:
            self.btn_info.Enable(True)
            self.btn_edit.Enable(True)
            self.btn_del.Enable(True)
        elif len(self.model.name_list) <= 0:
            self.btn_info.Enable(False)
            self.btn_edit.Enable(False)
            self.btn_del.Enable(False)
