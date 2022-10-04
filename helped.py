from abc import ABC, abstractmethod

import wx

import config as cfg
import Language.en as lang


def print_indicator(name_func: str, *args):
    print('=' * 20)
    print(f"Ім'я функції: {name_func}")
    for elem in args:
        print(elem)
    print('=' * 20)


class MyFrame(wx.Frame):
    def __init__(self, parent, _id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE,
                 name=wx.FrameNameStr):
        super().__init__(parent, _id, title, pos, size, style, name)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class MyPanel(wx.Panel):
    def __init__(self, parent, _id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.PanelNameStr):
        super().__init__(parent, _id, pos, size, style, name)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class MyDialog(wx.Dialog):
    def __init__(self, parent, _id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE,
                 name=wx.DialogNameStr):
        super().__init__(parent, _id, title, pos, size, style, name)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(cfg.FONT)
        self.SetFont(font)


class InterfaceListModel:
    def __init__(self):
        self.objects = {}
        self.ids = {}

    def create(self, *attrs):
        """Повертає створений Laborer."""
        raise NotImplemented

    def get_name_list(self) -> list[str]:
        """Повертає список імен object."""
        return [*self.ids.keys()]

    def get_object(self, select_id: int):
        """Повертає object за індексом."""
        return self.objects.get(select_id, 'None ID')

    def get_name(self, select_id: int) -> str:
        """Повертає ім'я за індексом"""
        raise NotImplemented

    def get_id(self, select_name: str) -> int | str:
        """Повертає індекс за ім'ям."""
        return self.ids.get(select_name, 'None Name')

    def add(self, _object):
        """Додає Object у словники:
        objects[id: object]
        ids[name: id]
        """
        raise NotImplemented

    def delete(self, select_id: int, select_name: str):
        """Видаляє Laborer та його атрибути з усіх словників"""
        self.del_object(select_id)
        self.del_id(select_name)

    def set_value_widgets(self, select_id: int, *wx_widgets):
        """Встановлює у wx_widgets значення атрибутів Object."""
        raise NotImplemented

    def set_attr_select_object(self, select_id: int, *attrs):
        """Встановлює в атрибути Object нове значення."""
        raise NotImplemented

    def change_name_select_object(self, select_id: int, select_name: str):
        """Змінює ім'я в словнику ids вибраного Object."""
        old_name = select_name
        new_name = self.get_name(select_id)
        if old_name != new_name:
            self.add_in_ids(new_name, self.get_id(old_name))
            self.del_id(old_name)

    def is_long_objects_equal_one(self) -> bool:
        if len(self.objects) == 1:
            return True
        return False

    def is_empty_objects(self) -> bool:
        if len(self.objects) <= 0:
            return True
        return False

    def add_in_objects(self, _id: int, _object):
        self.objects.setdefault(_id, _object)

    def add_in_ids(self, name: str, _id: int):
        self.ids.setdefault(name, _id)

    def del_object(self, select_id: int):
        del self.objects[select_id]

    def del_id(self, select_name: str):
        del self.ids[select_name]


class InterfaceListView(MyPanel):
    def __init__(self, parent, model: InterfaceListModel):
        super().__init__(parent)
        # Variables
        self.parent = parent
        self.select_id = None
        self.select_name = None
        self.editing = False
        self.model = model

        # Widgets
        st_title = wx.StaticText(self, label=lang.NAME_TITLE['laborer'])
        self.list_box = wx.ListBox(self, size=(210, 270), choices=self.model.get_name_list())
        self.btn_info = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['info'])
        self.btn_add = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['add'])
        self.btn_edit = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['edit'])
        self.btn_del = wx.Button(self, id=wx.ID_ANY, label=lang.NAME_BTN['del'])

        # Sizers
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(st_title, flag=wx.ALIGN_CENTRE | wx.TOP | wx.BOTTOM, border=10)
        main_box.Add(self.list_box, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_info, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_add, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_edit, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)
        main_box.Add(self.btn_del, flag=wx.ALIGN_CENTRE | wx.BOTTOM, border=10)

        self.SetSizer(main_box)

        # Binds
        self.Bind(wx.EVT_BUTTON, self.on_info, self.btn_info)
        self.Bind(wx.EVT_BUTTON, self.on_add, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.btn_del)
        self.Bind(wx.EVT_BUTTON, self.on_edit, self.btn_edit)
        self.Bind(wx.EVT_LISTBOX, self.on_select)

        # Methods
        self.disable_buttons()

    def on_select(self, event):
        index = self.list_box.GetSelection()
        self.select_name = self.model.get_name_list()[index]
        self.select_id = self.model.get_id(self.select_name)
        print(self.model.ids)
        print(self.model.objects)

    def on_info(self, event):
        self.show_info_view()

    def on_add(self, event):
        self.editing = False
        self.show_default_object_view()
        self.fulled_list()
        self.enable_buttons()

    def on_edit(self, event):
        if self.select_id is not None:
            self.editing = True
            self.show_fulled_object_view()
            self.fulled_list()

    def on_delete(self, event):
        if self.select_id is not None:
            self.model.delete(self.select_id, self.select_name)
            self.select_id = None
            self.select_name = None
            self.fulled_list()
            self.disable_buttons()

    def fulled_list(self):
        """Заповнює list_box"""
        self.list_box.SetItems(self.model.get_name_list())

    def enable_buttons(self):
        """Вмикає кнопки info, edit та del якщо в laborers є 1 елемент."""
        if self.model.is_long_objects_equal_one():
            self.btn_info.Enable(True)
            self.btn_edit.Enable(True)
            self.btn_del.Enable(True)

    def disable_buttons(self):
        """Вимикає кнопки info, edit та del якщо laborers порожній."""
        if self.model.is_empty_objects():
            self.btn_info.Enable(False)
            self.btn_edit.Enable(False)
            self.btn_del.Enable(False)

    def show_default_object_view(self):
        """Показує діалогове вікно Object заповнене за замовчуванням"""
        raise NotImplemented

    def show_fulled_object_view(self):
        """Показує діалогове вікно заповнене атрибутами вибраного Object."""
        raise NotImplemented

    def show_info_view(self):
        """Показує діалогове вікно заповнене інформацією вибраного Object."""
        raise NotImplemented
